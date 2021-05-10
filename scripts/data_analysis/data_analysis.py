# from Specsheet_Automation_2.helpers.jira_operations_helpers import *
#
# def get_test_case_results(dut_name, iot_cycle):
#     jira_operations = JiraOperations()
#     test_case = jira_operations.search_for_test_case(UECI_JIRA_TEST_CASE_KEY)["text"]
#     test_case_id = test_case["id"]
#     device_info = get_device_jira_info(dut_name, iot_cycle)
#
#     cycle_id = device_info["cycleId"]
#     version_id = device_info["versionId"]
#     project_id = device_info["projectId"]
#
#     test_case_status = check_for_test_case(cycle_id, project_id, version_id, test_case_id, UECI_JIRA_TEST_CASE_KEY)
#     execution_id = str(test_case_status[0]["id"])
#
#     supportedBandCombination_r10 = {
#          "path": "release_1020,rf-Parameters-v1020,supportedBandCombination-r10",
#          "value": []
#      }
#     BandCombinationParameters_r10 = {
#          "path": "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10",
#          "value": []
#      }
#     bandEUTRA_r10 = {
#          "path": "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
#                  "BandParameters-r10,bandEUTRA-r10",
#          "value": []
#      }
#     bandParametersUL_r10 = {
#          "path": "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
#                  "BandParameters-r10,bandParametersUL-r10",
#          "value": []
#      }
#     ca_BandwidthClassUL_r10 = {
#          "path": "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
#                  "BandParameters-r10,bandParametersUL-r10,CA-MIMO-ParametersUL-r10,ca-BandwidthClassUL-r10",
#          "value": []
#      }
#     bandParametersDL_r10 = {
#          "path": "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
#                  "BandParameters-r10,bandParametersDL-r10",
#          "value": []
#      }
#     ca_BandwidthClassDL_r10 = {
#          "path": "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
#                  "BandParameters-r10,bandParametersDL-r10,CA-MIMO-ParametersDL-r10,ca-BandwidthClassDL-r10",
#          "value": []
#      }
#     supportedMIMO_CapabilityDL_r10 = {
#         "path": "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
#                 "BandParameters-r10,bandParametersDL-r10,CA-MIMO-ParametersDL-r10,supportedMIMO-CapabilityDL-r10",
#         "value": []
#     }
#     supportedBandCombinationExt_r10 = {
#          "path": "release_1060,rf-Parameters-v1060,supportedBandCombinationExt-r10",
#          "value": []
#     }
#     supportedBandwidthCombinationSet_r10 = {
#          "path": "release_1060,rf-Parameters-v1060,supportedBandCombinationExt-r10,BandCombinationParametersExt-r10,"
#                  "supportedBandwidthCombinationSet-r10",
#          "value": []
#     }
#
#     supportedBandCombinationAdd_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11",
#         "value": []
#     }
#     bandParameterList_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandParameterList-r11",
#         "value": []
#     }
#     bandEUTRA_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandParameterList-r11,BandParameters-r11,bandEUTRA-r11",
#         "value": []
#     }
#     bandParametersUL_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandParameterList-r11,BandParameters-r11,bandParametersUL-r11",
#         "value": []
#     }
#     ca_BandwidthClassUL_r10_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandParameterList-r11,BandParameters-r11,bandParametersUL-r11,CA-MIMO-ParametersUL-r10,"
#                 "ca-BandwidthClassUL-r10",
#         "value": []
#     }
#     bandParametersDL_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandParameterList-r11,BandParameters-r11,bandParametersDL-r11",
#         "value": []
#     }
#     ca_BandwidthClassDL_r10_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandParameterList-r11,BandParameters-r11,bandParametersDL-r11,CA-MIMO-ParametersDL-r10,"
#                 "ca-BandwidthClassDL-r10",
#         "value": []
#     }
#     supportedMIMO_CapabilityDL_r10_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandParameterList-r11,BandParameters-r11,bandParametersDL-r11,CA-MIMO-ParametersDL-r10,"
#                 "supportedMIMO-CapabilityDL-r10",
#         "value": []
#     }
#     interFreqBandList_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandInfoEUTRA-r11,interFreqBandList",
#         "value": []
#     }
#     interFreqNeedForGaps_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandInfoEUTRA-r11,interFreqBandList,InterFreqBandInfo,interFreqNeedForGaps",
#         "value": []
#     }
#     interRAT_BandList_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandInfoEUTRA-r11,interRAT-BandList",
#         "value": []
#     }
#     interRAT_NeedForGaps_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "bandInfoEUTRA-r11,interRAT-BandList,InterRAT-BandInfo,interRAT-NeedForGaps",
#         "value": []
#     }
#     supportedBandwidthCombinationSet_r11 = {
#         "path": "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
#                 "supportedBandwidthCombinationSet-r11",
#         "value": []
#     }
#
#     ies_r10 = [supportedBandCombination_r10, BandCombinationParameters_r10, bandEUTRA_r10, bandParametersUL_r10,
#                ca_BandwidthClassUL_r10, bandParametersDL_r10, ca_BandwidthClassDL_r10, supportedMIMO_CapabilityDL_r10,
#                supportedBandCombinationExt_r10, supportedBandwidthCombinationSet_r10]
#
#     ies_r11 = [supportedBandCombinationAdd_r11, bandParameterList_r11, bandEUTRA_r11, bandParametersUL_r11,
#                ca_BandwidthClassUL_r10_r11, bandParametersDL_r11, ca_BandwidthClassDL_r10_r11,
#                supportedMIMO_CapabilityDL_r10_r11, interFreqBandList_r11, interFreqNeedForGaps_r11,
#                interRAT_BandList_r11, interRAT_NeedForGaps_r11, supportedBandwidthCombinationSet_r11]
#
#     offset = 1000
#     try:
#         while 1:
#             jira_test_steps = jira_operations.get_steps_result_by_execution(execution_id, offset)["text"]
#             if jira_test_steps.__len__() == 0:
#                 break
#             for jira_ie in jira_test_steps:
#                 for ie in ies_r10:
#                     if jira_ie["step"] == ie["path"]:
#                         ie["value"] = jira_ie["comment"].split(",")
#                 for ie in ies_r11:
#                     if jira_ie["step"] == ie["path"]:
#                         ie["value"] = jira_ie["comment"].split(",")
#
#             offset += 500
#     except Exception:
#         print("The following error was encountered while updating test results: {}\nPlease retry later."
#               .format(str(Exception)))
#
#     for ie in ies_r11:
#         print(ie)
#
#     def get_start_end(list_to_process, operator="!="):
#         # print(list_to_process)
#         start = 0
#         result = []
#         end = 0
#
#         def compare(op, item1, item2):
#             if op == "!=":
#                 return item1 != item2
#             if op == "<":
#                 return int(item1) < int(item2)
#
#         for e_index, e in enumerate(list_to_process):
#             if e_index == 0:
#                 continue
#             old_e = list_to_process[e_index - 1]
#             if compare(operator, e, old_e):
#                 end = e_index
#                 result.append([start, end])
#                 start = e_index
#         result.append([end, list_to_process.__len__()])
#         return result
#
#     def get_r10_band_combinations(band_combinations):
#         band_combs_r10 = get_start_end(supportedBandCombination_r10["value"])
#         ul_counter = 0
#         dl_counter = 0
#         band_comb_counter = 0
#
#         for bc in band_combs_r10:
#             bands_r10 = BandCombinationParameters_r10["value"][bc[0]:bc[1]]
#             one_band_r10 = get_start_end(bands_r10)
#             new_comb = {"ul": [], "dl": [], "bcs": ""}
#             for ob in one_band_r10:
#                 if (ob[1] - ob[0]) % 2 == 0:
#                     new_comb["ul"].append({"band": bandEUTRA_r10["value"][dl_counter],
#                                            "class": ca_BandwidthClassUL_r10["value"][ul_counter]})
#
#                     ul_counter += 1
#
#                 new_comb["dl"].append({"band": bandEUTRA_r10["value"][dl_counter],
#                                        "class": ca_BandwidthClassDL_r10["value"][dl_counter],
#                                        "mimo": supportedMIMO_CapabilityDL_r10["value"][dl_counter]})
#                 bcs = "default" if str(band_comb_counter) not in supportedBandCombinationExt_r10["value"] else\
#                     supportedBandwidthCombinationSet_r10["value"][supportedBandCombinationExt_r10["value"].index(
#                         str(band_comb_counter))]
#
#                 new_comb["bcs"] = bcs
#                 dl_counter += 1
#             band_comb_counter += 1
#             band_combinations.append(new_comb)
#
#     def get_r11_band_combinations(band_combinations):
#         inter_freq_r11 = get_start_end(interFreqBandList_r11["value"], "<")
#         inter_rat_r11 = get_start_end(interRAT_BandList_r11["value"], "<")
#         band_combinations_r11 = get_start_end(supportedBandCombinationAdd_r11["value"])
#         all_band_combinations = []
#
#         def get_length(item):
#             return int(item[1]) - int(item[0])
#         start = 0
#         for bc_r11, interf_r11, interr_r11 in zip(band_combinations_r11, inter_freq_r11, inter_rat_r11):
#             bcs = "default"
#             end = start + get_length(bc_r11) - get_length(interf_r11) - get_length(interr_r11)
#             band_combs = get_start_end(bandParameterList_r11["value"][start:end])
#             if get_length(band_combs[-1]) < 3:
#                 start = end - 1
#                 band_combs = band_combs[:-1]
#                 bcs = supportedBandwidthCombinationSet_r11["value"].pop(0)
#             elif band_combs.__len__() == 1 and get_length(band_combs[0]) == 5:
#                 band_combs = get_start_end(bandParameterList_r11["value"][start:end - 1])
#                 start = end - 1
#                 bcs = supportedBandwidthCombinationSet_r11["value"].pop(0)
#             else:
#                 start = end
#             all_band_combinations.append({"band_combs": band_combs, "bcs": bcs})
#
#         ul_counter = 0
#         dl_counter = 0
#         for bc in all_band_combinations:
#             new_comb = {"ul": [], "dl": [], "bcs": bc["bcs"]}
#
#             for ob in bc["band_combs"]:
#                 if (ob[1] - ob[0]) % 2 == 0:
#                     # noinspection PyTypeChecker
#                     new_comb["ul"].append({"band": bandEUTRA_r11["value"][dl_counter],
#                                            "class": ca_BandwidthClassUL_r10_r11["value"][ul_counter]})
#
#                     ul_counter += 1
#                 # noinspection PyTypeChecker
#                 new_comb["dl"].append({"band": bandEUTRA_r11["value"][dl_counter],
#                                        "class": ca_BandwidthClassDL_r10_r11["value"][dl_counter],
#                                        "mimo": supportedMIMO_CapabilityDL_r10_r11["value"][dl_counter]})
#                 dl_counter += 1
#             band_combinations.append(new_comb)
#
#     band_combination_list = []
#     get_r10_band_combinations(band_combination_list)
#     get_r11_band_combinations(band_combination_list)
#     for b in band_combination_list:
#         print("ul:", b["ul"])
#         print("dl:", b["dl"])
#         print("bcs:", b["bcs"])
#
#
# # TODO: add supportedBandwidthCombinationSet,c0 to both r10 and r11
# # TODO: account for non contiguous CA in uplink (update the structre of ul from dict to array)
# get_test_case_results("Samsung G988B (Galaxy S20 Ultra 5G) SW Testing", "MR2-IOT1")
