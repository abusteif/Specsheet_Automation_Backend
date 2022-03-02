from Specsheet_Automation.static_data.configuration import mimo_mapping, class_mapping

def pop_delimiters_from_ie_list(ie_list, single_item_list=None, split_list=None):
    for ie in ie_list:
        choice_list = True
        split_list_found = False

        if isinstance(ie_list[ie], list):
            for i in ie_list[ie]:
                if "special_" not in i:
                    choice_list = False

            if ie in split_list:
                ie_list[ie] = {
                    "primary": [a for a in ie_list[ie] if "special_" not in a],
                    "secondary": [a.split("special_")[1] for a in ie_list[ie] if "special_" in a]
                }
                split_list_found = True

            elif not choice_list:
                ie_list[ie] = [a for a in ie_list[ie] if "special_" not in a]

            if ie not in single_item_list:
                if not split_list_found:
                    ie_list[ie] = [a.split("_itemVal_")[0] for a in ie_list[ie]]
            if choice_list:
                ie_list[ie] = [a.split("special_")[1] for a in ie_list[ie]]


def initiate_feature_set_values(container, NR_items, LTE_items):
    try:
        container.featureSetsDownlink = NR_items["release_15,featureSets,featureSetsDownlink"]
        container.featureSetListPerDownlinkCC = NR_items["release_15,featureSets,featureSetsDownlink,"
                                                         "FeatureSetDownlink,featureSetListPerDownlinkCC"]
        container.FeatureSetDownlinkPerCC_Id = NR_items["release_15,featureSets,featureSetsDownlink,"
                                                        "FeatureSetDownlink,featureSetListPerDownlinkCC,"
                                                        "FeatureSetDownlinkPerCC-Id"]
        container.featureSetsDownlinkPerCC = NR_items["release_15,featureSets,featureSetsDownlinkPerCC"]
        container.supportedBandwidthDL = NR_items["release_15,featureSets,featureSetsDownlinkPerCC,"
                                                  "FeatureSetDownlinkPerCC,supportedBandwidthDL"]
    except KeyError:
        pass
    try:
        container.supportedBandwidthDLFR1 = NR_items["release_15,featureSets,featureSetsDownlinkPerCC,"
                                                     "FeatureSetDownlinkPerCC,supportedBandwidthDL,fr1"]
    except KeyError:
        pass
    try:
        container.supportedBandwidthDLFR2 = NR_items["release_15,featureSets,featureSetsDownlinkPerCC,"
                                                     "FeatureSetDownlinkPerCC,supportedBandwidthDL,fr2"]
    except KeyError:
        pass
    try:
        container.maxNumberMIMO_LayersPDSCH = NR_items["release_15,featureSets,featureSetsDownlinkPerCC,"
                                                       "FeatureSetDownlinkPerCC,maxNumberMIMO-LayersPDSCH"]
        container.supportedModulationOrderDL = NR_items["release_15,featureSets,featureSetsDownlinkPerCC,"
                                                        "FeatureSetDownlinkPerCC,supportedModulationOrderDL"]
    except KeyError:
        pass

    try:
        container.featureSetsDownlink_v1540 = NR_items["release_15,featureSets,featureSetsDownlink-v1540"]
    except KeyError:
        pass

    try:
        container.additionalDMRS_DL_Alt = NR_items["release_15,featureSets,featureSetsDownlink-v1540,"
                                                   "FeatureSetDownlink-v1540,additionalDMRS-DL-Alt"]
    except KeyError:
        pass

    try:
        container.oneFL_DMRS_TwoAdditionalDMRS_DL = NR_items["release_15,featureSets,featureSetsDownlink-v1540,"
                                                             "FeatureSetDownlink-v1540,oneFL-DMRS-TwoAdditionalDMRS-DL"]
    except KeyError:
        pass

    try:
        container.twoFL_DMRS_TwoAdditionalDMRS_DL = NR_items["release_15,featureSets,featureSetsDownlink-v1540,"
                                                             "FeatureSetDownlink-v1540,twoFL-DMRS-TwoAdditionalDMRS-DL"]
    except KeyError:
        pass

    # Uplink NR FeatureSet IEs
    try:
        container.featureSetsUplink = NR_items["release_15,featureSets,featureSetsUplink"]
        container.featureSetListPerUplinkCC = NR_items["release_15,featureSets,featureSetsUplink,FeatureSetUplink,"
                                                       "featureSetListPerUplinkCC"]
        container.FeatureSetUplinkPerCC_Id = NR_items["release_15,featureSets,featureSetsUplink,FeatureSetUplink,"
                                                      "featureSetListPerUplinkCC,FeatureSetUplinkPerCC-Id"]
        container.featureSetsUplinkPerCC = NR_items["release_15,featureSets,featureSetsUplinkPerCC"]
        container.supportedBandwidthUL = NR_items["release_15,featureSets,featureSetsUplinkPerCC,"
                                                  "FeatureSetUplinkPerCC,supportedBandwidthUL"]
    except KeyError:
        pass
    try:
        container.supportedBandwidthULFR1 = NR_items["release_15,featureSets,featureSetsUplinkPerCC,"
                                                     "FeatureSetUplinkPerCC,supportedBandwidthUL,fr1"]
    except KeyError:
        pass
    try:
        container.supportedBandwidthULFR2 = NR_items["release_15,featureSets,featureSetsUplinkPerCC,"
                                                     "FeatureSetUplinkPerCC,supportedBandwidthUL,fr2"]
    except KeyError:
        pass
    try:
        container.maxNumberMIMO_LayersCB_PUSCH = NR_items["release_15,featureSets,featureSetsUplinkPerCC,"
                                                          "FeatureSetUplinkPerCC,"
                                                          "mimo-CB-PUSCH,maxNumberMIMO-LayersCB-PUSCH"]
        container.supportedModulationOrderUL = NR_items["release_15,featureSets,featureSetsUplinkPerCC,"
                                                        "FeatureSetUplinkPerCC,supportedModulationOrderUL"]
    except KeyError:
        pass

    # LTE FeatureSet DL IE's
    try:
        container.featureSetsDL_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,featureSetsDL-r15"]
        container.featureSetPerCC_ListDL_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,featureSetsDL-r15,"
                                                         "FeatureSetDL-r15,featureSetPerCC-ListDL-r15"]
        container.FeatureSetDL_PerCC_Id_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,featureSetsDL-r15,"
                                                        "FeatureSetDL-r15,featureSetPerCC-ListDL-r15,"
                                                        "FeatureSetDL-PerCC-Id-r15"]
        container.featureSetsDL_PerCC_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,featureSetsDL-PerCC-r15"]
        container.supportedMIMO_CapabilityDL_MRDC_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,"
                                                                  "featureSetsDL-PerCC-r15,FeatureSetDL-PerCC-r15,"
                                                                  "supportedMIMO-CapabilityDL-MRDC-r15"]
    except KeyError:
        pass

