__author__ = 'etuka'

import xml.etree.ElementTree as ET
from urllib.request import urlopen

import re

import web_copo.copo_maps.utils.lookup as lkup
import web_copo.copo_maps.ena.uimodels.object_model as om
import web_copo.copo_maps.ena.uimodels.ena_copo_config as ecc


class DataFormats:
    def __init__(self, schema):
        self.error_messages = []
        self.schema = schema.upper()

    # generates template for UI rendering
    def generate_ui_template(self):
        out_dict = om.OUT_DICT
        new_dict = self.merge_dicts(self.do_mapping_ena("INVESTIGATION_FILE"),
                                    self.do_mapping_ena("STUDY_SAMPLE_FILE"),
                                    self.do_mapping_ena("STUDY_ASSAY_GENOME_SEQ_FILE"),
                                    self.do_mapping_ena("STUDY_ASSAY_METAGENOME_SEQ_FILE")
                                    )
        if new_dict:
            out_dict = self.objectify(new_dict, out_dict)
            out_dict = self.purify(out_dict)
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

        new_dict = ecc.ELEMENTS[arm]
        current_dict = ecc.ELEMENTS[arm]

        root = tree.getroot()

        # get the namespace of the xml document
        ns = self.namespace(root)

        fields = tree.findall(".//{%s}field" % ns)

        for key, value in current_dict.items():
            attr = lkup.SCHEMAS[self.schema]['ATTRIBUTE_MAPPINGS']
            # initialise attributes as defined in lookup, maintain default ones defined in the model
            for k in attr:
                if k in value.keys() and current_dict[key][k]:
                    new_dict[key].update({k: current_dict[key][k]})
                else:
                    new_dict[key].update({k: ''})

            for f in iter(fields):
                # 'ref' key in the config dictionary defined to match 'header' attribute in the xml file
                try:
                    if f.get("header") == current_dict[key]["ref"]:
                        for k, v in attr.items():
                            # modify for file field
                            if f.get("is-file-field") == "true" and k == "control":
                                try:
                                    # no need retaining the mapping key
                                    del new_dict[key][k]
                                    new_dict[key].update({k: "file"})
                                except KeyError:
                                    pass
                            if not current_dict[key][k]:
                                if v or k == "option_values":
                                    if k == "option_values":
                                        # get list values
                                        if f.get("data-type") == "List":
                                            try:
                                                ls = f.findall(".//{%s}list-values" % ns)
                                                options_split = ls[0].text.split(",")
                                                new_dict[key].update({k: options_split})
                                            except IndexError:
                                                pass
                                    else:
                                        new_dict[key].update({k: f.get(v)})
                                        if v == "data-type" and f.get(v) in lkup.SCHEMAS[self.schema][
                                            'CONTROL_MAPPINGS'].keys():
                                            new_dict[key].update(
                                                {k: lkup.SCHEMAS[self.schema]['CONTROL_MAPPINGS'][f.get(v)]})

                except KeyError:
                    pass

        return new_dict

    def objectify(self, source_dict, output_dict):
        new_dict = source_dict
        out_dict = output_dict

        for key in new_dict:
            # no need retaining the mapping key
            if "ref" in new_dict[key]:
                del new_dict[key]["ref"]

            # remove option_values for non select elements
            if not new_dict[key]["control"] == "select":
                del new_dict[key]["option_values"]

            new_dict[key].update({'id': key})
            key_split = key.split(".")

            if len(key_split) >= 2:
                out_dict = self.set_model_fields(out_dict, key_split[:-1], new_dict[key])

        return out_dict

    def set_model_fields(self, d, keys, val):
        out = d
        for k in keys[:-1]:
            out = out[k]
        out[keys[-1]]["fields"].append(val)
        return d

    def merge_dicts(self, *dict_args):
        result = {}

        for dictionary in dict_args:
            if dictionary:
                result.update(dictionary)

        return result

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
