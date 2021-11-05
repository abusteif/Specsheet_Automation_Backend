from Specsheet_Automation.helpers.specsheet_automation_helpers import get_delimiter, \
    extract_data, get_full_path, cleanup_files, extract_data_from_multiple_messages
#   upload_results_to_jira, check_if_test_case_executed, \
#   get_ie_results_from_jira, \
from Specsheet_Automation.static_data.file_info import dut_UECI_lists_file, NR_dut_UECI_lists_file
from Specsheet_Automation.static_data.LTE_specsheet_fields import MSR0835_all_UECI_fields
from Specsheet_Automation.scripts.data_analysis.populate_NR_LTE_specsheet import populate_NR_LTE_specsheet
from Specsheet_Automation.static_data.configuration import ATTACHREQUEST_MESSAGE_TYPE
from Specsheet_Automation.classes.jira_api import JiraApi
from Specsheet_Automation.static_data.jira_config import JIRA_ISSUE_TYPES, CONFIG_REFRESH_INTERVAL, JIRA_MANDATORY_FIELDS
from Specsheet_Automation.static_data.file_info import jira_config_file
from Specsheet_Automation.classes.jira_api import JiraApi

from datetime import datetime
import json
from json import JSONDecodeError

# def extract_and_upload(hex_data, message_type, sim_type, dut_name, iot_cycle, jira_token):
#
#     if message_type == ATTACHREQUEST_MESSAGE_TYPE:
#         return False, "Trying to upload invalid message type"
#     delimiter = get_delimiter(message_type)
#     converting = extract_data(hex_data, message_type, delimiter)
#     unique_folder_path = converting[1]
#     file_info = dut_UECI_lists_file if "4G" in message_type else NR_dut_UECI_lists_file
#     lists_file = get_full_path(file_info, unique_folder_path, True)
#
#     if not converting[0][0]:
#         cleanup_files(unique_folder_path)
#         return False, converting[0][1]
#
#     uploading = upload_results_to_jira(dut_name, iot_cycle, lists_file, message_type, sim_type, jira_token)
#
#     return uploading[0], uploading[1]


def extract_and_populate_specsheet(hex_data, dut_name, iot_cycle):
    extract_result = extract_data_from_multiple_messages(hex_data)
    if not extract_result[0]:
        return False, extract_result[1]
    attach_request_lists_file, UECapabilityInfo_lists_file, NR_UECapabilityInfo_lists_file, \
        unique_folder_path = extract_result[1]

    specsheet_full_path = get_full_path("NR_LTE_specsheet_template_{}_{}.xlsx".
                                        format(dut_name, iot_cycle), unique_folder_path, True)
    populating = populate_NR_LTE_specsheet(specsheet_full_path,
                                           UECapabilityInfo_lists_file=UECapabilityInfo_lists_file,
                                           NR_UECapabilityInfo_lists_file=NR_UECapabilityInfo_lists_file,
                                           attach_request_lists_file=attach_request_lists_file)

    if not populating[0]:
        return False, populating[1]
    return True, unique_folder_path, specsheet_full_path


def validate_data(hex_data, message_type):

    delimiter = get_delimiter(message_type)
    converting = extract_data(hex_data, message_type, delimiter)
    cleanup_files(converting[1])
    return converting[0][0], converting[0][1]

# def check_for_execution(message_type, sim_type, dut_name, iot_cycle, jira_token):
#     return check_if_test_case_executed(message_type, sim_type, dut_name, iot_cycle, jira_token)

def get_message_fields(message_type):
    if message_type == "UECapabilityInformation_4G":
        fields = []
        for ie in MSR0835_all_UECI_fields:
            if "processor" in list(ie.keys()):
                if not isinstance(ie["processor"], list):
                    fields.append(ie["processor"].split(","))

            else:
                if not isinstance(ie["path"], list):
                    fields.append(ie["path"].split(","))
                else:
                    fields.append(",".join(ie["path"]))
        return fields
    else:
        return []

# def get_all_ie_from_jira(message_type, sim_type, dut_name, iot_cycle, jira_token):
#     return get_ie_results_from_jira(message_type, sim_type, dut_name, iot_cycle, jira_token)

def initialise_jira(project_id, jira_token):
    try:
        with open(jira_config_file, "r+") as config_file:
            try:
                saved_data = json.load(config_file)
                if int(datetime.now().timestamp()) - saved_data["lastUpdated"] < CONFIG_REFRESH_INTERVAL:
                    return True, "Update not due"
            except JSONDecodeError:
                pass
            config_file.seek(0)
            config_file.truncate()
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
                # if issue == "Bug":
                #     print(jira.get_meta_data_for_issue_type(project_id, "1")["text"])
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
        return True, "Config data updated successfull"
    except Exception as e:
        return False, "Error updating Jira config file: {}".format(repr(e))

def create_jira_issue(issue_details, jira_token):
    jira = JiraApi(jira_token)
    with open(jira_config_file, "r") as config_file:
        jira_config = json.load(config_file)
    request_data = {}
    issue_type = issue_details["Issue Type"]
    assert sorted(issue_details.keys()) == sorted(JIRA_MANDATORY_FIELDS[issue_type])
    for field in issue_details:
        if field == "Project":
            request_data["project"] = {
                "value": issue_details["Project"],
                "type": "project"
            }
            continue
        if field == "Affect":
            request_data["update"] = issue_details[field]["Affect"]
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
    print(jira.create_issue(request_data))
