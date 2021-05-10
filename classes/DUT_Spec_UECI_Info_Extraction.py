from Specsheet_Automation.static_data.configuration import DUT_UECI_item_0_elements
from Specsheet_Automation.helpers.DUT_SPEC_UECI_Info_Extraction_helpers import extract_number_from_item, \
    get_list_items

import json
class DUT_UECI_Info_Extraction:
    def __init__(self, list_file, categories_file, warning_list_file):
        self.item_0_data = []
        self.trimmed_data = []
        self.releases = {}
        self.non_list_releases = {}
        self.list_releases = {}
        self.ie_non_list = {}
        self.ie_list = {}
        with open(list_file, "r") as UECI_list_file:
            processed_data = []
            list_data = UECI_list_file.readlines()
            for l_d in list_data:
                processed_data.append(l_d.strip().split(","))
        self.proccessed_data = processed_data
        with open(categories_file, "r") as release_categories:
            self.release_categories = json.load(release_categories)
        with open(warning_list_file, "r") as warning_list:
            self.warning_list = json.load(warning_list)["items_to_omit"]
        self.finalize_data()

    def get_item_0_data(self):
        item_0_data = []
        for ie in self.proccessed_data:
            result = True
            if ie.__len__() >= DUT_UECI_item_0_elements.__len__():
                for i in range(0, DUT_UECI_item_0_elements.__len__()):
                    result = result and ie[i] == DUT_UECI_item_0_elements[i]
                if result:
                    item_0_data.append(ie)
        self.item_0_data = item_0_data

    def trim_data(self):
        trimmed_data = []
        for i0 in self.item_0_data:
            new_data_without_prefix = []
            if i0[15:]:
                for j in i0[14:]:
                    if "lte-rrc." in j:
                        j = j.split("lte-rrc.")[1]
                    if "element" in j:
                        j = j.split("_element")[0]
                    new_data_without_prefix.append(j)
                trimmed_data.append(new_data_without_prefix)
        self.trimmed_data = trimmed_data

    def build_releases(self):
        releases = self.release_categories
        for td in self.trimmed_data:
            nonCriticalExtension_count = td.count("nonCriticalExtension")
            lateNonCriticalExtension_count = td.count("lateNonCriticalExtension_tree")

            if lateNonCriticalExtension_count > 0:
                if lateNonCriticalExtension_count == 1:
                    td = td[nonCriticalExtension_count + lateNonCriticalExtension_count + 1:]
                    releases["late"][list(releases["late"].keys())[nonCriticalExtension_count - 2]].append(td)
                if lateNonCriticalExtension_count >= 2:
                    # TODO: Update this to work with the late non critical extensions that have been moved to the
                    #  end of the list

                    td = td[nonCriticalExtension_count + lateNonCriticalExtension_count + 2:]
                    # releases["late"][list(releases["late"].keys())[nonCriticalExtension_count - 1]].append(td)
                    releases["late"][list(releases["late"].keys())[nonCriticalExtension_count - 1]].append(td)

            else:
                td = td[nonCriticalExtension_count:]
                releases["regular"][list(releases["regular"].keys())[nonCriticalExtension_count]].append(td)
        self.releases = releases

    def finalize_data(self):
        self.get_item_0_data()
        self.trim_data()
        self.build_releases()
        all_releases = self.split_data()
        self.non_list_releases = all_releases[0]
        self.list_releases = all_releases[1]
        self.get_ie_non_lists()
        self.get_ie_lists()

    def copy_releases(self):
        new_releases = {}
        for release_type in self.releases:
            new_releases[release_type] = {}
            for release in self.releases[release_type]:
                new_releases[release_type][release] = []
        return new_releases

    def split_data(self):

        edited_releases = self.copy_releases()
        edited_releases_with_lists = self.copy_releases()
        list_found = False

        for release_type in self.releases:
            for release in self.releases[release_type]:
                for ie_index, ie in enumerate(self.releases[release_type][release]):
                    new_ie = []
                    for e in ie:
                        for element_to_remove in ["_element", "_tree"]:
                            if element_to_remove in e:
                                e = e.split(element_to_remove)[0]
                        e = e.replace("_", "-")
                        new_ie.append(e)
                        if "Item" in e:
                            list_found = True
                    if not list_found:
                        edited_releases[release_type][release].append(new_ie)
                    else:
                        edited_releases_with_lists[release_type][release].append(new_ie)
                        list_found = False

        return edited_releases, edited_releases_with_lists

    def get_ie_non_lists(self):
        for release_type in self.release_categories:
            for release in self.non_list_releases[release_type]:
                for ie in self.non_list_releases[release_type][release]:
                    if [release] + ie[:-1] in self.warning_list:
                        continue
                    self.ie_non_list[",".join([release] + ie[:-1])] = ie[-1]

    def get_ie_lists(self):
        for release_type in self.release_categories:
            for release in self.list_releases[release_type]:
                for ie in self.list_releases[release_type][release]:
                    items = []
                    get_list_items(ie, items)
                    if [release] + items[-1][0] in self.warning_list:
                        continue
                    for item in items:
                        full_ie = ",".join([release] + item[0])
                        if full_ie in list(self.ie_list.keys()):
                            self.ie_list[full_ie].append(extract_number_from_item(item[1]))
                        else:
                            self.ie_list[full_ie] = [extract_number_from_item(item[1])]

    def find_ie(self, ie, selected_release):

        for release_type in self.releases:
            if selected_release not in self.releases[release_type]:
                continue
            if not isinstance(ie, list):
                edited_ie = ie.replace("-", "_")
                for i in self.releases[release_type][selected_release]:
                    if i[-2] == edited_ie:
                        return i[-1]
                return None
            else:
                edited_ie_list = [ie_element.replace("-", "_") for ie_element in ie]
                ie_found = False
                for element_line in self.releases[release_type][selected_release]:
                    ie_found = True
                    ie_found = ie_found and edited_ie_list == element_line[:-1]
                    if ie_found:
                        return element_line[-1]
                if not ie_found:

                    return None
