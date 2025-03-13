#! /usr/bin/env python

import os
from dotenv import load_dotenv
import runpod
import runpod.error
import json


# NOTE: My account indicates "0/20 Workers Deployed", strongly suggesting I have a limit of 20.


load_dotenv()
runpod_api_key = os.getenv("STRETCHYKEY")
runpod.api_key = runpod_api_key

env_dict = {
    "MOCK_RETURN": "This is the mock return value. This will be the job output.",
}

try:
    new_template = runpod.create_template(
        name="stretchy-rpagent--template-p1",
        image_name="docker.io/jimmygizmo/gizmorepo:stretchy-rpagent",
        # image_name="docker.io/jimmygizmo/gizmorepo:stretchy-stretchyagent",
        is_serverless=True,
        env=env_dict,
    )
    print(new_template)
    # SEE ABOVE FOR EXAMPLE RETURN

    new_endpoint = runpod.create_endpoint(
        name="stretchy-rpagent--endpoint-p1",
        template_id=new_template["id"],
        gpu_ids="AMPERE_16",
        workers_min=0,
        workers_max=1,
    )
    print(new_endpoint)


except runpod.error.QueryError as err:
    print(err)
    print(err.query)


################  FETCH ALL ENDPOINTS  ################
endpoints = runpod.get_endpoints()
print(endpoints)


##
#

# TODO: REFORMAT THIS. EXAMPLE OF SUCCESSFUL CREATION OF TEMPLATE, THEN OF ENDPOINT:
# {'id': '0jjdc1vdne', 'name': 'stretchy-rpagent--template-p1', 'imageName': 'docker.io/jimmygizmo/gizmorepo:stretchy-stretchyagent', 'dockerArgs': '', 'containerDiskInGb': 10, 'volumeInGb': 0, 'volumeMountPath': '/workspace', 'ports': '', 'env': [], 'isServerless': True}
# {'id': 'norx0cd12ei4ap', 'name': 'stretchy-rpagent--endpoint-p1', 'templateId': '0jjdc1vdne', 'gpuIds': 'AMPERE_16', 'networkVolumeId': None, 'locations': None, 'idleTimeout': 5, 'scalerType': 'QUEUE_DELAY', 'scalerValue': 4, 'workersMin': 0, 'workersMax': 1}

# EXAMPLE RETURN FROM .... CORRECT THIS ......
# TODO : CORRECT THIS DESCRIPTION. THIS IS THE RESULT FROM GET ALL ENDPOINTS.
# [
#     {'aiKey': 'GCX2TLBPM6BK2MM6T8M1B3P3URCAEGJ8VB76DSA4',
#      'gpuIds': 'AMPERE_16',
#      'id': 'vf6ghygvsptrzs',
#      'idleTimeout': 5,
#      'name': 'stretchy-rputil-test--endpoint-1',
#      'networkVolumeId': None,
#      'locations': None,
#      'scalerType': 'QUEUE_DELAY',
#      'scalerValue': 4,
#      'templateId': '7uqbs86e0r',
#      'type': 'QB',
#      'userId': 'user_2turitMc1r2D2TiS5ypfs032nT8',
#      'version': 2,
#      'workersMax': 1,
#      'workersMin': 0,
#      'workersStandby': 1,
#      'gpuCount': 1,
#      'env': None,
#      'createdAt': '2025-03-12T20:28:54.977Z',
#      'networkVolume': None,
#      },
#     {'aiKey': 'C426YIGQCPPROA9B6UCH4GOU7A4ENE6R907OB7E2',
#      'gpuIds': 'AMPERE_16', 'id': '1c8frrwyr6z95x',
#      'idleTimeout': 5,
#      'name': 'stretchy-rpagent--endpoint-p1',
#      'networkVolumeId': None,
#      'locations': None,
#      'scalerType': 'QUEUE_DELAY',
#      'scalerValue': 4,
#      'templateId': 'lp6791er8b',
#      'type': 'QB',
#      'userId': 'user_2turitMc1r2D2TiS5ypfs032nT8',
#      'version': 1,
#      'workersMax': 1,
#      'workersMin': 0,
#      'workersStandby': 1,
#      'gpuCount': 1,
#      'env': None,
#      'createdAt': '2025-03-12T22:05:52.714Z',
#      'networkVolume': None},
# ]


# ERROR EXAMPLE - PROCESS STILL EXITS WITH 0 - I USED THE SAME TEMPLATE ID/NAME
# Template
# name
# must
# be
# unique.
#
# mutation
# {
#     saveTemplate(
#         input: {
#         name: "stretchy-rpagent--template-p1", imageName: "docker.io/jimmygizmo/gizmorepo:stretchy-stretchyagent",
#         dockerArgs: "", containerDiskInGb: 10, volumeInGb: 0, ports: "", env: [], isServerless: true,
#         containerRegistryAuthId: "", startSsh: true, isPublic: false, readme: ""
#     }
# ) {
#     id
# name
# imageName
# dockerArgs
# containerDiskInGb
# volumeInGb
# volumeMountPath
# ports
# env
# {
#     key
# value
# }
# isServerless
# }
# }
#
# []
#
# Process
# finished
# with exit code 0
