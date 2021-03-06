from Specsheet_Automation.static_data.file_info import jira_config_file
from Specsheet_Automation.static_data.jira_config import JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING
def get_config_file_for_project(project_id):
    return "{}_{}.txt".format(jira_config_file, project_id)

def prepare_issue_data(issue_type, data):
    new_data = {}
    if issue_type == "device":
        new_data["Issue Type"] = "Capability"
    elif issue_type == "release":
        new_data["Issue Type"] = "Epic"
    elif issue_type == "iotCycle":
        new_data["Issue Type"] = "Story"

    for f in data:
        if f == "issueType":
            continue
        if f in JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING:
            new_data[JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING[f]] = data[f]
        else:
            new_data[f] = data[f]

        # if f == "vendor":
        #     new_data["Component/s"] = data[f]
        # elif f == "projectId":
        #     new_data["Project"] = data[f]
        # elif f == "summary":
        #     new_data["Summary"] = data[f]
        # elif f == "reporter":
        #     new_data["Reporter"] = data[f]
        # elif f == "modelMarketName":
        #     new_data["RAG Comment"] = data[f]
        # elif f == "deviceType":
        #     new_data["Section"] = data[f]
        # elif f == "issueType":
        #     pass
        # elif f == "parentLink":
        #     new_data["Parent Link"] = data[f]
        # elif f == "epicName":
        #     new_data["Epic Name"] = data[f]
        # elif f == "epicLink":
        #     new_data["Epic Link"] = data[f]
        # elif f == "testingRequestType":
        #     new_data["Testing Request Type"] = data[f]
        # elif f == "testingPriority":
        #     new_data["Testing Priority"] = data[f]
        # elif f == "wdaTestScope":
        #     new_data["WDA Test Scope"] = data[f]
        # elif f == "baselineDate":
        #     new_data["Baseline Date"] = data[f]
        # elif f == "plannedStartDate":
        #     new_data["Planned Start Date"] = data[f]
        # elif f == "plannedDeliveryDate":
        #     new_data["Planned Delivery Date"] = data[f]
        # elif f == "changeDescription":
        #     new_data["Change Description"] = data[f]
        # elif f == "funding":
        #     new_data["Funding"] = data[f]
        # elif f == "deviceModel":
        #     new_data["Device Model"] = data[f]
        # elif f == "deviceType":
        #     new_data["Device Type"] = data[f]
        # elif f == "bau":
        #     new_data["BAU Number"] = data[f]
        # else:
        #     new_data[f] = data[f]
        # if f == "projectId":
        #     new_data["Project"] = data[f]
    return new_data

def field_to_jql(data):
    new_data = {}
    for f in data:
        if f == "components":
            new_data["component"] = data[f]
        elif f == "Summary":
            new_data["summary"] = data[f]
        else:
            new_data[f] = data[f]
    return new_data