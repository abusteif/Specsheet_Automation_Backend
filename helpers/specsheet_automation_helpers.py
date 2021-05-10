from Specsheet_Automation.classes.Spec_UECI_Info_Extraction import convert_raw_hex_to_ws_readable_hex, \
    convert_ws_hex_to_pcap, convert_pcap_to_json, convert_json_to_lists
from Specsheet_Automation.classes.DUT_Spec_UECI_Info_Extraction import DUT_UECI_Info_Extraction
from Specsheet_Automation.classes.jira_interactions import JiraInteractions
from Specsheet_Automation.static_data.file_info import spec_UECI_categories_file, spec_UECI_warning_list_file, \
    temp_files_folder, UECapabilityInformation_converted_hex_file, UECapabilityInformation_pcap_file, \
    UECapabilityInfo_lists_file, UECapabilityInfo_json_file
from Specsheet_Automation.static_data.specsheet_fields import MSR0835_all_fields
from Specsheet_Automation.classes.data_analysis import DataAnalysis
from Specsheet_Automation.static_data.configuration import MAIN_JIRA_WDA_PROJECT_KEY, JIRA_TEST_CASE_KEYS, \
    DUT_UECI_excepted_elements
from Specsheet_Automation.static_data.specsheet_fields import jira_test_step_order_to_field_mapping
import os
import shutil
from copy import deepcopy
from uuid import uuid4
import time

def convert_DUT_UECI_files_hex_to_list(UECapabilityInformation_hex, DUT_UECI_excepted_elements_list, file_type, folder_path):

    try:
        print("Converting Hex to lists")
        start_index = 0

        while 1:
            # time.sleep(5)
            hex_file = get_full_temp_path(UECapabilityInformation_converted_hex_file, folder_path)
            pcap_file = get_full_temp_path(UECapabilityInformation_pcap_file, folder_path)
            json_file = get_full_temp_path(UECapabilityInfo_json_file, folder_path)
            lists_file = get_full_temp_path(UECapabilityInfo_lists_file, folder_path)

            crhtwr = convert_raw_hex_to_ws_readable_hex(UECapabilityInformation_hex, hex_file, file_type, start_index)
            print(crhtwr)
            if crhtwr[0]:
                start_index = crhtwr[1]
            else:
                return False, "Error while converting data"
            convert_ws_hex_to_pcap(hex_file, pcap_file)
            convert_pcap_to_json(pcap_file, json_file, file_type)
            cjtl = convert_json_to_lists(json_file, lists_file, DUT_UECI_excepted_elements_list)
            print(cjtl)
            if cjtl[0]:
                return True, "conversion successful"
    except Exception as e:
        return False, "Error while converting data: {}".format(repr(e))


def upload_results_to_jira(dut_name, iot_cycle, UECapabilityInfo_lists, message_type, sim_type, jira_token):
    try:
        print("Uploading to Jira")
        full_message_type = "{}_{}".format(message_type, sim_type)
        spec_sheet = DUT_UECI_Info_Extraction(UECapabilityInfo_lists, spec_UECI_categories_file,
                                              spec_UECI_warning_list_file)
        jira_interactions = JiraInteractions(dut_name, iot_cycle, MAIN_JIRA_WDA_PROJECT_KEY, jira_token)
        edited_list_ie = {}
        for ie in spec_sheet.ie_list:
            edited_list_ie[ie] = ",".join(spec_sheet.ie_list[ie])

        updating_results = jira_interactions.upload_results(JIRA_TEST_CASE_KEYS[full_message_type],
                                                            {**spec_sheet.ie_non_list, **edited_list_ie})

        if updating_results[0]:
            return True, "Results successfully uploaded to Jira"
        else:
            return False, updating_results[1]
    except Exception as e:
        return False, "Error while uploading to Jira: {}".format(repr(e))

