from Specsheet_Automation.static_data.file_info import spec_attach_request_sample_hex_file, spec_attach_request_sample_lists_file
from Specsheet_Automation.classes.DUT_spec_attach_request_info_extraction import DUTSpecAttachRequestInfoExtraction
from Specsheet_Automation.helpers.specsheet_automation_helpers import extract_data, get_full_path
from Specsheet_Automation.static_data.configuration import ATTACHREQUEST_MESSAGE_TYPE, ATTACHREQUEST_DELIMITER

with open(spec_attach_request_sample_hex_file, "r") as sample_hex_file:
    sample_hex_data = "".join([line.strip().replace(" ", "") for line in sample_hex_file.readlines()])

extracting = extract_data(sample_hex_data, ATTACHREQUEST_MESSAGE_TYPE, ATTACHREQUEST_DELIMITER, temp=False)
if extracting[0][0]:
    lists_file = get_full_path(spec_attach_request_sample_lists_file, extracting[1], False)
a = DUTSpecAttachRequestInfoExtraction(lists_file)
a.trim_data()
a.create_spec_ie()
a.check_for_extra_ie()
