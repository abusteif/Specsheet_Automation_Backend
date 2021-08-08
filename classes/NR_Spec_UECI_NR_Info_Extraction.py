import docx2txt
import csv
from itertools import zip_longest
from Specsheet_Automation.helpers.Spec_UECI_Info_Extraction_helpers import *
from Specsheet_Automation.helpers.data_conversion_helpers import *
from Specsheet_Automation.helpers.DUT_SPEC_UECI_Info_Extraction_helpers import get_data_from_csv

class NR_Spec_Doc_Info_Extraction:

    def __init__(self, release_word_doc_path, release_text_file_path):
        self.release_word_doc = release_word_doc_path
        self.release_text_file = release_text_file_path
        self.spec_plain_text = []
        self.releases = {}
        self.releases_full = {}
        self.all_ie_lists_file = ""

    def extract_info_from_release_word_doc(self):
        text_info = docx2txt.process(self.release_word_doc)
        start_recording = False
        start_capture = False
        first_occurrence = False
        with open(self.release_text_file, "w") as release_text:
            for line in text_info.split("\n"):
                if not line.strip():
                    continue
                if "UE capability information elements" in line.strip():
                    if first_occurrence:
                        start_recording = True
                    else:
                        first_occurrence = True
                    continue

                if "Other information elements" in line and start_recording:
                    return
                if "TAG" in line and "START" in line and start_recording:
                    start_capture = True
                    continue
                if "TAG" in line and "STOP" in line and start_recording:
                    start_capture = False
                    continue
                if start_capture:
                    if "--" in line:
                        if "non-critical" not in line:
                            if line.strip().startswith("--"):
                                continue
                            else:
                                line = line.split("--")[0]

                    parts = line.split("\t")
                    new_line = " ".join(parts)
                    new_line = " ".join(new_line.split())
                    if "::=" in new_line:
                        if " ::=" not in new_line:
                            new_line = "".join(new_line.split("::=")[0] + " ::=" + new_line.split("::=")[1])
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
            if line.startswith("-- Late non-critical extensions"):
                late = True
            if line.startswith("UE-NR-Capability ::="):
                self.releases["release_15"] = find_sequence(line_index, self.spec_plain_text)
                regular_releases["release_15"] = []
            if line.startswith("-- Regular non-critical extensions"):
                late = False
            if line.startswith("UE-NR-Capability-"):
                release = "release_" + line.split("-")[3].split()[0][1:]
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
        # for r in self.releases:
        #     print(r)
        #     print(self.releases[r])

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


#
# from Specsheet_Automation.static_data.file_info import NR_spec_UECI_word_doc, NR_spec_UECI_text_file, NR_spec_UECI_categories_file
#
# a = NR_Spec_Doc_Info_Extraction(NR_spec_UECI_word_doc, NR_spec_UECI_text_file)
# a.extract_info_from_release_word_doc()
# a.build_initial_releases(NR_spec_UECI_categories_file)

#     def build_initial_releases(self, categories_file):
#         with open(self.release_text_file, "r") as release_text:
#             self.spec_plain_text = release_text.readlines()
#         # for line_index, line in enumerate(self.spec_plain_text):
#         #     # if line.startswith("-- Late non critical extensions"):
#         #     #     late = True
#         #     if line.startswith("UE-NR-Capability ::="):
#         #         print(find_sequence(line_index, self.spec_plain_text))
#             print(find_sequence(1, self.spec_plain_text))
#
# from Specsheet_Automation.static_data.file_info import NR_spec_UECI_word_doc, NR_spec_UECI_text_file, spec_UECI_text_file
#
# NR_Spec_Doc_Info_Extraction(NR_spec_UECI_word_doc, spec_UECI_text_file).build_initial_releases("")