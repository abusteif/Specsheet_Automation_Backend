import requests
import json
from Specsheet_Automation.static_data.configuration import *
# from Specsheet_Automation_2.helpers.common_helpers import wrap_api_result
import time

JIRA_AUTH = (JIRA_USERNAME, JIRA_PASSWORD)
TIMEOUT = 10
def wrap_api_result(result):
    return {
        "text": result.json(),
        "status": result.status_code
    }

class JiraOperations:
    def __init__(self, cookies=None):
        if cookies:
            self.cookies = {"crowd.token_key": cookies}
        else:
            print("Getting Jira Cookie")

            # self.session = requests.Session()
            # self.session.get(JIRA_AUTH_URL, headers=JIRA_HEADERS, auth=(JIRA_USERNAME, JIRA_PASSWORD), timeout=TIMEOUT)
            self.cookies = requests.get(JIRA_AUTH_URL, headers=JIRA_HEADERS, auth=(JIRA_USERNAME, JIRA_PASSWORD), timeout=TIMEOUT).cookies
            print("Received Jira Cookie")

    def get_cookies(self):
        return self.cookies

    def get_project_id_from_project_key(self, project_key):
        url = "{}/{}/{}".format(JIRA_BASE_URL, JIRA_END_POINTS["get_project_id_from_project_key"], project_key)
        return wrap_api_result(requests.get(url, cookies=self.cookies))
        # return wrap_api_result(self.session.get(url))

    def get_all_versions(self, project_id):
        url = "{}/{}/{}/version?maxResults=1000".format(JIRA_BASE_URL, JIRA_END_POINTS["get_all_versions"], project_id)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

        # return wrap_api_result(self.session.get(url))

    # def check_zephyr_status(self):
    #     url = "{}/{}/-1".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_cycle_by_id"])
    #     return wrap_api_result(self.session.get(url))
    #     # return self.session.get(url)

    def get_all_cycles(self, project_id, version_id):
        url = "{}/{}?projectId={}&versionId={}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_all_cycles"],
                                                       project_id, version_id)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

        # return wrap_api_result(self.session.get(url))

    def get_cycle_by_id(self, cycle_id):
        url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_cycle_by_id"], cycle_id)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

        # return wrap_api_result(self.session.get(url))

    def get_all_executions(self, test_case_id):
        url = "{}/{}?issueId={}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_all_executions"], test_case_id)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

        # return wrap_api_result(self.session.get(url))

    def get_one_execution(self, cycle_id, project_id, version_id):
        url = "{}/{}?cycleId={}&projectId={}&versionId={}".\
            format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_one_execution"], cycle_id, project_id, version_id)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

        # return wrap_api_result(self.session.get(url))

    def get_execution_status(self, execution_id):
        url = "{}/{}/{}?expand=checksteps".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_execution_status"],
                                                  execution_id)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

        # return wrap_api_result(self.session.get(url))

    def add_test_case_to_cycle(self, cycle_id, project_id, version_id, test_case_key):
        url = "{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["add_test_case_to_cycle"])
        new_content = {
            "cycleId": cycle_id,
            "issues": [test_case_key],
            "projectId": project_id,
            "versionId": version_id,
            "method": "1"
        }
        json_payload = json.dumps(new_content)
        return wrap_api_result(requests.post(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies))

    def get_job_progress_status(self, job_progress_token):
        url = "{}/{}/{}?type=add_tests_to_cycle_job_progress".\
            format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_job_progress_status"], job_progress_token)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

    def get_steps_result_by_execution(self, execution_id, offset, limit=500):
        url = "{}/{}={}&limit={}&offset={}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_steps_by_execution"],
                                                   execution_id, limit, str(offset))

        for retry in range(MAX_RETRY_COUNT):
            try:
                return wrap_api_result(requests.get(url, cookies=self.cookies, timeout=20))

                # return wrap_api_result(self.session.get(url))
            except Exception as e:
                print("Following error occurred while fetching step results: {}\nRetrying..".format(repr(e)))
                time.sleep(RETRY_SLEEP)
                continue
        else:
            print("Unable to fetch results step results. Please try again later.")
            return

    def update_step_result_by_id(self, step_id, new_content):
        url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["update_step_result_by_id"], step_id)
        json_payload = json.dumps(new_content)

        for retry in range(MAX_RETRY_COUNT):
            try:
                return wrap_api_result(requests.put(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies,
                                                    timeout=TIMEOUT))

            except Exception as e:
                print("error while uploading test result: {} {}".format(step_id, new_content))
                time.sleep(RETRY_SLEEP)
                continue
        else:
            print("Unable to upload result to Jira.")
            return wrap_api_result(requests.put(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies))

    def search_for_test_case(self, test_case_key):
        url = "{}/{}/{}".format(JIRA_BASE_URL, JIRA_END_POINTS["search_for_test_case"], test_case_key)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

    def update_test_case_execution_status(self, execution_id, new_content):
        url = "{}/{}/{}/execute".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["update_test_case_execution_status"],
                                        execution_id)
        json_payload = json.dumps(new_content)
        return wrap_api_result(requests.put(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies))

    def delete_test_case_execution(self, execution_id):
        url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["delete_test_case_execution"], execution_id)
        for retry in range(MAX_RETRY_COUNT):
            try:
                return wrap_api_result(requests.delete(url, cookies=self.cookies))
            except Exception as e:
                print("error while deleting execution")
                time.sleep(RETRY_SLEEP)
                continue
        else:
            print("Unable to delete test case")
            return wrap_api_result(requests.delete(url, cookies=self.cookies))

    def get_test_case_steps(self, test_case_id):
        url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_test_case_steps"], test_case_id)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

        # return wrap_api_result(self.session.get(url))

    def create_step(self, test_case_id, new_content):
        url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["create_step"], test_case_id)
        json_payload = json.dumps(new_content)
        return wrap_api_result(requests.post(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies))

        # return wrap_api_result(self.session.post(url, data=json_payload, headers=JIRA_HEADERS))

    def delete_step(self, test_case_id, test_step_id):
        url = "{}/{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["delete_step"], test_case_id, test_step_id)
        return wrap_api_result(requests.get(url, cookies=self.cookies))

        # return wrap_api_result(self.session.get(url))
