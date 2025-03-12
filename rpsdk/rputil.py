
import os
from dotenv import load_dotenv
import runpod


# This will find the first .env file, moving up the directories.
# The .env file will be at the project root, where it is protected from repo-addition by .gitignore
load_dotenv()


runpod_api_key = os.getenv("RUNPOD_API_KEY")
print(runpod_api_key)

