from Specsheet_Automation.classes.jira_api import *
from Specsheet_Automation.static_data.jira_config import *
jira = JiraApi()
print(jira.cookies["crowd.token_key"])
# with open("bug_fields.txt", "w") as f:
#     f.write(json.dumps(jira.get_meta_data_for_issue_type("44008", "1")["text"]))
# print(jira.get_meta_data_for_issue_type("44008", "1")["text"])
# print(jira.get_meta_data(44008))
# print(jira.get_meta_data())
# print(jira.get_project_details("TOOLSUPPRT"))
# with open("issue_types.txt", "w") as i:
#     i.write(json.dumps(jira.get_all_issue_types()["text"]))
# print(jira.get_link_types())
print(jira.get_all_components("44008"))
# print(jira.create_version("44008", "MJA_test_version_1", "Associated story number goes here"))
