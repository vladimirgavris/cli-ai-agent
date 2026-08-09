# GitHub remotes

GitHub is a hosted service for Git repositories. A remote is the saved URL that
connects a local Git repository to a hosted repository.

Use `git remote -v` to inspect the fetch and push URLs without changing them.
Use `git push -u origin main` only after confirming that the repository exists
and the origin URL belongs to it.

"Repository not found" can mean that the URL is wrong, the repository does not
exist, or the signed-in account does not have access. Do not guess which one.