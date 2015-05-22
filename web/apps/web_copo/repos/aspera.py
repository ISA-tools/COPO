__author__ = 'etuka'

from project_copo.settings.repo_settings import *
from project_copo.settings.settings import *
from apps.web_copo.mongo.mongo_util import *
import pexpect
from datetime import datetime


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

    cpl = thread.compile_pattern_list([pexpect.EOF, '(\d+%)'])

    while True:
        i = thread.expect_list(cpl, timeout=None)
        if i == 0:  # EOF! Possible error point if encountered before transfer completion
            print("the sub process exited")
            break
        elif i == 1:
            trans_pct = thread.match.group(1)
            trans_pct = trans_pct.decode("utf-8")
            print("%s completed" % trans_pct)
            pct_val = trans_pct.rstrip("%")

            asperacollections.update({
                "_id": aspera_transfer_id
            }, {"$set": {"pct_complete": pct_val}}
            )

            if int(pct_val) == 100:
                exit_status = "success"
                # exit_status represents the transfer/completion status:
                # '' for running, 'success', 'failed'
                asperacollections.update({
                    "_id": aspera_transfer_id
                }, {"$set": {"exit_status": exit_status, "completed_on": datetime.now()}}
                )
                print(exit_status)
                break
    thread.close()