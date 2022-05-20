from Specsheet_Automation.classes.jira_api import JiraApi
from Specsheet_Automation.static_data.jira_config import JIRA_ISSUE_TYPES, CONFIG_REFRESH_INTERVAL, \
    JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING
from Specsheet_Automation.helpers.jira_automation_helpers import get_config_file_for_project, prepare_issue_data, field_to_jql
# from Specsheet_Automation.static_data.file_info import jira_config_file

import json
import os
from datetime import datetime
from json import JSONDecodeError
from urllib.parse import unquote
import time

def initialise_jira(project_id, jira_token, force_update=False):
    try:
        content_deleted = False
        project_config_file = get_config_file_for_project(project_id)
        if not os.path.exists(project_config_file):
            with open(project_config_file, 'w'):
                pass
        with open(project_config_file, "r+") as config_file:
            if not force_update:
                try:
                    saved_data = json.load(config_file)
                    if int(datetime.now().timestamp()) - saved_data["lastUpdated"] < CONFIG_REFRESH_INTERVAL:
                        return True, "Update not due"
                except JSONDecodeError:
                    pass
            config_file.seek(0)
            config_file.truncate()
            content_deleted = True
            jira = JiraApi(jira_token)
            issue_types = {}
            components = {}

            for i_t in jira.get_all_issue_types()["text"]:
                if i_t["name"] in JIRA_ISSUE_TYPES:
                    issue_types[i_t["name"]] = {
                        "id": i_t["id"],
                        "fields": {}
                    }
            for c in jira.get_all_components(project_id)["text"]:
                components[c["name"]] = c["id"]
            config_data = {
                "issueTypes": issue_types,
                "components": components,
                "lastUpdated": int(datetime.now().timestamp())
            }
            for issue in issue_types:
                meta_data = jira.get_meta_data_for_issue_type(project_id, issue_types[issue]["id"])["text"]["values"]
                for value in meta_data:
                    issue_types[issue]["fields"][value["name"]] = {
                        "id": value["fieldId"],
                        "allowedValues": None,
                        "type": value["schema"]["type"]
                    }
                    if "allowedValues" in value.keys():
                        issue_types[issue]["fields"][value["name"]]["allowedValues"] = [
                            {
                                "name": v["name"] if "name" in v else v["value"],
                                "id": v["id"],
                            } for v in value["allowedValues"]
                        ]
            config_file.write(json.dumps(config_data))
        return True, "Config data updated successful"
    except Exception as e:
        if content_deleted:
            with open(project_config_file, "r+") as config_file:
                config_file.seek(0)
                config_file.truncate()
                config_file.write(json.dumps(saved_data))
        return False, "Error updating Jira config file: {}".format(repr(e))

def get_vendors_from_local(project_id):
    try:
        project_config_file = get_config_file_for_project(project_id)
        with open(project_config_file, "r") as config_file:
            saved_data = json.load(config_file)
            vendors = [{"name": c, "id": saved_data["components"][c]} for c in saved_data["components"]]
        return True, vendors
    except Exception as e:
        return False, "Error while retreiving vendors list: {}".format(repr(e))


def get_from_local(issue_type, field, project_id):
    try:
        project_config_file = get_config_file_for_project(project_id)
        with open(project_config_file, "r") as config_file:
            saved_data = json.load(config_file)
            if issue_type == "release":
                testing_request_types = saved_data["issueTypes"]["Epic"]["fields"][field]["allowedValues"]
        return True, testing_request_types
    except Exception as e:
        return False, "Error while retreiving {}: {}".format(field, repr(e))

def get_device_types_from_local(project_id, issue_type="release"):
    return get_from_local(issue_type, "Device Type", project_id)


def get_testing_request_types_from_local(project_id, issue_type="release"):
    return get_from_local(issue_type, "Testing Request Type", project_id)


def get_testing_priorities_from_local(project_id, issue_type="release"):
    return get_from_local(issue_type, "Testing Priority", project_id)


