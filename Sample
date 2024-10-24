def get_current_branch(self, repo_path):
    """Get the current branch or commit hash if in detached HEAD."""
    try:
        # Try to get the symbolic branch name
        cmd = "git symbolic-ref --short HEAD"
        return self.run_command(cmd, cwd=repo_path)
    except RuntimeError as e:
        # If it fails, likely a detached HEAD, so fall back to the commit hash
        log.warning(f"Detached HEAD state in {repo_path}. Falling back to commit hash.")
        cmd = "git rev-parse --short HEAD"
        return self.run_command(cmd, cwd=repo_path)
