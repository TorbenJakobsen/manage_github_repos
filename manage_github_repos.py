import os

from colorama import Fore, Style
from colorama import init as colorama_init
from git import InvalidGitRepositoryError, Repo
from prettytable import PrettyTable
from pydantic_settings import BaseSettings, SettingsConfigDict

# For GitPython https://gitpython.readthedocs.io/en/stable/intro.html


def table_for_print_repos() -> PrettyTable:
    """Return an empty table with captions and alignment."""

    DIR: str = "Directory"
    IS_REPO: str = "?"
    UNTRACKED_FILES: str = "U"

    table = PrettyTable(
        [
            DIR,
            IS_REPO,
            UNTRACKED_FILES,
        ]
    )
    table.align[DIR] = "l"
    table.align[IS_REPO] = "c"
    table.align[UNTRACKED_FILES] = "r"
    return table


def print_repos(repos: list[str]) -> None:
    repo_table: PrettyTable = table_for_print_repos()

    for repo_name in repos:

        repo: Repo | None
        try:
            repo = Repo(f"/Users/torbenjakobsen/source/repos/Github/{repo_name}")
        except InvalidGitRepositoryError:
            repo = None
        finally:
            is_valid_repo = repo is not None

        untracked_files = len(repo.untracked_files) if is_valid_repo else 0

        repo_table.add_row(
            [
                repo_name,
                "X" if is_valid_repo else "",
                str(untracked_files) if untracked_files else "",
            ]
        )

    print(repo_table)


def main():
    sorted_dirs: list[str] = sorted(next(os.walk(".."))[1], key=str.casefold)

    print_repos(sorted_dirs)


if __name__ == "__main__":
    main()
