import docx2txt
import csv
from itertools import zip_longest
from Specsheet_Automation.helpers.Spec_UECI_Info_Extraction_helpers import *
from Specsheet_Automation.helpers.data_conversion_helpers import *
from Specsheet_Automation.helpers.DUT_SPEC_UECI_Info_Extraction_helpers import get_data_from_csv

class Spec_Doc_Info_Extraction:

    def __init__(self, release_word_doc_path, release_text_file_path):
        self.release_word_doc = release_word_doc_path
        self.release_text_file = release_text_file_path
        self.releases = {}
        self.releases_full = {}
        self.spec_plain_text = []
        self.all_ie_lists_file = ""

    def extract_info_from_release_word_doc(self):
        text_info = docx2txt.process(self.release_word_doc)
        start_recording = False
        with open(self.release_text_file, "w") as release_text:
            for line in text_info.split("\n"):
                if not line.strip():
                    continue
                if "-- ASN1STAR" in line:
                    continue
                if "UE-EUTRA-Capability information element" in line.strip():
                    start_recording = True
                if line.strip() == "-- ASN1STOP":
                    start_recording = False
                if start_recording:
                    parts = line.split("\t")
                    new_line = " ".join(parts)
                    new_line = " ".join(new_line.split())
                    if "::=" in new_line:
                        if " ::=" not in new_line:
                            new_line = "".join(new_line.split("::=")[0]+" ::="+new_line.split("::=")[1])
                    if new_line.strip().endswith("OPTIONAL}"):
                        release_text.write(new_line[:-1] + "\n")
                        release_text.write("}\n")
                        continue
                    if new_line.strip().endswith("OF"):
                        release_text.write(new_line + " ")

                    else:
                        release_text.write(new_line + "\n")

    def build_initial_releases(self, categories_file):
        with open(self.release_text_file, "r") as release_text:
            self.spec_plain_text = release_text.readlines()
        late = False
        late_releases = {}
        regular_releases = {}
        for line_index, line in enumerate(self.spec_plain_text):
            if line.startswith("-- Late non critical extensions"):
                late = True
            if line.startswith("UE-EUTRA-Capability ::="):
                self.releases["release_8"] = find_sequence(1, self.spec_plain_text)
                regular_releases["release_8"] = []
            if line.startswith("-- Regular non critical extensions"):
                late = False
            if line.startswith("UE-EUTRA-Capability-"):
                release = "release_" + line.split("-")[3][1:]
                if late:
                    late_releases[release] = []
                else:
                    regular_releases[release] = []
                self.releases[release] = find_sequence(line_index, self.spec_plain_text)
        with open(categories_file, "w") as release_categories:
            release_categories.write(json.dumps({
                "regular": regular_releases,
                "late": late_releases
            }))

    def build_all_releases(self, all_ie_json_file, all_ie_lists_file, categories_file):
        self.build_initial_releases(categories_file)
        self.releases_full = self.releases.copy()
        for release in self.releases:
            all_releases = get_data_structure(self.releases[release], self.spec_plain_text, {})
            self.releases[release] = all_releases[1]
            self.releases_full[release] = all_releases[0]

        self.releases = simplify_last_child(self.releases)

        self.releases_full = simplify_last_child_lists(self.releases_full)
        self.save_data_to_json(all_ie_json_file)
        self.convert_json_to_list(all_ie_json_file, all_ie_lists_file)

    def save_data_to_json(self, all_ie_json_file):
        with open(all_ie_json_file, "w") as all_ie:
            all_ie.write(json.dumps(self.releases))

    def convert_json_to_list(self, all_ie_json_file, all_ie_lists_file):
        self.all_ie_lists_file = all_ie_lists_file
        convert_json_to_lists(all_ie_json_file, all_ie_lists_file, [])

    def save_list_to_csv(self, csv_file, csv_list_file):
        def get_json_value(all_json_data, json_field):
            current_value = all_json_data
            columns_list = []
            found = False
            for d_num, d in enumerate(json_field):
                if isinstance(current_value[d], tuple):
                    if current_value[d][1]:
                        found = True
                        if json_field[:d_num+1] not in columns_list:
                            columns_list.append(json_field[:d_num+1])
                    current_value = current_value[d][0]
                else:
                    current_value = current_value[d]
            if found:
                columns_list.append(json_field)
            return columns_list

        with open(self.all_ie_lists_file, "r") as all_ie_lists:
            list_data = all_ie_lists.readlines()
            list_entries = []
            non_list_entries = []
            for l_d in list_data:
                l_d_list = l_d.strip().split(",")[:-1]
                lists_result = get_json_value(self.releases_full, l_d_list)
                if not lists_result:
                    non_list_entries.append(l_d_list)
                else:
                    for l_r in lists_result:
                        if l_r not in list_entries:
                            list_entries.append(l_r)
        for li in [list_entries, non_list_entries]:
            li.insert(0, ["ID"])
            csv_out_data = list(zip_longest(*li, fillvalue=''))
            csv_out_data.append(['' for _ in range(0, max([len(ie) for ie in csv_out_data]))])
            csv_file_to_use = csv_list_file if li == list_entries else csv_file
            with open(csv_file_to_use, 'w', newline='') as all_ie_csv_file:
                wr = csv.writer(all_ie_csv_file)
                wr.writerows(csv_out_data)

    def create_warning_list(self, csv_list_file, warning_list_file):
        columns = get_data_from_csv(csv_list_file)
        warning_list = {"items_to_omit": []}
        with open(warning_list_file, "w") as warning_file:
            for c1 in columns:
                for c2 in columns[columns.index(c1)+1:]:
                    if set(c1[:c1.index('')]) < set(c2):
                        warning_list["items_to_omit"].append(c1[:c1.index('')])
                        break
            warning_file.write(json.dumps(warning_list))
