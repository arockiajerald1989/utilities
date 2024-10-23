import subprocess
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Lock to prevent concurrent access to the same repository or submodule
lock = Lock()

# Function to run shell commands with error handling
def run_command(cmd, cwd=None):
    try:
        process = subprocess.run(cmd, shell=True, check=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {cmd}\nError: {e.stderr.decode().strip()}")
        return None

# Function to check if a branch is already checked out
def get_current_branch(repo_path):
    cmd = "git symbolic-ref --short HEAD"
    return run_command(cmd, cwd=repo_path)

# Function to check if there are any changes to pull
def is_up_to_date(repo_path, branch):
    cmd = f"git fetch origin {branch} && git status"
    output = run_command(cmd, cwd=repo_path)
    return output and "Your branch is up to date" in output

# Function to clone a repository if not already cloned
def clone_repository(repo_url, repo_name):
    if not os.path.exists(repo_name):
        print(f"Cloning the repository: {repo_url}")
        run_command(f"git clone {repo_url}")
    else:
        print(f"Repository {repo_name} already exists. Skipping clone.")

# Function to checkout and pull a branch only if necessary
def checkout_and_pull(repo_path, branch):
    with lock:
        current_branch = get_current_branch(repo_path)
        if current_branch != branch:
            print(f"Checking out branch {branch} in {repo_path} (currently on {current_branch})")
            run_command(f"git checkout {branch}", cwd=repo_path)
        
        if not is_up_to_date(repo_path, branch):
            print(f"Pulling latest changes for branch {branch} in {repo_path}")
            run_command(f"git pull origin {branch}", cwd=repo_path)
        else:
            print(f"Branch {branch} in {repo_path} is up to date. Skipping pull.")

# Function to initialize submodules if necessary and update them
def update_submodule(submodule_path, branch):
    with lock:
        print(f"Processing submodule {submodule_path} on branch {branch}")
        current_branch = get_current_branch(submodule_path)

        if current_branch != branch:
            print(f"Checking out submodule branch {branch} (currently on {current_branch})")
            run_command(f"git checkout {branch}", cwd=submodule_path)
        
        if not is_up_to_date(submodule_path, branch):
            print(f"Pulling latest changes for submodule {submodule_path}")
            run_command(f"git pull origin {branch}", cwd=submodule_path)
        else:
            print(f"Submodule {submodule_path} is up to date. Skipping pull.")

# Function to initialize submodules only if they haven't been initialized
def initialize_submodules(repo_path):
    with lock:
        submodule_config = os.path.join(repo_path, '.gitmodules')
        if not os.path.exists(submodule_config):
            print(f"No submodules found in {repo_path}.")
            return False

        print(f"Initializing submodules for {repo_path}")
        run_command("git submodule update --init --recursive --jobs 4", cwd=repo_path)
        return True

# Function to handle the repository cloning, branch checkout, and submodule updating
def process_repository(repo):
    repo_url = repo['repo_url']
    branch = repo['branch']
    submodules = repo.get('submodules', [])
    
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    
    # Clone repository if not present
    clone_repository(repo_url, repo_name)

    # Checkout and pull the main repository
    print(f"Checking out and pulling the main repository {repo_name}")
    checkout_and_pull(repo_name, branch)
    
    # Initialize and process submodules if any
    if submodules and initialize_submodules(repo_name):
        print(f"Processing submodules for {repo_name}...")
        for submodule in submodules:
            update_submodule(os.path.join(repo_name, submodule['path']), submodule['branch'])
    else:
        print(f"No submodules to process for {repo_name} or they are already initialized.")

# Main function to read JSON and process all repositories concurrently
def main():
    # Load JSON data from file
    with open('repositories.json') as f:
        data = json.load(f)

    repositories = data['repositories']

    # Process each repository concurrently with a controlled number of threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_repository, repo) for repo in repositories]
        for future in as_completed(futures):
            future.result()  # Wait for each to complete

if __name__ == "__main__":
    main()
