from Specsheet_Automation.helpers.data_conversion_helpers import convert_raw_hex_to_ws_readable_hex, \
    convert_ws_hex_to_pcap, convert_pcap_to_json, convert_json_to_lists
from Specsheet_Automation.classes.LTE_UECI_dut_info_extraction import LTEDutUECIInfoExtraction
from Specsheet_Automation.classes.jira_interactions import JiraInteractions
from Specsheet_Automation.static_data.file_info import spec_UECI_categories_file, spec_UECI_warning_list_file, \
    temp_files_folder, converted_hex_file_path, pcap_file_path, perm_files_folder, dut_attach_request_lists_file_path, \
    json_file_path, dut_UECI_lists_file, spec_attach_request_sample_lists_file, \
    spec_attach_request_sample_json_file, spec_attach_request_sample_pcap_file, \
    spec_attach_request_sample_converted_hex_file, NR_dut_UECI_lists_file
from Specsheet_Automation.static_data.LTE_specsheet_fields import MSR0835_all_UECI_fields
from Specsheet_Automation.classes.LTE_data_analysis import LTEDataAnalysis
from Specsheet_Automation.static_data.configuration import MAIN_JIRA_WDA_PROJECT_KEY, JIRA_TEST_CASE_KEYS, \
    DUT_UECI_excepted_elements, ATTACHREQUEST_DELIMITER, UECAPABILITYINFORMATION_DELIMITER, \
    ATTACHREQUEST_MESSAGE_TYPE, UECAPABILITYINFORMATION_MESSAGE_TYPE, DUT_SPEC_ATTACH_REQUEST_EXCEPTED_ELEMENTS

from Specsheet_Automation.static_data.LTE_specsheet_fields import jira_test_step_order_to_field_mapping
import os
import shutil
from copy import deepcopy
from uuid import uuid4

def convert_hex_to_list(hex_data, excepted_elements_list, file_type, folder_path, temp, delimiter, file_info):

    try:
        print("Converting Hex to lists")
        start_index = 0
        chfp = file_info["chfp"]
        pfp = file_info["pfp"]
        jfp = file_info["jfp"]
        lfp = file_info["lfp"]

        while 1:
            hex_file = get_full_path(chfp, folder_path, temp)
            pcap_file = get_full_path(pfp, folder_path, temp)
            json_file = get_full_path(jfp, folder_path, temp)
            lists_file = get_full_path(lfp, folder_path, temp)

            crhtwr = convert_raw_hex_to_ws_readable_hex(hex_data, hex_file, start_index, delimiter)
            if crhtwr[0]:
                start_index = crhtwr[1]
            else:
                return False, "Error while converting data"
            convert_ws_hex_to_pcap(hex_file, pcap_file)
            convert_pcap_to_json(pcap_file, json_file, file_type)
            cjtl = convert_json_to_lists(json_file, lists_file, excepted_elements_list, file_type)
            if cjtl[0]:
                return True, "conversion successful"
    except Exception as e:
        return False, "Error while converting data: {}".format(repr(e))


def upload_results_to_jira(dut_name, iot_cycle, UECapabilityInfo_lists, message_type, sim_type, jira_token):
    try:
        print("Uploading to Jira")
        full_message_type = "{}_{}".format(message_type, sim_type)
        spec_sheet = LTEDutUECIInfoExtraction(UECapabilityInfo_lists)
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
        data_analysis = LTEDataAnalysis(jira_test_cases[1])
        data_analysis.get_r10_band_combinations()
        data_analysis.get_r11_band_combinations()
        band_combs = data_analysis.band_combinations_list()
        jira_test_cases = jira_test_cases[1]
        MSR0835_all_fields_copy = deepcopy(MSR0835_all_UECI_fields)
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

def get_full_path(file_name, folder_path, temp):
    if temp:
        return temp_files_folder / folder_path / file_name
    else:
        return perm_files_folder / file_name

