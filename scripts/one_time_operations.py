from Specsheet_Automation.classes.Spec_UECI_Info_Extraction import *
from Specsheet_Automation.static_data.file_info import *


def extract_spec_UECI(release_word_doc, release_text_file, spec_json_file, spec_lists_file, spec_csv_file,
                      spec_csv_lists_file, warning_list_file):
    s = Spec_Doc_Info_Extraction(release_word_doc, release_text_file)
    s.extract_info_from_release_word_doc()
    s.build_all_releases(spec_json_file, spec_lists_file, spec_UECI_categories_file)
    s.save_list_to_csv(spec_csv_file, spec_csv_lists_file)
    s.create_warning_list(spec_csv_lists_file, warning_list_file)


if __name__ == "__main__":
    extract_spec_UECI(spec_UECI_word_doc, spec_UECI_text_file, spec_UECI_json_file, spec_UECI_lists_file,
                      spec_UECI_csv_file, spec_UECI_csv_lists_file, spec_UECI_warning_list_file)
    # add_steps_to_test_case(spec_UECI_csv_file, spec_UECI_lists_file)

