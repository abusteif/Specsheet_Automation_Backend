from Specsheet_Automation.helpers.data_analysis_helpers import get_start_end, get_length, map_mimo_num_to_value_dl_LTE, \
    get_value_from_itemVal
from Specsheet_Automation.helpers.NR_data_analysis_helpers import map_fr_bw_num_to_value, map_modulation_num_to_value, \
    map_mimo_num_to_value_ul_NR, map_mimo_num_to_value_dl_NR, initiate_feature_set_values, \
    initiate_band_combination_values, pop_delimiters_from_ie_list, get_bands_NR_dl, get_bands_NR_ul, get_bw_NR_dl, \
    get_lte_dl_layers, get_carriers_num, get_NR_modulation_ul, get_NR_modulation_dl, get_bw_NR_ul, \
    get_dss_support_status, map_bw_support_hex_to_value, initiate_NR_band_values, convert_bw_to_excel_ready, \
    pusch_TransCoherence_num_to_value, maxNumberNonGroupBeamReporting_num_to_value, mnrtbsdl_num_to_value, \
    brt_15_num_to_value, brt_30_num_to_value, brt_60_num_to_value, brt_120_num_to_value, \
    maxNumberSSB_CSI_RS_ResourceOneTx_num_to_value, maxNumberCSI_RS_Resource_num_to_value, \
    maxNumberCSI_RS_ResourceTwoTx_num_to_value, supportedCSI_RS_Density_num_to_value, \
    maxNumberAperiodicCSI_RS_Resource_num_to_value, initiate_empty_list, ue_PowerClass_num_to_value, \
    maxUplinkDutyCycle_PC2_FR1_num_to_value, modes_num_to_value, maxNumberTxPortsPerResource_num_to_value, \
    maxNumberConfiguredTCIstatesPerCC_num_to_value, maxNumberActiveTCI_PerBWP_num_to_value

from copy import deepcopy

