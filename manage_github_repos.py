import os

from colorama import Back, Fore, Style
from colorama import init as colorama_init
from git import InvalidGitRepositoryError, Repo
from prettytable import PrettyTable
from pydantic_settings import BaseSettings, SettingsConfigDict

# For GitPython https://gitpython.readthedocs.io/en/stable/intro.html


# TODO Use of colors assume dark (black) background


def table_for_print_repos() -> PrettyTable:
    """Return an empty table with captions and alignment."""

    DIR: str = "Directory"
    IS_REPO: str = "?"
    DIRTY_REPO: str = "D"
    HEADS = "Heads"
    UNTRACKED_FILES: str = "U"

    table = PrettyTable(
        [
            DIR,
            IS_REPO,
            DIRTY_REPO,
            HEADS,
            UNTRACKED_FILES,
        ]
    )
    table.align[DIR] = "l"
    table.align[IS_REPO] = "c"
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
            ]
        )

    print(repo_table)


def main():
    colorama_init()
    sorted_dirs: list[str] = sorted(next(os.walk(".."))[1], key=str.casefold)
    print_repos(sorted_dirs)


if __name__ == "__main__":
    main()
