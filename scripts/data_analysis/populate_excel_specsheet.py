# from openpyxl import load_workbook
# from shutil import copyfile
# from copy import deepcopy
# from Specsheet_Automation.classes.LTE_UECI_dut_info_extraction import LTEDutUECIInfoExtraction
# from Specsheet_Automation.static_data.file_info import spec_UECI_categories_file, spec_UECI_warning_list_file, \
#     LTE_specsheet_template
# from Specsheet_Automation.classes.DUT_spec_attach_request_info_extraction import DUTSpecAttachRequestInfoExtraction
# from Specsheet_Automation.static_data.LTE_specsheet_fields import MSR0835_all_UECI_fields, LTE_attach_request_fields
# from Specsheet_Automation.classes.LTE_data_analysis import LTEDataAnalysis
#
# def populate_specsheet(MSR0835_full_path, UECapabilityInfo_lists_file=None, attach_request_lists_file=None):
#     try:
#         print("Populating Spec sheet")
#         full_path = MSR0835_full_path
#         copyfile(LTE_specsheet_template, full_path)
#         workbook = load_workbook(filename=full_path)
#         elements_sheet = workbook["UE EUTRA Cap-SpecSheet"]
#         band_combinations_sheet = workbook["Band Combinations"]
#
#         if UECapabilityInfo_lists_file:
#             spec_sheet = LTEDutUECIInfoExtraction(UECapabilityInfo_lists_file)
#             ie_list = spec_sheet.ie_list
#             ie_non_list = spec_sheet.ie_non_list
#
#             old_cell = ""
#             old_result = ""
#             full_result = ""
#             data_analysis = LTEDataAnalysis({**ie_list, **ie_non_list})
#             data_analysis.get_r10_band_combinations()
#             data_analysis.get_r11_band_combinations()
#             band_combination_data = data_analysis.band_combinations_table()
#             for cell in band_combination_data:
#                 band_combinations_sheet[cell] = band_combination_data[cell]
#             MSR0835_all_fields_copy = deepcopy(MSR0835_all_UECI_fields)
#             for ie in MSR0835_all_fields_copy:
#                 if "processor" in list(ie.keys()):
#                     result = data_analysis.processors[ie["processor"]]()
#                     if "postProcessor" in list(ie.keys()):
#
#                         result = ie["postProcessor"](result)
#                     elements_sheet[ie["cell"]] = result
#                 else:
#                     result = spec_sheet.find_ie(ie["path"], ie["release"])
#                     if not result:
#                         try:
#                             result = ie["default"]
#                         except KeyError as e:
#                             return False, "Error while populating Specsheet: {}".format(repr(e))
#                     else:
#                         if "values" in ie.keys():
#                             result = ie["values"][int(result)]
#                         elif "func" in ie.keys():
#                             result = ie["func"](result)
#                     if ie["cell"] == old_cell:
#                         if old_result.__len__() > 0:
#                             full_result = "{}\n{}\n{},".format(full_result, old_result, result)
#                             old_result = ""
#                         else:
#                             full_result = "{}\n{},".format(full_result, result)
#                     else:
#                         if full_result.__len__() > 0:
#                             elements_sheet[old_cell] = full_result[:-1]
#                             elements_sheet[ie["cell"]] = result
#                             old_cell = ie["cell"]
#                             full_result = ""
#                         else:
#                             elements_sheet[ie["cell"]] = result
#                             old_cell = ie["cell"]
#                             old_result = result
#         if attach_request_lists_file:
#             attach_request = DUTSpecAttachRequestInfoExtraction(attach_request_lists_file)
#             for ie in LTE_attach_request_fields:
#                 result = attach_request.find_ie(ie["element"])
#                 if not result:
#                     try:
#                         result = ie["default"]
#                         elements_sheet[ie["cell"]] = result
#                     except KeyError as e:
#                         return False, "Mandatory Attach Request element not found: {}".format(ie)
#                 else:
#                     elements_sheet[ie["cell"]] = ie["values"][int(result)]
#         workbook.save(filename=full_path)
#
#     except Exception as e:
#         return False, "Error while populating Specsheet: {}".format(repr(e))
#     return True, "Successfully populated Specsheet"
