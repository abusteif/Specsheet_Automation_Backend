from Specsheet_Automation.classes.Spec_UECI_Info_Extraction import Spec_Doc_Info_Extraction
from Specsheet_Automation.classes.NR_Spec_UECI_NR_Info_Extraction import NR_Spec_Doc_Info_Extraction
from Specsheet_Automation.classes.jira_interactions import JiraInteractions
from Specsheet_Automation.classes.jira_operations_class import JiraOperations
from Specsheet_Automation.classes.DUT_spec_attach_request_info_extraction import DUTSpecAttachRequestInfoExtraction
from Specsheet_Automation.static_data.file_info import spec_UECI_categories_file, spec_UECI_word_doc,\
     spec_UECI_text_file, spec_UECI_json_file, spec_UECI_lists_file, spec_UECI_csv_file, spec_UECI_csv_lists_file, \
     spec_UECI_warning_list_file, spec_attach_request_sample_hex_file, spec_attach_request_sample_lists_file, \
     NR_spec_UECI_word_doc, NR_spec_UECI_text_file, NR_spec_UECI_categories_file, NR_spec_UECI_csv_file, \
     NR_spec_UECI_json_file, NR_spec_UECI_lists_file
from Specsheet_Automation.static_data.configuration import MAIN_JIRA_WDA_PROJECT_KEY, JIRA_TEST_CASE_KEYS, \
    ATTACHREQUEST_MESSAGE_TYPE, ATTACHREQUEST_DELIMITER
from Specsheet_Automation.helpers.specsheet_automation_helpers import extract_data, get_full_path

import time

def extract_spec_UECI(release_word_doc, release_text_file, spec_json_file, spec_lists_file, spec_csv_file,
                      spec_csv_lists_file, warning_list_file, categories_file):
    s = Spec_Doc_Info_Extraction(release_word_doc, release_text_file)
    s.extract_info_from_release_word_doc()
    s.build_all_releases(spec_json_file, spec_lists_file, categories_file)
    s.save_list_to_csv(spec_csv_file, spec_csv_lists_file)
    s.create_warning_list(spec_csv_lists_file, warning_list_file)
#     TODO: add upload to Jira function

def extract_NR_spec_UECI(release_word_doc, release_text_file, spec_json_file, spec_lists_file, categories_file):
    nr = NR_Spec_Doc_Info_Extraction(release_word_doc, release_text_file)
    # nr.extract_info_from_release_word_doc()
    nr.build_all_releases(spec_json_file, spec_lists_file, categories_file)

def extract_spec_attach_request(sample_hex_file_input):
    with open(sample_hex_file_input, "r") as sample_hex_file:
        sample_hex_data = "".join([line.strip().replace(" ", "") for line in sample_hex_file.readlines()])
    extracting = extract_data(sample_hex_data, ATTACHREQUEST_MESSAGE_TYPE, ATTACHREQUEST_DELIMITER, temp=False)
    if extracting[0][0]:
        lists_file = get_full_path(spec_attach_request_sample_lists_file, extracting[1], False)

    attach = DUTSpecAttachRequestInfoExtraction(lists_file)
    step_list = attach.create_spec_ie()
    # jira_token = JiraOperations().get_cookies().get_dict()["crowd.token_key"]
    # jira_interactions = JiraInteractions(project_key=MAIN_JIRA_WDA_PROJECT_KEY, jira_token=jira_token)
    # for test_case in JIRA_TEST_CASE_KEYS:
    #     if "attach_request" in test_case:
    #         jira_interactions.add_steps_to_test_case(JIRA_TEST_CASE_KEYS[test_case], step_list)
    #         time.sleep(20)


if __name__ == "__main__":
    # extract_spec_UECI(spec_UECI_word_doc, spec_UECI_text_file, spec_UECI_json_file, spec_UECI_lists_file,
    #                   spec_UECI_csv_file, spec_UECI_csv_lists_file, spec_UECI_warning_list_file,
    #                   spec_UECI_categories_file)
    # extract_spec_attach_request(spec_attach_request_sample_hex_file)
    extract_NR_spec_UECI(NR_spec_UECI_word_doc, NR_spec_UECI_text_file, NR_spec_UECI_json_file, NR_spec_UECI_lists_file,
                         NR_spec_UECI_categories_file)

