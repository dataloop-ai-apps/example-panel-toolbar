import sys
import os
import argparse

import dtlpy as dl
from dotenv import load_dotenv

example_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(example_dir, '.env'))
os.chdir(example_dir)

parser = argparse.ArgumentParser(description='Install Dataloop app in project')
parser.add_argument('-project_id', '--project_id', help='Project ID where the app will be installed')
args = parser.parse_args()

project_id = args.project_id or os.getenv('DTLPY_PROJECT_ID')
if not project_id:
    print("Error: project_id not provided. Pass --project_id or set DTLPY_PROJECT_ID in .env")
    sys.exit(1)

env = os.getenv('DTLPY_ENV')
if env:
    dl.setenv(env)

if dl.token_expired():
    token = os.getenv('DTLPY_TOKEN')
    if not token:
        print("Error: Token expired and DTLPY_TOKEN not set. Copy env.example to .env and fill in values.")
        sys.exit(1)
    dl.login_token(token)

try:
    print(f"Getting project: {project_id}")
    project = dl.projects.get(project_id=project_id)
    print(f"Project found: {project.name}")

    publish_dir = os.getcwd()
    print(f"\nPublishing DPK from: {publish_dir}")
    print("Contents:")
    for item in sorted(os.listdir(publish_dir)):
        kind = "dir " if os.path.isdir(os.path.join(publish_dir, item)) else "file"
        print(f"  [{kind}] {item}")
    print()
    dpk = project.dpks.publish()
    print(f"DPK published: {dpk.display_name} v{dpk.version}")

    try:
        print("Checking if app already exists...")
        app = project.apps.get(app_name=dpk.display_name)
        app.dpk_version = dpk.version
        app.update()
        print(f"App updated successfully: {app.name}")
    except dl.exceptions.NotFound:
        print("Installing new app...")
        app = project.apps.install(dpk=dpk, app_name=dpk.display_name)
        print(f"App installed successfully: {app.name}")

except dl.exceptions.NotFound:
    print(f"Error: Project with ID '{project_id}' not found")
    sys.exit(1)
except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)
