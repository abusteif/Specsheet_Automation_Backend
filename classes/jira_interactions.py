from Specsheet_Automation.classes.jira_operations_class import JiraOperations
import time
class JiraInteractions:

    def __init__(self, device_name=None, iot_cycle=None, project_key=None, jira_token=None):
        self.jira_operations = JiraOperations(jira_token)
        self.version_id = ""
        self.cycle_id = ""
        self.project_id = ""
        if device_name:
            self.get_device_jira_info(device_name, iot_cycle, project_key)

    def add_steps_to_test_case(self, test_case_key, new_steps_list):
        test_case = self.jira_operations.search_for_test_case(test_case_key)["text"]
        test_case_id = test_case["id"]
        all_steps = [step["step"] for step in
                     self.jira_operations.get_test_case_steps(test_case_id)["text"]["stepBeanCollection"]]

        for new_step in new_steps_list:
            if new_step not in all_steps:
                content = {"step": new_step}
                self.jira_operations.create_step(test_case_id, content)

    def get_device_jira_info(self, device_name, iot_cycle, project_key):
        self.project_id = self.jira_operations.get_project_id_from_project_key(project_key)["text"]["id"]
        all_versions = self.jira_operations.get_all_versions(self.project_id)["text"]
        if device_name in [version["id"] for version in all_versions["values"]]:
            self.version_id = device_name
        else:
            self.version_id = [version["id"] for version in all_versions["values"] if version["name"] == device_name][0]

        all_cycles = self.jira_operations.get_all_cycles(self.project_id, self.version_id)["text"]
        if iot_cycle in list(all_cycles.keys()):
            self.cycle_id = iot_cycle
        else:
            self.cycle_id = [cycle for cycle in all_cycles if isinstance(all_cycles[cycle], dict) and
                             all_cycles[cycle]["name"] == iot_cycle][0]

    def check_for_test_case(self, test_case_key, create_if_not_found=True, delete_if_found=False):
        test_case = self.jira_operations.search_for_test_case(test_case_key)["text"]
        test_case_id = test_case["id"]

        all_test_cases = self.jira_operations.get_one_execution(self.cycle_id, self.project_id,
                                                                self.version_id)["text"]["executions"]
        test_case_status = [test_case for test_case in all_test_cases if int(test_case["issueId"]) == int(test_case_id)]
        if delete_if_found and test_case_status:
            self.jira_operations.delete_test_case_execution(str(test_case_status[0]["id"]))
            test_case_status = None
        if not test_case_status:
            if not create_if_not_found:
                return test_case_status
            job_progress_token = self.jira_operations.add_test_case_to_cycle(self.cycle_id, self.project_id,
                                                                             self.version_id,
                                                                             test_case_key)["text"]["jobProgressToken"]
            while 1:
                time.sleep(1)
                job_progress_status = self.jira_operations.get_job_progress_status(job_progress_token)["text"]
                if job_progress_status["message"]:
                    break
        all_test_cases = self.jira_operations.get_one_execution(self.cycle_id, self.project_id,
                                                                self.version_id)["text"]["executions"]
        return [test_case for test_case in all_test_cases if int(test_case["issueId"]) == int(test_case_id)]

    def upload_results(self, test_case_key, results):
        test_case_status = self.check_for_test_case(test_case_key, delete_if_found=True)
        execution_id = str(test_case_status[0]["id"])
        # For some reason, if the call below is not executed, no results are returned by the following call!
        self.jira_operations.get_execution_status(execution_id)

        offset = 0
        try:
            while 1:
                jira_test_steps = self.jira_operations.get_steps_result_by_execution(execution_id, offset)["text"]
                if jira_test_steps.__len__() == 0:
                    break
                for test_step in jira_test_steps:
                    if test_step["step"] in results:
                        if not self.jira_operations.update_step_result_by_id(str(test_step["id"]),
                                                                      {"comment": results[test_step["step"]],
                                                                       "status": "1"})["status"]:
                            print(test_step)
                offset += 500
        except Exception as e:
            print("The following error was encountered while updating test results: {}\nPlease retry later."
                  .format(repr(e)))
            self.jira_operations.delete_test_case_execution(execution_id)
            return False, "The following error was encountered while updating test results: {}\nPlease retry later."\
                .format(repr(e))
        else:
            self.jira_operations.update_test_case_execution_status(execution_id, {"status": "1",
                                                                                  "executedBy": "n110382"})
            return True, "Success"

    def get_test_case_results(self, test_case_key):
        test_case = self.jira_operations.search_for_test_case(test_case_key)["text"]
        test_case_id = test_case["id"]
        test_case_status = self.check_for_test_case(test_case_id, test_case_key)
        execution_id = str(test_case_status[0]["id"])
        offset = 0
        all_results = []

        try:
            while 1:
                jira_test_steps = self.jira_operations.get_steps_result_by_execution(execution_id, offset)["text"]
                if jira_test_steps.__len__() == 0:
                    break
                else:
                    all_results.append(jira_test_steps)
                offset += 500

            return True, all_results
        except Exception as e:
            return False, "The following error was encountered while retrieving test results: {}".format(repr(e))

    def get_step_result(self, test_case_key, step_order):
        test_case_status = self.check_for_test_case(test_case_key, create_if_not_found=False)
        if not test_case_status:
            return False, 404
        execution_id = str(test_case_status[0]["id"])
        results = {}
        try:
            for s in step_order:
                result = self.jira_operations.get_steps_result_by_execution(execution_id, s, 1)["text"]
                if "comment" in result[0] and result[0]["comment"] != '':
                    results[result[0]["step"]] = result[0]["comment"].split(",")
            return True, results
        except Exception as e:
            print(e)
            return False, "The following error was encountered while retrieving test results: {}".format(repr(e))
