
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
import time
import uuid


app = FastAPI()


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


jobs = {}


@app.post("/start-job")
async def start_job(request: JobRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "in-progress", "result": None}

    # Simulate the job running asynchronously
    asyncio.create_task(run_job(job_id, request.prompt))

    return {"job_id": job_id}


async def run_job(job_id: str, prompt: str):
    # Simulate a third-party LLM API call
    result = simulate_llm_api(prompt)

    # Update the job status
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result


@app.get("/job-status/{job_id}")
async def job_status(job_id: str):
    job = jobs.get(job_id)
    if job:
        return JobStatus(status=job["status"], result=job["result"])
    else:
        return {"status": "error", "result": "Job not found"}


##
#

