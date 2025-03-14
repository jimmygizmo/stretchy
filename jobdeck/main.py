
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
import time
import uuid
# Below here adding imports now for generating from the RP-SD endpoint
import os
from dotenv import load_dotenv
import requests


endpoint_id = '3qoede027zvklf'

load_dotenv()
runpod_api_key = os.getenv("STRETCHYKEY")
print(f"DEBUG: runpod_api_key: {runpod_api_key}")


app = FastAPI()

headers_rp = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {runpod_api_key}"
}


# Add CORS middleware to allow cross-origin requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only localhost:3000 (your React app)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Simulating a third-party LLM API
def simulate_llm_api(prompt: str):
    delay = random.randint(3, 8)  # Random delay between 3 and 8 seconds
    time.sleep(delay)
    return f"Simulated response for: {prompt}"


class JobRequest(BaseModel):
    prompt: str


class JobStatus(BaseModel):
    status: str
    result: str = None


def endpoint_start_job(prompt):
    request_body_jason = {
        'input': {"prompt": prompt}
    }
    endpoint_url = f"https://api.runpod.ai/v2/{endpoint_id}/run"
    response = requests.post(
        endpoint_url,
        headers=headers_rp,
        json=request_body_jason,
    )
    print(f"DEBUG: endpoint_start_job RESPONSE:")
    print(f"{response.json()}")
    return response.json()


def endpoint_get_status(rp_request_id):
    endpoint_url = f"https://api.runpod.ai/v2/{endpoint_id}/status/{rp_request_id}"
    response = requests.get(
        endpoint_url,
        headers=headers_rp,
    )
    print(f"DEBUG: endpoint_get_status RESPONSE:")
    print(f"{response.json()}")
    return response.json()


jobs = {}


@app.post("/start-job")
async def start_job(request: JobRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "in-progress", "result": None}

    # Simulate the job running asynchronously
    # asyncio.create_task(run_job(job_id, request.prompt))
    result_json = endpoint_start_job(request.prompt)

    rp_request_id = result_json["id"]
    print(f"DEBUG: rp_request_id:")
    print(f"{rp_request_id}")
    # return {"job_id": job_id}  # old code - delete soon
    rp_request_status = endpoint_get_status(rp_request_id)

    return result_json

# # NOT USING THIS RIGNT NOW
# async def run_job(job_id: str, prompt: str):
#     # Simulate a third-party LLM API call
#     # result = simulate_llm_api(prompt)
#     result = endpoint_start_job(prompt)
#
#     # Update the job status
#     jobs[job_id]["status"] = "completed"
#     jobs[job_id]["result"] = result


@app.get("/job-status/{rp_request_id}")
async def job_status(rp_request_id: str):
    # https://api.runpod.ai/v2/3qoede027zvklf/status/5734ff85-a776-4021-81d4-d069fbde2e22-u2

    # rp_request_id = "5734ff85-a776-4021-81d4-d069fbde2e22-u2"
    result_json = endpoint_get_status(rp_request_id)

    # job = jobs.get(job_id)
    # if job:
    #     return JobStatus(status=job["status"], result=job["result"])
    # else:
    #     return {"status": "error", "result": "Job not found"}

    return result_json

##
#

# {
#     'delayTime': 1568,
#     'executionTime': 3022,
#     'id': 'b80c3a65-399c-451a-a823-8257767164a1-u2',
#     'output': [{'image': 'iVBORw0--------IMAGE-DATA--------RK5CYII=', 'seed': 63372}],
#     'status': 'COMPLETED',
#     'workerId': '0ezc8z7hubzl60',
# }
#
# OUTPUT



