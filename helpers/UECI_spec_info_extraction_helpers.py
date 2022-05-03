def handle_of(line):

    if "OF" not in line:
        return None
    if " OF " in line:
        return line.split()[0], line.split("OF")[1].strip().split(" ")[0]


def find_sequence(line_index, lines):

    bracket_count = 0
    dict_sequence = {}
    start_recording = False
    skip_line = False

    for line_num, line_to_check in enumerate(lines[line_index:]):
        line_to_check = line_to_check.strip()
        if line_to_check[-1] == ",":
            line_to_check = line_to_check[:-1]

        if skip_line:
            if "{" in line_to_check:
                if "}" not in line_to_check:
                    bracket_count += line_to_check.count("{")
                    continue
                else:
                    continue
            if "}" not in line_to_check:
                continue

        if line_to_check.startswith("nonCriticalExtension") or line_to_check.startswith("lateNonCriticalExtension"):
            continue

        of_value = handle_of(line_to_check)
        if not start_recording and of_value:

            return {of_value[1]: (of_value[1], check_for_subsequent_exceptions(lines, of_value[1] + " ")["list"])}

        if "{" in line_to_check:
            if "ENUMERATED" in line_to_check:
                if line_num == 0:
                    return "ENUMERATED"
                dict_sequence[line_to_check.strip().split(" ")[0]] = ("ENUMERATED", False)
                if "}" not in line_to_check:
                    bracket_count += line_to_check.count("{")

                    skip_line = True
                continue
            start_recording = True
            bracket_count += line_to_check.count("{")

        if "}" in line_to_check and bracket_count > 0:
            bracket_count -= line_to_check.count("}")
            if skip_line:
                if bracket_count == 1:
                    skip_line = False
                continue

        if bracket_count == 0 and start_recording:
            return dict_sequence

        if start_recording:

            if line_to_check.strip().split(" ").__len__() < 2:
                continue
            if line_to_check.strip().split(" ")[0] == "nonCriticalExtension" or \
                    line_to_check.strip().split(" ")[0] == "lateNonCriticalExtension" or "Following" in line_to_check:
                continue
            if "::=" in line_to_check.split()[1]:
                if "CHOICE" not in line_to_check:
                    continue
            if "[[" in line_to_check:
                line_to_check = line_to_check[2:].strip()
                of_value = handle_of(line_to_check)

            if ("SEQUENCE" in line_to_check or "CHOICE" in line_to_check) and not of_value and line_num != 0:
                dict_sequence[line_to_check.strip().split(" ")[0]] = (find_sequence(line_num + line_index, lines), "CHOICE" in line_to_check)
                skip_line = True
                continue
            if ("SEQUENCE" in line_to_check or "CHOICE" in line_to_check) and line_num == 0:
                continue

            if "SEQUENCE" in line_to_check and of_value:
                dict_sequence[of_value[0]] = ({of_value[1]: (of_value[1],
                                                             check_for_subsequent_exceptions(lines, of_value[1] +
                                                                                             " ")["list"])}, True)
                continue

            if of_value:
                dict_sequence[of_value[0]] = (of_value[1], True)
            else:
                check_for_exceptions = check_for_subsequent_exceptions(lines, line_to_check.strip().split(" ")[1].split(",")[0] + " ")
                if check_for_exceptions["end"]:
                    dict_sequence[line_to_check.strip().split(" ")[0]] = (check_for_exceptions["end"], False)
                else:
                    dict_sequence[line_to_check.strip().split(" ")[0]] = (line_to_check.strip().split(" ")[1].split(",")[0], check_for_exceptions["list"])
        else:
            return {lines[line_index].strip().split(" ")[0]: (lines[line_index].strip().split(" ")[2], False)}

def check_for_subsequent_exceptions(lines, keyword):
    result = {
        "list": False,
        "end": ""
    }

    for line_n, line in enumerate(lines):
        if line.startswith(keyword):
            if "CHOICE" in line:
                result["list"] = True
            else:
                r = find_sequence(line_n, lines)

                if isinstance(r, dict) and list(r.keys()).__len__() == 1 and r[list(r.keys())[0]][0] == list(r.keys())[0]:
                    result["list"] = True

                if "SEQUENCE" not in line:
                    if isinstance(r, dict) and list(r.keys()).__len__() == 1 and r[list(r.keys())[0]][0] == "BIT":
                        result["end"] = "BIT"
    return result


def get_data_structure(dict_to_search, spec_lines, result_dict, trimmed_dict=None):

    if trimmed_dict is None:
        trimmed_dict = {}
    for ie in dict_to_search:
        found = False
        if isinstance(dict_to_search[ie][0], dict):
            result_dict[ie] = get_data_structure(dict_to_search[ie][0], spec_lines, {})[0], dict_to_search[ie][1]
            trimmed_dict[ie] = get_data_structure(dict_to_search[ie][0], spec_lines, {})[1]
            continue
        for line in spec_lines:
            if line.startswith(dict_to_search[ie][0] + " "):

                found = True
                result = find_sequence(spec_lines.index(line), spec_lines)
                if isinstance(result, dict):
                    output = get_data_structure(result, spec_lines, {})
                    result_dict[ie] = output[0], dict_to_search[ie][1]
                    trimmed_dict[ie] = output[1]
                else:
                    result_dict[ie] = result, False
                    trimmed_dict[ie] = result

        if not found:
            result_dict[ie] = dict_to_search[ie][0], False
            trimmed_dict[ie] = dict_to_search[ie][0]

    return result_dict, trimmed_dict

def lower_case_first_letter(word):
    return word[0].lower() + word[1:]

def upper_case_first_letter(word):
    return word[0].upper() + word[1:]

def simplify_last_child(sequence):

    for s in sequence:
        if not isinstance(sequence[s], dict):
            continue
        if s in sequence[s].keys():
            sequence[s] = sequence[s][s]
        elif s in [lower_case_first_letter(k) for k in sequence[s].keys()]:
            sequence[s] = sequence[s][upper_case_first_letter(s)]
        else:
            simplify_last_child(sequence[s])
    return sequence

def simplify_last_child_lists(sequence):

    for s in sequence:
        element_to_check = sequence[s]
        if isinstance(element_to_check, tuple):
            element_to_check = element_to_check[0]
        if not isinstance(element_to_check, dict):
            continue
        if s in element_to_check.keys():
            sequence[s] = sequence[s][0][s]

        elif s in [lower_case_first_letter(k) for k in element_to_check.keys()]:
            sequence[s] = sequence[s][0][upper_case_first_letter(s)]
        else:
            simplify_last_child_lists(element_to_check)
    return sequence

def make_wireshark_related_adjustments_helper(sequence):
    for s in sequence:
        element_to_check = sequence[s]
        if isinstance(element_to_check, tuple):
            element_to_check = element_to_check[0]
        if not isinstance(element_to_check, dict):
            continue
        for k in list(element_to_check.keys()):
            if k[-2:] == "Id" and k[-3] != "-":
                sequence[s] = ("INTEGER", sequence[s][1])
            if k == "FreqBandIndicatorEUTRA":
                if s == "bandEUTRA":
                    sequence[s] = ("INTEGER", sequence[s][1])

        make_wireshark_related_adjustments_helper(element_to_check)