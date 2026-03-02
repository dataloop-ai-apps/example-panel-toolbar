import sys
import os

import dtlpy as dl
from dotenv import load_dotenv

load_dotenv()

env = os.getenv('DTLPY_ENV')
token = os.getenv('DTLPY_TOKEN')

if not env or not token:
    print("Error: DTLPY_ENV and DTLPY_TOKEN must be set in .env")
    sys.exit(1)

dl.setenv(env)
dl.login_token(token)
print(f"Authenticated to Dataloop ({env})")
