import os

from colorama import Fore, Style
from colorama import init as colorama_init
from git import InvalidGitRepositoryError, Repo
from prettytable import PrettyTable

# For GitPython https://gitpython.readthedocs.io/en/stable/intro.html

# TODO For now, it is assumed the git host server is GitHub

# TODO Use of colors assume dark (black) background


def read_repos_from_file(filename: str) -> list[dict[str, str]]:
    with open(filename) as f:
        lines: list[str] = [
            line
            for line in [line.strip() for line in f]
            if not line.startswith("#")  # no comments
            if not len(line) == 0  # no empty lines
        ]
        return [
            {"local_dir": t[0], "repo_url": t[1]}
            for t in [line.split(",") for line in lines]
        ]


REPOS: list[dict[str, str]] = read_repos_from_file("repos.cfg")


def is_local_dir_managed(local_dir: str) -> bool:
    for r in REPOS:
        if r["local_dir"] == local_dir:
            return True
    return False


def clone_managed_repos() -> None:
    for r in REPOS:
        repo_url = r["repo_url"]
        local_dir = f'../{r["local_dir"]}'
        if not os.path.isdir(local_dir):
            print(f"Cloning into '{local_dir}'")
            repo_clone = Repo.clone_from(repo_url, local_dir)


def table_for_print_repos() -> PrettyTable:
    """Return an empty table with captions and alignment."""

    # Table headers

    DIR: str = "Directory"
    IS_REPO: str = "?"
    MANAGED = "Man"
    DIRTY_REPO: str = "Dty"
    HEADS = "Heads"
    UNTRACKED_FILES: str = "Unt"
    MODIFIED_FILES: str = "Mod"
    STAGED_FILES: str = "Stg"

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
    table.align[MODIFIED_FILES] = "r"
    table.align[STAGED_FILES] = "r"
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
                (
                    f"{Fore.GREEN}{Style.BRIGHT}M{Fore.RESET}"
                    if is_local_dir_managed(repo_name)
                    else ""
                ),
                # Dirty repo
                (
                    f"{Fore.YELLOW}{Style.BRIGHT}D{Fore.RESET}"
                    if (repo and repo.is_dirty())
                    else ""
                ),
                # Untracked
                ", ".join(a_head_names),
                (
                    f"{Fore.YELLOW}{Style.BRIGHT}{untracked_files}{Fore.RESET}"
                    if untracked_files
                    else ""
                ),
                # Modified
                (
                    f"{Fore.YELLOW}{Style.BRIGHT}{modified_files}{Fore.RESET}"
                    if modified_files
                    else ""
                ),
                # Staged
                (
                    f"{Fore.YELLOW}{Style.BRIGHT}{staged_files}{Fore.RESET}"
                    if staged_files
                    else ""
                ),
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
