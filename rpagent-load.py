
import os
from dotenv import load_dotenv
import runpod
import random
import threading
import time


# TODO: "LOAD" in the filename indicates this will use thread spawning to allow the
#           client to multiplex and load the endpoint to force it to spawn more workers, up to the max.
#           We can take different load strategies, but just having some delay/duration to the jobs and then having
#           simultaneous jobs is all we need to do to cause the endpoint to expand its workers (in theory.)

simultaneous_clients = 10  # Int count of parallel clients
startup_delay_range = 4000  # miliseconds. Minimum is 100 ms delay, up to this many milliseconds delay.

load_dotenv()
runpod_api_key = os.getenv("STRETCHYKEY")
runpod.api_key = runpod_api_key

endpoint_id = "eo8uv310z6pt2c"  # The dynamically-generated ID, from the time of endpoint creation

input_payload = {"prompt": "Hello, World! This is the prompt payload."}

endpoint = runpod.Endpoint(endpoint_id)


# ################  CHECK HEALTH ################
def health_check():
    try:
        run_health_result = endpoint.health(timeout=60)
        print(f"health check result:\n{run_health_result}")
    except TimeoutError:
        print("Health check timed out.")


# ################  SYNCHRONOUS (BLOCKING/SIMPLE) RUN ################
def run_synchronous():
    time.sleep(random.randint(100, startup_delay_range))
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


def main():
    # run_synchronous()
    # health_check()

    load_threads = []

    for _ in range(simultaneous_clients):
        thread = threading.Thread(target=run_synchronous, args=())
        thread.start()
        load_threads.append(thread)


if __name__ == "__main__":
    main()
    # health_check()


##
#


# TODO: Continue more examples on this page:
# https://docs.runpod.io/sdks/python/endpoints


# Python Asyncio
# https://docs.python.org/3/library/asyncio.html


##
#