def get_ie_results_from_jira(message_type, sim_type, dut_name, iot_cycle, jira_token):

    print("Getting test results from Jira")
    try:
        full_message_type = "{}_{}".format(message_type, sim_type)

        test_case_key = JIRA_TEST_CASE_KEYS[full_message_type]
        jira_interactions = JiraInteractions(dut_name, iot_cycle, MAIN_JIRA_WDA_PROJECT_KEY, jira_token)
        steps = [jira_test_step_order_to_field_mapping[s] for s in jira_test_step_order_to_field_mapping]
        jira_test_cases = jira_interactions.get_step_result(test_case_key, steps)
        if not jira_test_cases[0]:
            return False, jira_test_cases[1]
        individual_ie = {}
        data_analysis = DataAnalysis(jira_test_cases[1])
        data_analysis.get_r10_band_combinations()
        data_analysis.get_r11_band_combinations()
        band_combs = data_analysis.band_combinations_list()
        jira_test_cases = jira_test_cases[1]
        MSR0835_all_fields_copy = deepcopy(MSR0835_all_fields)
        for ie in MSR0835_all_fields_copy:
            if "processor" in [*ie]:
                individual_ie[ie["processor"]] = data_analysis.processors[ie["processor"]]()

            else:
                if isinstance(ie["path"], list):
                    ie["path"] = ",".join(ie["path"])
                path = ie["release"] + "," + ie["path"]
                if path not in [*jira_test_cases]:
                    # individual_ie[ie["path"]] = ie["default"]
                    try:
                        individual_ie[ie["path"]] = ie["default"]
                    except KeyError as e:
                        print(ie)
                        return False, "Error occurred while getting test results from Jira: {}".format(repr(e))
                else:
                    if "values" in [*ie]:
                        individual_ie[ie["path"]] = ie["values"][int(jira_test_cases[path][0])]
                    elif "func" in [*ie]:
                        individual_ie[ie["path"]] = ie["func"](jira_test_cases[path][0])
        return True, {
            "bandCombinations": band_combs,
            "individualIE": individual_ie
        }
    except Exception as e:
        return False, "Error occurred while getting test results from Jira: {}".format(repr(e))

def check_if_test_case_executed(message_type, sim_type, dut_name, iot_cycle, jira_token):
    try:
        full_message_type = "{}_{}".format(message_type, sim_type)
        jira_interactions = JiraInteractions(dut_name, iot_cycle, MAIN_JIRA_WDA_PROJECT_KEY, jira_token)
        status = jira_interactions.check_for_test_case(JIRA_TEST_CASE_KEYS[full_message_type],
                                                       create_if_not_found=False)
        if status:
            return True, True
        else:
            return True, False
    except Exception as e:
        return False, "An error occurred while check test case execution status: {}".format(repr(e))


def cleanup_files(files_directory):
    try:
        shutil.rmtree(files_directory)
        return True, "Clean-up complete"

    except Exception as e:
        return False, "Error while deleting the temp files directory: {}".format(repr(e))

def get_full_temp_path(file_name, folder_path):
    print(temp_files_folder / folder_path / file_name)
    return temp_files_folder / folder_path / file_name

def create_files_folder(name):
    unique_folder_path = temp_files_folder / name
    try:
        os.mkdir(unique_folder_path)
        return True, unique_folder_path
    except Exception as e:

        return False, "Error while creating a folder: {}".format(repr(e))

# def convert(hex_data, unique_folder_path, message_type):
#     hex_file = get_full_temp_path(UECapabilityInformation_converted_hex_file, unique_folder_path)
#     pcap_file = get_full_temp_path(UECapabilityInformation_pcap_file, unique_folder_path)
#     json_file = get_full_temp_path(UECapabilityInfo_json_file, unique_folder_path)
#     lists_file = get_full_temp_path(UECapabilityInfo_lists_file, unique_folder_path)
#
#     return convert_DUT_UECI_files_hex_to_list(hex_data, DUT_UECI_excepted_elements, message_type, unique_folder_path)

def extract_data(hex_data, message_type, unique_id=None):
    new_id = unique_id if unique_id else str(uuid4())
    unique_folder_path = create_files_folder(new_id)
    if not unique_folder_path[0]:
        return [unique_folder_path[0], unique_folder_path[1]], None
    unique_folder_path = unique_folder_path[1]
    return convert_DUT_UECI_files_hex_to_list(hex_data, DUT_UECI_excepted_elements, message_type, unique_folder_path), unique_folder_path
