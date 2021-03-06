import requests
import json
from json import JSONDecodeError
from Specsheet_Automation.static_data.jira_config import JIRA_USERNAME, JIRA_PASSWORD, JIRA_BASE_URL, JIRA_AUTH_URL, \
    JIRA_HEADERS
import time
from multiprocessing import Value

JIRA_AUTH = (JIRA_USERNAME, JIRA_PASSWORD)
TIMEOUT = 10
counter_rate_limit = Value('i', 0)


def rate_limiter(api_call):
    def wrapper(*args, **kwargs):
        sleep = 2
        while True:
            result = api_call(*args, **kwargs)
            status_code = result.status_code
            if status_code == 429:
                with counter_rate_limit.get_lock():
                    counter_rate_limit.value += 1
                    print("rate limit error: " + str(counter_rate_limit.value))
                time.sleep(sleep)
                sleep *= 2
            else:
                try:
                    return {
                        "text": result.json(),
                        "status": result.status_code
                    }
                except JSONDecodeError:
                    return {
                        "text": "",
                        "status": result.status_code
                    }
    return wrapper

class JiraApi:
    def __init__(self, cookies=None):
        if cookies:
            self.cookies = {"crowd.token_key": cookies}
        else:
            self.cookies = requests.get(JIRA_AUTH_URL, headers=JIRA_HEADERS, auth=JIRA_AUTH, timeout=TIMEOUT).cookies

    def get_cookies(self):
        return self.cookies

    @rate_limiter
    def get_user_details(self, user_id):
        url = "{}/user?username={}".format(JIRA_BASE_URL, user_id)
        # return wrap_api_result(requests.get(url, cookies=self.cookies))
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def get_project_details(self, project_key):
        url = "{}/project/{}".format(JIRA_BASE_URL, project_key)
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def get_all_issue_types(self):
        url = "{}/issuetype".format(JIRA_BASE_URL)
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def get_all_issue_fields(self):
        url = "{}/field".format(JIRA_BASE_URL)
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def get_all_components(self, project_id):
        url = "{}/project/{}/components".format(JIRA_BASE_URL, project_id)
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def get_meta_data_for_issue_type(self, project_key, issue_type):
        url = "{}/issue/createmeta/{}/issuetypes/{}?maxResults=100".format(JIRA_BASE_URL, project_key, issue_type)
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def get_link_types(self):
        url = "{}/issueLinkType".format(JIRA_BASE_URL)
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def get_issue_details(self, key_or_id, fields_to_return=None):
        url = "{}/issue/{}".format(JIRA_BASE_URL, key_or_id)
        if fields_to_return:
            url += "?fields=" + ",".join(fields_to_return)
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def get_all_versions(self, project_id):
        url = "{}/project/{}/versions".format(JIRA_BASE_URL, project_id)
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def get_version_details(self, version_id):
        url = "{}/version/{}".format(JIRA_BASE_URL, version_id)
        return requests.get(url, cookies=self.cookies)

    @rate_limiter
    def create_issue(self, fields):
        return self.create_update_issue(fields)
        # url = "{}/{}".format(JIRA_BASE_URL, "issue")
        # body = {
        #     "fields": dict()
        # }
        # for f in fields:
        #     if f == "update":
        #         continue
        #     if fields[f]["type"] == "string" or \
        #             fields[f]["type"] == "any" or \
        #             fields[f]["type"] == "date" or \
        #             fields[f]["type"] == "number":
        #         body["fields"][f] = fields[f]["value"]
        #
        #     if fields[f]["type"] == "array":
        #         if fields[f]["allowedValues"]:
        #             body["fields"][f] = [
        #                 {
        #                     "id": fields[f]["value"]
        #                 }
        #             ]
        #         else:
        #             body["fields"][f] = [fields[f]["value"]]
        #
        #     if fields[f]["type"] == "option":
        #         if fields[f]["allowedValues"]:
        #             body["fields"][f] = {
        #                     "id": fields[f]["value"]
        #                 }
        #
        #     if fields[f]["type"] == "project" or \
        #             fields[f]["type"] == "issuetype":
        #         body["fields"][f] = {
        #             "id": fields[f]["value"]
        #         }
        #
        #     if fields[f]["type"] == "user":
        #         body["fields"][f] = {
        #             "name": fields[f]["value"]
        #         }
        # print(body)
        # json_payload = json.dumps(body)
        # # return {"text": "", "status": 400}
        # return requests.post(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies)

    @rate_limiter
    def update_issue(self, issue_key, fields):
        return self.create_update_issue(fields, issue_key)
        # url = "{}/issue/{}".format(JIRA_BASE_URL, issue_key)
        # body = {
        #     "fields": dict()
        # }
        # for f in fields:
        #     body["fields"][f] = fields[f]
        # json_payload = json.dumps(body)
        # return requests.put(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies)

    def create_update_issue(self, fields, issue_key=None):
        if issue_key:
            url = "{}/issue/{}".format(JIRA_BASE_URL, issue_key)
        else:
            url = "{}/issue".format(JIRA_BASE_URL)

        body = {
            "fields": dict()
        }
        for f in fields:
            if f == "update":
                continue
            if fields[f]["type"] == "string" or \
                    fields[f]["type"] == "any" or \
                    fields[f]["type"] == "date" or \
                    fields[f]["type"] == "number":
                body["fields"][f] = fields[f]["value"]

            if fields[f]["type"] == "array":
                if fields[f]["allowedValues"]:
                    body["fields"][f] = [
                        {
                            "id": fields[f]["value"]
                        }
                    ]
                else:
                    body["fields"][f] = [fields[f]["value"]]

            if fields[f]["type"] == "option":
                if fields[f]["allowedValues"]:
                    body["fields"][f] = {
                            "id": fields[f]["value"]
                        }

            if fields[f]["type"] == "project" or \
                    fields[f]["type"] == "issuetype":
                body["fields"][f] = {
                    "id": fields[f]["value"]
                }

            if fields[f]["type"] == "user":
                body["fields"][f] = {
                    "name": fields[f]["value"]
                }

        print(body)
        json_payload = json.dumps(body)
        if issue_key:
            return requests.put(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies)
        else:
            return requests.post(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies)

    @rate_limiter
    def create_version(self, project, name, description=None):
        url = "{}/version".format(JIRA_BASE_URL)
        body = {
            "projectId": project,
            "name": name,
            "description": description,
        }
        json_payload = json.dumps(body)
        return requests.post(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies)

    @rate_limiter
    def update_version(self, name, description, version_id):
        url = "{}/version/{}".format(JIRA_BASE_URL, version_id)
        body = {
            "name": name,
            "description": description,
        }
        json_payload = json.dumps(body)
        return requests.put(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies)

    @rate_limiter
    def search_story(self, query, fields_to_return):
        query_string = " AND ".join(["'{}'='{}'".format(q, query[q]) for q in [*query]])

        url = "{}/search".format(JIRA_BASE_URL)
        body = {
            "jql": query_string,
            "fields": fields_to_return
        }
        json_payload = json.dumps(body)
        print(body)
        # return requests.post(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies))
        return requests.post(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies)


    # def get_project_id_from_project_key(self, project_key):
    #     url = "{}/{}/{}".format(JIRA_BASE_URL, JIRA_END_POINTS["get_project_id_from_project_key"], project_key)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
        # return wrap_api_result(self.session.get(url))
    #
    # def get_all_versions(self, project_id):
    #     url = "{}/{}/{}/version?maxResults=1000".format(JIRA_BASE_URL, JIRA_END_POINTS["get_all_versions"], project_id)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    #     # return wrap_api_result(self.session.get(url))
    #
    # # def check_zephyr_status(self):
    # #     url = "{}/{}/-1".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_cycle_by_id"])
    # #     return wrap_api_result(self.session.get(url))
    # #     # return self.session.get(url)
    #
    # def get_all_cycles(self, project_id, version_id):
    #     url = "{}/{}?projectId={}&versionId={}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_all_cycles"],
    #                                                    project_id, version_id)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    #     # return wrap_api_result(self.session.get(url))
    #
    # def get_cycle_by_id(self, cycle_id):
    #     url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_cycle_by_id"], cycle_id)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    #     # return wrap_api_result(self.session.get(url))
    #
    # def get_all_executions(self, test_case_id):
    #     url = "{}/{}?issueId={}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_all_executions"], test_case_id)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    #     # return wrap_api_result(self.session.get(url))
    #
    # def get_one_execution(self, cycle_id, project_id, version_id):
    #     url = "{}/{}?cycleId={}&projectId={}&versionId={}".\
    #         format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_one_execution"], cycle_id, project_id, version_id)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    #     # return wrap_api_result(self.session.get(url))
    #
    # def get_execution_status(self, execution_id):
    #     url = "{}/{}/{}?expand=checksteps".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_execution_status"],
    #                                               execution_id)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    #     # return wrap_api_result(self.session.get(url))
    #
    # def add_test_case_to_cycle(self, cycle_id, project_id, version_id, test_case_key):
    #     url = "{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["add_test_case_to_cycle"])
    #     new_content = {
    #         "cycleId": cycle_id,
    #         "issues": [test_case_key],
    #         "projectId": project_id,
    #         "versionId": version_id,
    #         "method": "1"
    #     }
    #     json_payload = json.dumps(new_content)
    #     return wrap_api_result(requests.post(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies))
    #
    # def get_job_progress_status(self, job_progress_token):
    #     url = "{}/{}/{}?type=add_tests_to_cycle_job_progress".\
    #         format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_job_progress_status"], job_progress_token)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    # def get_steps_result_by_execution(self, execution_id, offset, limit=500):
    #     url = "{}/{}={}&limit={}&offset={}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_steps_by_execution"],
    #                                                execution_id, limit, str(offset))
    #
    #     for retry in range(MAX_RETRY_COUNT):
    #         try:
    #             return wrap_api_result(requests.get(url, cookies=self.cookies, timeout=20))
    #
    #             # return wrap_api_result(self.session.get(url))
    #         except Exception as e:
    #             print("Following error occurred while fetching step results: {}\nRetrying..".format(repr(e)))
    #             time.sleep(RETRY_SLEEP)
    #             continue
    #     else:
    #         print("Unable to fetch results step results. Please try again later.")
    #         return
    #
    # def update_step_result_by_id(self, step_id, new_content):
    #     url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["update_step_result_by_id"], step_id)
    #     json_payload = json.dumps(new_content)
    #
    #     for retry in range(MAX_RETRY_COUNT):
    #         try:
    #             return wrap_api_result(requests.put(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies,
    #                                                 timeout=TIMEOUT))
    #
    #         except Exception as e:
    #             print("error while uploading test result: {} {}".format(step_id, new_content))
    #             time.sleep(RETRY_SLEEP)
    #             continue
    #     else:
    #         print("Unable to upload result to Jira.")
    #         return wrap_api_result(requests.put(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies))
    #
    # def search_for_test_case(self, test_case_key):
    #     url = "{}/{}/{}".format(JIRA_BASE_URL, JIRA_END_POINTS["search_for_test_case"], test_case_key)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    # def update_test_case_execution_status(self, execution_id, new_content):
    #     url = "{}/{}/{}/execute".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["update_test_case_execution_status"],
    #                                     execution_id)
    #     json_payload = json.dumps(new_content)
    #     return wrap_api_result(requests.put(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies))
    #
    # def delete_test_case_execution(self, execution_id):
    #     url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["delete_test_case_execution"], execution_id)
    #     for retry in range(MAX_RETRY_COUNT):
    #         try:
    #             return wrap_api_result(requests.delete(url, cookies=self.cookies))
    #         except Exception as e:
    #             print("error while deleting execution")
    #             time.sleep(RETRY_SLEEP)
    #             continue
    #     else:
    #         print("Unable to delete test case")
    #         return wrap_api_result(requests.delete(url, cookies=self.cookies))
    #
    # def get_test_case_steps(self, test_case_id):
    #     url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["get_test_case_steps"], test_case_id)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    #     # return wrap_api_result(self.session.get(url))
    #
    # def create_step(self, test_case_id, new_content):
    #     url = "{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["create_step"], test_case_id)
    #     json_payload = json.dumps(new_content)
    #     return wrap_api_result(requests.post(url, data=json_payload, headers=JIRA_HEADERS, cookies=self.cookies))
    #
    #     # return wrap_api_result(self.session.post(url, data=json_payload, headers=JIRA_HEADERS))
    #
    # def delete_step(self, test_case_id, test_step_id):
    #     url = "{}/{}/{}/{}".format(ZEPHYR_BASE_URL, ZEPHYR_END_POINTS["delete_step"], test_case_id, test_step_id)
    #     return wrap_api_result(requests.get(url, cookies=self.cookies))
    #
    #     # return wrap_api_result(self.session.get(url))
