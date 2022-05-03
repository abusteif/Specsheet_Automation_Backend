from Specsheet_Automation.helpers.specsheet_automation_helpers import extract_data, get_full_path
from Specsheet_Automation.static_data.file_info import spec_attach_request_sample_lists_file, \
    spec_attach_request_ie_file
from Specsheet_Automation.static_data.configuration import ATTACHREQUEST_DELIMITER, ATTACHREQUEST_MESSAGE_TYPE, \
     DUT_SPEC_ATTACH_REQUEST_COMMON_ELEMENTS, DUT_SPEC_ATTACH_REQUEST_EXCEPTED_ELEMENTS

class DUTSpecAttachRequestInfoExtraction:

    def __init__(self, lists_file):
        self.lists_file = lists_file
        self.trimmed_data = []
        self.trim_data()

    # def extract_data(self):
    #     extracting = extract_data(self.hex_data, ATTACHREQUEST_MESSAGE_TYPE, ATTACHREQUEST_DELIMITER, temp=self.is_dut)
    #     if extracting[0][0]:
    #         self.lists_file = get_full_path(spec_attach_request_sample_lists_file, extracting[1], self.is_dut)
    #     return extracting[0][0], extracting[0][1]

    def trim_data(self):
        with open(self.lists_file, "r") as attach_lists_file:
            lines = attach_lists_file.readlines()

            for line in lines:
                match = True
                line = line.strip()
                line_list = line.split(",")
                for index, element in enumerate(DUT_SPEC_ATTACH_REQUEST_COMMON_ELEMENTS):
                    if line_list.__len__() <= DUT_SPEC_ATTACH_REQUEST_COMMON_ELEMENTS.__len__() or \
                            line_list[index] != element:
                        match = False
                        break
                if match:
                    if line_list[-2] not in DUT_SPEC_ATTACH_REQUEST_EXCEPTED_ELEMENTS:
                        self.trimmed_data.append(line_list[-2:])

    def create_spec_ie(self):
        with open(spec_attach_request_ie_file, "w") as spec_file:
            all_ie = [line[0] for line in self.trimmed_data]
            spec_file.write(",".join(all_ie))
        return all_ie

    def check_for_extra_ie(self):
        with open(spec_attach_request_ie_file, "r+") as spec_file:
            new_ie_found = False
            current_ie_list = spec_file.readlines()[0].strip().split(",")
            spec_file.seek(0)
            new_ie_list = [line[0] for line in self.trimmed_data]
            for new_ie in new_ie_list:
                if new_ie not in current_ie_list:
                    print(new_ie)
                    new_ie_found = True
                    current_ie_list.append(new_ie)
            if new_ie_found:
                spec_file.write(",".join(current_ie_list))
                return True
        return False

    def find_ie(self, ie_to_find):
        for ie in self.trimmed_data:
            if ie[0] == ie_to_find:
                return ie[1]
        return None




