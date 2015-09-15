import json

__author__ = 'etuka'

import re
import itertools
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import web.apps.web_copo.uiconfigs.utils.lookup as lkup
import web.apps.web_copo.uiconfigs.ena.uimodels.ena_copo_config as ecc


class DataFormats:
    def __init__(self, schema):
        self.error_messages = []
        self.schema = schema.upper()

    # generates template for UI rendering
    def generate_ui_template(self):
        out_dict = self.json_to_pytype(ecc.MODEL_FILES["ISA_OBJECT_MODEL"])

        new_list = list(itertools.chain(self.do_mapping_ena("INVESTIGATION_FILE"),
                                        self.do_mapping_ena("STUDY_SAMPLE_FILE"),
                                        self.do_mapping_ena("STUDY_ASSAY_GENOME_SEQ_FILE"),
                                        self.do_mapping_ena("STUDY_ASSAY_METAGENOME_SEQ_FILE")
                                        ))

        if new_list:
            out_dict = self.objectify(new_list, out_dict)
            out_dict = {"status": "success", "data": out_dict}
        else:
            out_dict = {}
            out_dict = {"status": "failed", "messages": self.error_messages, "data": out_dict}

        return out_dict

    def do_mapping_ena(self, arm):
        try:
            tree = ET.parse(urlopen(lkup.SCHEMAS[self.schema]['PATHS_AND_URIS'][arm]))
        except:
            self.error_messages.append(
                "Possible Network Error: Cannot access remote config resource:" +
                lkup.SCHEMAS[self.schema]['PATHS_AND_URIS'][arm] + "!")
            return

        new_list = self.json_to_pytype(ecc.CONFIG_FILES[arm])
        current_list = new_list

        root = tree.getroot()

        # get the namespace of the xml document
        ns = self.namespace(root)

        fields = tree.findall(".//{%s}field" % ns)

        for elem_dict in current_list:
            if "ref" not in elem_dict or "id" not in elem_dict:
                continue

            # get index and retain for accessing copy element in new_list
            indx = new_list.index(elem_dict)
            attr = lkup.SCHEMAS[self.schema]['ATTRIBUTE_MAPPINGS']
            # assign attributes defined in lkup, maintain default ones defined in the model
            for k in attr:
                if k not in elem_dict.keys():
                    new_list[indx][k] = ""

            for f in iter(fields):
                # 'ref' key in the config is defined to match 'header' attribute in the ISA xml
                if f.get("header") == elem_dict["ref"]:

                    # modify for file fields
                    if f.get("is-file-field") == "true":
                        new_list[indx]["control"] = "file"

                    # handle list values
                    if f.get("data-type") == "List":
                        try:
                            ls = f.findall(".//{%s}list-values" % ns)
                            options_split = ls[0].text.split(",")
                            new_list[indx]["option_values"] = options_split
                        except IndexError:
                            pass

                    for k, v in attr.items():
                        if not new_list[indx][k]:
                            new_list[indx][k] = f.get(v)

                            if v == "data-type" and f.get(v) in lkup.SCHEMAS[self.schema]['CONTROL_MAPPINGS'].keys():
                                new_list[indx][k] = lkup.SCHEMAS[self.schema]['CONTROL_MAPPINGS'][f.get(v)]

        return new_list

    def objectify(self, source_list, output_dict):
        new_list = source_list
        out_dict = output_dict

        for elem_dict in new_list:
            # no need retaining the mapping key
            if "ref" in elem_dict:
                del elem_dict["ref"]

            # remove option_values for non select elements
            if not elem_dict["control"] == "select":
                del elem_dict["option_values"]

            # set all null fields to ""
            for k, v in elem_dict.items():
                if not v:
                    elem_dict[k] = ""

            key_split = elem_dict["id"].split(".")

            if len(key_split) >= 2:
                out_dict = self.set_model_fields(out_dict, key_split[:-1], elem_dict)

        return out_dict

    def set_model_fields(self, d, keys, val):
        out = d
        for k in keys[:-1]:
            out = out[k]
        out[keys[-1]]["fields"].append(val)
        return d

    def purify(self, out_dict):
        for k, v in out_dict.items():
            if isinstance(v, dict):
                self.purify(v)
            elif isinstance(v, list):
                # de-duplicate fields list
                new_list = v
                found_list = []
                for idx, val in enumerate(new_list):
                    if val["id"] in found_list:
                        del v[idx]
                    else:
                        found_list.append(val["id"])
        return out_dict

    def namespace(self, element):
        match = re.search(r'\{(.+)\}', element.tag)
        return match.group(1) if match else ''

    def json_to_pytype(self, path_to_json):
        data = ""
        with open(path_to_json, encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
        return data