def initiate_band_combination_values(container, NR_items):
    try:
        container.supportedBandCombinationList = NR_items["release_15,rf-ParametersMRDC,"
                                                          "supportedBandCombinationList"]
        container.bandList = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,BandCombination,"
                                      "bandList"]
        container.bandParameters_NR_LTE = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                   "BandCombination,bandList,BandParameters"]
        container.bandEUTRA_list = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                            "BandCombination,bandList,BandParameters,eutra,bandEUTRA"]
        container.bandNR_list = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                         "BandCombination,bandList,BandParameters,nr,bandNR"]

        container.ca_BandwidthClassDL_EUTRA = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                       "BandCombination,bandList,"
                                                       "BandParameters,eutra,ca-BandwidthClassDL-EUTRA"]

        container.ca_BandwidthClassUL_EUTRA = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                       "BandCombination,bandList,"
                                                       "BandParameters,eutra,ca-BandwidthClassUL-EUTRA"]

        container.ca_BandwidthClassDL_NR = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                    "BandCombination,bandList,BandParameters,nr,"
                                                    "ca-BandwidthClassDL-NR"]
        container.ca_BandwidthClassUL_NR = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                    "BandCombination,bandList,BandParameters,nr,"
                                                    "ca-BandwidthClassUL-NR"]
        container.featureSetCombination = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                   "BandCombination,featureSetCombination"]
        container.featureSetCombinations_declared = NR_items["release_15,featureSetCombinations"]
        container.featureSetCombination_declared = NR_items["release_15,featureSetCombinations,"
                                                            "FeatureSetCombination"]
        container.FeatureSetsPerBand = NR_items["release_15,featureSetCombinations,FeatureSetCombination,"
                                                "FeatureSetsPerBand"]
        container.FeatureSet = NR_items["release_15,featureSetCombinations,FeatureSetCombination,"
                                        "FeatureSetsPerBand,FeatureSet"]
        container.downlinkSetEUTRA = NR_items["release_15,featureSetCombinations,FeatureSetCombination,"
                                              "FeatureSetsPerBand,FeatureSet,eutra,downlinkSetEUTRA"]
        container.uplinkSetEUTRA = NR_items["release_15,featureSetCombinations,FeatureSetCombination,"
                                            "FeatureSetsPerBand,FeatureSet,eutra,uplinkSetEUTRA"]
        container.downlinkSetNR = NR_items["release_15,featureSetCombinations,FeatureSetCombination,"
                                           "FeatureSetsPerBand,FeatureSet,nr,downlinkSetNR"]
        container.uplinkSetNR = NR_items["release_15,featureSetCombinations,FeatureSetCombination,"
                                         "FeatureSetsPerBand,FeatureSet,nr,uplinkSetNR"]

    except KeyError as e:
        print(e)
        pass

