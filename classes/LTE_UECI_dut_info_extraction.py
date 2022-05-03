from Specsheet_Automation.classes.UECI_dut_info_extraction import UECIDutInfoExtraction
from Specsheet_Automation.static_data.configuration import UECI_dut_item_0_elements
from Specsheet_Automation.static_data.file_info import spec_UECI_warning_list_file, spec_UECI_categories_file

class LTEDutUECIInfoExtraction(UECIDutInfoExtraction):
    def __init__(self, list_file):
        super().__init__(list_file, spec_UECI_categories_file, spec_UECI_warning_list_file)
        self.lines_to_remove = UECI_dut_item_0_elements
        self.finalize_data()
