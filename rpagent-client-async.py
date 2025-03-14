
import asyncio
import aiohttp
import os
from dotenv import load_dotenv
import runpod
from runpod import AsyncioEndpoint, AsyncioJob


# TODO: Continue more examples on this page:
# https://docs.runpod.io/sdks/python/endpoints
# TODO: Streaming, Status, Cancel + timeout, Purge queue

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # For Windows users.

load_dotenv()
runpod_api_key = os.getenv("STRETCHYKEY")
runpod.api_key = runpod_api_key

endpoint_id = "26l5fgd0x8pugz"  # The dynamically-generated ID, from the time of endpoint creation

# input_payload = {"prompt": "Hello, World! This is the prompt payload."}

# NOTE: Passing this mock_return like this does get to the correct place in the rpagent async_generator_handler
#           although I am not seeing anything but an empty array in the response, but that could be other factors.
input_payload = {
    "prompt": "Hello, World! This is the prompt payload.",
    "mock_delay": 1,
    "mock_return": [
            'a beautiful high resolution image of the sunset',
            'a beautiful abstract drawing of the sunset in pastel colors',
            'a beautiful, award-winning image of the sunset over rolling green hills',
            'a masterpiece painting of the sunset over green hillsides. vibrant colors',
        ],
}


async def main():
    async with aiohttp.ClientSession() as session:
        endpoint = AsyncioEndpoint(endpoint_id, session)
        job: AsyncioJob = await endpoint.run(input_payload)

        # Polling job status
        while True:
            status = await job.status()
            print(f"Current job status: {status}")
            if status == "COMPLETED":
                output = await job.output()
                print("Job output:", output)
                break  # Exit the loop once the job is completed.
            elif status in ["FAILED"]:
                print("Job failed or encountered an error.")

                break
            else:
                print("Job in queue or processing. Waiting 3 seconds...")
                await asyncio.sleep(3)  # Wait for 3 seconds before polling again


# This is not async:
def health_check():
    endpoint = runpod.Endpoint(endpoint_id)  # The dynamically-generated ID, from the time of endpoint creation
    health_result = endpoint.health()
    print(f"health_result: {health_result}")


if __name__ == "__main__":
    asyncio.run(main())
    health_check()


##
#


# TODO: Continue more examples on this page:
# https://docs.runpod.io/sdks/python/endpoints


# Python Asyncio
# https://docs.python.org/3/library/asyncio.html


##
#