def initiate_NR_band_values(container, NR_items):
    container.all_bands = NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,bandNR"]


def map_fr_bw_num_to_value(num, fr):
    fr1 = ["5", "10", "15", "20", "25", "30", "40", "50", "60", "80", "100"]
    fr2 = ["50", "100", "200", "400"]
    if fr == "fr1":
        return fr1[int(num)]
    if fr == "fr2":
        return fr2[int(num)]

def map_mimo_num_to_value_ul_NR(num):
    return ["1", "2", "4"][int(num)]

def map_mimo_num_to_value_dl_NR(num):
    return ["2", "4", "8"][int(num)]

def map_modulation_num_to_value(num):
    return ["bpsk-halfpi", "bpsk", "qpsk", "16qam", "64qam", "256qam"][int(num)]

def map_bw_support_hex_to_value(bw_num):

    values_list = {
        "fr1": ["5", "10", "15", "20", "25", "30", "40", "50", "60", "80", "100"],
        "fr2": ["50", "100", "200"]
    }

    result = dict()
    one_found = False
    for bn in bw_num:
        if not bw_num[bn][0]:
            continue
        num = "".join(bw_num[bn][0].split(":"))
        if num == "0000":
            continue
        else:
            one_found = True
            bw_result = []
            num = bin(int(num, 16))[2:].zfill(len(num) * 4)[:10]
            for digit_index, digit in enumerate(num):
                if int(digit) == 1:
                    bw_result.append(values_list[bw_num[bn][1]][digit_index])
            result[bn] = ", ".join(bw_result)

    return result if one_found else "all supported BWs as per 3GPP"

def get_bands_NR_dl(band_comb):
    edited_band_comb = []
    for lte_band_index, lte_band in enumerate(band_comb["lte"]["bands"]):
        lte_mimo_declared = band_comb["featureSetCombination"]["lte"]["dl"][lte_band_index]
        lte_mimo = ",".join([m["supportedMIMO_CapabilityDL_MRDC_r15"] for m in lte_mimo_declared])
        edited_band_comb.append(
            "{}{}({})".format(
                lte_band,
                class_mapping[int(band_comb["lte"]["bandwidthClass"]["dl"][lte_band_index])],
                lte_mimo
            )
        )

    for nr_band_index, nr_band in enumerate(band_comb["nr"]["bands"]):
        nr_mimo_declared = band_comb["featureSetCombination"]["nr"]["dl"][nr_band_index]
        nr_mimo = ",".join([m["maxNumberMIMO_LayersPDSCH"] for m in nr_mimo_declared])
        # nr_mimo = 2 if nr_band == "78" else 4
        edited_band_comb.append(
            "n{}{}({})".format(
                nr_band,
                class_mapping[int(band_comb["nr"]["bandwidthClass"]["dl"][nr_band_index])],
                nr_mimo
            )
        )

    return "-".join(edited_band_comb)

def get_bands_NR_ul(band_comb):
    index_of_ul_lte = None
    nr_ul_index = None
    ul_layer_num = None
    for index, item in enumerate(band_comb["featureSetCombination"]["lte"]["ul"]):
        if item != "0":
            index_of_ul_lte = index
            break

    for nr_ul_index, nr_ul in enumerate(band_comb["featureSetCombination"]["nr"]["ul"]):
        if isinstance(nr_ul[0], dict):
            ul_layer_num = nr_ul[0]["maxNumberMIMO_LayersCB_PUSCH"]
            break

    return "{}{}-n{}{}({})".format(
        band_comb["lte"]["bands"][index_of_ul_lte],
        class_mapping[int(band_comb["lte"]["bandwidthClass"]["ul"][0])],
        band_comb["nr"]["bands"][nr_ul_index],
        class_mapping[int(band_comb["nr"]["bandwidthClass"]["ul"][0])],
        ul_layer_num
    )


def get_bw_NR_dl(band_comb):
    # return ",".join([bw[0]["supportedBandwidthDL"] for bw in band_comb["featureSetCombination"]["nr"]["dl"]])
    return ",".join([item["supportedBandwidthDL"] for sublist in
                     band_comb["featureSetCombination"]["nr"]["dl"] for item in sublist if isinstance(item, dict)])

def get_bw_NR_ul(band_comb):
    # return ",".join([bw[0]["supportedBandwidthDL"] for bw in band_comb["featureSetCombination"]["nr"]["dl"]])
    return ",".join([item["supportedBandwidthUL"] for sublist in
                     band_comb["featureSetCombination"]["nr"]["ul"] for item in sublist if isinstance(item, dict)])

def get_lte_dl_layers(band_comb):
    return sum([int(item["supportedMIMO_CapabilityDL_MRDC_r15"]) for sublist in
                band_comb["featureSetCombination"]["lte"]["dl"] for item in sublist])

