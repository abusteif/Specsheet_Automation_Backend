import docx2txt
import json
from Specsheet_Automation.classes.UECI_spec_info_extraction import UECISpecInfoExtraction
from Specsheet_Automation.helpers.UECI_spec_info_extraction_helpers import *

class NRUECISpecInfoExtraction(UECISpecInfoExtraction):

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
            if line.startswith("UE-NR-Capability ::=") or line.startswith("UE-MRDC-Capability ::="):
                release_items = find_sequence(line_index, self.spec_plain_text)
                if "release_15" in regular_releases:
                    self.releases["release_15"].update(release_items)
                else:
                    regular_releases["release_15"] = []
                    self.releases["release_15"] = release_items

            if line.startswith("-- Regular non-critical extensions"):
                late = False
            if line.startswith("UE-NR-Capability-") or line.startswith("UE-MRDC-Capability-"):
                release = "release_" + line.split("-")[3].split()[0][1:]
                if line.startswith("UE-NR-Capability-"):
                    if late:
                        late_releases[release] = []
                    else:
                        regular_releases[release] = []
                release_items = find_sequence(line_index, self.spec_plain_text)
                if release not in self.releases:
                    self.releases[release] = release_items
                else:
                    self.releases[release].update(release_items)

        with open(categories_file, "w") as release_categories:
            release_categories.write(json.dumps({
                "regular": regular_releases,
                "late": late_releases
            }))

    def deal_with_wireshark_issues(self):

        # This function is temporary until Wireshark fixes IE's with "Id" in them
        # List of keywords that were fully or partially removed:
        # FreqBandIndicatorEUTRA
        # FeatureSetCombinationId
        # FeatureSetEUTRA-DownlinkId
        # FeatureSetEUTRA-UplinkId
        # FeatureSetDownlinkId
        # FeatureSetUplinkId
        with open(self.all_ie_lists_file, "r+") as all_ie_lists:
            list_lines = all_ie_lists.readlines()
            all_ie_lists.seek(0)
            all_ie_lists.truncate()
            for line in list_lines:

                if ("Id" not in line or "-Id" in line) and "bandEUTRA,FreqBandIndicatorEUTRA" not in line:
                    all_ie_lists.write(line)
                    continue

                if "Id" in line:
                    # all_ie_lists.write(line)
                    split_line = line.split(",")
                    (id_id, id_value) = [(index, l) for index, l in enumerate(split_line) if "Id" in l][0]
                    if id_value[-2:] != "Id":
                        all_ie_lists.write(line)
                        continue
                    split_line.pop(id_id)
                if "bandEUTRA,FreqBandIndicatorEUTRA" in line:
                    split_line = line.split(",")
                    split_line.pop(split_line.index("FreqBandIndicatorEUTRA"))

                line = ",".join(split_line)
                all_ie_lists.write(line)

    def make_wireshark_related_adjustments(self):
        # This function is temporary until Wireshark fixes IE's with "Id" in them
        make_wireshark_related_adjustments_helper(self.releases_full)