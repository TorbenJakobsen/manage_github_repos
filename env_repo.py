from pydantic import BaseModel, ConfigDict


class EnvRepo(BaseModel):
    """
    >>> EnvRepo(
    >>>     repo_url="https://github.com/TorbenJakobsen/manage_github_repos",
    >>>     local_dir="manage_github_repos"
    >>> )
    """

    repo_url: str
    local_dir: str