def get_carriers_num(band_comb, rat, direction):
    carrier_num = 0
    for dl in band_comb[rat]["bandwidthClass"][direction]:
        if dl == "0":
            carrier_num += 1
        else:
            carrier_num += 2
    return carrier_num

def get_NR_modulation_dl(band_comb):
    return ",".join([item["supportedModulationOrderDL"] for sublist in
                     band_comb["featureSetCombination"]["nr"]["dl"] for item in sublist if isinstance(item, dict)])

def get_NR_modulation_ul(band_comb):
    return ",".join([item["supportedModulationOrderUL"] for sublist in
                     band_comb["featureSetCombination"]["nr"]["ul"] for item in sublist if isinstance(item, dict)])

def get_dss_support_status(band_comb):
    return "Supported" if False not in band_comb["featureSetCombination"]["dss"] else "Not Supported"

def convert_bw_to_excel_ready(all_bw):
    if not isinstance(all_bw, dict):
        return all_bw
    lines = []
    for b in all_bw:
        lines.append("{}: {}".format(b, all_bw[b]))
    return "\n".join(lines)

def maxNumberConfiguredTCIstatesPerCC_num_to_value(num):
    return ["n4", "n8", "n16", "n32", "n64", "n128"][int(num)] if num else ["No Information"]

def maxNumberActiveTCI_PerBWP_num_to_value(num):
    return ["n1", "n2", "n4", "n8"][int(num)] if num else "No Information"

def pusch_TransCoherence_num_to_value(num):
    return ["nonCoherent", "partialCoherent", "fullCoherent"][int(num)] if num else "No Information"

def maxNumberNonGroupBeamReporting_num_to_value(num):
    return ["n1", "n2", "n4"][int(num)] if num else "No Information"

def mnrtbsdl_num_to_value(num):
    return ["n4", "n7", "n14"][int(num)] if num else "No Information"

def brt_15_num_to_value(num):
    return ["sym2", "sym4", "sym8"][int(num)] if num else "No Information"

def brt_30_num_to_value(num):
    return ["sym4", "sym8", "sym14", "sym28"][int(num)] if num else "No Information"

def brt_60_num_to_value(num):
    return ["sym8", "sym14", "sym28"][int(num)] if num else "No Information"

def brt_120_num_to_value(num):
    return ["sym14", "sym28", "sym56"][int(num)] if num else "No Information"

def maxNumberSSB_CSI_RS_ResourceOneTx_num_to_value(num):
    return ["n0", "n8", "n16", "n32", "n64"][int(num)] if num else "No Information"

def maxNumberCSI_RS_Resource_num_to_value(num):
    return ["n0", "n4", "n8", "n16", "n32", "n64"][int(num)] if num else "No Information"

def maxNumberCSI_RS_ResourceTwoTx_num_to_value(num):
    return ["n0", "n4", "n8", "n16", "n32", "n64"][int(num)] if num else "No Information"

def supportedCSI_RS_Density_num_to_value(num):
    return ["one", "three", "oneAndThree"][int(num)] if num else "No Information"

def maxNumberAperiodicCSI_RS_Resource_num_to_value(num):
    return ["n0", "n1", "n4", "n8", "n16", "n32", "n64"][int(num)] if num else "No Information"

def ue_PowerClass_num_to_value(num):
    return ["pc1", "pc2", "pc3", "pc4"][int(num)] if num else "No Information"

def maxUplinkDutyCycle_PC2_FR1_num_to_value(num):
    return ["n60", "n70", "n80", "n90", "n100"][int(num)] if num else "No Information"

def modes_num_to_value(num):
    return ["mode1", "mode1andMode2"][int(num)] if num else "No Information"

def maxNumberTxPortsPerResource_num_to_value(num):
    return ["p2", "p4", "p8", "p12", "p16", "p24", "p32"][int(num)] if num else "No Information"

def get_value_from_itemVal(list_of_elements, max_size):
    converted = []
    values = [item.split("_itemVal_")[0] for item in list_of_elements]
    indices = [int(item.split("_itemVal_")[1]) for item in list_of_elements]
    for i in range(max_size):
        if i in indices:
            converted.append(values[indices.index(i)])
        else:
            converted.append(None)
    return converted

def initiate_empty_list(num_of_var, max_length):
    result = []
    for i in range(num_of_var):
        result.append([None] * max_length)
    return result

def convert_hex_to_binary(hex_num, min_zeros=32):
    if not hex_num:
        return hex_num
    hex_num = hex_num.replace(":", "")
    return bin(int(hex_num, 16))[2:].zfill(min_zeros)

def present_bw(bw):
    if not bw:
        return None
    return "{} ({})".format(bw, convert_hex_to_binary(bw, 10)[:10])
