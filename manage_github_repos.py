import os

from colorama import Fore, Style
from colorama import init as colorama_init
from git import InvalidGitRepositoryError, Repo
from prettytable import PrettyTable

# For GitPython https://gitpython.readthedocs.io/en/stable/intro.html

# TODO For now, it is assumed the git host server is GitHub

# TODO Use of colors assume dark (black) background

"""
    {
        "repo_url": "",
        "local_dir": "",
    },
"""


repos = [
    {
        "repo_url": "https://github.com/TorbenJakobsen/decimaldate",
        "local_dir": "decimaldate",
    },
    {
        "repo_url": "https://github.com/TorbenJakobsen/manage_configuration_with_stow",
        "local_dir": "manage_configuration_with_stow",
    },
    {
        "repo_url": "https://github.com/TorbenJakobsen/matrix_digital_rain",
        "local_dir": "matrix_digital_rain",
    },
    {
        "repo_url": "https://github.com/TorbenJakobsen/manage_github_repos",
        "local_dir": "manage_github_repos",
    },
    {
        "repo_url": "https://github.com/TorbenJakobsen/setup_fedora_linux_as_workstation",
        "local_dir": "setup_fedora_linux_as_workstation",
    },
    {
        "repo_url": "https://github.com/TorbenJakobsen/setup_terminal_and_shell",
        "local_dir": "setup_terminal_and_shell",
    },
]


def is_local_dir_managed(local_dir: str) -> bool:
    for r in repos:
        if r["local_dir"] == local_dir:
            return True
    return False


def clone_managed_repos() -> None:
    """
    _summary_
    """
    # EnvRepo(
    #    repo_url="https://github.com/TorbenJakobsen/manage_github_repos",
    #    local_dir="manage_github_repos",
    # )

    for r in repos:
        repo_url = r["repo_url"]
        local_dir = f'../{r["local_dir"]}'
        if not os.path.isdir(local_dir):
            print(f"Cloning into '{local_dir}'")
            _ = Repo.clone_from(repo_url, local_dir)


def table_for_print_repos() -> PrettyTable:
    """Return an empty table with captions and alignment."""

    # Table headers

    DIR: str = "Directory"
    IS_REPO: str = "?"
    MANAGED = "MAN"
    DIRTY_REPO: str = "Dty"
    HEADS = "Heads"
    UNTRACKED_FILES: str = "U"
    MODIFIED_FILES: str = "MOD"
    STAGED_FILES: str = "S"

    table = PrettyTable(
        [
            DIR,
            IS_REPO,
            MANAGED,
            DIRTY_REPO,
            HEADS,
            UNTRACKED_FILES,
            MODIFIED_FILES,
            STAGED_FILES,
        ]
    )
    table.align[DIR] = "l"
    table.align[IS_REPO] = "c"
    table.align[MANAGED] = "c"
    table.align[DIRTY_REPO] = "c"
    table.align[HEADS] = "l"
    table.align[UNTRACKED_FILES] = "r"
    return table


def print_repos(repos: list[str]) -> None:
    repo_table: PrettyTable = table_for_print_repos()

    for repo_name in repos:

        repo: Repo | None
        try:
            repo = Repo(f"/Users/torbenjakobsen/source/repos/Github/{repo_name}")
            # TODO Handle the need for absolute paths
            # TODO Handle hardcoded paths
        except InvalidGitRepositoryError:
            repo = None
        finally:
            is_valid_repo = repo is not None

        untracked_files = len(repo.untracked_files) if is_valid_repo else 0
        repo_heads = repo.heads if is_valid_repo else []
        head_names = sorted([h.name for h in repo_heads])
        active_branch = repo.active_branch.name if repo else ""
        a_head_names = [
            (
                f"{Fore.GREEN}{Style.BRIGHT}{hn}{Fore.RESET}"
                if hn == active_branch
                else f"{Fore.WHITE}{hn}{Fore.RESET}"
            )
            for hn in head_names
        ]

        staged_files = len(repo.index.diff("HEAD")) if repo else 0
        modified_files = len(repo.index.diff(None)) if repo else 0

        repo_table.add_row(
            [
                # Repo name
                (
                    f"{Fore.RED}{Style.BRIGHT}{repo_name}{Fore.RESET}"
                    if not is_valid_repo
                    else (
                        f"{Fore.YELLOW}{Style.BRIGHT}{repo_name}{Fore.RESET}"
                        if repo.is_dirty() or untracked_files
                        else f"{repo_name}"
                    )
                ),
                # IS_REPO
                (
                    f"{Fore.GREEN}{Style.BRIGHT}Y{Fore.RESET}"
                    if is_valid_repo
                    else f"{Fore.RED}{Style.BRIGHT}N{Fore.RESET}"
                ),
                # Managed
                ("M" if is_local_dir_managed(repo_name) else ""),
                # Dirty repo
                (
                    f"{Fore.RED}{Style.BRIGHT}D{Fore.RESET}"
                    if (repo and repo.is_dirty())
                    else ""
                ),
                #
                ", ".join(a_head_names),
                (
                    f"{Fore.RED}{Style.BRIGHT}{untracked_files}{Fore.RESET}"
                    if untracked_files
                    else ""
                ),
                str(modified_files) if modified_files else "",
                str(staged_files) if staged_files else "",
            ]
        )

    print(repo_table)


def main():
    colorama_init()

    clone_managed_repos()

    sorted_dirs: list[str] = sorted(next(os.walk(".."))[1], key=str.casefold)
    print_repos(sorted_dirs)


if __name__ == "__main__":
    main()