class NRDataAnalysis:
    def __init__(self, NR_ie_list, LTE_ie_list):

        single_item_list = [
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,"
            "tci-StatePDSCH,maxNumberConfiguredTCIstatesPerCC",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,tci-StatePDSCH,"
            "maxNumberActiveTCI-PerBWP",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,pusch-TransCoherence",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,aperiodicBeamReport",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,maxNumberNonGroupBeamReporting",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,maxNumberCSI-RS-SSB-CBD",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,periodicBeamReport",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand"
            ",maxNumberRxTxBeamSwitchDL,scs-15kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,"
            "maxNumberRxTxBeamSwitchDL,scs-30kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,"
            "maxNumberRxTxBeamSwitchDL,scs-60kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,"
            "maxNumberRxTxBeamSwitchDL,scs-120kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,"
            "maxNumberRxTxBeamSwitchDL,scs-240kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,beamReportTiming,scs-15kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,beamReportTiming,scs-30kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,beamReportTiming,scs-60kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,beamReportTiming,scs-120kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
            "maxNumberSSB-CSI-RS-ResourceOneTx",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
            "maxNumberCSI-RS-Resource",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
            "maxNumberCSI-RS-ResourceTwoTx",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
            "supportedCSI-RS-Density",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
            "maxNumberAperiodicCSI-RS-Resource",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,codebookParameters,type1,"
            "singlePanel,modes",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,codebookParameters,type1,"
            "singlePanel,maxNumberCSI-RS-PerResourceSet",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,multipleTCI",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,pusch-256QAM",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,ue-PowerClass",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,channelBWs-DL,fr1,scs-15kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,channelBWs-DL,fr1,scs-30kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,channelBWs-DL,fr1,scs-60kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,channelBWs-DL,fr2,scs-120kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,channelBWs-UL,fr1,scs-15kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,channelBWs-UL,fr1,scs-30kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,channelBWs-UL,fr1,scs-60kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,channelBWs-UL,fr2,scs-60kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,channelBWs-UL,fr2,scs-120kHz",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,maxUplinkDutyCycle-PC2-FR1",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,powerBoosting-pi2BPSK",
            "release_15,rf-Parameters,supportedBandListNR,BandNR,rateMatchingLTE-CRS",
            "release_15,featureSets,featureSetsDownlink-v1540,FeatureSetDownlink-v1540,additionalDMRS-DL-Alt",
            # "release_1540,ims-Parameters,ims-ParametersFRX-Diff,voiceOverNR"
        ]

        split_list = [
            "release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,codebookParameters,type1,"
            "singlePanel,supportedCSI-RS-ResourceList"
        ]
        print(NR_ie_list["release_1540,ims-Parameters,ims-ParametersFRX-Diff,voiceOverNR"])
        pop_delimiters_from_ie_list(NR_ie_list, single_item_list, split_list)
        pop_delimiters_from_ie_list(LTE_ie_list, [], [])

        self.NR_items = NR_ie_list
        self.LTE_items = LTE_ie_list

        self.processors = {
            "Supported NR Band": self.supportedNRBand,
            "supportedBandListNR": self.supportedBandListNR
        }

        # Downlink NR FeatureSet IEs
        self.featureSetsDownlink = None
        self.featureSetListPerDownlinkCC = None
        self.FeatureSetDownlinkPerCC_Id = None
        self.featureSetsDownlinkPerCC = None
        self.supportedBandwidthDL = None
        self.supportedBandwidthDLFR1 = None
        self.supportedBandwidthDLFR2 = None
        self.maxNumberMIMO_LayersPDSCH = None
        self.supportedModulationOrderDL = None
        self.featureSetsDownlink_v1540 = None
        self.additionalDMRS_DL_Alt = None
        self.oneFL_DMRS_TwoAdditionalDMRS_DL = None
        self.twoFL_DMRS_TwoAdditionalDMRS_DL = None

        # Uplink NR FeatureSet IEs
        self.featureSetsUplink = None
        self.featureSetListPerUplinkCC = None
        self.FeatureSetUplinkPerCC_Id = None
        self.featureSetsUplinkPerCC = None
        self.supportedBandwidthUL = None
        self.supportedBandwidthULFR1 = None
        self.supportedBandwidthULFR2 = None
        self.maxNumberMIMO_LayersCB_PUSCH = None
        self.supportedModulationOrderUL = None

        # LTE FeatureSet DL IEs
        self.featureSetsDL_r15 = None
        self.FeatureSetDL_PerCC_Id_r15 = None
        self.featureSetPerCC_ListDL_r15 = None
        self.featureSetsDL_PerCC_r15 = None
        self.supportedMIMO_CapabilityDL_MRDC_r15 = None

        # LTE FeatureSet UL IEs
        self.featureSetsUL_r15 = None
        self.featureSetPerCC_ListUL_r15 = None
        self.FeatureSetUL_PerCC_Id_r15 = None
        self.featureSetsUL_PerCC_r15 = None
        self.supportedMIMO_CapabilityUL_r15 = None

        # declared NR IEs
        self.band_combinations = []
        self.bandParameters = None
        self.bandParameters_NR_LTE = None
        self.supportedBandCombinationList = None
        self.bandList = None
        self.bandEUTRA_list = None
        self.bandNR_list = None
        self.ca_BandwidthClassDL_EUTRA = None
        self.ca_BandwidthClassUL_EUTRA = None
        self.ca_BandwidthClassDL_NR = None
        self.ca_BandwidthClassUL_NR = None
        self.featureSetCombination = None
        self.featureSetCombinations_declared = None
        self.featureSetCombination_declared = None
        self.FeatureSetsPerBand = None
        self.FeatureSet = None
        self.downlinkSetEUTRA = None
        self.uplinkSetEUTRA = None
        self.downlinkSetNR = None
        self.uplinkSetNR = None

        # NR Band IEs
        self.all_bands = []

        self.declared_band_combs = []
        self.dss_support_list = []
        self.featureSetPerCC_ListDL_LTE = []
        self.FeatureSetDownlink_NR = []
        self.FeatureSetUplink_NR = []
        self.band_combinations = []
        self.NR_bands = []

    def get_supported_NR_band_details(self):

        initiate_NR_band_values(self, self.NR_items)
        [mnctipc, mnatpw, ptc, abr, mnngbr, mncrsc, pbr, mnrtbsdl_15, mnrtbsdl_30, mnrtbsdl_60, mnrtbsdl_120,
         mnrtbsdl_240, brt_15, brt_30, brt_60, brt_120, mnscrrot, mnscrr, mnscrrtt, scrd, mnacrr,
         mtci, p256q, uepc, bw_dl_fr1_15, bw_dl_fr1_30, bw_dl_fr1_60, bw_dl_fr2_120, bw_ul_fr1_15, bw_ul_fr1_30,
         bw_ul_fr1_60, bw_ul_fr2_120, mudcp2f1, pbp, rmlc, von, modes,
         mncrprs] = initiate_empty_list(38, len(self.all_bands))

        try:
            mnctipc = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                           "mimo-ParametersPerBand,tci-StatePDSCH,"
                                                           "maxNumberConfiguredTCIstatesPerCC"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mnatpw = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                          "mimo-ParametersPerBand,tci-StatePDSCH,"
                                                          "maxNumberActiveTCI-PerBWP"], len(self.all_bands))
        except KeyError:
            pass
        try:
            ptc = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                       "mimo-ParametersPerBand,pusch-TransCoherence"],
                                         len(self.all_bands))
        except KeyError:
            pass
        try:
            abr = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                       "mimo-ParametersPerBand,aperiodicBeamReport"],
                                         len(self.all_bands))
        except KeyError:
            pass
        try:
            mnngbr = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                          "mimo-ParametersPerBand,maxNumberNonGroupBeamReporting"],
                                            len(self.all_bands))
        except KeyError:
            pass
        try:
            mncrsc = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                          "mimo-ParametersPerBand,maxNumberCSI-RS-SSB-CBD"],
                                            len(self.all_bands))
        except KeyError:
            pass
        try:
            pbr = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                       "mimo-ParametersPerBand,periodicBeamReport"],
                                         len(self.all_bands))
        except KeyError:
            pass
        try:
            mnrtbsdl_15 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                               "mimo-ParametersPerBand,maxNumberRxTxBeamSwitchDL,"
                                                               "scs-15kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mnrtbsdl_30 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                               "mimo-ParametersPerBand,maxNumberRxTxBeamSwitchDL,"
                                                               "scs-30kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mnrtbsdl_60 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                               "mimo-ParametersPerBand,maxNumberRxTxBeamSwitchDL,"
                                                               "scs-60kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mnrtbsdl_120 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                "mimo-ParametersPerBand,maxNumberRxTxBeamSwitchDL,"
                                                                "scs-120kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mnrtbsdl_240 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                "mimo-ParametersPerBand,maxNumberRxTxBeamSwitchDL,"
                                                                "scs-240kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            brt_15 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                          "mimo-ParametersPerBand,beamReportTiming,scs-15kHz"],
                                            len(self.all_bands))
        except KeyError:
            pass
        try:
            brt_30 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                          "mimo-ParametersPerBand,beamReportTiming,scs-30kHz"],
                                            len(self.all_bands))
        except KeyError:
            pass
        try:
            brt_60 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                          "mimo-ParametersPerBand,beamReportTiming,scs-60kHz"],
                                            len(self.all_bands))
        except KeyError:
            pass
        try:
            brt_120 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                           "mimo-ParametersPerBand,beamReportTiming,scs-120kHz"],
                                             len(self.all_bands))
        except KeyError:
            pass
        try:
            mnscrrot = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                            "mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
                                                            "maxNumberSSB-CSI-RS-ResourceOneTx"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mnscrr = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                          "mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
                                                          "maxNumberCSI-RS-Resource"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mnscrrtt = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                            "mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
                                                            "maxNumberCSI-RS-ResourceTwoTx"], len(self.all_bands))
        except KeyError:
            pass
        try:
            scrd = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                        "mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
                                                        "supportedCSI-RS-Density"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mnacrr = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                          "mimo-ParametersPerBand,beamManagementSSB-CSI-RS,"
                                                          "maxNumberAperiodicCSI-RS-Resource"], len(self.all_bands))
        except KeyError:
            pass
        try:
            modes = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                         "mimo-ParametersPerBand,codebookParameters,type1,"
                                                         "singlePanel,modes"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mncrprs = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                           "mimo-ParametersPerBand,codebookParameters,"
                                                           "type1,singlePanel,maxNumberCSI-RS-PerResourceSet"],
                                             len(self.all_bands))
        except KeyError:
            pass
        try:
            mtci = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                        "multipleTCI"], len(self.all_bands))
        except KeyError:
            pass
        try:
            p256q = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                         "pusch-256QAM"], len(self.all_bands))
        except KeyError:
            pass
        try:
            uepc = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                        "ue-PowerClass"], len(self.all_bands))
        except KeyError:
            pass
        try:
            bw_dl_fr1_15 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                "channelBWs-DL,fr1,scs-15kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            bw_dl_fr1_30 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                "channelBWs-DL,fr1,scs-30kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:

            bw_dl_fr1_60 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                "channelBWs-DL,fr1,scs-60kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            bw_dl_fr2_120 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                 "channelBWs-DL,fr2,scs-120kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            bw_ul_fr1_15 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                "channelBWs-UL,fr1,scs-15kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            bw_ul_fr1_30 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                "channelBWs-UL,fr1,scs-30kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            bw_ul_fr1_60 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                "channelBWs-UL,fr1,scs-60kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            bw_ul_fr2_120 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                                 "channelBWs-UL,fr2,scs-120kHz"], len(self.all_bands))
        except KeyError:
            pass
        try:
            mudcp2f1 = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                            "maxUplinkDutyCycle-PC2-FR1"], len(self.all_bands))
        except KeyError:
            pass
        try:
            pbp = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                       "powerBoosting-pi2BPSK"], len(self.all_bands))
        except KeyError:
            pass
        try:
            rmlc = get_value_from_itemVal(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                        "rateMatchingLTE-CRS"], len(self.all_bands))
        except KeyError:
            pass


        single_panel_data = self.get_singlePanel_data()
        for band_index, band in enumerate(self.all_bands):
            band_details = {
                "NR Band": band,
                "supportedBW":
                    map_bw_support_hex_to_value(
                        {
                            "scs-15kHz": [bw_dl_fr1_15[band_index] if bw_dl_fr1_15[band_index] else None, "fr1"],
                            "scs-30kHz": [bw_dl_fr1_30[band_index] if bw_dl_fr1_30[band_index] else None, "fr1"],
                            "scs-60kHz": [bw_dl_fr1_60[band_index] if bw_dl_fr1_60[band_index] else None, "fr1"],
                            "scs-120kHz": [bw_dl_fr2_120[band_index] if bw_dl_fr2_120[band_index] else None, "fr2"]
                        }
                    ),
                "maxNumberConfiguredTCIstatesPerCC": maxNumberConfiguredTCIstatesPerCC_num_to_value(
                    mnctipc[band_index]),
                "maxNumberActiveTCI-PerBWP": maxNumberActiveTCI_PerBWP_num_to_value(mnatpw[band_index]),
                "pusch-TransCoherence": pusch_TransCoherence_num_to_value(ptc[band_index]),
                "aperiodicBeamReport": "Supported" if abr[band_index] else "Not Supported",
                "maxNumber Non Group Beam Reporting": maxNumberNonGroupBeamReporting_num_to_value(mnngbr[band_index]),
                "maxNumberCSI-RS-SSB-CBD": mncrsc[band_index] if mncrsc[band_index] else "No Information",
                "periodicBeamReport": "Supported" if pbr[band_index] else "Not Supported",
                "maxNumberRxTxBeamSwitchDL->scs-15kHz": mnrtbsdl_num_to_value(mnrtbsdl_15[band_index]),
                "maxNumberRxTxBeamSwitchDL->scs-30kHz": mnrtbsdl_num_to_value(mnrtbsdl_30[band_index]),
                "maxNumberRxTxBeamSwitchDL->scs-60kHz": mnrtbsdl_num_to_value(mnrtbsdl_60[band_index]),
                "maxNumberRxTxBeamSwitchDL->scs-120kHz": mnrtbsdl_num_to_value(mnrtbsdl_120[band_index]),
                "maxNumberRxTxBeamSwitchDL->scs-240kHz": mnrtbsdl_num_to_value(mnrtbsdl_240[band_index]),
                "beamReportTiming->scs-15kHz": brt_15_num_to_value(brt_15[band_index]),
                "beamReportTiming->scs-30kHz": brt_30_num_to_value(brt_30[band_index]),
                "beamReportTiming->scs-60kHz": brt_60_num_to_value(brt_60[band_index]),
                "beamReportTiming->scs-120kHz": brt_120_num_to_value(brt_120[band_index]),
                "maxNumberSSB-CSI-RS-ResourceOneTx": maxNumberSSB_CSI_RS_ResourceOneTx_num_to_value(
                    mnscrrot[band_index]),
                "maxNumberCSI-RS-Resource": maxNumberCSI_RS_Resource_num_to_value(mnscrr[band_index]),
                "maxNumberCSI-RS-ResourceTwoTx": maxNumberCSI_RS_ResourceTwoTx_num_to_value(mnscrrtt[band_index]),
                "supportedCSI-RS-Density": supportedCSI_RS_Density_num_to_value(scrd[band_index]),
                "maxNumberAperiodicCSI-RS-Resource": maxNumberAperiodicCSI_RS_Resource_num_to_value(mnacrr[band_index]),
                "codebookParameters(Type1 singlePanel)->maxNumberTxPortsPerResource":
                    single_panel_data["mntppr"][band_index],
                "codebookParameters(Type1 singlePanel)->maxNumberResourcesPerBand":
                    single_panel_data["mnrpb"][band_index],
                "codebookParameters(Type1 singlePanel)->totalNumberTxPortsPerBand":
                    single_panel_data["tntppb"][band_index],
                "codebookParameters(Type1 singlePanel)->modes": modes_num_to_value(modes[band_index]),
                "codebookParameters(Type1 singlePanel)->maxNumberCSI-RS-PerResourceSet": mncrprs[band_index],
                "multipleTCI": "Supported" if mtci[band_index] else "Not Supported",
                "pusch-256QAM": "Supported" if p256q[band_index] else "Not Supported",
                "ue-PowerClass": ue_PowerClass_num_to_value(uepc[band_index]),
                "channelBWsDL->scs-15kHz": bw_dl_fr1_15[band_index],
                "channelBWsDL->scs-30kHz": bw_dl_fr1_30[band_index],
                "channelBWsDL->scs-60kHz": bw_dl_fr1_60[band_index],
                "channelBWsDL->scs-120kHz": bw_dl_fr2_120[band_index],
                "channelBWsUL->scs-15kHz": bw_ul_fr1_15[band_index],
                "channelBWsUL->scs-30kHz": bw_ul_fr1_30[band_index],
                "channelBWsUL->scs-60kHz": bw_ul_fr1_60[band_index],
                "channelBWsUL->scs-120kHz": bw_ul_fr2_120[band_index],
                "maxUplinkDutyCycle-PC2-FR1": maxUplinkDutyCycle_PC2_FR1_num_to_value(mudcp2f1[band_index]),
                "powerBoosting-pi2BPSK": "Supported" if pbp[band_index] else "Not Supported",
                "rateMatchingLTE-CRS": "Supported" if rmlc[band_index] else "Not Supported",
            }
            self.NR_bands.append(band_details)

    def supportedNRBand(self):
        return ",".join(self.all_bands)

    def supportedBandListNR(self):
        return "{} items".format(len(self.all_bands))

    def get_singlePanel_data(self):
        maxNumberTxPortsPerResource = self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                    "mimo-ParametersPerBand,codebookParameters,type1,singlePanel,"
                                                    "supportedCSI-RS-ResourceList,SupportedCSI-RS-Resource"
                                                    ",maxNumberTxPortsPerResource"]
        maxNumberResourcesPerBand = self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                  "mimo-ParametersPerBand,codebookParameters,type1,singlePanel,"
                                                  "supportedCSI-RS-ResourceList,SupportedCSI-RS-Resource,"
                                                  "maxNumberResourcesPerBand"]
        totalNumberTxPortsPerBand = self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,"
                                                  "mimo-ParametersPerBand,codebookParameters,type1,singlePanel,"
                                                  "supportedCSI-RS-ResourceList,SupportedCSI-RS-Resource,"
                                                  "totalNumberTxPortsPerBand"]

        mntppr = []
        mnrpb = []
        tntppb = []

        all_resource_list = self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,mimo-ParametersPerBand,"
                                          "codebookParameters,type1,singlePanel,"
                                          "supportedCSI-RS-ResourceList"]["secondary"]
        for r in all_resource_list:
            mntppr.append(", ".join(maxNumberTxPortsPerResource[0:int(r)]))
            mnrpb.append(", ".join(maxNumberResourcesPerBand[0:int(r)]))
            tntppb.append(", ".join(totalNumberTxPortsPerBand[0:int(r)]))

            maxNumberTxPortsPerResource = maxNumberTxPortsPerResource[int(r):]
            maxNumberResourcesPerBand = maxNumberResourcesPerBand[int(r):]
            totalNumberTxPortsPerBand = totalNumberTxPortsPerBand[int(r):]

        return {
            "mntppr": mntppr,
            "mnrpb": mnrpb,
            "tntppb": tntppb
        }

    def create_feature_set_details(self):
        initiate_feature_set_values(self, self.NR_items, self.LTE_items)

        self.create_feature_set_details_NR()
        self.create_feature_set_details_LTE()

    def create_feature_set_details_LTE(self):

        lte_FeatureSetDL_PerCC_r15 = [{"supportedMIMO_CapabilityDL_MRDC_r15": map_mimo_num_to_value_dl_LTE(int(m))}
                                      for m in self.supportedMIMO_CapabilityDL_MRDC_r15]
        fset_dlcc = get_start_end(self.featureSetPerCC_ListDL_r15, "<=")
        for f in fset_dlcc:
            fset_dl = self.FeatureSetDL_PerCC_Id_r15[0:get_length(f)]
            self.FeatureSetDL_PerCC_Id_r15 = self.FeatureSetDL_PerCC_Id_r15[get_length(f):]
            self.featureSetPerCC_ListDL_LTE.append([
                lte_FeatureSetDL_PerCC_r15[int(f_dl)] for f_dl in fset_dl
            ])

    def get_dss_support_list(self):
        fs_dl_1540 = get_start_end(self.featureSetsDownlink_v1540)
        self.dss_support_list = [True if item else False for item in get_value_from_itemVal(
            self.additionalDMRS_DL_Alt, len(fs_dl_1540))]

    def create_feature_set_details_NR(self):

        # DL Feature Sets

        assert len(self.supportedBandwidthDL) == len(self.supportedModulationOrderDL) == \
            len(self.maxNumberMIMO_LayersPDSCH)
        nr_featureSetDownlinkPerCC = []
        for b_dl_index, b_dl in enumerate(self.supportedBandwidthDL):
            bw = None
            if int(b_dl) == 0:
                bw = map_fr_bw_num_to_value(self.supportedBandwidthDLFR1.pop(0), "fr1")
            elif int(b_dl) == 1:
                bw = map_fr_bw_num_to_value(self.supportedBandwidthDLFR2.pop(0), "fr2")
            nr_featureSetDownlinkPerCC.append({
                "supportedBandwidthDL": bw,
                "maxNumberMIMO_LayersPDSCH": map_mimo_num_to_value_dl_NR(self.maxNumberMIMO_LayersPDSCH[b_dl_index]),
                "supportedModulationOrderDL": map_modulation_num_to_value(self.supportedModulationOrderDL[b_dl_index])
            })

        fset_dlcc = get_start_end(self.featureSetListPerDownlinkCC, "<=")
        for f in fset_dlcc:
            fset_dl = self.FeatureSetDownlinkPerCC_Id[0:get_length(f)]
            self.FeatureSetDownlinkPerCC_Id = self.FeatureSetDownlinkPerCC_Id[get_length(f):]
            self.FeatureSetDownlink_NR.append([
                nr_featureSetDownlinkPerCC[int(f_dl) - 1] for f_dl in fset_dl
            ])

        # UL Feature Sets
        assert len(self.supportedBandwidthUL) == len(self.supportedModulationOrderUL) == \
            len(self.maxNumberMIMO_LayersCB_PUSCH)
        nr_featureSetUplinkPerCC = []
        for b_ul_index, b_ul in enumerate(self.supportedBandwidthUL):
            bw = None
            if int(b_ul) == 0:
                bw = map_fr_bw_num_to_value(self.supportedBandwidthULFR1.pop(0), "fr1")
            elif int(b_ul) == 1:
                bw = map_fr_bw_num_to_value(self.supportedBandwidthULFR2.pop(0), "fr2")
            nr_featureSetUplinkPerCC.append({
                "supportedBandwidthUL": bw,
                "maxNumberMIMO_LayersCB_PUSCH": map_mimo_num_to_value_ul_NR(
                    self.maxNumberMIMO_LayersCB_PUSCH[b_ul_index]),
                "supportedModulationOrderUL": map_modulation_num_to_value(self.supportedModulationOrderUL[b_ul_index])
            })

        fset_ulcc = get_start_end(self.featureSetListPerUplinkCC, "<=")
        for f in fset_ulcc:
            fset_ul = self.FeatureSetUplinkPerCC_Id[0:get_length(f)]
            self.FeatureSetUplinkPerCC_Id = self.FeatureSetUplinkPerCC_Id[get_length(f):]
            self.FeatureSetUplink_NR.append([
                nr_featureSetUplinkPerCC[int(f_ul) - 1] for f_ul in fset_ul
            ])

        return

    def prepare_band_declared_feature_set(self):
        empty_band_combination = {
                    "lte": {
                        "ul": [],
                        "dl": []
                    },
                    "nr": {
                        "ul": [],
                        "dl": []
                    },
                    "dss": []
                }

        fsc_d_s1 = get_start_end(self.featureSetCombination_declared, "<")
        for f1 in fsc_d_s1:
            small = True
            fsc_d_s2 = get_start_end(self.featureSetCombination_declared[f1[0]:f1[1]])
            for f2 in fsc_d_s2:
                if get_length(f2) > 2:
                    # When multiple band combinations are under the same featureSetCombinations Item,
                    # each of the featureSetCombination Item's sub-items contains more than 2 children
                    small = False
                    break
            band_comb_len = int(get_length(f1) / 2)
            band_combination = deepcopy(empty_band_combination)

            if small:
                for f in self.FeatureSet[0: band_comb_len]:
                    if int(f) == 0:
                        band_combination["lte"]["ul"].append(self.uplinkSetEUTRA.pop(0))
                        band_combination["lte"]["dl"].append(self.downlinkSetEUTRA.pop(0))
                    elif int(f) == 1:
                        nr_f_ul = self.uplinkSetNR.pop(0)
                        nr_f_dl = self.downlinkSetNR.pop(0)
                        band_combination["nr"]["ul"].append(nr_f_ul)
                        band_combination["nr"]["dl"].append(nr_f_dl)
                        band_combination["dss"].append(self.dss_support_list[int(nr_f_dl) - 1])
                self.declared_band_combs.append([band_combination])

                self.FeatureSet = self.FeatureSet[band_comb_len:]

                self.FeatureSetsPerBand = self.FeatureSetsPerBand[band_comb_len * 2:]
            else:
                nr_lte_featureSet = get_start_end(self.FeatureSet[0: band_comb_len])

                self.FeatureSet = self.FeatureSet[band_comb_len:]
                multi_band_combs = get_start_end(self.FeatureSetsPerBand[0: band_comb_len * 2], "<")

                nr_ca = get_length(nr_lte_featureSet[1]) != int(get_length(multi_band_combs[-1]) / 2)
                declared_multi_band_comb = []

                for _ in range(int(get_length(multi_band_combs[-1]) / 2)):
                    declared_multi_band_comb.append(deepcopy(empty_band_combination))

                if nr_ca:
                    lte_multi_band_combs = multi_band_combs[:-2]
                    nr_multi_band_combs_2 = multi_band_combs[-2]
                else:
                    lte_multi_band_combs = multi_band_combs[:-1]
                    nr_multi_band_combs_2 = None
                nr_multi_band_combs_1 = multi_band_combs[-1]

                for lte_bc in lte_multi_band_combs:
                    for lte_band_index, _ in enumerate(get_start_end(self.FeatureSetsPerBand[lte_bc[0]:lte_bc[1]])):
                        declared_multi_band_comb[lte_band_index]["lte"]["ul"].append(self.uplinkSetEUTRA.pop(0))
                        declared_multi_band_comb[lte_band_index]["lte"]["dl"].append(self.downlinkSetEUTRA.pop(0))

                for nr_band_index_1, _ in enumerate(
                        get_start_end(self.FeatureSetsPerBand[nr_multi_band_combs_1[0]:nr_multi_band_combs_1[1]])):
                    nr_f_ul = self.uplinkSetNR.pop(0)
                    nr_f_dl = self.downlinkSetNR.pop(0)
                    declared_multi_band_comb[nr_band_index_1]["nr"]["ul"].append(nr_f_ul)
                    declared_multi_band_comb[nr_band_index_1]["nr"]["dl"].append(nr_f_dl)
                    declared_multi_band_comb[nr_band_index_1]["dss"].append(self.dss_support_list[int(nr_f_dl) - 1])

                if nr_multi_band_combs_2:
                    for nr_band_index_2, _ in enumerate(
                            get_start_end(self.FeatureSetsPerBand[nr_multi_band_combs_2[0]:nr_multi_band_combs_2[1]])):
                        nr_f_ul = self.uplinkSetNR.pop(0)
                        nr_f_dl = self.downlinkSetNR.pop(0)
                        declared_multi_band_comb[nr_band_index_2]["nr"]["ul"].append(nr_f_ul)
                        declared_multi_band_comb[nr_band_index_2]["nr"]["dl"].append(nr_f_dl)
                        declared_multi_band_comb[nr_band_index_2]["dss"].append(self.dss_support_list[int(nr_f_dl) - 1])

                self.declared_band_combs.append(declared_multi_band_comb)

                self.FeatureSetsPerBand = self.FeatureSetsPerBand[band_comb_len * 2:]

        return

    def get_band_combinations(self):
        initiate_band_combination_values(self, self.NR_items)
        self.create_feature_set_details()
        self.get_dss_support_list()
        self.prepare_band_declared_feature_set()

        # TODO: NEED TO HANDLE FR2 FEATURE SETS
        bandParameters_NR_LTE = get_start_end(self.bandParameters_NR_LTE)

        nr_lte_bands = dict()
        nr_lte_bands["lte"] = [b for b in bandParameters_NR_LTE if bandParameters_NR_LTE.index(b) % 2 == 0]
        nr_lte_bands["nr"] = [b for b in bandParameters_NR_LTE if bandParameters_NR_LTE.index(b) % 2 == 1]

        lte_bands_combs = []
        nr_bands_combs = []
        lte_counter = 0
        nr_counter = 0
        band_comb_counter = 0

        # print(self.featureSetPerCC_ListDL_LTE)
        for lte_bands, nr_bands in zip(nr_lte_bands["lte"], nr_lte_bands["nr"]):
            lte_bands_combs.append(self.bandEUTRA_list[lte_counter:lte_counter + get_length(lte_bands)])
            nr_bands_combs.append(self.bandNR_list[nr_counter:nr_counter + get_length(nr_bands)])

            feature_set = self.declared_band_combs[int(self.featureSetCombination[band_comb_counter])]
            for f in feature_set:
                new_feature_set = deepcopy(f)
                for lte_downlink_index, lte_downlink in enumerate(f["lte"]["dl"]):
                    new_feature_set["lte"]["dl"][lte_downlink_index] = \
                        self.featureSetPerCC_ListDL_LTE[int(lte_downlink) - 1]
                for nr_downlink_index, nr_downlink in enumerate(f["nr"]["dl"]):
                    new_feature_set["nr"]["dl"][nr_downlink_index] = self.FeatureSetDownlink_NR[int(nr_downlink) - 1]
                for nr_uplink_index, nr_uplink in enumerate(f["nr"]["ul"]):
                    if int(nr_uplink) == 0:
                        new_feature_set["nr"]["ul"][nr_uplink_index] = ["0"]
                    else:
                        new_feature_set["nr"]["ul"][nr_uplink_index] = self.FeatureSetUplink_NR[int(nr_uplink) - 1]
                self.band_combinations.append({
                    "lte": {
                        "bands": self.bandEUTRA_list[lte_counter:lte_counter + get_length(lte_bands)],
                        "bandwidthClass": {
                            "dl": self.ca_BandwidthClassDL_EUTRA[lte_counter:lte_counter + get_length(lte_bands)],
                            "ul": [self.ca_BandwidthClassUL_EUTRA[band_comb_counter]]
                        }
                    },
                    "nr": {
                        "bands": self.bandNR_list[nr_counter:nr_counter + get_length(nr_bands)],
                        "bandwidthClass": {
                            "dl": self.ca_BandwidthClassDL_NR[nr_counter:nr_counter + get_length(nr_bands)],
                            "ul": [self.ca_BandwidthClassUL_NR[band_comb_counter]]
                        }
                    },
                    "featureSetCombination": new_feature_set
                })
            lte_counter += get_length(lte_bands)
            nr_counter += get_length(nr_bands)
            band_comb_counter += 1
        # for i in self.band_combinations:
        #     print(i)

    def band_combinations_table(self):

        band_comb_num = "A"
        dl_combination = "B"
        ul_combination = "C"
        dl_bandwidth = "D"
        lte_dl_layers = "E"
        lte_dl_carriers = "F"
        nr_dl_carriers = "G"
        nr_ul_carriers = "H"
        nr_ul_modulation = "I"
        nr_ul_bandwidth = "J"
        nr_dl_modulation = "K"
        dss_support = "L"

        nr_band = "N"
        supported_bandwidth = "O"
        power_class = "P"
        dss_support_per_band = "Q"

        offset = 2
        data = dict()
        for b_c_index, b_c in enumerate(self.band_combinations):
            data["{}{}".format(band_comb_num, b_c_index + offset)] = b_c_index + 1
            data["{}{}".format(dl_combination, b_c_index + offset)] = get_bands_NR_dl(b_c)
            data["{}{}".format(ul_combination, b_c_index + offset)] = get_bands_NR_ul(b_c)
            data["{}{}".format(dl_bandwidth, b_c_index + offset)] = get_bw_NR_dl(b_c)
            data["{}{}".format(lte_dl_layers, b_c_index + offset)] = get_lte_dl_layers(b_c)
            data["{}{}".format(lte_dl_carriers, b_c_index + offset)] = get_carriers_num(b_c, "lte", "dl")
            data["{}{}".format(nr_dl_carriers, b_c_index + offset)] = get_carriers_num(b_c, "nr", "dl")
            data["{}{}".format(nr_ul_carriers, b_c_index + offset)] = get_carriers_num(b_c, "nr", "ul")
            data["{}{}".format(nr_ul_modulation, b_c_index + offset)] = get_NR_modulation_ul(b_c)
            data["{}{}".format(nr_ul_bandwidth, b_c_index + offset)] = get_bw_NR_ul(b_c)
            data["{}{}".format(nr_dl_modulation, b_c_index + offset)] = get_NR_modulation_dl(b_c)
            data["{}{}".format(dss_support, b_c_index + offset)] = get_dss_support_status(b_c)

        for band_info_index, band_info in enumerate(self.NR_bands):
            data["{}{}".format(nr_band, band_info_index + offset)] = band_info["NR Band"]
            data["{}{}".format(supported_bandwidth, band_info_index + offset)] = \
                convert_bw_to_excel_ready(band_info["supportedBW"])
            data["{}{}".format(power_class, band_info_index + offset)] = band_info["ue-PowerClass"]
            data["{}{}".format(dss_support_per_band, band_info_index + offset)] = band_info["rateMatchingLTE-CRS"]

        return data
