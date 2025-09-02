import dtlpy as dl
from dotenv import load_dotenv
import os
import argparse
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Install Dataloop app in project')
parser.add_argument('-project_id', '--project_id', required=True, help='Project ID where the app will be installed')
args = parser.parse_args()

env = os.getenv('DTLPY_ENV')
token = os.getenv('DTLPY_TOKEN')

dl.setenv(env)
dl.login_token(token)

try:
    print(f"Getting project: {args.project_id}")
    project = dl.projects.get(project_id=args.project_id)
    print(f"Project found: {project.name}")
    
    print("Publishing DPK...")
    dpk = project.dpks.publish()
    print(f"DPK published: {dpk.display_name} v{dpk.version}")
    
    try:
        # Update app in project
        print("Checking if app already exists...")
        app = project.apps.get(app_name=dpk.display_name)
        app.dpk_version = dpk.version
        app.update()
        print(f"App updated successfully: {app.name}")
    
    except dl.exceptions.NotFound:
        # Install app in project
        print("Installing new app...")
        app = project.apps.install(dpk=dpk, app_name=dpk.display_name)
        print(f"App installed successfully: {app.name}")

except dl.exceptions.NotFound as e:
    print(f"Error: Project with ID '{args.project_id}' not found")
    exit(1)
except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)