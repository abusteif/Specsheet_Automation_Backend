from Specsheet_Automation.helpers.specsheet_automation_helpers import convert_DUT_UECI_files_hex_to_list, convert_raw_hex_to_ws_readable_hex
from Specsheet_Automation.static_data.file_info import *

# convert_DUT_UECI_files_hex_to_list(spec_attach_request_sample_hex_file, UECapabilityInformation_converted_hex,
#                                        UECapabilityInformation_pcap, UECapabilityInfo_json, UECapabilityInfo_lists,
#                                        DUT_UECI_excepted_elements_list, file_type):

with open(spec_attach_request_sample_hex_file, "r") as sample_hex_file:
    sample_hex_data = "".join([line.strip().replace(" ", "") for line in sample_hex_file.readlines()])
    print(sample_hex_data)


print(convert_raw_hex_to_ws_readable_hex(sample_hex_data, spec_attach_request_sample_converted_hex_file))