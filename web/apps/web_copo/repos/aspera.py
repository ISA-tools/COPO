__author__ = 'etuka'

from datetime import datetime
import time
import pexpect
import os
import re
import sys

from services import *
from dal import ObjectId
from master_settings import BASE_DIR
from dal.mongo_util import get_collection_ref


class AsperaTransfer:
    def __init__(self, transfer_token):
        self.transfer_token = transfer_token
        self.do_aspera_transfer()

    def do_aspera_transfer(self):
        # reference to the database collection
        AsperaCollection = get_collection_ref("AsperaCollections")


        # test start
        for i in range(21):
            if i > 0:
                time.sleep(1)
            print("executing token: " + str(self.transfer_token) + " " + str(i * 2))
            AsperaCollection.update(
                {"_id": self.transfer_token},
                {"$set": {"transfer_status": "transferring",
                          "pct_completed": str(i * 5)
                          }
                 })
        print("finished for: " + str(self.transfer_token))
        AsperaCollection.update(
            {"_id": self.transfer_token},
            {"$set": {"transfer_status": "completed"
                      }
             })

        # test end



        # file_path = ""
        # doc = AsperaCollection.find_one({"_id": self.transfer_token})
        # if doc:
        #     file_path = doc["file_path"]
        # else:
        #     # error message, store in db, and abort process
        #     pass
        #
        # user_name = REPOSITORIES['ASPERA']['user_token']
        # password = REPOSITORIES['ASPERA']['password']
        # remote_path = REPOSITORIES['ASPERA']['remote_path']
        # cmd = "./ascp -d -QT -l300M -L- {file_path!s} {user_name!s}:{remote_path!s}".format(**locals())
        # path2library = os.path.join(BASE_DIR, REPOSITORIES['ASPERA']['resource_path'])
        #
        # os.chdir(path2library)
        #
        # thread = pexpect.spawn(cmd, timeout=None)
        # thread.expect(["assword:", pexpect.EOF])
        # thread.sendline(password)
        #
        # cpl = thread.compile_pattern_list([pexpect.EOF, '(.+)'])
        #
        # while True:
        #     i = thread.expect_list(cpl, timeout=None)
        #     if i == 0:  # EOF! possible error if encountered before transfer completion
        #         print("Process termination - check exit status!")
        #         break
        #     elif i == 1:
        #         pexp_match = thread.match.group(1)
        #
        #         if "ETA" in pexp_match.decode("utf-8"):
        #             pct_match = re.search('(\d+%)', pexp_match.decode("utf-8"))
        #
        #             if pct_match:
        #                 pct_val = pct_match.group(1)
        #                 print("completed", pct_val.rstrip("%"))
        #                 AsperaCollection.update(
        #                     {"_id": self.transfer_token},
        #                     {"$set": {"pct_completed": pct_val.rstrip("%"),
        #                               "transfer_status": "transferring"
        #                               }
        #                      })
        #
        #         if "LOG FASP Transfer Stop" in pexp_match.decode("utf-8"):
        #             exit_status = ""
        #             transfer_rate = ""
        #             elapsed_time = ""
        #             bytes_lost = ""
        #             file_size = ""
        #             tokens = pexp_match.decode("utf-8").split(" ")
        #             for token in tokens:
        #                 token_of_interest = token.split("=")
        #                 if token_of_interest[0] == "status":
        #                     exit_status = token_of_interest[1]
        #                     # print("Exit status: %s" % exit_status)
        #                 elif token_of_interest[0] == "rate":
        #                     transfer_rate = token_of_interest[1]
        #                     # print("Average transfer rate : %s" % transfer_rate)
        #                 elif token_of_interest[0] == "elapsed":
        #                     elapsed_time = token_of_interest[1]
        #                     # print("Elapsed time : %s" % elapsed_time)
        #                 elif token_of_interest[0] == "loss":
        #                     bytes_lost = token_of_interest[1]
        #                     # print("Bytes lost : %s" % bytes_lost)
        #                 elif token_of_interest[0] == "size":
        #                     file_size = token_of_interest[1]
        #                     # print("File size (bytes): %s" % file_size)
        #
        #                 AsperaCollection.update(
        #                     {"_id": self.transfer_token},
        #                     {"$set": {"transfer_status": exit_status,
        #                               "transfer_completed": str(datetime.now()),
        #                               "transfer_rate": transfer_rate,
        #                               "elapsed_time": elapsed_time,
        #                               "bytes_lost": bytes_lost,
        #                               "file_size(bytes)": file_size
        #                               }
        #                      })
        #
        # thread.close()
