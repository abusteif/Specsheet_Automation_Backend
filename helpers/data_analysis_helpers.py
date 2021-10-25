from Specsheet_Automation.static_data.configuration import mimo_mapping, class_mapping

def get_length(item):
    return int(item[1]) - int(item[0]) if item.__len__() > 0 else 0

def get_start_end(list_to_process, operator="!="):
    start = 0
    result = []
    end = 0

    def compare(op, item1, item2):
        if op == "!=":
            return item1 != item2
        if op == "<":
            return int(item1) < int(item2)
        if op == "<=":
            return int(item1) <= int(item2)

    for e_index, e in enumerate(list_to_process):
        if e_index == 0:
            continue
        old_e = list_to_process[e_index - 1]
        if compare(operator, e, old_e):
            end = e_index
            result.append([start, end])
            start = e_index
    result.append([end, list_to_process.__len__()])
    return result


def get_bands(bands_data):
    result = ""
    for bd in bands_data:
        one_band = "{}{}".format(bd["band"], class_mapping[bd["class"]])
        if "mimo" in list(bd.keys()):
            one_band += "({})".format(mimo_mapping[int(bd["mimo"])])
        result += "{}-".format(one_band)
    return result[:-1]


def calculate_num_of_carriers(carriers_data):
    num = 0
    for carrier in carriers_data:
        if carrier["class"] == "0":
            num += 1
        if carrier["class"] == "1" or carrier["class"] == "2":
            num += 2
    return num


def calculate_num_of_layers(carriers_data):
    num = 0
    for carrier in carriers_data:
        if carrier["class"] == "0":
            num += mimo_mapping[int(carrier["mimo"])]
        if carrier["class"] == "1" or carrier["class"] == "2":
            num += 2 * mimo_mapping[int(carrier["mimo"])]
    return num

def pop_special_from_ie_list(ie_list):
    for ie in ie_list:
        if isinstance(ie_list[ie], list):
            ie_list[ie] = [i for i in ie_list[ie] if "special_" not in i]


def map_mimo_num_to_value_dl_LTE(num):
    return ["2", "4", "8"][int(num)]
