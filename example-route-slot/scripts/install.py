import sys
import os
import argparse

import dtlpy as dl


def main(project_id: str):
    example_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(example_dir)

    if dl.token_expired():
        dl.login()

    try:
        print(f"Getting project: {project_id}")
        project = dl.projects.get(project_id=project_id)
        print(f"Project found: {project.name}")

        publish_dir = os.getcwd()
        print(f"\nPublishing DPK from: {publish_dir}")

        # dtlpy reads .gitignore to decide what to exclude from the zip.
        # If there isn't one in the publish dir, create a temporary one so
        # node_modules and other non-code dirs don't bloat the upload.
        gitignore_path = os.path.join(publish_dir, '.gitignore')
        created_gitignore = False
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, 'w') as f:
                f.write('node_modules/\n.env\n__pycache__/\n.pytest_cache/\n.dataloop/\n')
            created_gitignore = True

        try:
            dpk = project.dpks.publish()
        finally:
            if created_gitignore:
                os.remove(gitignore_path)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Install Dataloop app in project')
    parser.add_argument('--project_id', required=False, help='Project ID where the app will be installed')
    args = parser.parse_args()
    project_id = args.project_id or input("Enter your Dataloop project ID: ").strip()
    if not project_id:
        print("Error: project ID is required")
        sys.exit(1)
    main(project_id)
