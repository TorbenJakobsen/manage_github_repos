import os

from colorama import Fore, Style
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
    HEAD = "Head"
    UNTRACKED_FILES: str = "U"

    table = PrettyTable(
        [
            DIR,
            IS_REPO,
            DIRTY_REPO,
            HEADS,
            HEAD,
            UNTRACKED_FILES,
        ]
    )
    table.align[DIR] = "l"
    table.align[IS_REPO] = "c"
    table.align[DIRTY_REPO] = "c"
    table.align[HEADS] = "l"
    table.align[HEAD] = "l"
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
        heads = repo.heads if is_valid_repo else []
        head_names = [h.name for h in heads]
        # a_head_names = [h. for h in heads]

        repo_table.add_row(
            [
                # Repo name
                repo_name if is_valid_repo else f"{Fore.RED}{repo_name}{Fore.RESET}",
                # IS_REPO
                "X" if is_valid_repo else "",
                # Dirty repo
                f"{Fore.RED}D{Fore.RESET}" if (repo and repo.is_dirty()) else "",
                #
                ",".join(head_names),
                str(repo.head) if is_valid_repo else "",
                f"{Fore.RED}{untracked_files}{Fore.RESET}" if untracked_files else "",
            ]
        )

    print(repo_table)


def main():
    colorama_init()
    sorted_dirs: list[str] = sorted(next(os.walk(".."))[1], key=str.casefold)
    print_repos(sorted_dirs)


if __name__ == "__main__":
    main()