def get_wda_test_scopes_from_local(project_id, issue_type="release"):
    return get_from_local(issue_type, "WDA Test Scope", project_id)


def get_funding_from_local(project_id, issue_type="release"):
    return get_from_local(issue_type, "Funding", project_id)

def create_jira_issue(issue_type, issue_details_raw, jira_token):
    try:
        jira = JiraApi(jira_token)

        jira_config, issue_details = prepare_jira_data(issue_details_raw, issue_type)
        project_id = issue_details["Project"]

        request_data = {}
        issue_type = issue_details["Issue Type"]

        version_id = 0
        if issue_type == "Story":
            try:
                version_id = jira.create_version(project_id, issue_details["Summary"])["text"]["id"]
            except KeyError:
                print("Version already exists")
                return False, "Story already exists"

        for field in issue_details:
            if field == "Project":
                request_data["project"] = {
                    "value": project_id,
                    "type": "project"
                }
                continue

            if jira_config["issueTypes"][issue_type]["fields"][field]["allowedValues"]:
                value = [v["id"] for v in jira_config["issueTypes"][issue_type]["fields"][field]["allowedValues"]
                         if v["name"] == issue_details[field]][0]
            else:
                value = issue_details[field]
            request_data[jira_config["issueTypes"][issue_type]["fields"][field]["id"]] = {
                "type": jira_config["issueTypes"][issue_type]["fields"][field]["type"],
                "allowedValues": jira_config["issueTypes"][issue_type]["fields"][field]["allowedValues"],
                "value": value
            }

        # The lines below are a dirty cheat to make version work without having to make another api call to update story
        # or update the whole porject config file
        if version_id:
            request_data["versions"] = {
                "type": "array",
                "allowedValues": True,
                "value": version_id
            }

        create_response = jira.create_issue(request_data)

        if create_response["status"] == 201:
            if issue_type == "Story":
                jira.update_version(issue_details["Summary"], create_response["text"]["key"], version_id)
                update_body = {
                    "bau": issue_details_raw["bau"],
                    "projectId": issue_details_raw["projectId"]
                }
                update_jira_issue("release", update_body, issue_details["Epic Link"], jira_token)

        return True, create_response
    except Exception as e:
        return False, "Error while creating Jira Issue: {}".format(repr(e))

def update_jira_issue(issue_type, issue_details_raw, jira_ticket_id, jira_token):
    try:
        jira = JiraApi(jira_token)
        jira_config, issue_details = prepare_jira_data(issue_details_raw, issue_type)
        request_data = {}
        issue_type = issue_details["Issue Type"]
        print(issue_details["Project"])
        for field in issue_details:
            if field == "Project" or field == "Issue Type":
                continue
            if issue_type == "Capability":
                if field == "Device Model" or field == "Device Type":
                    continue
            if jira_config["issueTypes"][issue_type]["fields"][field]["allowedValues"]:
                value = [v["id"] for v in jira_config["issueTypes"][issue_type]["fields"][field]["allowedValues"]
                         if v["name"] == issue_details[field]][0]
            else:
                value = issue_details[field]

            request_data[jira_config["issueTypes"][issue_type]["fields"][field]["id"]] = {
                "type": jira_config["issueTypes"][issue_type]["fields"][field]["type"],
                "allowedValues": jira_config["issueTypes"][issue_type]["fields"][field]["allowedValues"],
                "value": value
            }
        update_response = jira.update_issue(jira_ticket_id, request_data)
        if update_response["status"] == 204:
            if issue_type == "Capability":
                releases = get_releases_for_device(jira_ticket_id, jira_token, issue_details["Project"])[1]
                for release in releases:
                    new_details = {
                        "projectId": issue_details_raw["projectId"]
                    }
                    if "modelMarketName" in issue_details_raw:
                        new_details["deviceModel"] = issue_details_raw["modelMarketName"]
                        try:
                            if "WDA_New Device Testing" in release["name"]:
                                new_details["epicName"] = issue_details_raw["vendor"] + " " + \
                                                          issue_details_raw["modelMarketName"] + "_" + "WDA_New Device Testing"
                            else:
                                new_details["epicName"] = issue_details_raw["vendor"] + " " + \
                                                          issue_details_raw["modelMarketName"] + "_" +  \
                                                          release["name"].split("_")[-1]
                        except Exception as e:
                            print(e)
                            pass
                    if "deviceType" in issue_details_raw:
                        new_details["deviceType"] = issue_details_raw["deviceType"]

                    print(update_jira_issue("release", new_details, release["key"], jira_token))
        return True, update_response

    except Exception as e:
        return False,  "Error while updating Jira Issue: {}".format(repr(e))

