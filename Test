import subprocess
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import RLock, Lock
import logging
import multiprocessing
import time
import shlex
import shutil
from datetime import datetime

# Set up logging to log to both console and file
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class GitRepositoryManager:
    """
    A class to manage multiple Git repositories with support for cloning, checking out branches,
    pulling updates, handling submodules, and caching to improve efficiency.

    Attributes:
        repo_locks (dict): Dictionary of repository paths with corresponding reentrant locks.
        repo_lock_global (Lock): Global lock to synchronize access to repo_locks dictionary.
        timeout (int): Maximum time allowed for each Git command before timing out.
        retries (int): Number of retry attempts for each command upon failure.
        reference_repo (str): Path to a local Git reference repository for faster cloning.
        processed_repos (set): Set of repositories that have been processed, loaded from cache.
        submodule_cache (dict): Cache storing the latest submodule status per repository.
    """

    def __init__(self, log_level=logging.INFO, timeout=120, retries=3, log_file='git_repository_manager.log',
                 reference_repo=None):
        """
        Initialize the GitRepositoryManager with optional configurations for logging,
        command timeout, retry attempts, and a reference repository for cloning.

        Args:
            log_level (int): Logging level, e.g., logging.INFO or logging.DEBUG.
            timeout (int): Default timeout in seconds for each command.
            retries (int): Number of retry attempts per command.
            log_file (str): Path to the log file.
            reference_repo (str): Optional path to a reference repository to speed up cloning.
        """
        self.repo_locks = {}
        self.repo_lock_global = Lock()
        self.timeout = timeout
        self.retries = retries
        self.reference_repo = reference_repo
        self.processed_repos = set()
        self.submodule_cache = {}  # Cache to store submodule status for each repo
        log.setLevel(log_level)

        # Load processed repos from cache file to skip already processed ones
        self.load_processed_repos()

        # Set up logging handlers for console and file outputs
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file)
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        log.addHandler(console_handler)
        log.addHandler(file_handler)

    def load_processed_repos(self, state_file='processed_repos.json'):
        """
        Load previously processed repositories from a cache file to avoid redundant work.

        Args:
            state_file (str): Path to the JSON file that stores processed repository names.
        """
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                self.processed_repos = set(json.load(f))
        else:
            self.processed_repos = set()

    def save_processed_repos(self, state_file='processed_repos.json'):
        """
        Save the state of processed repositories to a JSON file for caching purposes.

        Args:
            state_file (str): Path to the JSON file to save processed repository names.
        """
        with open(state_file, 'w') as f:
            json.dump(list(self.processed_repos), f)

    def run_command(self, cmd, cwd=None, timeout=None):
        """
        Execute a shell command with retry logic, exponential backoff, and logging.

        Args:
            cmd (str): The command to execute.
            cwd (str, optional): Directory where the command will run.
            timeout (int, optional): Specific timeout for the command.

        Returns:
            str: Standard output of the command as a string.

        Raises:
            RuntimeError: If the command fails after all retry attempts.
        """
        attempt, backoff = 0, 1
        timeout = timeout or self.timeout
        while attempt < self.retries:
            try:
                log.debug(f"Running command: {cmd} in {cwd}")
                with subprocess.Popen(shlex.split(cmd), cwd=cwd, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE) as process:
                    stdout, stderr = process.communicate(timeout=timeout)
                    if process.returncode != 0:
                        raise subprocess.CalledProcessError(process.returncode, cmd, stderr)
                log.debug(f"Command output: {stdout.decode().strip()}")
                return stdout.decode().strip()
            except subprocess.CalledProcessError as e:
                log.error(f"Command failed: {e.stderr.decode().strip()} (Attempt {attempt + 1}/{self.retries})")
                if "fatal" in e.stderr.decode().lower():
                    raise RuntimeError(f"Fatal error during execution: {cmd}")
            except subprocess.TimeoutExpired:
                log.error(f"Command timed out: {cmd} in {cwd}")
            attempt += 1
            if attempt >= self.retries:
                raise RuntimeError(f"Command failed after {self.retries} attempts: {cmd}")
            time.sleep(backoff)
            backoff *= 2

    def get_current_branch(self, repo_path):
        """
        Determine the current branch of the repository or commit hash if in a detached HEAD state.

        Args:
            repo_path (str): Path to the repository.

        Returns:
            str: Current branch name or commit hash.
        """
        try:
            return self.run_command("git symbolic-ref --short HEAD", cwd=repo_path)
        except RuntimeError:
            detached_head = self.run_command("git rev-parse --short HEAD", cwd=repo_path)
            log.info(f"Repository {repo_path} is in detached HEAD state. Current commit: {detached_head}")
            return detached_head

    def is_up_to_date(self, repo_path):
        """
        Check if the repository is synchronized with its remote origin.

        Args:
            repo_path (str): Path to the repository.

        Returns:
            bool: True if up-to-date; False otherwise.
        """
        try:
            return self.run_command("git rev-parse @", cwd=repo_path) == self.run_command("git rev-parse @{u}",
                                                                                          cwd=repo_path)
        except subprocess.CalledProcessError as e:
            log.warning(e.stderr.decode().strip())
            return False

    def clone_repository(self, repo_url, repo_name, branch, depth=1):
        """
        Clone a repository if it does not already exist locally, using a reference repository if available.

        Args:
            repo_url (str): Repository URL.
            repo_name (str): Local name of the repository.
            branch (str): Branch to clone.
            depth (int, optional): Depth for shallow cloning.
        """
        repo_git_path = os.path.join(repo_name, ".git")
        if not os.path.exists(repo_git_path):
            log.info(f"Cloning {repo_url} (branch: {branch})")
            depth_arg = f"--depth {depth}" if depth else ""
            reference_arg = f"--reference {self.reference_repo}" if self.reference_repo and os.path.exists(
                self.reference_repo) else ""
            try:
                self.run_command(f"git clone {depth_arg} {reference_arg} --branch {branch} --single-branch {repo_url}")
            except RuntimeError:
                shutil.rmtree(repo_name, ignore_errors=True)
                raise
        else:
            log.info(f"Repository {repo_name} already exists. Skipping clone.")
            if not self.is_up_to_date(repo_name):
                log.info(f"Repository {repo_name} is not up to date. Attempting to pull latest changes.")
                self.run_command(f"git pull origin {branch}", cwd=repo_name)

    def checkout_and_pull(self, repo_path, branch):
        """
        Check out a branch and pull the latest changes if the repository is not up-to-date.

        Args:
            repo_path (str): Path to the repository.
            branch (str): Branch to check out.
        """
        with self._get_repo_lock(repo_path):
            current_branch = self.get_current_branch(repo_path)
            if current_branch != branch and not self.run_command(f"git branch --list {branch}", cwd=repo_path):
                log.error(f"Branch {branch} does not exist in {repo_path}. Attempting to fetch from remote.")
                self.run_command(f"git fetch origin {branch}", cwd=repo_path)
            if current_branch != branch:
                self.run_command(f"git checkout {branch}", cwd=repo_path)
            if not self.is_up_to_date(repo_path):
                self.run_command(f"git pull origin {branch}", cwd=repo_path)

    def initialize_submodules(self, repo_path):
        """
        Initialize and update submodules if they have changed since the last check.

        Args:
            repo_path (str): Path to the repository.

        Returns:
            bool: True if submodules were initialized or updated; False if no updates were needed.
        """
        if not os.path.exists(os.path.join(repo_path, '.gitmodules')):
            log.info(f"No submodules to initialize in {repo_path}")
            return False

        submodule_status = self.run_command("git submodule status", cwd=repo_path)
        if self.submodule_cache.get(repo_path) == submodule_status:
            log.info(f"Submodules are up to date for {repo_path}, skipping update.")
            return True

        log.info(f"Initializing and updating submodules for {repo_path}")
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.submit(self.run_command, "git submodule update --init --recursive --jobs 4", cwd=repo_path)

        self.submodule_cache[repo_path] = submodule_status
        return True

    def update_submodule(self, repo_path, submodule, branch="main"):
        """
        Update a specific submodule to the latest version on a given branch.

        Args:
            repo_path (str): Path to the repository.
            submodule (str): Name of the submodule.
            branch (str): Branch to update the submodule to.
        """
        submodule_path = os.path.join(repo_path, submodule.split()[1])
        lock_file = os.path.join(repo_path, f".git/modules/{submodule_path}/index.lock")

        log.info(f"Checking and updating submodule {submodule} in {repo_path}")

        with self._get_repo_lock(submodule_path):
            if os.path.exists(lock_file):
                log.info(f"Removing lock file {lock_file}")
                os.remove(lock_file)

            if not os.path.isdir(os.path.join(submodule_path, ".git")):
                log.warning(f"Submodule directory {submodule_path} is missing, forcing reinitialization")
                shutil.rmtree(submodule_path, ignore_errors=True)
                self.run_command("git submodule update --init --recursive --force", cwd=repo_path)

            log.debug(f"Fetching remote branches for submodule {submodule} in {repo_path}")
            if self.run_command(f"git ls-remote --heads origin {branch}", cwd=submodule_path):
                log.info(f"Checking out branch {branch} for submodule {submodule}")
                self.run_command(f"git checkout {branch}", cwd=submodule_path)

            if not self.is_up_to_date(submodule_path):
                log.info(f"Pulling latest changes for submodule {submodule} on branch {branch}")
                self.run_command(f"git pull origin {branch}", cwd=submodule_path)
            else:
                log.info(f"Submodule {submodule} is already up to date on branch {branch}")

    def process_repository(self, repo):
        """
        Process a repository by cloning, checking out, pulling, and initializing submodules.

        Args:
            repo (dict): Dictionary containing repository details such as URL and branch.
        """
        repo_url = repo['repo_url']
        branch = repo['branch']
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        timeout = repo.get('timeout', self.timeout)
        retries = repo.get('retries', self.retries)

        if repo_name in self.processed_repos:
            log.info(f"Repository {repo_name} already processed. Skipping.")
            return

        log.info(f"Processing repository: {repo_name} (branch: {branch})")
        self.clone_repository(repo_url, repo_name, branch)
        self.checkout_and_pull(repo_name, branch)
        self.initialize_submodules(repo_name)
        self.processed_repos.add(repo_name)

    def process_all_repositories(self, json_file):
        """
        Process all repositories listed in a JSON file concurrently.

        Args:
            json_file (str): Path to the JSON file containing repository details.
        """
        with open(json_file) as f:
            repositories = json.load(f)['repositories']
        max_workers = min(32, multiprocessing.cpu_count())
        failed_repos = []

        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="RepoWorker") as executor:
            futures = [executor.submit(self.process_repository, repo) for repo in repositories]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    failed_repos.append(str(e))
                    log.error(f"Error processing repository: {e}")

        if failed_repos:
            log.error(f"Failed to process the following repositories: {failed_repos}")

        self.save_processed_repos()

    def _get_repo_lock(self, repo_path):
        """
        Retrieve a lock for the specified repository path, creating one if necessary.

        Args:
            repo_path (str): Path to the repository.

        Returns:
            RLock: Reentrant lock for the repository path.
        """
        with self.repo_lock_global:
            if repo_path not in self.repo_locks:
                self.repo_locks[repo_path] = RLock()
        return self.repo_locks[repo_path]


if __name__ == "__main__":
    # Initialize the GitRepositoryManager with options for logging, timeout, retries, and reference repo
    manager = GitRepositoryManager(log_level=logging.DEBUG, timeout=120, retries=3, log_file='git_repo_manager.log',
                                   reference_repo='/path/to/reference/repo')

    # Process all repositories from the JSON configuration file
    manager.process_all_repositories('repositories.json')
