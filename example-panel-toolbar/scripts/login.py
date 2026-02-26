import dtlpy as dl
from dotenv import load_dotenv
import os
load_dotenv()

env =  os.getenv('DTLPY_ENV')
token = os.getenv('DTLPY_TOKEN')

dl.setenv(env)
dl.login_token(token)
