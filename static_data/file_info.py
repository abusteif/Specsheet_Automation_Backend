from pathlib import Path
from Specsheet_Automation.static_data.configuration import MAIN_FILES_FOLDER_PATH

main_files_folder = Path(MAIN_FILES_FOLDER_PATH)
temp_files_folder = main_files_folder / "temp_files"
perm_files_folder = main_files_folder / "perm_files"
log_files_folder = main_files_folder / "log_files"

NR_files_folder = perm_files_folder / "NR"
jira_files_folder = perm_files_folder / "jira"
json_file_path = "json_file.txt"
logs_file_path = log_files_folder / "logs.txt"
dut_attach_request_lists_file_path = "dut_attach_request_lists_file.txt"
dut_UECI_lists_file = "dut_UECI_lists_file.txt"
NR_dut_UECI_lists_file = "NR_dut_UECI_lists_file.txt"
hex_file_path = temp_files_folder / "hex_file.txt"
converted_hex_file_path = "converted_hex_file.txt"
pcap_file_path = "pcap_file.pcap"

jira_config_file = jira_files_folder / "jira_config"
LTE_specsheet_template = perm_files_folder / "MSR0835_template.xlsx"
ENDC_specsheet_template = NR_files_folder / "ENDC_specsheet_template.xlsx"
NR_LTE_specsheet_template = perm_files_folder / "NR_LTE_specsheet_template.xlsx"

spec_UECI_word_doc = perm_files_folder / "36331-g30.docx"
spec_UECI_text_file = perm_files_folder / "latest_release_text_file.txt"
spec_UECI_json_file = perm_files_folder / "spec_UECI_json.txt"
spec_UECI_lists_file = perm_files_folder / "spec_UECI_lists.txt"
spec_UECI_csv_file = perm_files_folder / "spec_UECI_csv.csv"
spec_UECI_csv_lists_file = perm_files_folder / "spec_UECI_csv_lists.csv"
spec_UECI_categories_file = perm_files_folder / "spec_UECI_release_categories.txt"
spec_UECI_warning_list_file = perm_files_folder / "spec_warning_list.txt"

NR_spec_UECI_word_doc = NR_files_folder / "NR_16.5.0.docx"
NR_spec_UECI_text_file = NR_files_folder / "NR_latest_release_text_file.txt"
NR_spec_UECI_json_file = NR_files_folder / "NR_spec_UECI_json.txt"
NR_spec_UECI_lists_file = NR_files_folder / "NR_spec_UECI_lists.txt"
NR_spec_UECI_csv_file = NR_files_folder / "NR_spec_UECI_csv.csv"
NR_spec_UECI_csv_lists_file = NR_files_folder / "NR_spec_UECI_csv_lists.csv"
NR_spec_UECI_categories_file = NR_files_folder / "NR_spec_UECI_release_categories.txt"
NR_spec_UECI_warning_list_file = NR_files_folder / "NR_spec_warning_list.txt"

spec_attach_request_sample_hex_file = perm_files_folder / "spec_attach_request_sample_hex.txt"
spec_attach_request_sample_converted_hex_file = perm_files_folder / "spec_attach_request_sample_converted_hex.txt"
spec_attach_request_sample_pcap_file = perm_files_folder / "spec_attach_request_sample_pcap.pcap"
spec_attach_request_sample_json_file = perm_files_folder / "spec_attach_request_sample_json.txt"
spec_attach_request_sample_lists_file = perm_files_folder / "spec_attach_request_sample_lists.txt"
spec_attach_request_ie_file = perm_files_folder / "spec_attach_request_ie.txt"
