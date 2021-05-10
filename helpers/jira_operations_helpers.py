# from Specsheet_Automation_2.classes.jira_operations_class import *
# from Specsheet_Automation_2.static_data.configuration import *
# from Specsheet_Automation_2.helpers.DUT_SPEC_UECI_Info_Extraction_helpers import get_data_from_csv, extract_number_from_item
# import time
#
# def add_steps_to_test_case(source_csv_file, source_csv_list_file):
#     jira_operations = JiraOperations()
#     test_case = jira_operations.search_for_test_case(UECI_JIRA_TEST_CASE_KEY)["text"]
#     test_case_id = test_case["id"]
#     all_steps = [step["step"] for step in jira_operations.get_test_case_steps(test_case_id)["text"]["stepBeanCollection"]]
#     csv_data = get_data_from_csv(source_csv_file)
#     csv_data_list = get_data_from_csv(source_csv_list_file)
#     csv_data = [",".join(data[:data.index('')]) for data in csv_data]
#     csv_data_list = [",".join(data[:data.index('')]) for data in csv_data_list]
#
#     for data in csv_data:
#         if data not in all_steps and not data == "ID":
#             content = {"step": data}
#             jira_operations.create_step(test_case_id, content)
#
#     for data in csv_data_list:
#         if data not in all_steps and not data == "ID":
#             print(data)
#             content = {"step": data}
#             jira_operations.create_step(test_case_id, content)
#
# # Get Jira ID's associated with the DUT
# def get_device_jira_info(device_name, iot_cycle):
#     jira_operations = JiraOperations()
#     project_id = jira_operations.get_project_id_from_project_key(MAIN_JIRA_WDA_PROJECT_KEY)["text"]["id"]
#
#     all_versions = jira_operations.get_all_versions(project_id)["text"]
#     version_id = [version["id"] for version in all_versions["values"] if version["name"] == device_name][0]
#
#     all_cycles = jira_operations.get_all_cycles(project_id, version_id)["text"]
#     cycle_id = [cycle for cycle in all_cycles if isinstance(all_cycles[cycle], dict) and
#                 all_cycles[cycle]["name"] == iot_cycle][0]
#
#     return {
#         "projectId": project_id,
#         "versionId": version_id,
#         "cycleId": cycle_id
#     }
#
# # Checks if test case exists and creates it if it doesn't
# def check_for_test_case(cycle_id, project_id, version_id, test_case_id, test_case_key):
#     jira_operations = JiraOperations()
#     all_test_cases = jira_operations.get_one_execution(cycle_id, project_id, version_id)["text"]["executions"]
#     test_case_status = [test_case for test_case in all_test_cases if int(test_case["issueId"]) == int(test_case_id)]
#     if not test_case_status:
#         job_progress_token = jira_operations.add_test_case_to_cycle(cycle_id, project_id, version_id,
#                                                                     test_case_key)["text"]["jobProgressToken"]
#         while 1:
#             time.sleep(1)
#             job_progress_status = jira_operations.get_job_progress_status(job_progress_token)["text"]
#             if job_progress_status["message"]:
#                 break
#     # print(jira_operations.get_test_case_steps(test_case_id))
#     all_test_cases = jira_operations.get_one_execution(cycle_id, project_id, version_id)["text"]["executions"]
#     return [test_case for test_case in all_test_cases if int(test_case["issueId"]) == int(test_case_id)]
#
# def update_results(dut_name, iot_cycle, lists_file):
#     jira_operations = JiraOperations()
#     test_case = jira_operations.search_for_test_case(UECI_JIRA_TEST_CASE_KEY)["text"]
#     test_case_id = test_case["id"]
#     device_info = get_device_jira_info(dut_name, iot_cycle)
#
#     cycle_id = device_info["cycleId"]
#     version_id = device_info["versionId"]
#     project_id = device_info["projectId"]
#
#     test_case_status = check_for_test_case(cycle_id, project_id, version_id, test_case_id, UECI_JIRA_TEST_CASE_KEY)
#     execution_id = str(test_case_status[0]["id"])
#
#     # For some reason, if the call below is not executed, no results are returned by the following call!
#     jira_operations.get_execution_status(execution_id)
#
#     csv_types = (update_list_results(csv_list_file_name), update_non_list_results(csv_file_name))
#
#     offset = 0
#     try:
#         while 1:
#             jira_test_steps = jira_operations.get_steps_result_by_execution(execution_id, offset)["text"]
#             print(jira_test_steps)
#             if jira_test_steps.__len__() == 0:
#                 break
#             for csv_type in csv_types:
#                 for test_step, result in csv_type:
#                     for jira_ie in jira_test_steps:
#                         if jira_ie["step"] == test_step:
#                             jira_operations.update_step_result_by_id(str(jira_ie["id"]),
#                                                                      {"comment": result, "status": "1"})
#                             break
#             offset += 500
#     except Exception:
#         print("The following error was encountered while updating test results: {}\nPlease retry later."
#               .format(str(Exception)))
#     else:
#         jira_operations.update_test_case_execution_status(execution_id, {"status": "1", "executedBy": "n110382"})
#
#
# # def update_non_list_results(source_csv_file):
# #     csv_result_data = get_data_from_csv(source_csv_file)
# #     output = []
# #     for test_step in csv_result_data:
# #         ie = ",".join(test_step[:test_step.index('')])
# #         result = test_step[-1] if test_step[-1] != '' else "No Information"
# #         output.append((ie, result))
# #     return output
# #
# #
# # def update_list_results(source_csv_list_file):
# #
# #     output = []
# #     csv_result_data = get_data_from_csv(source_csv_list_file)
# #     for test_step in csv_result_data:
# #         ie = ",".join(test_step[:test_step.index('')])
# #         result = ",".join([extract_number_from_item(item) for item in test_step[test_step.index(''):] if item != ''])
# #         if not result:
# #             result = "No Information"
# #         output.append((ie, result))
# #     return output
#
# def update_non_list_results(non_list_result):
#     for test_step in non_list_result:
#         ie = ",".join(test_step[:test_step.index('')])
#         result = test_step[-1] if test_step[-1] != '' else "No Information"
#         output.append((ie, result))
#     return output
#
#
# def update_list_results(source_csv_list_file):
#
#     output = []
#     csv_result_data = get_data_from_csv(source_csv_list_file)
#     for test_step in csv_result_data:
#         ie = ",".join(test_step[:test_step.index('')])
#         result = ",".join([extract_number_from_item(item) for item in test_step[test_step.index(''):] if item != ''])
#         if not result:
#             result = "No Information"
#         output.append((ie, result))
#     return output