def prepare_jira_data(issue_details_raw, issue_type=None, project_id=None):
    issue_details = prepare_issue_data(issue_type, issue_details_raw)
    if not project_id:
        project_id = issue_details["Project"]
    project_config_file = get_config_file_for_project(project_id)
    with open(project_config_file, "r") as config_file:
        return json.load(config_file), issue_details

def prepare_jira_search(jira_config, issue_details, issue_type=None):
    request_body = {}
    for f in issue_details:
        request_body[jira_config["issueTypes"][issue_type]["fields"][f]["id"]] = issue_details[f]
    return field_to_jql(request_body)

def prepare_issue_details(issue_details, issue_type, project_id):
    jira_config, issue_details = prepare_jira_data(issue_details, issue_type, project_id)
    request_data = {}

    for field in issue_details:
        if jira_config["issueTypes"][issue_type]["fields"][field]["allowedValues"]:
            value = [v["id"] for v in jira_config["issueTypes"][issue_type]["fields"][field]["allowedValues"]
                     if v["name"] == issue_details[field]][0]
        else:
            value = issue_details[field]
        if "customfield" not in jira_config["issueTypes"][issue_type]["fields"][field]["id"]:
            request_data[jira_config["issueTypes"][issue_type]["fields"][field]["id"]] = {
                    "name": value
            }
        else:
            request_data[jira_config["issueTypes"][issue_type]["fields"][field]["id"]] = value
    return request_data

def get_devices_for_vendor(vendor, jira_token, project_id):
    try:
        jira = JiraApi(jira_token)
        data = {
            "vendor": vendor,
            "projectId": project_id
        }
        jira_config, issue_details = prepare_jira_data(data, "device")
        issue_details_updated = prepare_jira_search(jira_config, issue_details, "Capability")

        fields_to_return = ["summary", "modelMarketName", "type"]
        d = {}
        for f in fields_to_return:
            d[JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING[f]] = None

        update_fields_to_return = {}

        for f in d:
            if f != "Issue Type":
                update_fields_to_return[f] = jira_config["issueTypes"]["Capability"]["fields"][f]["id"]
        result = jira.search_story(issue_details_updated, [*update_fields_to_return.values()])

        final_result = []
        for r in result["text"]["issues"]:

            final_result.append({
                "key": r["key"],
                "summary": r["fields"]["summary"],
                "modelMarketName": r["fields"][update_fields_to_return[
                    JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING["modelMarketName"]]],
                "type": r["fields"][update_fields_to_return[JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING["type"]]],

            })
        return True, final_result
    except Exception as e:
        return False,  "Error while searching for a Jira Issue: {}".format(repr(e))

