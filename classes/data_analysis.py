from Specsheet_Automation.helpers.data_analysis_helpers import get_start_end, get_bands, calculate_num_of_carriers, \
    calculate_num_of_layers
from Specsheet_Automation.static_data.specsheet_fields import convert_hex_to_binary
from Specsheet_Automation.static_data.configuration import mimo_mapping, class_mapping, string_mimo_mapping

class DataAnalysis:
    def __init__(self, ie_list):
        self.list_items = ie_list
        self.processors = {
                "rf-Parameters,supportedBandListEUTRA": self.supportedBandListEUTRA,
                "measParameters,interFreqNeedForGaps supported on all LTE Bands":
                self.release_8_interFreqNeedForGaps,
                "measParameters,interRAT-NeedForGaps supported on all GSM and WCDMA bands":
                self.release_8_interRatNeedForGaps,
                "interRAT-Parameters,utraFDD": self.utraFDD,
                "interRAT-Parameters,geran": self.geran,
                "rf-Parameters-v1020,supportedBandCombination-r10 and ca-BandwidthClassDL-r10": self.release_1020_DL,
                "ca-BandwidthClassUL-r10 on all supported CA combinations": self.release_1020_UL,
                "supportedMIMO-CapabilityDL-r10 on all Supported CA combinations": self.release_1020_layers,
                "interFreqNeedForGaps supported on all supported LTE Bandcombinations":
                self.release_1020_interFreqNeedForGaps,
                "interRAT-NeedForGaps supported on all supported LTE Bandcombinations":
                self.release_1020_interRatNeedForGaps,
                "rf-Parameters-v1250,dl-256QAM": self.release_1250_dl_256QAM,
                "rf-Parameters-v1250,ul-64QAM": self.release_1250_ul_64QAM,
                "rf-Parameters-v1430,ul-256QAM": self.release_1430_ul_256QAM


        }
        self.band_combinations = []
        self.supportedBandCombination_r10 = None
        self.BandCombinationParameters_r10 = None
        self.bandEUTRA_r10 = None
        self.bandParametersUL_r10 = None
        self.ca_BandwidthClassUL_r10 = None
        self.bandParametersDL_r10 = None
        self.ca_BandwidthClassDL_r10 = None
        self.supportedMIMO_CapabilityDL_r10 = None
        self.supportedMIMO_CapabilityDL_r10 = None
        self.supportedBandCombinationExt_r10 = None
        self.supportedBandwidthCombinationSet_r10 = None

        self.supportedBandCombinationAdd_r11 = None
        self.bandParameterList_r11 = None
        self.bandEUTRA_r11 = None
        self.bandParametersUL_r11 = None
        self.ca_BandwidthClassUL_r10_r11 = None
        self.bandParametersDL_r11 = None
        self.ca_BandwidthClassDL_r10_r11 = None
        self.supportedMIMO_CapabilityDL_r10_r11 = None
        self.interFreqBandList_r11 = None
        self.interFreqNeedForGaps_r11 = None
        self.interRAT_BandList_r11 = None
        # self.interRAT_NeedForGaps_r11 = None
        self.supportedBandwidthCombinationSet_r11 = None
        self.multipleTimingAdvance_r11 = None

    def supportedBandListEUTRA(self):
        return self.list_items["release_8,rf-Parameters,supportedBandListEUTRA,SupportedBandEUTRA,bandEUTRA"]

    def release_8_interFreqNeedForGaps(self):
        try:
            interFreqNeedForGaps = self.list_items["release_8,measParameters,bandListEUTRA,BandInfoEUTRA,"
                                                   "interFreqBandList,InterFreqBandInfo,interFreqNeedForGaps"]
        except KeyError:
            return "No Information"
        for i in interFreqNeedForGaps:
            if i != "1":
                return "FALSE"
        return "TRUE"

    def release_8_interRatNeedForGaps(self):
        try:
            interRatNeedForGaps = self.list_items["release_8,measParameters,bandListEUTRA,"
                                                  "BandInfoEUTRA,interRAT-BandList,"
                                                  "InterRAT-BandInfo,interRAT-NeedForGaps"]
        except KeyError:
            return "No Information"
        for i in interRatNeedForGaps:
            if i != "1":
                return "FALSE"
        return "TRUE"

    def utraFDD(self):
        utraFDD_bands = ["bandI", "bandII", "bandIII", "bandIV", "bandV", "bandVI", "bandVII", "bandVIII", "bandIX",
                         "bandX", "bandXI", "bandXII", "bandXIII", "bandXIV", "bandXV", "bandXVI", "...", "bandXVII-8a0",
                         "bandXVIII-8a0", "bandXIX-8a0", "bandXX-8a0", "bandXXI-8a0", "bandXXII-8a0", "bandXXIII-8a0",
                         "bandXXIV-8a0", "bandXXV-8a0", "bandXXVI-8a0", "bandXXVII-8a0", "bandXXVIII-8a0",
                         "bandXXIX-8a0", "bandXXX-8a0", "bandXXXI-8a0", "bandXXXII-8a0"]
        try:
            mapped_bands = [utraFDD_bands[int(band)] for band in
                            self.list_items[
                                "release_8,interRAT-Parameters,utraFDD,supportedBandListUTRA-FDD,SupportedBandUTRA-FDD"]]
        except KeyError:
            return ["UTRAN not supported"]
        return mapped_bands

    def geran(self):
        geran_bands = ["gsm450", "gsm480", "gsm710", "gsm750", "gsm810", "gsm850", "gsm900P", "gsm900E", "gsm900R",
                       "gsm1800", "gsm1900"]
        try:
            mapped_bands = [
                geran_bands[int(band)] for band in
                self.list_items["release_8,interRAT-Parameters,geran,supportedBandListGERAN,SupportedBandGERAN"]
                ]
            return mapped_bands
        except KeyError:
            return ["Geran not supported"]

    def get_r10_band_combinations(self):
        try:
            # print(self.list_items[
            #     "release_1020,rf-Parameters-v1020,supportedBandCombinatiodn-r10"])
            self.supportedBandCombination_r10 = self.list_items[
                "release_1020,rf-Parameters-v1020,supportedBandCombination-r10"]
            self.BandCombinationParameters_r10 = self.list_items[
                "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10"]
            self.bandEUTRA_r10 = self.list_items[
                "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
                "BandParameters-r10,bandEUTRA-r10"]
            self.bandParametersUL_r10 = self.list_items[
                "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,"
                "BandCombinationParameters-r10,BandParameters-r10,bandParametersUL-r10"]
            self.ca_BandwidthClassUL_r10 = self.list_items[
                "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
                "BandParameters-r10,bandParametersUL-r10,CA-MIMO-ParametersUL-r10,ca-BandwidthClassUL-r10"]
            self.bandParametersDL_r10 = self.list_items[
                "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
                "BandParameters-r10,bandParametersDL-r10"]
            self.ca_BandwidthClassDL_r10 = self.list_items[
                "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
                "BandParameters-r10,bandParametersDL-r10,CA-MIMO-ParametersDL-r10,ca-BandwidthClassDL-r10"]
            self.supportedMIMO_CapabilityDL_r10 = self.list_items[
                "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,"
                "BandParameters-r10,bandParametersDL-r10,CA-MIMO-ParametersDL-r10,supportedMIMO-CapabilityDL-r10"]
            self.supportedBandCombinationExt_r10 = self.list_items[
                "release_1060,rf-Parameters-v1060,supportedBandCombinationExt-r10"]
            self.supportedBandwidthCombinationSet_r10 = self.list_items[
                "release_1060,rf-Parameters-v1060,supportedBandCombinationExt-r10,BandCombinationParametersExt-r10,"
                "supportedBandwidthCombinationSet-r10"]

        except KeyError:
            return False

        band_combs_r10 = get_start_end(self.supportedBandCombination_r10)
        ul_counter = 0
        dl_counter = 0
        band_comb_counter = 0
        for bc in band_combs_r10:
            bands_r10 = self.BandCombinationParameters_r10[bc[0]:bc[1]]
            one_band_r10 = get_start_end(bands_r10)
            new_comb = {"ul": [], "dl": [], "bcs": ""}
            for ob in one_band_r10:
                if (ob[1] - ob[0]) % 2 == 0:
                    new_comb["ul"].append({"band": self.bandEUTRA_r10[dl_counter],
                                           "class": self.ca_BandwidthClassUL_r10[ul_counter]})

                    ul_counter += 1
                new_comb["dl"].append({"band": self.bandEUTRA_r10[dl_counter],
                                       "class": self.ca_BandwidthClassDL_r10[dl_counter],
                                       "mimo": self.supportedMIMO_CapabilityDL_r10[dl_counter]})

                bcs = "default" if str(band_comb_counter) not in self.supportedBandCombinationExt_r10 else \
                    self.supportedBandwidthCombinationSet_r10[self.supportedBandCombinationExt_r10.
                                                              index(str(band_comb_counter))]
                new_comb["bcs"] = bcs
                dl_counter += 1
            band_comb_counter += 1
            self.band_combinations.append(new_comb)
        # for index, i in enumerate(self.band_combinations):
        #     print(index, i)

    def get_r11_band_combinations(self,):

        try:
            self.supportedBandCombinationAdd_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11"]
            self.bandParameterList_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandParameterList-r11"]
            self.bandEUTRA_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandParameterList-r11,BandParameters-r11,bandEUTRA-r11"]
            self.bandParametersUL_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandParameterList-r11,BandParameters-r11,bandParametersUL-r11"]
            self.ca_BandwidthClassUL_r10_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandParameterList-r11,BandParameters-r11,bandParametersUL-r11,CA-MIMO-ParametersUL-r10,"
                "ca-BandwidthClassUL-r10"]
            self.bandParametersDL_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandParameterList-r11,BandParameters-r11,bandParametersDL-r11"]
            self.ca_BandwidthClassDL_r10_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandParameterList-r11,BandParameters-r11,bandParametersDL-r11,CA-MIMO-ParametersDL-r10,"
                "ca-BandwidthClassDL-r10"]
            self.supportedMIMO_CapabilityDL_r10_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandParameterList-r11,BandParameters-r11,bandParametersDL-r11,CA-MIMO-ParametersDL-r10,"
                "supportedMIMO-CapabilityDL-r10"]
        except KeyError:
            pass
        try:
            self.interFreqBandList_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandInfoEUTRA-r11,interFreqBandList"]
        except KeyError:
            pass
        try:
            self.interFreqNeedForGaps_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandInfoEUTRA-r11,interFreqBandList,InterFreqBandInfo,interFreqNeedForGaps"]
        except KeyError:
            pass
        try:
            self.supportedBandwidthCombinationSet_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "supportedBandwidthCombinationSet-r11"]
        except KeyError:
            self.supportedBandwidthCombinationSet_r11 = []
            pass
        try:
            self.multipleTimingAdvance_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "multipleTimingAdvance-r11"]
        except KeyError:
            pass
        try:
            self.interRAT_BandList_r11 = self.list_items[
                "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
                "bandInfoEUTRA-r11,interRAT-BandList"]
        except KeyError as e:
            pass

        inter_freq_r11 = get_start_end(self.interFreqBandList_r11, "<") if self.interFreqBandList_r11 else None
        inter_rat_r11 = get_start_end(self.interRAT_BandList_r11, "<") if self.interRAT_BandList_r11 else None
        band_combinations_r11 = get_start_end(self.supportedBandCombinationAdd_r11) \
            if self.supportedBandCombinationAdd_r11 else None
        all_band_combinations = []

        def get_length(item):
            return int(item[1]) - int(item[0]) if item.__len__() > 0 else 0
        start = 0
        if not band_combinations_r11:
            return
        inter_rat_r11 = inter_rat_r11 if inter_rat_r11 else [[]]*band_combinations_r11.__len__()
        inter_freq_r11 = inter_freq_r11 if inter_freq_r11 else [[]]*band_combinations_r11.__len__()

        for bc_r11, interf_r11, interr_r11 in zip(band_combinations_r11, inter_freq_r11, inter_rat_r11):
            bcs = "default"
            end = start + get_length(bc_r11) - get_length(interf_r11) - get_length(interr_r11)
            band_combs = get_start_end(self.bandParameterList_r11[start:end])

            # TODO: Check if "get_length(band_combs[0]) != 5" below is actually required
            if get_length(band_combs[-1]) == 1 and get_length(band_combs[0]) != 5:
                start = end - 1
                band_combs = band_combs[:-1]
                # This checks if there is uplink CA in which case it assumes the extra number is
                # multipleTimingAdvance_r11
                length_check = [True for b in band_combs if get_length(b) == 4]
                if length_check.__len__() < 2:
                    bcs = self.supportedBandwidthCombinationSet_r11.pop(0)
            elif get_length(band_combs[-1]) == 2:
                # This assumes that multipleTimingAdvance_r11 and supportedBandwidthCombinationSet_r11 are there
                start = end - 2
                band_combs = band_combs[:-1]
                bcs = self.supportedBandwidthCombinationSet_r11.pop(0)
            elif band_combs.__len__() == 1 and get_length(band_combs[0]) == 5:
                band_combs = get_start_end(self.bandParameterList_r11[start:end - 1])
                start = end - 1
                bcs = self.supportedBandwidthCombinationSet_r11.pop(0)
            else:
                start = end
            all_band_combinations.append({"band_combs": band_combs, "bcs": bcs})
        if self.supportedBandwidthCombinationSet_r11.__len__() > 0:
            all_band_combinations[-1]["bcs"] = self.supportedBandwidthCombinationSet_r11.pop(0)
        print( self.supportedBandwidthCombinationSet_r11)

        ul_counter = 0
        dl_counter = 0
        for bc in all_band_combinations:
            new_comb = {"ul": [], "dl": [], "bcs": bc["bcs"]}

            for ob in bc["band_combs"]:
                if (ob[1] - ob[0]) % 2 == 0:
                    # noinspection PyTypeChecker
                    new_comb["ul"].append({"band": self.bandEUTRA_r11[dl_counter],
                                           "class": self.ca_BandwidthClassUL_r10_r11[ul_counter]})

                    ul_counter += 1
                # noinspection PyTypeChecker
                new_comb["dl"].append({"band": self.bandEUTRA_r11[dl_counter],
                                       "class": self.ca_BandwidthClassDL_r10_r11[dl_counter],
                                       "mimo": self.supportedMIMO_CapabilityDL_r10_r11[dl_counter]})
                dl_counter += 1
            # print(new_comb)
            self.band_combinations.append(new_comb)

    def band_combinations_table(self):
        # for i in self.band_combinations:
        #     print(i)
        lte_bands = "B1"
        dl_cat = "B2"
        ul_cat = "B3"
        band_comb_num = "A"
        band_comb = "B"
        uplink_band = "C"
        BCS = "D"
        dl_carriers = "E"
        ul_carriers = "F"
        dl_layers = "G"
        row_offset = 6

        data = {lte_bands: ",".join(self.supportedBandListEUTRA())}
        all_categories = self.get_all_categories()
        data[dl_cat] = ",".join(all_categories["dl"])
        data[ul_cat] = ",".join(all_categories["ul"])

        for b_c_index, b_c in enumerate(self.band_combinations):
            data["{}{}".format(band_comb_num, b_c_index + row_offset)] = b_c_index + 1
            data["{}{}".format(band_comb, b_c_index + row_offset)] = get_bands(b_c["dl"])
            data["{}{}".format(uplink_band, b_c_index + row_offset)] = get_bands(b_c["ul"])
            data["{}{}".format(BCS, b_c_index + row_offset)] = "Default" if b_c["bcs"] == "default" else \
                convert_hex_to_binary(b_c["bcs"][:2], min_zeros=4)
            data["{}{}".format(dl_carriers, b_c_index + row_offset)] = calculate_num_of_carriers(b_c["dl"])
            data["{}{}".format(ul_carriers, b_c_index + row_offset)] = calculate_num_of_carriers(b_c["ul"])
            data["{}{}".format(dl_layers, b_c_index + row_offset)] = calculate_num_of_layers(b_c["dl"])
        return data

    def band_combinations_list(self):
        data = []
        for b_c_index, b_c in enumerate(self.band_combinations):
            data_item = {"bcs": "Default" if b_c["bcs"] == "default" else
                         convert_hex_to_binary(b_c["bcs"][:2], min_zeros=4)}
            ul_list = []
            dl_list = []
            for dl in b_c["dl"]:
                dl_list.append("{}{}({})".format(dl["band"], class_mapping[dl["class"]], mimo_mapping[int(dl["mimo"])]))
            for ul in b_c["ul"]:
                ul_list.append("{}{}".format(ul["band"], class_mapping[ul["class"]]))
            data_item["ulBands"] = ul_list
            data_item["dlBands"] = dl_list
            data_item["dlCarriers"] = calculate_num_of_carriers(b_c["dl"])
            data_item["ulCarriers"] = calculate_num_of_carriers(b_c["ul"])
            data_item["dlLayers"] = calculate_num_of_layers(b_c["dl"])

            data.append(data_item)
        return data

    def get_all_categories(self):
        categories = {
            "dl": [],
            "ul": []
        }
        for element in self.list_items:
            if "Category" in element:
                if isinstance(element, list):
                    element = element[0]
                if "UL" in element:
                    categories["ul"].append(self.list_items[element])
                else:
                    categories["dl"].append(self.list_items[element])
        return categories

    def get_release_class_mimo(self, ul_dl):
        classes = []
        mimo = []
        for band in self.band_combinations:
            for band_dl in band[ul_dl]:
                if class_mapping[band_dl["class"]] not in classes:
                    classes.append(class_mapping[band_dl["class"]])
                if "mimo" in list(band_dl.keys()) and string_mimo_mapping[int(band_dl["mimo"])] not in mimo:
                    mimo.append(string_mimo_mapping[int(band_dl["mimo"])])
        return classes, mimo

    def release_1020_DL(self):
        return self.get_release_class_mimo("dl")[0]

    def release_1020_UL(self):
        return self.get_release_class_mimo("ul")[0]

    def release_1020_layers(self):
        return self.get_release_class_mimo("dl")[1]

    def release_1020_interFreqNeedForGaps(self):
        try:
            interFreqNeedForGaps = self.list_items["release_1020,measParameters-v1020,bandCombinationListEUTRA-r10,"
                                                   "BandInfoEUTRA,interFreqBandList,"
                                                   "InterFreqBandInfo,interFreqNeedForGaps"]
            for i in interFreqNeedForGaps:
                if i != "1":
                    return "FALSE"
            return "TRUE"
        except KeyError:
            return "No Information"

    def release_1020_interRatNeedForGaps(self):
        try:
            interRatNeedForGaps = self.list_items["release_1020,measParameters-v1020,bandCombinationListEUTRA-r10,"
                                                  "BandInfoEUTRA,interRAT-BandList,"
                                                  "InterRAT-BandInfo,interRAT-NeedForGaps"]
            for i in interRatNeedForGaps:
                if i != "1":
                    return "FALSE"
            return "TRUE"
        except KeyError:
            return "No Information"

    def release_1250_dl_256QAM(self):
        try:
            dl_256QAM = self.list_items["release_1250,rf-Parameters-v1250,supportedBandListEUTRA-v1250,"
                                        "SupportedBandEUTRA-v1250,dl-256QAM-r12"]
            for i in dl_256QAM:
                if i != "0":
                    return "Not Supported"
            return "Supported"
        except KeyError:
            return "No Information"

    def release_1250_ul_64QAM(self):
        try:
            ul_64QAM = self.list_items["release_1250,rf-Parameters-v1250,supportedBandListEUTRA-v1250,"
                                       "SupportedBandEUTRA-v1250,ul-64QAM-r12"]
            for i in ul_64QAM:
                if i != "0":
                    return "Not Supported"
            return "Supported"
        except KeyError:
            return "No Information"

    def release_1430_ul_256QAM(self):
        try:
            ul_256QAM = self.list_items["release_1430,rf-Parameters-v1430,supportedBandCombination-v1430,"
                                        "bandParameterList-v1430,BandParameters-v1430,ul-256QAM-r14"]
            for i in ul_256QAM:
                if i != "0":
                    return "Not Supported"
            return "Supported"
        except KeyError:
            return "No Information"
