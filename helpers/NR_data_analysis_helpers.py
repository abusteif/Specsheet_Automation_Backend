def initiate_feature_set_values(container, NR_items, NR_special_ie_list, LTE_items):
    try:
        container.featureSetsDownlink = NR_items["release_15,featureSets,featureSetsDownlink"]
        container.featureSetListPerDownlinkCC = NR_items["release_15,featureSets,featureSetsDownlink,"
                                                         "FeatureSetDownlink,featureSetListPerDownlinkCC"]
        container.FeatureSetDownlinkPerCC_Id = NR_items["release_15,featureSets,featureSetsDownlink,"
                                                        "FeatureSetDownlink,featureSetListPerDownlinkCC,"
                                                        "FeatureSetDownlinkPerCC-Id"]
        container.featureSetsDownlinkPerCC = NR_items["release_15,featureSets,featureSetsDownlinkPerCC"]
        container.supportedBandwidthDL = NR_special_ie_list["release_15,featureSets,featureSetsDownlinkPerCC,"
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

    # Uplink NR FeatureSet IEs
    try:
        container.featureSetsUplink = NR_items["release_15,featureSets,featureSetsUplink"]
        container.featureSetListPerUplinkCC = NR_items["release_15,featureSets,featureSetsUplink,FeatureSetUplink,"
                                                       "featureSetListPerUplinkCC"]
        container.FeatureSetUplinkPerCC_Id = NR_items["release_15,featureSets,featureSetsUplink,FeatureSetUplink,"
                                                      "featureSetListPerUplinkCC,FeatureSetUplinkPerCC-Id"]
        container.featureSetsUplinkPerCC = NR_items["release_15,featureSets,featureSetsUplinkPerCC"]
        container.supportedBandwidthUL = NR_special_ie_list["release_15,featureSets,featureSetsUplinkPerCC,"
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

    # LTE FeatureSet UL IE's
    try:
        container.featureSetsUL_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,featureSetsUL-r15"]
        container.featureSetPerCC_ListUL_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,featureSetsUL-r15,"
                                                         "FeatureSetUL-r15,featureSetPerCC-ListUL-r15"]
        container.FeatureSetUL_PerCC_Id_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,featureSetsUL-r15,"
                                                        "FeatureSetUL-r15,featureSetPerCC-ListUL-r15,"
                                                        "FeatureSetUL-PerCC-Id-r15"]
        container.featureSetsUL_PerCC_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,featureSetsUL-PerCC-r15"]
        container.supportedMIMO_CapabilityUL_MRDC_r15 = LTE_items["release_1510,featureSetsEUTRA-r15,"
                                                                  "featureSetsUL-PerCC-r15,FeatureSetUL-PerCC-r15,"
                                                                  "supportedMIMO-CapabilityUL-r15"]
    except KeyError:
        pass

def initiate_band_combination_values(container, NR_items, NR_special_ie_list):
    try:
        container.supportedBandCombinationList = NR_items["release_15,rf-ParametersMRDC,"
                                                          "supportedBandCombinationList"]
        container.bandList = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,BandCombination,"
                                      "bandList"]
        container.bandParameters_NR_LTE = NR_special_ie_list["release_15,rf-ParametersMRDC,"
                                                             "supportedBandCombinationList,"
                                                             "BandCombination,bandList,BandParameters"]
        container.bandEUTRA_list = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                            "BandCombination,bandList,BandParameters,eutra,bandEUTRA"]
        container.bandNR_list = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                         "BandCombination,bandList,BandParameters,nr,bandNR"]

        container.ca_BandwidthClassDL_EUTRA = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                       "BandCombination,bandList,"
                                                       "BandParameters,eutra,ca-BandwidthClassDL-EUTRA"]
        container.ca_BandwidthClassDL_NR = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                    "BandCombination,bandList,BandParameters,nr,"
                                                    "ca-BandwidthClassDL-NR"]
        container.ca_BandwidthClassUL_NR = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                    "BandCombination,bandList,BandParameters,nr,"
                                                    "ca-BandwidthClassUL-NR"]
        container.featureSetCombination_used = NR_items["release_15,rf-ParametersMRDC,supportedBandCombinationList,"
                                                        "BandCombination,featureSetCombination"]
        container.featureSetCombination_declared = NR_items["release_15,featureSetCombinations,"
                                                            "FeatureSetCombination"]
        container.FeatureSetsPerBand = NR_items["release_15,featureSetCombinations,FeatureSetCombination,"
                                                "FeatureSetsPerBand"]
        container.FeatureSet = NR_special_ie_list["release_15,featureSetCombinations,FeatureSetCombination,"
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
def map_fr_bw_num_to_value(num, fr):
    fr1 = ["mhz5", "mhz10", "mhz15", "mhz20", "mhz25", "mhz30", "mhz40", "mhz50", "mhz60", "mhz80", "mhz100"]
    fr2 = ["mhz50", "mhz100", "mhz200", "mhz400"]
    if fr == "fr1":
        return fr1[int(num)]
    if fr == "fr2":
        return fr2[int(num)]

def map_mimo_num_to_value_ul(num):
    return ["oneLayer", "twoLayers", "fourLayers"][int(num)]

def map_mimo_num_to_value_dl(num):
    return ["twoLayers", "fourLayers", "eightLayers"][int(num)]

def map_modulation_num_to_value(num):
    return ["bpsk-halfpi", "bpsk", "qpsk", "qam16", "qam64", "qam256"][int(num)]