def get_releases_for_device(device_ticket_id, jira_token, project_id, fields_to_return=None):
    try:
        jira = JiraApi(jira_token)

        issue_details = {
            "Parent Link": device_ticket_id
        }
        if not fields_to_return:
            fields_to_return = []
        fields_to_return.extend(["epicName", "bau", "testingRequestType"])
        fields = dict()
        for f in fields_to_return:
            fields[f] = None

        update_fields_to_return = {}
        jira_config, d = prepare_jira_data(fields, "release", project_id)
        for f in d:
            update_fields_to_return[f] = {
                "id": jira_config["issueTypes"]["Epic"]["fields"][f]["id"],
                "type": jira_config["issueTypes"]["Epic"]["fields"][f]["type"]
            }

        # result = jira.search_story(issue_details, [*update_fields_to_return.values()])
        result = jira.search_story(issue_details, [update_fields_to_return[f]["id"] for f in update_fields_to_return])

        final_result = []
        # for r in result["text"]["issues"]:
        #     final_result.append({
        #         "key": r["key"],
        #         "name": r["fields"][update_fields_to_return[JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING["epicName"]]["id"]],
        #         "bau": r["fields"][update_fields_to_return[JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING["bau"]]["id"]],
        #         "testingRequestType": r["fields"][update_fields_to_return[
        #             JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING["testingRequestType"]]["id"]]["value"],
        #         "funding": r["fields"][update_fields_to_return[
        #             JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING["funding"]]["id"]]["value"]
        #     })

        for r in result["text"]["issues"]:
            result_fields = {
                "key": r["key"],
                "name": r["fields"][update_fields_to_return[JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING["epicName"]]["id"]]
            }
            for f in fields_to_return:
                if f == "epicName":
                    continue
                if update_fields_to_return[JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING[f]]["type"] == "option":
                    result_fields[f] = r["fields"][update_fields_to_return[
                            JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING[f]]["id"]]["value"]
                else:
                    result_fields[f] = r["fields"][update_fields_to_return[
                            JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING[f]]["id"]]

            final_result.append(result_fields)

        return True, final_result
    except Exception as e:
        return False,  "Error while searching for a Jira Issue: {}".format(repr(e))


def get_user(d_number, jira_token):
    try:
        jira = JiraApi(jira_token)
        user_details = jira.get_user_details(d_number)
        return True, user_details
    except Exception as e:
        return False,  "Error while retreiving user details: {}".format(repr(e))


def extract_story_from_url(url):
    url = unquote(url)
    project_url = url[url.index("project"):]
    project = project_url.split(" ")[2].replace('"', "")
    version_url = url[url.index("fixVersion"):]
    version = version_url.split("AND")[0].split("=")[1].strip().replace('"', "")
    print("Project: {}\nSoftware: {}".format(project, version))
    return project, version

def create_defect(issue_details, url, jira_token):
    project_id, version = extract_story_from_url(url)
    jira = JiraApi(jira_token)
    project_id = jira.get_project_details(project_id)["text"]["id"]
    project_config_file = get_config_file_for_project(project_id)

    all_versions = jira.get_all_versions(project_id)["text"]
    version_id = [v["id"] for v in all_versions if v["name"] == version][0]
    story_key = jira.get_version_details(version_id)["text"]["description"]
    print("Linked Story: {}".format(story_key))
    fields_to_retreive = [
        "Component/s",
        "Affects Version/s",
        "Epic Link"
    ]
    with open(project_config_file, "r") as config_file:
        jira_config = json.load(config_file)
    mapped_fields = [jira_config["issueTypes"]["Story"]["fields"][f]["id"] for f in fields_to_retreive]
    values = jira.get_issue_details(story_key, mapped_fields)["text"]["fields"]
    print(values)
    return
    keys_values = {}
    for v_index, v in enumerate(values):
        keys_values[fields_to_retreive[mapped_fields.index(v)]] = values[v]
    keys_values["Component/s"] = keys_values["Component/s"][0]["name"]
    keys_values["Affects Version/s"] = keys_values["Affects Version/s"][0]["name"]

    summary = issue_details["summary"]
    description = issue_details["description"]

    issue_details = {
        "Project": project_id,
        "Issue Type": "Bug",
        "Summary": summary,
        "Component/s": keys_values["Component/s"],
        "Description": description,
        "Affects Version/s": keys_values["Affects Version/s"],
        "Epic Link": keys_values["Epic Link"],
        "Affect": story_key
}
    print("Issue details: ")
    for f in issue_details:
        print("{}: {}".format(f, issue_details[f]))
    return create_jira_issue(issue_details, jira_token)

