import os
from functools import total_ordering
from typing import Any, Self

from colorama import Fore, Style
from colorama import init as colorama_init
from git import InvalidGitRepositoryError, Repo
from prettytable import PrettyTable
from pydantic import BaseModel
from tqdm import tqdm

# For Pydantic   :  https://docs.pydantic.dev/latest/
# For GitPython  :  https://gitpython.readthedocs.io/en/stable/intro.html
# For tqdm       :  https://tqdm.github.io/

# -----------------------


@total_ordering
class ManagedRepo(BaseModel):
    local_dir: str
    repo_url: str

    def _is_valid_operand(self: Self, other: Any):
        return hasattr(other, "local_dir") and hasattr(other, "repo_url")

    def __eq__(self: Self, other: Any):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.local_dir.lower(), self.repo_url.lower()) == (
            other.local_dir.lower(),
            other.repo_url.lower(),
        )

    def __lt__(self: Self, other: Any):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.local_dir.lower(), self.repo_url.lower()) < (
            other.local_dir.lower(),
            other.repo_url.lower(),
        )


# -----------------------


class ManagedRepoList:

    @staticmethod
    def __read_lines_from_file(filename: str) -> list[str]:
        """All lines from a file."""
        with open(filename) as f:
            return [line for line in f]

    @staticmethod
    def __read_repos_from_csv_file(filename: str) -> list[ManagedRepo]:
        """All repositories in CSV file."""
        all_lines_read: list[str] = ManagedRepoList.__read_lines_from_file(filename)
        # Remove blank lines and comments
        clean_lines: list[str] = [
            line
            for line in [line.strip() for line in all_lines_read]
            if not line.startswith("#")  # no comments
            if not len(line) == 0  # no empty lines
        ]
        # Process CSV lines as `local_dir,repo_url`
        return [
            ManagedRepo(
                local_dir=t[0].strip(),
                repo_url=t[1].strip(),
            )
            for t in [line.split(",") for line in clean_lines]
        ]

    @staticmethod
    def read_repos_from_csv_file(filename: str):
        repos = ManagedRepoList.__read_repos_from_csv_file(filename)
        return ManagedRepoList(repos)

    # ---

    def __init__(self: Self, repos: list[ManagedRepo]):
        self._repos = repos

    def __len__(self: Self) -> int:
        return len(self._repos)

    def __iter__(self: Self):
        return self._repos.__iter__()

    # ---

    @property
    def max_name_len(self: Self) -> int:
        """Maximum length of ``local_dir`` for managed repositories."""
        return max([len(r.local_dir) for r in self._repos])

    def is_local_dir_managed(
        self: Self,
        local_dir: str,
    ) -> bool:
        """``True`` if argument path is in initial argument list of managed repositories;
        ``False`` otherwise."""
        for r in self._repos:
            if r.local_dir == local_dir:
                return True
        return False

    def clone_managed_repos(self: Self) -> None:
        """Traververse initial argument list of managed repositories
        and if any repository is not present (as a directory) then clone it."""
        pbar: tqdm = tqdm(self._repos, desc="Clone", unit="rp")
        max_len: int = self.max_name_len
        for managed_repo in pbar:
            pbar.set_description(f"Clone: {managed_repo.local_dir.ljust(max_len)}")
            repo_url: str = managed_repo.repo_url
            rel_local_dir: str = (
                f"../{managed_repo.local_dir}"  # hardcode - use parent always
            )
            if not os.path.isdir(rel_local_dir):
                pbar.set_description(f"CLONE: {managed_repo.local_dir.ljust(max_len)}")
                _ = Repo.clone_from(repo_url, rel_local_dir)
            pbar.set_description(f"Clone: {''.ljust(max_len)}")

    def fetch_remotes(self: Self) -> None:
        """Traververse initial argument list of managed repositories
        and fetch any remotes."""
        pbar: tqdm = tqdm(self._repos, desc="Fetch", unit="rp")
        max_len: int = self.max_name_len
        for managed_repo in pbar:
            pbar.set_description(f"Fetch: {managed_repo.local_dir.ljust(max_len)}")
            rel_repo_dir = managed_repo.local_dir
            repo = Repo(f"../{rel_repo_dir}")
            for remote in repo.remotes:
                remote.fetch()
            pbar.set_description(f"Fetch: {''.ljust(max_len)}")


# -----------------------

# TODO For now, it is assumed the git host server is GitHub

# TODO Use of colors assume dark (black) background


