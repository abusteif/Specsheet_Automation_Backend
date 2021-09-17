from Specsheet_Automation.classes.UECI_dut_info_extraction import UECIDutInfoExtraction
from Specsheet_Automation.static_data.configuration import UECI_dut_item_0_and_1_elements
from Specsheet_Automation.static_data.file_info import NR_spec_UECI_categories_file, NR_spec_UECI_warning_list_file

class NRDutUECIInfoExtraction(UECIDutInfoExtraction):
    def __init__(self, list_file):
        super().__init__(list_file, NR_spec_UECI_categories_file, NR_spec_UECI_warning_list_file)
        self.lines_to_remove = UECI_dut_item_0_and_1_elements
        self.finalize_data()
