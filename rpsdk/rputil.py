#! /usr/bin/env python

import os
from dotenv import load_dotenv
import runpod
# I noticed that runpod.erroor needs to be imported independently. Possibly, the runpod module needs a small fix.
import runpod.error
# NOTE: Simply using "import runpod" SHOULD work for runpod.error, but the runpod module's __init__.py might need
# adjustment or a correct __all__ list. NOTE: My IDE is inconsistently showing the "import runpod" as used and not
# used, so something is incorrect in the __init__.py or elsewhere I suspect.
import json


# TODO: Find out documented limits on max workers etc. In some of our tests we will attempt to exceed that.
#         Try different configurations of min, max (spare) workers etc.
# TODO: UPDATE: My account indicates "0/20 Workers Deployed", strongly suggesting I have a limit of 20.


load_dotenv()
# This load_dotenv() will find the first .env file, moving up the directories.
# The .env file will be at the project root, where it is protected from repo-addition by .gitignore

# runpod_api_key = os.getenv("RUNPOD_API_KEY")
runpod_api_key = os.getenv("STRETCHYKEY")
# print(runpod_api_key)

runpod.api_key = runpod_api_key


################  FETCH ALL ENDPOINTS  ################
endpoints = runpod.get_endpoints()
print(endpoints)


################  FETCH ALL AVAILABLE GPUs  ################
gpus = runpod.get_gpus()
print(json.dumps(gpus, indent=2))
# EXAMPLE RETURN FOR GPUs - ACTUAL LIST IS MUCH LONGER
# [
#     {
#     "id": "AMD Instinct MI300X OAM",
#     "displayName": "MI300X",
#     "memoryInGb": 192
#     },
#     {
#     "id": "NVIDIA A100 80GB PCIe",
#     "displayName": "A100 PCIe",
#     "memoryInGb": 80
#     },
#     {
#     "id": "NVIDIA A100-SXM4-80GB",
#     "displayName": "A100 SXM",
#     "memoryInGb": 80
#     },
# ]


################  CREATE TEMPLATE  ################
try:
    new_template = runpod.create_template(
        name="stretchy-rputil-test--template-1",
        image_name="runpod/base:0.1.0",
    )
    print(new_template)
    # EXAMPLE RETURN FOR SUCCESSFUL TEMPLATE CREATION
    # {
    #     'id': 'bdbtve7cas',
    #     'name': 'stretchy-rputil-test',
    #     'imageName': 'runpod/base:0.1.0',
    #     'dockerArgs': '',
    #     'containerDiskInGb': 10,
    #     'volumeInGb': 0,
    #     'volumeMountPath': '/workspace',
    #     'ports': '',
    #     'env': [],
    #     'isServerless': False,
    # }

except runpod.error.QueryError as err:
    print(err)
    print(err.query)


################  CREATE TEMPLATE AND ENDPOINT  ################
try:
    new_template = runpod.create_template(
        name="stretchy-rputil-test--template-2",
        image_name="runpod/base:0.6.2-cuda12.4.1",
        is_serverless=True,
    )
    print(new_template)
    # SEE ABOVE FOR EXAMPLE RETURN

    new_endpoint = runpod.create_endpoint(
        name="stretchy-rputil-test--endpoint-1",
        template_id=new_template["id"],
        gpu_ids="AMPERE_16",
        workers_min=0,
        workers_max=1,
    )
    print(new_endpoint)
    # EXAMPLE RETURN FOR SUCCESSFUL ENDPOINT CREATION
    # {
    #     'id': 'vf6ghygvsptrzs',
    #     'name': 'stretchy-rputil-test--endpoint-1',
    #     'templateId': '7uqbs86e0r',
    #     'gpuIds': 'AMPERE_16',
    #     'networkVolumeId': None,
    #     'locations': None,
    #     'idleTimeout': 5,
    #     'scalerType': 'QUEUE_DELAY',
    #     'scalerValue': 4,
    #     'workersMin': 0,
    #     'workersMax': 1,
    # }

except runpod.error.QueryError as err:
    print(err)
    print(err.query)


################  GET GPUs BY ID  ################
gpus = runpod.get_gpu("NVIDIA A100 80GB PCIe")
print(json.dumps(gpus, indent=2))

gpus = runpod.get_gpu("NVIDIA L40")
print(json.dumps(gpus, indent=2))

gpus = runpod.get_gpu("NVIDIA L40S")
print(json.dumps(gpus, indent=2))

gpus = runpod.get_gpu("NVIDIA GeForce RTX 4090")
print(json.dumps(gpus, indent=2))


##
#

