from Specsheet_Automation.classes.jira_api import *
from Specsheet_Automation.static_data.jira_config import *
jira = JiraApi()
# with open("bug_fields.txt", "w") as f:
#     f.write(json.dumps(jira.get_meta_data_for_issue_type("44008", "1")["text"]))
# print(jira.get_meta_data_for_issue_type("44008", "1")["text"])
# print(jira.get_meta_data(44008))
# print(jira.get_meta_data())
# print(jira.get_project_details("TOOLSUPPRT"))
# with open("issue_types.txt", "w") as i:
#     i.write(json.dumps(jira.get_all_issue_types()["text"]))
print(jira.get_link_types())