def prepare_table_for_print_repos() -> PrettyTable:
    """Return an empty table (header) with captions and alignment."""

    # Table headers

    DIR: str = "Directory"
    IS_REPO: str = "?"
    MANAGED = "M"
    DIRTY_REPO: str = "D"
    HEADS = "Heads"
    UNTRACKED_FILES: str = "Unt"
    MODIFIED_FILES: str = "Mod"
    STAGED_FILES: str = "Stg"

    table = PrettyTable(
        [
            MANAGED,
            IS_REPO,
            DIRTY_REPO,
            DIR,
            UNTRACKED_FILES,
            MODIFIED_FILES,
            STAGED_FILES,
            HEADS,
        ]
    )
    table.align[MANAGED] = "c"
    table.align[IS_REPO] = "c"
    table.align[DIRTY_REPO] = "c"
    table.align[DIR] = "l"
    table.align[HEADS] = "l"
    table.align[UNTRACKED_FILES] = "r"
    table.align[MODIFIED_FILES] = "r"
    table.align[STAGED_FILES] = "r"
    return table


def yellow_text(text: str) -> str:
    return f"{Fore.YELLOW}{Style.BRIGHT}{text}{Fore.RESET}"


def red_text(text: str) -> str:
    return f"{Fore.RED}{Style.BRIGHT}{text}{Fore.RESET}"


def blue_text(text: str) -> str:
    return f"{Fore.BLUE}{Style.BRIGHT}{text}{Fore.RESET}"


def green_text(text: str) -> str:
    return f"{Fore.GREEN}{Style.BRIGHT}{text}{Fore.RESET}"


def white_text(text: str) -> str:
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Fore.RESET}"


RED_UNDERSCORE: str = red_text("_")


def print_repos(
    dir_list: list[str],
    repos: ManagedRepoList,
) -> None:
    repo_table: PrettyTable = prepare_table_for_print_repos()

    for dir_name in dir_list:

        try:
            repo = Repo(f"../{dir_name}")
        except InvalidGitRepositoryError:
            repo = None

        if repo:
            local_managed: bool = repos.is_local_dir_managed(dir_name)

            # TODO Don't use try/except as program flow
            try:
                staged_files: int = len(repo.index.diff("HEAD"))
            except Exception:
                staged_files = 0

            modified_files: int = len(repo.index.diff(None))
            untracked_files: int = len(repo.untracked_files)
            head_names: list[str] = sorted([h.name for h in repo.heads])
            active_branch_name: str = repo.active_branch.name
            colored_head_names: list[str] = [
                (
                    green_text(head_name)
                    if head_name == active_branch_name
                    else white_text(head_name)
                )
                for head_name in head_names
            ]

            # ---

            repo_table.add_row(
                [
                    # Managed
                    green_text("M") if local_managed else "",
                    # Is repo
                    "",
                    # Dirty repo
                    (
                        (yellow_text("D") if local_managed else blue_text("D"))
                        if repo.is_dirty()
                        else ""
                    ),
                    # Repo name
                    (
                        (
                            yellow_text(dir_name)
                            if local_managed
                            else blue_text(dir_name)
                        )
                        if repo.is_dirty() or untracked_files
                        else (green_text(dir_name) if local_managed else f"{dir_name}")
                    ),
                    # Untracked
                    (
                        (
                            yellow_text(untracked_files)
                            if local_managed
                            else blue_text(untracked_files)
                        )
                        if untracked_files
                        else ""
                    ),
                    # Modified
                    (
                        (
                            f"{Fore.YELLOW}{Style.BRIGHT}{modified_files}{Fore.RESET}"
                            if local_managed
                            else f"{Fore.BLUE}{modified_files}{Fore.RESET}"
                        )
                        if modified_files
                        else ""
                    ),
                    # Staged
                    (
                        (
                            f"{Fore.YELLOW}{Style.BRIGHT}{staged_files}{Fore.RESET}"
                            if local_managed
                            else f"{Fore.BLUE}{staged_files}{Fore.RESET}"
                        )
                        if staged_files
                        else ""
                    ),
                    # Head names
                    ", ".join(colored_head_names),
                ]
            )
        else:
            repo_table.add_row(
                [
                    # Managed
                    RED_UNDERSCORE,
                    # Is repo
                    f"{Fore.RED}{Style.BRIGHT}N{Fore.RESET}",
                    # Dirty repo
                    RED_UNDERSCORE,
                    # Repo name
                    f"{Fore.RED}{Style.BRIGHT}{dir_name}{Fore.RESET}",
                    # Untracked
                    "",
                    # Modified
                    "",
                    # Staged
                    "",
                    # Heads
                    RED_UNDERSCORE,
                ]
            )

    print(repo_table)


def main() -> None:

    # Sanity checks
    if not os.path.exists("repos.csv"):
        print("File 'repos.csv' not found - copy from 'example.csv'")
        return

    # Colors in terminal
    colorama_init()

    managed_repos: ManagedRepoList = ManagedRepoList.read_repos_from_csv_file(
        "repos.csv"
    )
    # Observe: Repos will be created in parent directory by design
    managed_repos.clone_managed_repos()

    # Fetch all remotes (no merge or rebase)
    managed_repos.fetch_remotes()

    # Sorted parent directory names, ignore case
    # Not all directories are repositories and not all are managed
    sorted_dirs: list[str] = sorted(next(os.walk(".."))[1], key=str.casefold)
    print_repos(sorted_dirs, managed_repos)


if __name__ == "__main__":
    main()
