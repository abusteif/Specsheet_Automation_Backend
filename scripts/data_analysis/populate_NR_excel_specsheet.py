# from openpyxl import load_workbook
# from openpyxl.styles import Border, Side
# from shutil import copyfile
# from copy import deepcopy, copy
# from Specsheet_Automation.classes.NR_UECI_dut_info_extraction import NRDutUECIInfoExtraction
# from Specsheet_Automation.classes.LTE_UECI_dut_info_extraction import LTEDutUECIInfoExtraction
# from Specsheet_Automation.static_data.file_info import spec_UECI_categories_file, spec_UECI_warning_list_file, \
#     ENDC_specsheet_template, NR_spec_UECI_warning_list_file, NR_spec_UECI_categories_file
# from Specsheet_Automation.classes.DUT_spec_attach_request_info_extraction import DUTSpecAttachRequestInfoExtraction
# from Specsheet_Automation.static_data.NR_specsheet_fields import NR_all_UECI_fields, NR_attach_request_fields, \
#     NR_band_fields
# from Specsheet_Automation.classes.NR_data_analysis import NRDataAnalysis
#
# def populate_NR_specsheet(ENDC_template_full_path, UECapabilityInfo_lists_file=None,
#                           NR_UECapabilityInfo_lists_file=None, attach_request_lists_file=None):
#     try:
#         print("Populating NR Spec sheet")
#         full_path = ENDC_template_full_path
#         copyfile(ENDC_specsheet_template, full_path)
#         workbook = load_workbook(filename=full_path)
#         elements_sheet = workbook["NR Specsheet"]
#         ie_column = "B"
#         value_column = "C"
#         band_combinations_sheet = workbook["NR Band Combinations"]
#
#         NR_data = NRDutUECIInfoExtraction(NR_UECapabilityInfo_lists_file)
#         LTE_data = LTEDutUECIInfoExtraction(UECapabilityInfo_lists_file)
#
#         old_cell = ""
#         old_result = ""
#         full_result = ""
#
#         NR_ie_list = NR_data.ie_list
#         NR_ie_non_list = NR_data.ie_non_list
#
#         LTE_ie_list = LTE_data.ie_list
#         LTEie_non_list = LTE_data.ie_non_list
#         NR_data_analysis = NRDataAnalysis({**NR_ie_list, **NR_ie_non_list},
#                                           {**LTE_ie_list, **LTEie_non_list})
#
#         NR_data_analysis.get_band_combinations()
#         NR_data_analysis.get_supported_NR_band_details()
#         nr_band_details = NR_data_analysis.NR_bands
#         band_num = len(nr_band_details)
#         band_combination_data = NR_data_analysis.band_combinations_table()
#         for cell in band_combination_data:
#             band_combinations_sheet[cell] = band_combination_data[cell]
#         ENDC_all_fields_copy = deepcopy(NR_all_UECI_fields)
#         for ie in ENDC_all_fields_copy:
#             if "processor" in list(ie.keys()):
#                 result = NR_data_analysis.processors[ie["processor"]]()
#                 if "postProcessor" in list(ie.keys()):
#
#                     result = ie["postProcessor"](result)
#                 elements_sheet[ie["cell"]] = result
#             else:
#                 result = NR_data.find_ie(ie["path"], ie["release"])
#                 if not result:
#                     try:
#                         result = ie["default"]
#                     except KeyError as e:
#                         return False, "Error while populating Specsheet: {}".format(repr(e))
#                 else:
#                     if "values" in ie.keys():
#                         result = ie["values"][int(result)]
#                     elif "func" in ie.keys():
#                         result = ie["func"](result)
#                 if ie["cell"] == old_cell:
#                     if old_result.__len__() > 0:
#                         full_result = "{}\n{}\n{},".format(full_result, old_result, result)
#                         old_result = ""
#                     else:
#                         full_result = "{}\n{},".format(full_result, result)
#                 else:
#                     if full_result.__len__() > 0:
#                         elements_sheet[old_cell] = full_result[:-1]
#                         elements_sheet[ie["cell"]] = result
#                         old_cell = ie["cell"]
#                         full_result = ""
#                     else:
#                         elements_sheet[ie["cell"]] = result
#                         old_cell = ie["cell"]
#                         old_result = result
#         row_counter = elements_sheet.max_row
#         ie_ref_cell = elements_sheet["B35"]
#         value_ref_cell = elements_sheet["C35"]
#         for band_index, _ in enumerate(nr_band_details):
#             for ie in NR_band_fields:
#
#                 row_counter += 1
#                 elements_sheet["{}{}".format(ie_column, str(row_counter))] = ie
#                 apply_styling(ie_ref_cell, elements_sheet["{}{}".format(ie_column, str(row_counter))])
#
#                 elements_sheet["{}{}".format(value_column, str(row_counter))] = nr_band_details[band_index][ie]
#                 apply_styling(value_ref_cell, elements_sheet["{}{}".format(value_column, str(row_counter))])
#
#                 if ie == "NR Band":
#                     thick = Side(border_style="thick")
#                     thin = Side(border_style="thin")
#                     elements_sheet["{}{}".format(ie_column, str(row_counter))].border = Border(top=thick, right=thin, left=thin, bottom=thin)
#                     elements_sheet["{}{}".format(value_column, str(row_counter))].border = Border(top=thick, right=thin, left=thin, bottom=thin)
#         if attach_request_lists_file:
#             attach_request = DUTSpecAttachRequestInfoExtraction(attach_request_lists_file)
#             for ie in NR_all_attach_request_fields:
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
#         assert False
#     except Exception as e:
#         print(repr(e))
#         return False, "Error while populating Specsheet: {}".format(repr(e))
#     return True, "Successfully populated Specsheet"
#
# def apply_styling(ref_cell, current_cell):
#     current_cell.font = copy(ref_cell.font)
#     current_cell.border = copy(ref_cell.border)
#     current_cell.fill = copy(ref_cell.fill)
#     current_cell.alignment = copy(ref_cell.alignment)