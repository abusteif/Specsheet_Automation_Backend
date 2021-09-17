from Specsheet_Automation.classes.NR_UECI_dut_info_extraction import NRDutUECIInfoExtraction
from Specsheet_Automation.static_data.file_info import NR_dut_UECI_dev_list, NR_spec_UECI_categories_file, \
    NR_spec_UECI_warning_list_file, NR_spec_UECI_csv_file, NR_spec_UECI_csv_lists_file
from Specsheet_Automation.helpers.UECI_info_extraction_helpers import get_data_from_csv

a = NRDutUECIInfoExtraction(NR_dut_UECI_dev_list)
spec_non_list = get_data_from_csv(NR_spec_UECI_csv_file)
spec_list = get_data_from_csv(NR_spec_UECI_csv_lists_file)
edited_spec_non_list = []
edited_spec_list = []

for s in spec_non_list:
    edited_spec_non_list.append(",".join(s[:s.index('')]))

for s in spec_list:
    edited_spec_list.append(",".join(s[:s.index('')]))

for e in a.ie_non_list:
    if e not in edited_spec_non_list:
        print(e, a.ie_non_list[e])


for e in a.ie_list:
    if e not in edited_spec_list:
        print(e, a.ie_list[e])

# print(a.ie_list["release_15,rf-Parameters,supportedBandListNR,BandNR,bandNR"])
