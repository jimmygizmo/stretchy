
import os
from dotenv import load_dotenv
import runpod
import random
import threading
import time


simultaneous_clients = 12  # Int count of parallel clients
startup_delay_range = 8000  # miliseconds. Minimum is 100 ms delay, up to this many milliseconds delay.

load_dotenv()
runpod_api_key = os.getenv("STRETCHYKEY")
runpod.api_key = runpod_api_key

endpoint_id = "26l5fgd0x8pugz"  # The dynamically-generated ID, from the time of endpoint creation

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
def run_synchronous(thread_id):
    rand_start_delay_seconds = random.randint(100, startup_delay_range)/1000
    print(f"#### Starting endpoint.run_sync thread. ID: {thread_id}   Start-delay: {rand_start_delay_seconds} seconds")
    time.sleep(random.randint(100, startup_delay_range)/1000)
    try:
        run_request = endpoint.run_sync(
            {
                "prompt": f"job input (prompt) from rpagent-load, thread: {thread_id}",
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

    for x in range(simultaneous_clients):
        thread = threading.Thread(target=run_synchronous, args=(x,))
        thread.start()
        load_threads.append(thread)


if __name__ == "__main__":
    main()
    # health_check()


##
#


# Python Asyncio
# https://docs.python.org/3/library/asyncio.html


##
#
