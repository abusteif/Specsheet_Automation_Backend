def convert_hex_to_binary(hex_num, min_zeros=32):
    hex_num = hex_num.replace(":", "")
    return bin(int(hex_num, 16))[2:].zfill(min_zeros)

def supportedBandListEUTRA(band_list):
    return ",".join(band_list)

def utraFDD_geran(bands):
    return ",\n".join(bands)

def classes_mimo(class_mimo):
    return ", ".join(class_mimo)


jira_test_step_order_to_field_mapping = {
    "release_8,accessStratumRelease": 0,
    "release_8,ue-Category": 1,
    "release_8,pdcp-Parameters,supportedROHC-Profiles,profile0x0001-r15": 2,
    "release_8,pdcp-Parameters,supportedROHC-Profiles,profile0x0002-r15": 3,
    "release_8,pdcp-Parameters,supportedROHC-Profiles,profile0x0003-r15": 4,
    "release_8,pdcp-Parameters,supportedROHC-Profiles,profile0x0004-r15": 5,
    "release_8,pdcp-Parameters,supportedROHC-Profiles,profile0x0006-r15": 6,
    "release_8,pdcp-Parameters,supportedROHC-Profiles,profile0x0101-r15": 7,
    "release_8,pdcp-Parameters,supportedROHC-Profiles,profile0x0102-r15": 8,
    "release_8,pdcp-Parameters,supportedROHC-Profiles,profile0x0103-r15": 9,
    "release_8,pdcp-Parameters,supportedROHC-Profiles,profile0x0104-r15": 10,
    "release_8,pdcp-Parameters,maxNumberROHC-ContextSessions": 11,
    "release_8,phyLayerParameters,ue-TxAntennaSelectionSupported": 12,
    "release_8,phyLayerParameters,ue-SpecificRefSigsSupported": 13,
    "release_8,featureGroupIndicators": 14,
    "release_8,interRAT-Parameters,geran,interRAT-PS-HO-ToGERAN": 15,
    "release_9a0,featureGroupIndRel9Add-r9": 20,
    "release_9a0,fdd-Add-UE-EUTRA-Capabilities-r9,phyLayerParameters-r9,ue-TxAntennaSelectionSupported": 21,
    "release_9a0,fdd-Add-UE-EUTRA-Capabilities-r9,phyLayerParameters-r9,ue-SpecificRefSigsSupported": 22,
    "release_9a0,fdd-Add-UE-EUTRA-Capabilities-r9,featureGroupIndicators-r9": 23,
    "release_9a0,fdd-Add-UE-EUTRA-Capabilities-r9,featureGroupIndRel9Add-r9": 24,
    "release_9a0,tdd-Add-UE-EUTRA-Capabilities-r9,phyLayerParameters-r9,ue-TxAntennaSelectionSupported": 32,
    "release_9a0,tdd-Add-UE-EUTRA-Capabilities-r9,phyLayerParameters-r9,ue-SpecificRefSigsSupported": 33,
    "release_9a0,tdd-Add-UE-EUTRA-Capabilities-r9,featureGroupIndicators-r9": 34,
    "release_9a0,tdd-Add-UE-EUTRA-Capabilities-r9,featureGroupIndRel9Add-r9": 35,
    "release_920,phyLayerParameters-v920,enhancedDualLayerFDD-r9": 79,
    "release_920,phyLayerParameters-v920,enhancedDualLayerTDD-r9": 80,
    "release_920,interRAT-ParametersGERAN-v920,dtm-r9": 81,
    "release_920,interRAT-ParametersGERAN-v920,e-RedirectionGERAN-r9": 82,
    "release_920,interRAT-ParametersUTRA-v920,e-RedirectionUTRA-r9": 83,
    "release_920,csg-ProximityIndicationParameters-r9,intraFreqProximityIndication-r9": 87,
    "release_920,csg-ProximityIndicationParameters-r9,interFreqProximityIndication-r9": 88,
    "release_920,csg-ProximityIndicationParameters-r9,utran-ProximityIndication-r9": 89,
    "release_920,neighCellSI-AcquisitionParameters-r9,intraFreqSI-AcquisitionForHO-r9": 90,
    "release_920,neighCellSI-AcquisitionParameters-r9,interFreqSI-AcquisitionForHO-r9": 91,
    "release_920,neighCellSI-AcquisitionParameters-r9,utran-SI-AcquisitionForHO-r9": 92,
    "release_920,son-Parameters-r9,rach-Report-r9": 93,
    "release_1020,ue-Category-v1020": 94,
    "release_1020,featureGroupIndRel10-r10": 101,
    "release_1020,ue-BasedNetwPerfMeasParameters-r10,loggedMeasurementsIdle-r10": 103,
    "release_1020,ue-BasedNetwPerfMeasParameters-r10,standaloneGNSS-Location-r10": 104,
    "release_1060,fdd-Add-UE-EUTRA-Capabilities-v1060,featureGroupIndRel10-v1060": 112,
    "release_1060,tdd-Add-UE-EUTRA-Capabilities-v1060,featureGroupIndRel10-v1060": 123,
    "release_1130,pdcp-Parameters-v1130,pdcp-SN-Extension-r11": 128,
    "release_1130,pdcp-Parameters-v1130,supportRohcContextContinue-r11": 129,
    "release_1130,phyLayerParameters-v1130,multiACK-CSI-Reporting-r11": 132,
    "release_1130,phyLayerParameters-v1130,ss-CCH-InterfHandl-r11": 133,
    "release_1130,phyLayerParameters-v1130,tdd-SpecialSubframe-r11": 134,
    "release_1280,phyLayerParameters-v1280,alternativeTBS-Indices-r12": 250,
    "release_1430,phyLayerParameters-v1430,alternativeTBS-Index-r14": 456,
    "release_1310,pdcp-Parameters-v1310,pdcp-SN-Extension-18bits-r13": 253,
    "release_1170,ue-Category-v1170": 165,
    "release_11a0,ue-Category-v11a0": 173,
    "release_1250,ue-CategoryDL-r12": 188,
    "release_1250,ue-CategoryUL-r12": 189,
    "release_1260,ue-CategoryDL-v1260": 249,
    "release_1330,ue-CategoryDL-v1330": 410,
    "release_1430,ue-CategoryUL-v1430": 460,
    "release_1460,ue-CategoryDL-v1460": 606,
    "release_8,rf-Parameters,supportedBandListEUTRA,SupportedBandEUTRA,bandEUTRA": 1390,
    "release_8,measParameters,bandListEUTRA,BandInfoEUTRA,interFreqBandList,InterFreqBandInfo,interFreqNeedForGaps":
        1394,
    "release_8,measParameters,bandListEUTRA,BandInfoEUTRA,interRAT-BandList,InterRAT-BandInfo,interRAT-NeedForGaps":
        1396,
    "release_8,interRAT-Parameters,utraFDD,supportedBandListUTRA-FDD,SupportedBandUTRA-FDD": 1398,
    "release_8,interRAT-Parameters,geran,supportedBandListGERAN,SupportedBandGERAN": 1406,
    "release_1020,rf-Parameters-v1020,supportedBandCombination-r10": 1475,
    "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10": 1476,
    "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,BandParameters-r10,"
    "bandEUTRA-r10": 1477,
    "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,BandParameters-r10,"
    "bandParametersUL-r10": 1478,
    "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,BandParameters-r10,"
    "bandParametersUL-r10,CA-MIMO-ParametersUL-r10,ca-BandwidthClassUL-r10": 1479,
    "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,BandParameters-r10,"
    "bandParametersDL-r10": 1481,
    "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,BandParameters-r10,"
    "bandParametersDL-r10,CA-MIMO-ParametersDL-r10,ca-BandwidthClassDL-r10": 1482,
    "release_1020,rf-Parameters-v1020,supportedBandCombination-r10,BandCombinationParameters-r10,BandParameters-r10,"
    "bandParametersDL-r10,CA-MIMO-ParametersDL-r10,supportedMIMO-CapabilityDL-r10": 1483,
    "release_1060,rf-Parameters-v1060,supportedBandCombinationExt-r10": 1493,
    "release_1060,rf-Parameters-v1060,supportedBandCombinationExt-r10,BandCombinationParametersExt-r10,"
    "supportedBandwidthCombinationSet-r10": 1494,
    "release_1020,measParameters-v1020,bandCombinationListEUTRA-r10,BandInfoEUTRA,interFreqBandList,InterFreqBandInfo,"
    "interFreqNeedForGaps": 1486,
    "release_1020,measParameters-v1020,bandCombinationListEUTRA-r10,BandInfoEUTRA,interRAT-BandList,InterRAT-BandInfo,"
    "interRAT-NeedForGaps": 1488,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11": 1505,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandParameterList-r11": 1506,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandParameterList-r11,BandParameters-r11,bandEUTRA-r11": 1507,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandParameterList-r11,BandParameters-r11,bandParametersUL-r11": 1508,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandParameterList-r11,BandParameters-r11,bandParametersUL-r11,CA-MIMO-ParametersUL-r10,"
    "ca-BandwidthClassUL-r10": 1509,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandParameterList-r11,BandParameters-r11,bandParametersDL-r11": 1511,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandParameterList-r11,BandParameters-r11,bandParametersDL-r11,CA-MIMO-ParametersDL-r10,"
    "ca-BandwidthClassDL-r10": 1512,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandParameterList-r11,BandParameters-r11,bandParametersDL-r11,CA-MIMO-ParametersDL-r10,"
    "supportedMIMO-CapabilityDL-r10": 1513,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandInfoEUTRA-r11,interFreqBandList": 1518,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandInfoEUTRA-r11,interFreqBandList,InterFreqBandInfo,interFreqNeedForGaps": 1519,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandInfoEUTRA-r11,interRAT-BandList": 1520,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "bandInfoEUTRA-r11,interRAT-BandList,InterRAT-BandInfo,interRAT-NeedForGaps": 1521,
    "release_1180,rf-Parameters-v1180,supportedBandCombinationAdd-r11,BandCombinationParameters-r11,"
    "supportedBandwidthCombinationSet-r11": 1515,
    "release_1250,rf-Parameters-v1250,supportedBandListEUTRA-v1250,SupportedBandEUTRA-v1250,dl-256QAM-r12": 1526,
    "release_1250,rf-Parameters-v1250,supportedBandListEUTRA-v1250,SupportedBandEUTRA-v1250,ul-64QAM-r12": 1527,
}


