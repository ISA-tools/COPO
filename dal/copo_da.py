__author__ = 'felix.shaw@tgac.ac.uk - 22/10/15'
import pymongo
from web.apps.web_copo.schemas.utils import data_utils
from dal.copo_base_da import DataSchemas

class Publication:

    def save_publication(self, autofields):
        schema = DataSchemas("COPO").get_ui_template()['copo']['publication']
        fields = data_utils.get_schema_fields(autofields, schema)
