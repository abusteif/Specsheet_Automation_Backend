from Specsheet_Automation.classes.UECI_dut_info_extraction import UECIDutInfoExtraction
from Specsheet_Automation.helpers.UECI_info_extraction_helpers import get_list_items, extract_number_from_item
from Specsheet_Automation.static_data.configuration import UECI_dut_item_0_and_1_elements
from Specsheet_Automation.static_data.file_info import NR_spec_UECI_categories_file, NR_spec_UECI_warning_list_file

class NRDutUECIInfoExtraction(UECIDutInfoExtraction):
    def __init__(self, list_file):
        super().__init__(list_file, NR_spec_UECI_categories_file, NR_spec_UECI_warning_list_file)
        self.lines_to_remove = UECI_dut_item_0_and_1_elements
        self.finalize_data()

    def get_ie_lists(self):
        for release_type in self.release_categories:
            for release in self.list_releases[release_type]:
                for ie in self.list_releases[release_type][release]:
                    items = []
                    get_list_items(ie, items)
                    if [release] + items[-1][0] in self.warning_list:
                        full_ie = ",".join([release] + items[-1][0])
                        if full_ie in list(self.ie_list.keys()):
                            self.ie_list[full_ie].append("special_{}".format(str(items[-1][1])))
                        else:
                            self.ie_list[full_ie] = ["special_{}".format(str(items[-1][1]))]
                        continue
                    for item_index, item in enumerate(items):
                        full_ie = ",".join([release] + item[0])
                        value = extract_number_from_item(item[1])
                        if len(items) == 2 and item_index == len(items) - 1:
                            # print(full_ie)
                            value = "{}_itemVal_{}".format(value, extract_number_from_item(items[0][1]))

                        if full_ie in list(self.ie_list.keys()):
                            self.ie_list[full_ie].append(value)
                        else:
                            self.ie_list[full_ie] = [value]
