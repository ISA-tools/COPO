__author__ = 'felix.shaw@tgac.ac.uk - 26/08/15'

'''
This is the base class for ENA exporters. Inheriting classes should
provide implementations for the following methods.
'''

class base_exporter:

    # some sort of check that the provided json is valid
    def do_validate(self, collection_id):
        raise NotImplementedError()

    # the actual exporting code, this should
    # call one of ISA converters eventually
    def do_export(self, collection_id, dest):
        raise NotImplementedError()