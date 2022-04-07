from Specsheet_Automation.classes.jira_api import JiraApi
from Specsheet_Automation.static_data.jira_config import JIRA_ISSUE_TYPES, CONFIG_REFRESH_INTERVAL, JIRA_MANDATORY_FIELDS
from Specsheet_Automation.helpers.jira_automation_helpers import get_config_file_for_project, prepare_issue_data
# from Specsheet_Automation.static_data.file_info import jira_config_file

import json
import os
from datetime import datetime
from json import JSONDecodeError
from urllib.parse import unquote


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
                print(meta_data)
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

def get_device_types_from_local(project_id):
    try:
        project_config_file = get_config_file_for_project(project_id)
        with open(project_config_file, "r") as config_file:
            saved_data = json.load(config_file)
            device_types = saved_data["issueTypes"]["Epic"]["fields"]["Device Type"]["allowedValues"]
        return True, device_types
    except Exception as e:
        return False, "Error while retreiving vendors list: {}".format(repr(e))


def create_jira_issue(issue_type, issue_details, jira_token):
    try:
        issue_details = prepare_issue_data(issue_type, issue_details)
        jira = JiraApi(jira_token)
        project_id = issue_details["Project"]
        project_config_file = get_config_file_for_project(project_id)

        print("Getting issue field details")
        with open(project_config_file, "r") as config_file:
            jira_config = json.load(config_file)
        request_data = {}
        issue_type = issue_details["Issue Type"]
        assert sorted(issue_details.keys()) >= sorted(JIRA_MANDATORY_FIELDS[issue_type])

        version_id = 0
        if issue_type == "Story":
            print("Issue is a Story. Creating the associated Version")
            version_id = jira.create_version(project_id, issue_details["Summary"])["text"]["id"]
            initialise_jira(project_id, jira_token, True)
            with open(project_config_file, "r") as config_file:
                jira_config = json.load(config_file)

        for field in issue_details:
            print(field)
            if field == "Project":
                request_data["project"] = {
                    "value": project_id,
                    "type": "project"
                }
                continue
            if field == "Affect":
                print("Linking Story to Epic")
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
        print("Creating Ticket")
        response = jira.create_issue(request_data)
        print(response)
        if response["status"] == 201:
            if issue_type == "Story":
                jira.update_version(issue_details["Summary"], response["text"]["key"], version_id)

        return True, response
    except Exception as e:
        return False,  "Error while creating Jira Issue: {}".format(repr(e))

def create_version(project_id, name, description, jira_token):
    jira = JiraApi(jira_token)
    jira.create_version(project_id, name, description)
    return

def extract_story_from_url(url):
    print("Extracting Information from URL")
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
