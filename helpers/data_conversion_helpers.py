from subprocess import check_output
from Specsheet_Automation.static_data.tools_info import text2pcap_path, tshark_path
from Specsheet_Automation.static_data.configuration import UECAPABILITYINFORMATION_MESSAGE_TYPE, \
    ATTACHREQUEST_MESSAGE_TYPE
import json


# TODO: add support for data from IRIS. This can be done by:
# 1 - Extracting the HEX Stream of the entire UECapabilityIndication message
# 2 - Updating convert_raw_hex_to_ws_readable_hex to always start at the first character regardless of whether it
# matches the delimiter. This is going to be a single use case to check if the HEX is for an IRIS message
# 3 - Modifying convert_ws_hex_to_pcap to accept a new argument that will tell it if it's a standard
# UECapabilityInformation message or a an IRIS UECapabilityIndication.
# In the case of IRIS message, the command should simply be:
# check_output(path_wrapper(text2pcap_path) + '-q -l 1 ' + path_wrapper(input_hex_file) + ' ' +
#              path_wrapper(output_pcap_file))
# The 1 is for ethernet frame
# 4 - Modifying convert_pcap_to_json to accept a new argument that wil tell it if it's a standard
# UECapabilityInformation message or a an IRIS UECapabilityIndication.
# In the case of IRIS message, the command should simply be:
#         json_output = check_output(path_wrapper(tshark_path) + ' -r ' + path_wrapper(input_pcap_file) + ' -T json ')
# 5 - Modifying convert_json_to_lists to check for the presence of keywords such as "slap" to confirm that it's an
# an IRIS UECapabilityIndication message and read it accordingly.
# In the case of IRIS message, the function should check that here is no "data" field to confirm that it's a properly
# formed IRIS UECapabilityIndication message
# 6 - Modifying the LTE and NR UECI_info_extraction classes to remove extra lines associated with
# IRIS UECapabilityIndication and extracting the desired message only

def convert_raw_hex_to_ws_readable_hex(input_hex, output_hex_file, start_index, delimiter):
    try:
        def add_zeros(hex_num):
            return "".join(["0"] * (5 - hex_num.__len__())) + hex_num

        input_hex = input_hex.strip()
        input_hex = "".join(input_hex.split(" "))
        raw_hex_data = []
        new_index = input_hex.find(delimiter, start_index, input_hex.__len__())
        assert new_index != -1
        input_hex = input_hex[new_index:]
        for i in range(0, input_hex.__len__() - 1, 2):
            raw_hex_data.append(input_hex[i] + input_hex[i + 1])
        with open(output_hex_file, "w") as converted_file:
            prefix = "00000 "
            length_list = [i for i in range(0, raw_hex_data.__len__() + 16, 16)]

            for j in range(1, length_list.__len__()):
                converted_file.write(prefix + " ".join(raw_hex_data[length_list[j - 1]:length_list[j]]) + "\n")
                prefix = add_zeros(str(hex(length_list[j]))[2:]) + " "
        return True, new_index + 1
    except Exception as e:
        return False, "Error while converting HEX to Wireshark readable HEX: {}".format(repr(e))

def convert_ws_hex_to_pcap(input_hex_file, output_pcap_file):
    try:
        check_output(path_wrapper(text2pcap_path) + '-q -l 147 ' + path_wrapper(input_hex_file) + ' ' +
                     path_wrapper(output_pcap_file))
        return True, "Successfully converted HEX to PCAP"
    except Exception as e:
        return False, "Error while converting HEX to PCAP: {}".format(repr(e))


def convert_pcap_to_json(input_pcap_file, output_json_file, file_type):
    try:
        # dissect = "lte-rrc.ul.dcch" if file_type == "UE Capability Information - 4G" else "nas-eps"
        # dissect = "lte-rrc.ul.dcch" if "UECapabilityInformation" in file_type else "nas-eps"
        if UECAPABILITYINFORMATION_MESSAGE_TYPE in file_type:
            dissect = "lte-rrc.ul.dcch"
        elif file_type == ATTACHREQUEST_MESSAGE_TYPE:
            dissect = "nas-eps"
        json_output = check_output(path_wrapper(tshark_path) + '-o "uat:user_dlts:\\"User 0 (DLT=147)\\",\\"'
                                   + dissect + '\\",\\"0\\",\\"\\",\\"0\\",\\"\\"" -r '
                                   + path_wrapper(input_pcap_file) + ' -T json ')
        assert "Malformed" not in json_output.decode("utf-8")
        assert "Unknown Message Type" not in json_output.decode("utf-8")
        with open(output_json_file, "w") as json_o: 
            json_o.write(json_output.decode("utf-8"))
        return True, "Successfully converted PCAP to JSON"
    except AssertionError:
        return False, "Malformed HEX data"
    except Exception as e:
        return "Error while converting PCAP to JSON: {}".format(repr(e))


def convert_json_to_lists_helper(remaining_keys, current_path, all_data, output_file, excepted_elements):
    count = 0
    for k in remaining_keys:
        if not remaining_keys[k]:
            remaining_keys[k] = "Null"
        if isinstance(remaining_keys[k], dict):
            current_path.append(k)
            convert_json_to_lists_helper(remaining_keys[k], current_path, all_data, output_file, excepted_elements)
        else:
            if k in excepted_elements:
                pass
            else:
                new_path = current_path[:]
                new_path.append(k)
                new_path.append(remaining_keys[k]) if remaining_keys[k] else new_path.append("Null")
                all_data.append(new_path)
                output_file.write(",".join(new_path)+"\n")
        count += 1
        if count == remaining_keys.__len__():
            if current_path:
                current_path.pop()

def convert_json_to_lists(input_json_file, output_lists_file, excepted_elements, file_type=""):
    try:
        with open(input_json_file, "r") as input_file:
            lines = json.load(input_file)

            if isinstance(lines, list):
                lines = lines[0]
            with open(output_lists_file, "w") as output_file:
                convert_json_to_lists_helper(lines, [], [], output_file, excepted_elements)
        with open(output_lists_file, "r") as complete_output_file:
            complete_lines = complete_output_file.readlines()
            found = False
            if UECAPABILITYINFORMATION_MESSAGE_TYPE in file_type:
                for li in complete_lines:
                    if "CapabilityRAT_ContainerList," in li:
                        found = True
                        if li.strip()[-1] == "0":
                            return False, "Error while converting JSON to LIST"
                        else:
                            break
                if not found:
                    return False, "Error while converting JSON to LIST"
            # elif file_type == ATTACHREQUEST_MESSAGE_TYPE:

        return True, "successfully converted JSON to LIST"
    except Exception as e:
        return False, "Error while converting JSON to LIST: {}".format(repr(e))

def path_wrapper(path):
    return '"' + path.__str__() + '" '
