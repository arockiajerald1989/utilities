def clone_repository(self, repo_url, repo_name, branch, depth=1):
    repo_git_path = os.path.join(repo_name, ".git")
    if not os.path.exists(repo_git_path):
        log.info(f"Cloning {repo_url} (branch: {branch})")
        depth_arg = f"--depth {depth}" if depth else ""
        reference_arg = f"--reference {self.reference_repo}" if self.reference_repo and os.path.exists(self.reference_repo) else ""
        
        try:
            self.run_command(f"git clone {depth_arg} {reference_arg} --branch {branch} --single-branch {repo_url} {repo_name}")
            
            # After cloning, explicitly check out the specified branch
            self.run_command(f"git checkout {branch}", cwd=repo_name)
        except RuntimeError:
            shutil.rmtree(repo_name, ignore_errors=True)
            raise
    else:
        log.info(f"Repository {repo_name} already exists. Skipping clone.")
        if not self.is_up_to_date(repo_name):
            log.info(f"Repository {repo_name} is not up to date. Attempting to pull latest changes.")
            self.run_command(f"git pull origin {branch}", cwd=repo_name)
