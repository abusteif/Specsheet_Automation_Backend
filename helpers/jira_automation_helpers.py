from Specsheet_Automation.static_data.file_info import jira_config_file

def get_config_file_for_project(project_id):
    return "{}_{}.txt".format(jira_config_file, project_id)

def prepare_issue_data(issue_type, data):
    new_data = {}
    if issue_type == "device":
        new_data["Issue Type"] = "Capability"
        for f in data:
            if f == "vendor":
                new_data["Component/s"] = data[f]
            if f == "summary":
                new_data["Summary"] = data[f]
            if f == "projectId":
                new_data["Project"] = data[f]
    return new_data
