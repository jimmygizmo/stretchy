
import os
from dotenv import load_dotenv
import runpod


load_dotenv()
runpod_api_key = os.getenv("STRETCHYKEY")
runpod.api_key = runpod_api_key

endpoint = runpod.Endpoint("2iuy5wqxgh0xvb")  # The dynamically-generated ID, from the time of endpoint creation


# ################  CHECK HEALTH ################
try:
    run_request = endpoint.health(timeout=60)
    print(run_request)
except TimeoutError:
    print("Health check timed out.")


# ################  SYNCHRONOUS (BLOCKING/SIMPLE) RUN ################
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


# ################  ASYNCHRONOUS (NON-BLOCKING/STATUS-CHECKING) RUN ################
input_payload = {
    "prompt": "This is the input payload; in this case, the prompt.",
}

run_request = endpoint.run(input_payload)
print(run_request)

# Initial check without blocking, useful for quick tasks
status = run_request.status()
print(f"Initial job status: {status}")

# TODO: Not clear exactly HOW this "waits" for the completion. I guess this below part is blocking, but obviously
#         a real implementation would be non-blocking and have an indepedent process/component watching for this
#         status change, meaning it would have a monitoring loop, delay or callback mechanism in place.
#         TODO: Look at the docs, etc to figure out exactly how the async results part works.
print(f"Now entering blocking wait until we get the COMPLETED status or time out (60 seconds).")
if status != "COMPLETED":
    # Polling with timeout for long-running tasks  # ** The implication is clearly that THIS PART IS BLOCKING. **
    # Anywhere you see a timeout like this set, it implies a blocking call. This is not the only way we know this is
    # blocking, as these comments around here discuss.
    output = run_request.output(timeout=60)
else:
    output = run_request.output()
print(f"Status: COMPLETED. Job output: {output}")


##
#

# EXAMPLE IN-QUEUE RESPONSE (ASYNC) FROM GUI, AS YOU WAIT FOR COMPLETED STATUS:
# {
#     "id": "7dbcdfbd-7e7f-459c-ac7f-10b02c0445d0-u1",
#     "status": "IN_QUEUE",
# }


# EXAMPLE REQUEST FROM THE GUI (ASYNC) (WHICH LOOKS IDENTICAL TO WHAT THIS FILE DOES)
# https://api.runpod.ai/v2/cm1symsjmy4op1/run
# POST:
# {
#     "input": {
#         "prompt": "Hello World",
#     },
# }


# REQUEST TO GET THE FINAL RESPONSE RESULTS (ASYNC) FROM THE GUI TEST:
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


# Python Asyncio
# https://docs.python.org/3/library/asyncio.html


##
#