MSR0835_all_UECI_fields = [
    {
        "release": "release_8",
        "path": "accessStratumRelease",
        "cell": "E37",
        "values": ["rel8", "rel9", "rel10", "rel11", "rel12", "rel13", "rel14", "rel15", "rel16"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": "ue-Category",
        "cell": "E38",
        "values": [None, "Cat1", "Cat2", "Cat3", "Cat4", "Cat5"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "supportedROHC-Profiles", "profile0x0001-r15"],
        "cell": "E40",
        "values": ["profile0x0001_r15, FALSE", "profile0x0001_r15 TRUE"],
        "default": "No Information"

    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "supportedROHC-Profiles", "profile0x0002-r15"],
        "cell": "E40",
        "values": ["profile0x0002_r15, FALSE", "profile0x0002_r15 TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "supportedROHC-Profiles", "profile0x0003-r15"],
        "cell": "E40",
        "values": ["profile0x0003_r15, FALSE", "profile0x0003_r15 TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "supportedROHC-Profiles", "profile0x0004-r15"],
        "cell": "E40",
        "values": ["profile0x0004-r15, FALSE", "profile0x0004-r15 TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "supportedROHC-Profiles", "profile0x0006-r15"],
        "cell": "E40",
        "values": ["profile0x0006-r15, FALSE", "profile0x0006-r15 TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "supportedROHC-Profiles", "profile0x0101-r15"],
        "cell": "E40",
        "values": ["profile0x0101-r15, FALSE", "profile0x0101-r15 TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "supportedROHC-Profiles", "profile0x0102-r15"],
        "cell": "E40",
        "values": ["profile0x0102-r15, FALSE", "profile0x0102-r15 TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "supportedROHC-Profiles", "profile0x0103-r15"],
        "cell": "E40",
        "values": ["profile0x0103-r15, FALSE", "profile0x0103-r15 TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "supportedROHC-Profiles", "profile0x0104-r15"],
        "cell": "E40",
        "values": ["profile0x0104-r15, FALSE", "profile0x0104-r15 TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["pdcp-Parameters", "maxNumberROHC-ContextSessions"],
        "cell": "E41",
        "values": ["cs2", "cs4", "cs8", "cs12", "cs16", "cs24", "cs32", "cs48", "cs64", "cs128", "cs256", "cs512",
                   "cs1024", "cs16384"],
        "default": "cs16"
    },
    {
        "release": "release_8",
        "path": ["phyLayerParameters", "ue-TxAntennaSelectionSupported"],
        "cell": "E43",
        "values": ["FALSE", "TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "path": ["phyLayerParameters", "ue-SpecificRefSigsSupported"],
        "cell": "E44",
        "values": ["FALSE", "TRUE"],
        "default": "No Information"
    },
    {
        "release": "release_8",
        "processor": "rf-Parameters,supportedBandListEUTRA",
        "postProcessor": supportedBandListEUTRA,
        "cell": "E46"
    },
    {
        "release": "release_8",
        "processor": "measParameters,interFreqNeedForGaps supported on all LTE Bands",
        "cell": "E48"
    },
    {
        "release": "release_8",
        "processor": "measParameters,interRAT-NeedForGaps supported on all GSM and WCDMA bands",
        "cell": "E49"
    },
    {
        "release": "release_8",
        "path": "featureGroupIndicators",
        "cell": "E50",
        "default": "No Information",
        "func": convert_hex_to_binary
    },
    {
        "release": "release_8",
        "processor": "interRAT-Parameters,utraFDD",
        "postProcessor": utraFDD_geran,
        "cell": "E52"
    },
    {
        "release": "release_8",
        "processor": "interRAT-Parameters,geran",
        "postProcessor": utraFDD_geran,
        "cell": "E53",
        "default": "Geran not supported"
    },
    {
        "release": "release_8",
        "path": ["interRAT-Parameters", "geran", "interRAT-PS-HO-ToGERAN"],
        "cell": "E54",
        "values": ["FALSE", "TRUE"],
        "default": "Geran not supported"

    },
    {
        "release": "release_920",
        "path": ["phyLayerParameters-v920", "enhancedDualLayerFDD-r9"],
        "cell": "E56",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["phyLayerParameters-v920", "enhancedDualLayerTDD-r9"],
        "cell": "E57",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["interRAT-ParametersGERAN-v920", "dtm-r9"],
        "cell": "E59",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["interRAT-ParametersGERAN-v920", "e-RedirectionGERAN-r9"],
        "cell": "E60",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["interRAT-ParametersUTRA-v920", "e-RedirectionUTRA-r9"],
        "cell": "E62",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["csg-ProximityIndicationParameters-r9", "intraFreqProximityIndication-r9"],
        "cell": "E64",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["csg-ProximityIndicationParameters-r9", "interFreqProximityIndication-r9"],
        "cell": "E65",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["csg-ProximityIndicationParameters-r9", "utran-ProximityIndication-r9"],
        "cell": "E66",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["neighCellSI-AcquisitionParameters-r9", "intraFreqSI-AcquisitionForHO-r9"],
        "cell": "E68",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["neighCellSI-AcquisitionParameters-r9", "interFreqSI-AcquisitionForHO-r9"],
        "cell": "E69",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["neighCellSI-AcquisitionParameters-r9", "utran-SI-AcquisitionForHO-r9"],
        "cell": "E70",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_920",
        "path": ["son-Parameters-r9", "rach-Report-r9"],
        "cell": "E72",
        "values": ["Supported", "Not Supported"],
        "default": "No Information"
    },
    {
        "release": "release_9a0",
        "path": "featureGroupIndRel9Add-r9",
        "cell": "E73",
        "default": "No Information",
        "func": convert_hex_to_binary
    },
    {
        "release": "release_9a0",
        "path": ["fdd-Add-UE-EUTRA-Capabilities-r9", "phyLayerParameters-r9", "ue-TxAntennaSelectionSupported"],
        "cell": "E79",
        "values": ["Not Supported", "Supported"],
        "default": "No Information",
    },
    {
        "release": "release_9a0",
        "path": ["fdd-Add-UE-EUTRA-Capabilities-r9", "phyLayerParameters-r9", "ue-SpecificRefSigsSupported"],
        "cell": "E80",
        "values": ["Not Supported", "Supported"],
        "default": "No Information",
    },
    {
        "release": "release_9a0",
        "path": ["fdd-Add-UE-EUTRA-Capabilities-r9", "featureGroupIndicators-r9"],
        "cell": "E81",
        "default": "No Information",
        "func": convert_hex_to_binary
    },
    {
        "release": "release_9a0",
        "path": ["fdd-Add-UE-EUTRA-Capabilities-r9", "featureGroupIndRel9Add-r9"],
        "cell": "E82",
        "default": "No Information",
        "func": convert_hex_to_binary
    },
    {
        "release": "release_9a0",
        "path": ["tdd-Add-UE-EUTRA-Capabilities-r9", "phyLayerParameters-r9", "ue-TxAntennaSelectionSupported"],
        "cell": "E85",
        "values": ["Not Supported", "Supported"],
        "default": "No Information",
    },
    {
        "release": "release_9a0",
        "path": ["tdd-Add-UE-EUTRA-Capabilities-r9", "phyLayerParameters-r9", "ue-SpecificRefSigsSupported"],
        "cell": "E86",
        "values": ["Not Supported", "Supported"],
        "default": "No Information",
    },
    {
        "release": "release_9a0",
        "path": ["tdd-Add-UE-EUTRA-Capabilities-r9", "featureGroupIndicators-r9"],
        "cell": "E88",
        "default": "No Information",
        "func": convert_hex_to_binary
    },
    {
        "release": "release_9a0",
        "path": ["tdd-Add-UE-EUTRA-Capabilities-r9", "featureGroupIndRel9Add-r9"],
        "cell": "E89",
        "default": "No Information",
        "func": convert_hex_to_binary
    },
    {
        "release": "release_1020",
        "path": "ue-Category-v1020",
        "cell": "E92",
        "values": [None, None, None, None, None, None, "Cat6", "Cat7", "Cat8"],
        "default": "No Information",
    },
    {
        "release": "release_1020",
        "processor": "rf-Parameters-v1020,supportedBandCombination-r10 and ca-BandwidthClassDL-r10",
        "postProcessor": classes_mimo,
        "cell": "E95"
    },
    {
        "release": "release_1020",
        "processor": "ca-BandwidthClassUL-r10 on all supported CA combinations",
        "postProcessor": classes_mimo,
        "cell": "E96"
    },
    {
        "release": "release_1020",
        "processor": "supportedMIMO-CapabilityDL-r10 on all Supported CA combinations",
        "postProcessor": classes_mimo,
        "cell": "E97"
    },
    {
        "release": "release_1020",
        "processor": "interFreqNeedForGaps supported on all supported LTE Bandcombinations",
        "cell": "E99"
    },
    {
        "release": "release_1020",
        "processor": "interRAT-NeedForGaps supported on all supported LTE Bandcombinations",
        "cell": "E100"
    },
    {
        "release": "release_1020",
        "path": "featureGroupIndRel10-r10",
        "cell": "E101",
        "default": "No Information",
        "func": convert_hex_to_binary
    },
    {
        "release": "release_1020",
        "path": ["ue-BasedNetwPerfMeasParameters-r10", "loggedMeasurementsIdle-r10"],
        "cell": "E103",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1020",
        "path": ["ue-BasedNetwPerfMeasParameters-r10", "standaloneGNSS-Location-r10"],
        "cell": "E104",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1060",
        "path": ["fdd-Add-UE-EUTRA-Capabilities-v1060", "featureGroupIndRel10-v1060"],
        "cell": "E106",
        "default": "No Information",
        "func": convert_hex_to_binary
    },
    {
        "release": "release_1060",
        "path": ["tdd-Add-UE-EUTRA-Capabilities-v1060", "featureGroupIndRel10-v1060"],
        "cell": "E108",
        "default": "No Information",
        "func": convert_hex_to_binary
    },
    {
        "release": "release_1130",
        "path": ["pdcp-Parameters-v1130", "pdcp-SN-Extension-r11"],
        "cell": "E113",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1130",
        "path": ["pdcp-Parameters-v1130", "supportRohcContextContinue-r11"],
        "cell": "E114",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1130",
        "path": ["phyLayerParameters-v1130", "multiACK-CSI-Reporting-r11"],
        "cell": "E116",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1130",
        "path": ["phyLayerParameters-v1130", "ss-CCH-InterfHandl-r11"],
        "cell": "E117",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1130",
        "path": ["phyLayerParameters-v1130", "tdd-SpecialSubframe-r11"],
        "cell": "E118",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1250",
        "processor": "rf-Parameters-v1250,dl-256QAM",
        "cell": "E119"
    },
    {
        "release": "release_1250",
        "processor": "rf-Parameters-v1250,ul-64QAM",
        "cell": "E120"
    },
    {
        "release": "release_1280",
        "path": ["phyLayerParameters-v1280", "alternativeTBS-Indices-r12"],
        "cell": "E121",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1430",
        "path": ["phyLayerParameters-v1430", "alternativeTBS-Index-r14"],
        "cell": "E122",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1310",
        "path": ["pdcp-Parameters-v1310", "pdcp-SN-Extension-18bits-r13"],
        "cell": "E123",
        "values": ["Supported", "Not Supported"],
        "default": "No Information",
    },
    {
        "release": "release_1170",
        "path":  "ue-Category-v1170",
        "cell": "E124",
        "values": [None, None, None, None, None, None, None, None, None, "Cat9", "Cat10"],
        "default": "No Information",
    },
    {
        "release": "release_11a0",
        "path": "ue-Category-v11a0",
        "cell": "E125",
        "values": [None, None, None, None, None, None, None, None, None, None, None, "Cat11", "Cat12"],
        "default": "No Information",
    },
    {
        "release": "release_1250",
        "path": "ue-CategoryDL-r12",
        "cell": "E126",
        "values": [None, "Cat1", "Cat2", "Cat3", "Cat4", "Cat5", "Cat6", "Cat7", "Cat8", "Cat9", "Cat10", "Cat11",
                   "Cat12", "Cat13", "Cat14"],
        "default": "No Information",
    },
    {
        "release": "release_1250",
        "path": "ue-CategoryUL-r12",
        "cell": "E127",
        "values": [None, "Cat1", "Cat2", "Cat3", "Cat4", "Cat5", "Cat6", "Cat7", "Cat8", "Cat9", "Cat10", "Cat11",
                   "Cat12", "Cat13"],
        "default": "No Information",
    },
    {
        "release": "release_1260",
        "path": "ue-CategoryDL-v1260",
        "cell": "E128",
        "values": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "Cat15",
                   "Cat16"],
        "default": "No Information",
    },
    {
        "release": "release_1330",
        "path": "ue-CategoryDL-v1330",
        "cell": "E129",
        "values": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                   None, "Cat18", "Cat19"],
        "default": "No Information",
    },
    {
        "release": "release_1450",
        "path": "ue-CategoryDL-v1450",
        "cell": "E130",
        "values": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                   None, None, None, "Cat20"],
        "default": "No Information",
    },
    {
        "release": "release_1430",
        "path": "ue-CategoryUL-v1430",
        "cell": "E131",
        "values": ["n16", "n17", "n18", "n19", "n20", "m2"],
        "default": "No Information",
    },
    {
        "release": "release_1430",
        "processor": "rf-Parameters-v1430,ul-256QAM",
        "cell": "E132"
    },
]

LTE_attach_request_fields = [
    {
        "element": "nas_eps.emm.eps_att_type",
        "values": [None, "EPS attach", "combined EPS/IMSI attach", "EPS RLOS attach", None, None,
                   "EPS emergency attach", "Reserved"],
        "cell": "E13"
    },
    {
        "element": "nas_eps.esm_pdn_type",
        "values": [None, "IPv4", "IPv6", "IPv4v6", None, "none IP", "Ethernet"],
        "cell": "E14"
    },
    {
        "element": "nas_eps.esm.eit",
        "values": ["0 security protected ESM information transfer not required",
                   "1 security protected ESM information transfer required"],
        "cell": "E15",
        "default": "No Information"
    },
    {
        "element": "nas_eps.emm.eea0",
        "values": ["Not Supported", "Supported"],
        "cell": "E17",
        "default": "No Information"
    },
    {
        "element": "nas_eps.emm.128eea1",
        "values": ["Not Supported", "Supported"],
        "cell": "E18",
        "default": "No Information"
    },
    {
        "element": "nas_eps.emm.128eea2",
        "values": ["Not Supported", "Supported"],
        "cell": "E19",
        "default": "No Information"
    },
    {
        "element": "nas_eps.emm.eea3",
        "values": ["Not Supported", "Supported"],
        "cell": "E20",
        "default": "No Information"
    },
    {
        "element": "nas_eps.emm.eia0",
        "values": ["Not Supported", "Supported"],
        "cell": "E21",
        "default": "No Information"
    },
    {
        "element": "nas_eps.emm.128eia1",
        "values": ["Not Supported", "Supported"],
        "cell": "E22",
        "default": "No Information"
    },
    {
        "element": "nas_eps.emm.128eia2",
        "values": ["Not Supported", "Supported"],
        "cell": "E23",
        "default": "No Information"
    },
    {
        "element": "nas_eps.emm.eia3",
        "values": ["Not Supported", "Supported"],
        "cell": "E24",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.net_cap.lcs",
        "values": ["Not Supported", "Supported"],
        "cell": "E25",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.net_cap.ps_irat_iu",
        "values": ["Not Supported", "Supported"],
        "cell": "E26",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.net_cap.ps_irat_s1",
        "values": ["Not Supported", "Supported"],
        "cell": "E27",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.net_cap.comb_proc",
        "values": ["Not Supported", "Supported"],
        "cell": "E28",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.net_cap.isr",
        "values": ["Not Supported", "Supported"],
        "cell": "E29",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.net_cap.srvcc_to_geran",
        "values": ["Not Supported", "Supported"],
        "cell": "E30",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.net_cap.epc",
        "values": ["Not Supported", "Supported"],
        "cell": "E31",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.net_cap.nf",
        "values": ["Not Supported", "Supported"],
        "cell": "E32",
        "default": "No Information"
    },
    {
        "element": "nas_eps.emm.add_upd_type",
        "values": ["no additional information", "SMS only"],
        "cell": "E33",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.ue_usage_setting",
        "values": ["Voice Centric", "Data Centric"],
        "cell": "E35",
        "default": "No Information"
    },
    {
        "element": "gsm_a.gm.gmm.voice_domain_pref_for_eutran",
        "values": ["CS Voice only", "IMS PS Voice only", "CS voice preferred, IMS PS Voice as secondary",
                   "IMS PS voice preferred, CS Voice as secondary", ],
        "cell": "E36",
        "default": "No Information"
    },
]