JIRA_USERNAME = "n110382"
JIRA_PASSWORD = "Mtsrobo67@"
JIRA_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
JIRA_AUTH_URL = "https://jira.tools.telstra.com/rest/auth/1/session"
JIRA_BASE_URL = "https://jira.tools.telstra.com/rest/api/latest"
JIRA_PROJECT_KEY = "WDACERT"
JIRA_PROJECT_ID = "44008"
JIRA_ISSUE_TYPES = ["Capability", "Epic", "Story", "Bug"]
JIRA_MANDATORY_FIELDS = {
    "Capability": [
        "Project",
        "Issue Type",
        "Summary",
        "Component/s"
    ],
    "Epic": [
        "Project",
        "Issue Type",
        "Summary",
        "Component/s",
        "Parent Link",
        "Epic Name",
        "Target start",
        "Target end",
        # "Production Deployment Scheduled Start",
        # "Production Deployment Scheduled End"
    ],
    "Story": [
        "Project",
        "Issue Type",
        "Summary",
        "Component/s",
        "Epic Link",
        "Affects Version/s",
        "Start date",
        "Current Finish Date",
        # "Due Date",
        # "Baseline Finish Date"
    ],
    "Bug": [
        "Project",
        "Issue Type",
        "Summary",
        "Component/s",
        "Description",
        "Affects Version/s",
        "Epic Link",
        "Affect"
    ]
}
# CONFIG_REFRESH_INTERVAL = 24 * 3600
CONFIG_REFRESH_INTERVAL = 1