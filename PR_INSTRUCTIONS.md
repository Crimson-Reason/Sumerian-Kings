# Push & Pull Request (PR) Instructions

This file contains step-by-step instructions to push changes to your fork and create a Pull Request.

1) Prepare authentication

- Option A: HTTPS + Git Credential Manager (recommended for Windows)
  - Create a Personal Access Token (PAT) on GitHub with `repo` scope.
  - When `git push` prompts for credentials, use your GitHub username and the PAT as the password.

- Option B: SSH
  - Generate an SSH key on your machine with `ssh-keygen` and add the public key to GitHub (Settings → SSH and GPG keys).
  - Ensure `ssh -T git@github.com` works before pushing.

2) Push your branch to your fork

Use the helper script `push_to_fork.ps1` from the repo root. Examples:

PowerShell (from repo root):
```
.\push_to_fork.ps1                 # pushes current branch to 'fork' remote if present, otherwise 'origin'
.\push_to_fork.ps1 -ForkUrl https://github.com/your-username/Sumerian-Kings.git
.\push_to_fork.ps1 -Branch feature-xyz
```

3) Create the Pull Request

- Option A: Open the URL printed by the script in your browser and follow the GitHub PR UI.
- Option B: Use the GitHub CLI (if you have it installed):
```
gh pr create --base main --head your-username:feature-xyz --title "Describe change" --body "Longer description"
```

4) Notes & troubleshooting

- If you get `Permission denied (publickey)` over SSH, add your SSH public key to GitHub or use the HTTPS+PAT approach.
- If `git push` fails with credential errors, re-run the push and ensure Git Credential Manager prompts you.
- If you need to push to a new remote name, pass `-ForkUrl` to `push_to_fork.ps1` to add/update the `fork` remote.

If you want, I can also prepare the PR description template and a list of files changed to paste into the PR body.
