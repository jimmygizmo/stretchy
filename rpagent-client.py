
import os
from dotenv import load_dotenv
import runpod


load_dotenv()
runpod_api_key = os.getenv("STRETCHYKEY")
runpod.api_key = runpod_api_key

endpoint = runpod.Endpoint("cm1symsjmy4op1")  # The dynamically-generated ID, from the time of endpoint creation


try:
    run_request = endpoint.health(timeout=60)
    print(run_request)
except TimeoutError:
    print("Health check timed out.")


try:
    run_request = endpoint.run_sync(
        {
            "prompt": "Hello, world!",
        },
        timeout=60,  # Timeout in seconds.
    )

    print(run_request)
except TimeoutError:
    print("Job timed out.")


##
#


# EXAMPLE REQUEST FROM THE GUI (WHICH LOOKS IDENTICAL TO WHAT THIS FILE DOES)
# https://api.runpod.ai/v2/cm1symsjmy4op1/run
# POST:
# {
#     "input": {
#         "prompt": "Hello World",
#     },
# }


# REQUEST TO GET THE FINAL RESPONSE RESULTS FROM THE GUI TEST:
# https://api.runpod.ai/v2/cm1symsjmy4op1/status/68877b47-6efd-4d0f-aa76-779d596b5eb5-u2

# THE GUI OFFERS THE SAME TEST REQUEST AND HERE IS THE RAW RESPONSE:
# {
#     "delayTime": 5227,
#     "executionTime": 70,
#     "id": "68877b47-6efd-4d0f-aa76-779d596b5eb5-u2",
#     "output": "Hello World!",
#     "status": "COMPLETED",
#     "workerId": "ysvg41tw8y9pja",
# }

