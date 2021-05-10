from Specsheet_Automation.classes.jira_operations_class import JiraOperations
from Specsheet_Automation.static_data.configuration import MAX_RETRY_COUNT

def wrap_api_result(result):
    return {
        "text": result.json(),
        "status": result.status_code
    }

