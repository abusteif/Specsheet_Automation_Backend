from Specsheet_Automation.scripts.specsheet_automation import extract_and_populate_specsheet

hex_data = {"UECapabilityInformation_4G": "1A0F500F60018700FB04000000000B000000008702380108282DDB80504003020E10204F84F8"
                                          "4F84F84FBF06EC4D00101BB04800000002A77C0000000B51003003002400C108608430421821"
                                          "0C1006080300304218210C1006080304218018200C100610021840086100218210410821002"
                                          "1840086100218018210410820841042084008610021840086006080304018012D7D54621540"
                                          "18000082063000208184000820638002001880008006000024838C0008280104146083800008"
                                          "20E100020A0041050820E000020838E0008080104147081800008206300024838C0008284104"
                                          "14608384000820E38002023041051C206300020838400082841040C200049071C00101082082"
                                          "8E10308001042C60004042082801042460818400082801042460808410700001041C20004940"
                                          "0800A1049C0000400B1C001010820A0041091C206100020A0041091C2021041C000041030004"
                                          "1241C600049420800A3049C2000400718001050824028C10708001202C700040460828410424"
                                          "70818C00082841042470808C10708001040C601049071C001010824828E10308001240C20104"
                                          "95013E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E1"
                                          "3E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13E13ED9D000011A8043C3C3C3C3C5E2"
                                          "F1787878BC5E2E8FE3F87878723F8FE3F87878722F178BC5C334001F3841B00060207AF34080"
                                          "2913FFCD29778A01D00010008A4A100100025828802401200900480240120281010480A04041"
                                          "202810104802405020209014080824050200901408082409002040810200480A040412048010"
                                          "20408100240081C050202090140808240900204081020048010380A0404120040C412E680026"
                                          "BC0800000410000A320400020000042200010008208400",
            "attachRequest": "980100000100000010008A008A00EDB095A482468706F300010905000741020BF605F510C54570DBB93ACF07F"
                             "070C04018009000370204D031D127308080211001000010810600000000830600000000000D00000300000A00"
                             "000500001000001100001A01010023000024005205F51020115C0A00310465E024011305F510015111035758A"
                             "6F15D0104E0C11002C7806F04F0007000"
            }


print(extract_and_populate_specsheet(hex_data, "a", "b"))

# from Specsheet_Automation.static_data.file_info import spec_attach_request_sample_hex_file, spec_attach_request_sample_lists_file
# from Specsheet_Automation.classes.DUT_spec_attach_request_info_extraction import DUTSpecAttachRequestInfoExtraction
# from Specsheet_Automation.helpers.specsheet_automation_helpers import extract_data, get_full_path
# from Specsheet_Automation.static_data.configuration import ATTACHREQUEST_MESSAGE_TYPE, ATTACHREQUEST_DELIMITER
#
# with open(spec_attach_request_sample_hex_file, "r") as sample_hex_file:
#     sample_hex_data = "".join([line.strip().replace(" ", "") for line in sample_hex_file.readlines()])
#
# extracting = extract_data(sample_hex_data, ATTACHREQUEST_MESSAGE_TYPE, ATTACHREQUEST_DELIMITER, temp=False)
# if extracting[0][0]:
#     lists_file = get_full_path(spec_attach_request_sample_lists_file, extracting[1], False)
# a = DUTSpecAttachRequestInfoExtraction(lists_file)
# a.trim_data()
# a.create_spec_ie()
# a.check_for_extra_ie()
