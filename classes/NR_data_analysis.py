from Specsheet_Automation.helpers.data_analysis_helpers import get_start_end, get_bands, calculate_num_of_carriers, \
    calculate_num_of_layers, get_length
from Specsheet_Automation.helpers.NR_data_analysis_helpers import map_fr_bw_num_to_value, map_modulation_num_to_value, \
    map_mimo_num_to_value_ul, map_mimo_num_to_value_dl, initiate_feature_set_values, initiate_band_combination_values
from Specsheet_Automation.static_data.LTE_specsheet_fields import convert_hex_to_binary
from Specsheet_Automation.static_data.configuration import mimo_mapping, class_mapping, string_mimo_mapping

class NRDataAnalysis:
    def __init__(self, NR_ie_list, LTE_ie_list, NR_special_ie_list):
        self.NR_items = NR_ie_list
        self.LTE_items = LTE_ie_list
        self.NR_special_ie_list = NR_special_ie_list

        self.processors = {
            "Supported NR Band": self.supportedNRBand,
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
        self.supportedMIMO_CapabilityUL_MRDC_r15 = None

        # declared NR IEs
        self.band_combinations = []
        self.bandParameters = None
        self.bandParameters_NR_LTE = None
        self.supportedBandCombinationList = None
        self.bandList = None
        self.bandEUTRA_list = None
        self.bandNR_list = None
        self.ca_BandwidthClassDL_EUTRA = None
        self.ca_BandwidthClassDL_NR = None
        self.ca_BandwidthClassUL_NR = None
        self.featureSetCombination_used = None
        self.featureSetCombination_declared = None
        self.FeatureSetsPerBand = None
        self.FeatureSet = None
        self.downlinkSetEUTRA = None
        self.uplinkSetEUTRA = None
        self.downlinkSetNR = None
        self.uplinkSetNR = None

    def supportedNRBand(self):
        return ",".join(self.NR_items["release_15,rf-Parameters,supportedBandListNR,BandNR,bandNR"])

    def create_feature_set_details(self):
        initiate_feature_set_values(self, self.NR_items, self.NR_special_ie_list, self.LTE_items)

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
                "maxNumberMIMO_LayersPDSCH": map_mimo_num_to_value_dl(self.maxNumberMIMO_LayersPDSCH[b_dl_index]),
                "supportedModulationOrderDL": map_modulation_num_to_value(self.supportedModulationOrderDL[b_dl_index])
            })
        # for i in nr_featureSetDownlinkPerCC:
        #     print(i)

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
                "maxNumberMIMO_LayersCB_PUSCH": map_mimo_num_to_value_ul(self.maxNumberMIMO_LayersCB_PUSCH[b_ul_index]),
                "supportedModulationOrderUL": map_modulation_num_to_value(self.supportedModulationOrderUL[b_ul_index])
            })
        for i in nr_featureSetUplinkPerCC:
            print(i)

        FeatureSetDownlink = []
        # print(get_start_end(self.featureSetListPerDownlinkCC, "<="))

        return
    def get_band_combinations(self):

        # TODO: NEED TO HANDLE FR2 FEATURE SETS
        initiate_band_combination_values(self, self.NR_items, self.NR_special_ie_list)
        bandParameters_NR_LTE = get_start_end(self.bandParameters_NR_LTE)

        nr_lte_bands = dict()
        nr_lte_bands["lte"] = [b for b in bandParameters_NR_LTE if bandParameters_NR_LTE.index(b) % 2 == 0]
        nr_lte_bands["nr"] = [b for b in bandParameters_NR_LTE if bandParameters_NR_LTE.index(b) % 2 == 1]

        lte_bands_combs = []
        nr_bands_combs = []
        lte_counter = 0
        nr_counter = 0
        for lte_bands in nr_lte_bands["lte"]:
            lte_bands_combs.append(self.bandEUTRA_list[lte_counter:lte_counter + get_length(lte_bands)])
            lte_counter += get_length(lte_bands)
        for nr_bands in nr_lte_bands["nr"]:
            nr_bands_combs.append(self.bandNR_list[nr_counter:nr_counter + get_length(nr_bands)])
            nr_counter += get_length(nr_bands)
        print(lte_bands_combs, len(lte_bands_combs))
        print(nr_bands_combs, len(nr_bands_combs))


        return
