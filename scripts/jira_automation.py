from Specsheet_Automation.classes.jira_api import JiraApi
from Specsheet_Automation.static_data.jira_config import JIRA_ISSUE_TYPES, CONFIG_REFRESH_INTERVAL, JIRA_MANDATORY_FIELDS
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

def create_jira_issue(issue_type, issue_details, new_user, jira_token):
    try:
        jira = JiraApi(jira_token)

        jira_config, issue_details = prepare_jira_data(issue_details, issue_type)
        project_id = issue_details["Project"]
        project_config_file = get_config_file_for_project(project_id)
        request_data = {}
        issue_type = issue_details["Issue Type"]

        version_id = 0
        if issue_type == "Story":
            version_id = jira.create_version(project_id, issue_details["Summary"])["text"]["id"]
            initialise_jira(project_id, jira_token, True)
            with open(project_config_file, "r") as config_file:
                jira_config = json.load(config_file)

        for field in issue_details:
            if field == "Project":
                request_data["project"] = {
                    "value": project_id,
                    "type": "project"
                }
                continue
            if field == "Affect":
                request_data["update"] = issue_details["Affect"]
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
        create_response = jira.create_issue(request_data)
        if new_user and create_response["status"] == 201:
            body = {"reporter": {"name": new_user}}
            update_response = jira.update_issue(create_response["text"]["id"], body)
        if create_response["status"] == 201:
            if issue_type == "Story":
                jira.update_version(issue_details["Summary"], create_response["text"]["key"], version_id)

        return True, create_response
    except Exception as e:
        return False,  "Error while creating Jira Issue: {}".format(repr(e))

def update_issue_details(issue_key, issue_details, project_id, issue_type, jira_token):
    try:

        request_data = prepare_issue_details(issue_details, issue_type, project_id)
        jira = JiraApi(jira_token)
        update_result = jira.update_issue(issue_key, request_data)
        if update_result["status"] == 204:
            return True, "Jira ticket updated sucessfully"
        return False, update_result["text"]
    except Exception as e:
        return False,  "Error while updating Jira Issue: {}".format(repr(e))


def prepare_jira_data(issue_details, issue_type=None, project_id=None):
    issue_details = prepare_issue_data(issue_type, issue_details)
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

def get_devices_for_vendor(vendor, jira_token, project_id, fields_to_return=None):
    try:
        jira = JiraApi(jira_token)
        data = {
            "vendor": vendor,
            "projectId": project_id
        }
        jira_config, issue_details = prepare_jira_data(data, "device")
        issue_details = prepare_jira_search(jira_config, issue_details, issue_details["Issue Type"])
        if not fields_to_return:
            fields_to_return = ["summary"]
        result = jira.search_story(issue_details, fields_to_return)
        final_result = []
        for r in result["text"]["issues"]:
            final_result.append({
                "key": r["key"],
                "summary": r["fields"]["summary"]
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
            fields_to_return = {
                "epicName": None,
                "bau": None,
                "testingRequestType": None

            }
        update_fields_to_return = {}
        jira_config, d = prepare_jira_data(fields_to_return, "release", project_id)
        for f in d:
            update_fields_to_return[f] = jira_config["issueTypes"]["Epic"]["fields"][f]["id"]

        result = jira.search_story(issue_details, [*update_fields_to_return.values()])
        final_result = []
        for r in result["text"]["issues"]:
            final_result.append({
                "key": r["key"],
                "name": r["fields"][update_fields_to_return["Epic Name"]],
                "bau": r["fields"][update_fields_to_return["BAU Number"]],
                "testingRequestType": r["fields"][update_fields_to_return["Testing Request Type"]]["value"]

            })
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

def create_version(project_id, name, description, jira_token):
    jira = JiraApi(jira_token)
    jira.create_version(project_id, name, description)
    return

def extract_story_from_url(url):
    url = unquote(url)
    project_url = url[url.index("project"):]
    project = project_url.split(" ")[2].replace('"', "")
    version_url = url[url.index("fixVersion"):]
    version = version_url.split("AND")[0].split("=")[1].strip().replace('"', "")
    print("Project: {}\nSoftware: {}".format(project, version))
    return project, version

def create_defect(url, summary, description, jira_token):
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
    keys_values = {}
    for v_index, v in enumerate(values):
        keys_values[fields_to_retreive[mapped_fields.index(v)]] = values[v]
    keys_values["Component/s"] = keys_values["Component/s"][0]["name"]
    keys_values["Affects Version/s"] = keys_values["Affects Version/s"][0]["name"]

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

