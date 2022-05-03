import docx2txt
from Specsheet_Automation.classes.UECI_spec_info_extraction import UECISpecInfoExtraction
from Specsheet_Automation.helpers.UECI_spec_info_extraction_helpers import *

class LTEUECISpecInfoExtraction(UECISpecInfoExtraction):

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
        # This has to be done manually as late non critical extensions need to be adjusted
        # with open(categories_file, "w") as release_categories:
        #     release_categories.write(json.dumps({
        #         "regular": regular_releases,
        #         "late": late_releases
        #     }))