def create_files_folder(name):
    unique_folder_path = temp_files_folder / name
    try:
        os.mkdir(unique_folder_path)
        return True, unique_folder_path
    except WindowsError as e:
        if e.winerror == 183:
            return True, unique_folder_path
        else:
            return False, "Error while creating a folder: {}".format(repr(e))
    except Exception as e:
        return False, "Error while creating a folder: {}".format(repr(e))

def extract_data(hex_data, message_type, delimiter, temp=True, unique_id=None):
    file_info = None
    excepted_elements = None
    new_id = unique_id if unique_id else str(uuid4())
    unique_folder_path = create_files_folder(new_id)
    if not unique_folder_path[0]:
        return [unique_folder_path[0], unique_folder_path[1]], None
    unique_folder_path = unique_folder_path[1]
    file_info = {
        "chfp": converted_hex_file_path,
        "pfp": pcap_file_path,
        "jfp": json_file_path,
        "lfp": None
    }
    if message_type == ATTACHREQUEST_MESSAGE_TYPE:
        excepted_elements = DUT_SPEC_ATTACH_REQUEST_EXCEPTED_ELEMENTS
        if temp:
            file_info["lfp"] = dut_attach_request_lists_file_path
        else:
            file_info = {
                "chfp": spec_attach_request_sample_converted_hex_file,
                "pfp": spec_attach_request_sample_pcap_file,
                "jfp": spec_attach_request_sample_json_file,
                "lfp": spec_attach_request_sample_lists_file,
            }
    elif UECAPABILITYINFORMATION_MESSAGE_TYPE in message_type:
        excepted_elements = DUT_UECI_excepted_elements
        file_info["lfp"] = dut_UECI_lists_file if "4G" in message_type else NR_dut_UECI_lists_file

    return convert_hex_to_list(hex_data, excepted_elements, message_type, unique_folder_path, temp,
                               delimiter, file_info), unique_folder_path

def extract_data_from_multiple_messages(hex_data):
    unique_id = str(uuid4())
    UECapabilityInfo_lists_file = None
    NR_UECapabilityInfo_lists_file = None
    attach_request_lists_file = None
    unique_folder_path = None
    for message_type in hex_data:
        delimiter = get_delimiter(message_type)
        converting = extract_data(hex_data[message_type], message_type, delimiter, unique_id=unique_id)
        unique_folder_path = converting[1]
        if not converting[0][0]:
            cleanup_files(unique_folder_path)
            return False, converting[0][1]
        if message_type == ATTACHREQUEST_MESSAGE_TYPE:
            attach_request_lists_file = get_full_path(dut_attach_request_lists_file_path, unique_folder_path, True)
        elif UECAPABILITYINFORMATION_MESSAGE_TYPE in message_type:
            if "4G" in message_type:
                UECapabilityInfo_lists_file = get_full_path(dut_UECI_lists_file, unique_folder_path, True)
            elif "5G" in message_type:
                NR_UECapabilityInfo_lists_file = get_full_path(NR_dut_UECI_lists_file, unique_folder_path, True)
        try:
            os.remove(get_full_path(json_file_path, unique_folder_path, True))
            os.remove(get_full_path(pcap_file_path, unique_folder_path, True))
            os.remove(get_full_path(converted_hex_file_path, unique_folder_path, True))
        except OSError as e:
            print(e)
            return False, "Error while deleting a file: {}".format(repr(e))

    return True, (attach_request_lists_file, UECapabilityInfo_lists_file, NR_UECapabilityInfo_lists_file,
                  unique_folder_path)

def get_delimiter(message_type):
    if UECAPABILITYINFORMATION_MESSAGE_TYPE in message_type:
        return UECAPABILITYINFORMATION_DELIMITER
    elif message_type == ATTACHREQUEST_MESSAGE_TYPE:
        return ATTACHREQUEST_DELIMITER
    return None
