JIRA_USERNAME = "n110382"
JIRA_PASSWORD = "Jjhsydx@22"
JIRA_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
JIRA_AUTH_URL = "https://jira.tools.telstra.com/rest/auth/1/session"
JIRA_BASE_URL = "https://jira.tools.telstra.com/rest/api/latest"
JIRA_PROJECT_KEY = "WDACERT"
JIRA_PROJECT_ID = "44008"
JIRA_ISSUE_TYPES = ["Capability", "Epic", "Story", "Bug"]

JIRA_FRONTEND_TO_BACKEND_FIELD_MAPPING = {
    "vendor": "Component/s",
    "projectId": "Project",
    "summary": "Summary",
    "reporter": "Reporter",
    "modelMarketName": "RAG Comment",
    "type": "Section",
    "parentLink": "Parent Link",
    "epicName": "Epic Name",
    "epicLink": "Epic Link",
    "testingRequestType": "Testing Request Type",
    "testingPriority": "Testing Priority",
    "wdaTestScope": "WDA Test Scope",
    "baselineDate": "Baseline Date",
    "plannedStartDate": "Planned Start Date",
    "plannedDeliveryDate": "Planned Delivery Date",
    "changeDescription": "Change Description",
    "funding": "Funding",
    "deviceModel": "Device Model",
    "deviceType": "Device Type",
    "bau": "BAU Number",
}

CONFIG_REFRESH_INTERVAL = 24 * 3600
# CONFIG_REFRESH_INTERVAL = 1