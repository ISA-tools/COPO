__author__ = 'etuka'

from datetime import datetime

import pexpect
import os
import re

from services import *
from dal import ObjectId
from master_settings import BASE_DIR
from dal.mongo_util import get_collection_ref
import web.apps.web_copo.copo_maps.utils.lookup as lkup
import web.apps.web_copo.copo_maps.utils.data_utils as d_utils


class AsperaTransfer:
    def __init__(self):
        path_to_json = lkup.SCHEMAS["COPO"]['PATHS_AND_URIS']['ASPERA_COLLECTION']
        db_template = d_utils.json_to_pytype(path_to_json)

        AsperaCollection = get_collection_ref("AsperaCollections")
        self.aspera_transfer_id = AsperaCollection.insert(db_template)

    # sets up database collection to help in tracking the upload progress
    def get_transfer_token(self):
        return self.aspera_transfer_id

    def do_aspera_transfer(aspera_transfer_id):
        asperacollections = get_collection_ref("AsperaCollections")

        document = list(asperacollections.find({"_id": ObjectId(aspera_transfer_id)}, {"file": 1}))
        file_path = document[0]['file']

        user_name = REPOSITORIES['ENA']['credentials']['user_token']
        password = REPOSITORIES['ENA']['credentials']['password']
        remote_path = REPOSITORIES['ENA']['credentials']['remote_path']
        cmd = "./ascp -d -QT -l300M -L- {file_path!s} {user_name!s}:{remote_path!s}".format(**locals())
        path2library = os.path.join(BASE_DIR, REPOSITORIES['ENA']['resource_path'])

        os.chdir(path2library)

        thread = pexpect.spawn(cmd, timeout=None)
        thread.expect(["assword:", pexpect.EOF])
        thread.sendline(password)

        cpl = thread.compile_pattern_list([pexpect.EOF, '(.+)'])

        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0:  # EOF! possible error if encountered before transfer completion
                print("Process termination - check exit status!")
                break
            elif i == 1:
                pexp_match = thread.match.group(1)

                if "ETA" in pexp_match.decode("utf-8"):
                    pct_match = re.search('(\d+%)', pexp_match.decode("utf-8"))

                    if pct_match:
                        pct_val = pct_match.group(1)
                        print("completed", pct_val)
                        asperacollections.update({
                            "_id": self.aspera_transfer_id
                        }, {"$set": {"pct_complete": pct_val.rstrip("%")}}
                        )

                if "LOG FASP Transfer Stop" in pexp_match.decode("utf-8"):
                    exit_status = ""
                    transfer_rate = ""
                    elapsed_time = ""
                    bytes_lost = ""
                    file_size = ""
                    tokens = pexp_match.decode("utf-8").split(" ")
                    for token in tokens:
                        token_of_interest = token.split("=")
                        if token_of_interest[0] == "status":
                            exit_status = token_of_interest[1]
                            # print("Exit status: %s" % exit_status)
                        elif token_of_interest[0] == "rate":
                            transfer_rate = token_of_interest[1]
                            # print("Average transfer rate : %s" % transfer_rate)
                        elif token_of_interest[0] == "elapsed":
                            elapsed_time = token_of_interest[1]
                            # print("Elapsed time : %s" % elapsed_time)
                        elif token_of_interest[0] == "loss":
                            bytes_lost = token_of_interest[1]
                            # print("Bytes lost : %s" % bytes_lost)
                        elif token_of_interest[0] == "size":
                            file_size = token_of_interest[1]
                            # print("File size (bytes): %s" % file_size)

                        asperacollections.update({
                            "_id": aspera_transfer_id
                        }, {"$set": {"exit_status": exit_status,
                                     "completed_on": datetime.now(),
                                     "transfer_rate": transfer_rate,
                                     "elapsed_time": elapsed_time,
                                     "bytes_lost": bytes_lost,
                                     "file_size (bytes)": file_size}}
                        )

        thread.close()
