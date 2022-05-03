from Specsheet_Automation.helpers.specsheet_automation_helpers import get_delimiter, \
    extract_data, get_full_path, cleanup_files, extract_data_from_multiple_messages
from Specsheet_Automation.static_data.LTE_specsheet_fields import MSR0835_all_UECI_fields
from Specsheet_Automation.scripts.data_analysis.populate_NR_LTE_specsheet import populate_NR_LTE_specsheet


def extract_and_populate_specsheet(hex_data, dut_name, iot_cycle):
    extract_result = extract_data_from_multiple_messages(hex_data)
    if not extract_result[0]:
        return False, extract_result[1]
    attach_request_lists_file, UECapabilityInfo_lists_file, NR_UECapabilityInfo_lists_file, \
        unique_folder_path = extract_result[1]

    specsheet_full_path = get_full_path("NR_LTE_specsheet_template_{}_{}.xlsx".
                                        format(dut_name, iot_cycle), unique_folder_path, True)
    populating = populate_NR_LTE_specsheet(specsheet_full_path,
                                           UECapabilityInfo_lists_file=UECapabilityInfo_lists_file,
                                           NR_UECapabilityInfo_lists_file=NR_UECapabilityInfo_lists_file,
                                           attach_request_lists_file=attach_request_lists_file)

    if not populating[0]:
        return False, populating[1]
    return True, unique_folder_path, specsheet_full_path


def validate_data(hex_data, message_type):

    delimiter = get_delimiter(message_type)
    converting = extract_data(hex_data, message_type, delimiter)
    cleanup_files(converting[1])
    return converting[0][0], converting[0][1]

def get_message_fields(message_type):
    if message_type == "UECapabilityInformation_4G":
        fields = []
        for ie in MSR0835_all_UECI_fields:
            if "processor" in list(ie.keys()):
                if not isinstance(ie["processor"], list):
                    fields.append(ie["processor"].split(","))

            else:
                if not isinstance(ie["path"], list):
                    fields.append(ie["path"].split(","))
                else:
                    fields.append(",".join(ie["path"]))
        return fields
    else:
        return []
