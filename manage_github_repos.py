import os
from functools import total_ordering
from typing import Any, Self

from colorama import Fore, Style
from colorama import init as colorama_init
from git import InvalidGitRepositoryError, Remote, Repo
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
        return (
            self.local_dir.lower(),
            self.repo_url.lower(),
        ) == (
            other.local_dir.lower(),
            other.repo_url.lower(),
        )

    def __lt__(self: Self, other: Any):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (
            self.local_dir.lower(),
            self.repo_url.lower(),
        ) < (
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
        """
        ``True`` if argument path is in initial argument list of managed repositories;
        ``False`` otherwise.
        """
        for r in self._repos:
            if r.local_dir == local_dir:
                return True
        return False

    def clone_managed_repos(
        self: Self,
        ignore_error: bool = False,
    ) -> None:
        """
        Traververse initial argument list of managed repositories
        and if any repository is not present (as a directory) then clone it.
        """
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
                try:
                    _ = Repo.clone_from(repo_url, rel_local_dir)
                except Exception as e:
                    if not ignore_error:
                        raise e

            pbar.set_description(f"Clone: {''.ljust(max_len)}")

    def fetch_remotes(
        self: Self,
        ignore_error: bool = False,
    ) -> None:
        """
        Traververse initial argument list of managed repositories
        and fetch any remotes.
        """
        pbar: tqdm = tqdm(self._repos, desc="Fetch", unit="rp")
        max_len: int = self.max_name_len
        for managed_repo in pbar:
            pbar.set_description(f"Fetch: {managed_repo.local_dir.ljust(max_len)}")
            rel_repo_dir = managed_repo.local_dir
            repo = Repo(f"../{rel_repo_dir}")
            try:
                for remote in repo.remotes:
                    remote.fetch()
            except Exception as e:
                if not ignore_error:
                    raise e
            pbar.set_description(f"Fetch: {''.ljust(max_len)}")


# -----------------------


# TODO Don't use color names - instead use decoration functions like: `decorate_color_as_missing_repo`


class ColorDecorator:

    def __init__(
        self: Self,
        use_colors: bool = True,
    ):
        self._use_colors = use_colors

    # YELLOW

    def yellow_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.YELLOW}{Style.BRIGHT}{text}{Fore.RESET}"

    # RED

    def red_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.RED}{Style.BRIGHT}{text}{Fore.RESET}"

    # BLUE

    def blue_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.BLUE}{Style.BRIGHT}{text}{Fore.RESET}"

    # GREEN

    def green_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.GREEN}{Style.BRIGHT}{text}{Fore.RESET}"

    # WHITE

    def white_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.WHITE}{Style.BRIGHT}{text}{Fore.RESET}"

    def dim_white_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.WHITE}{Style.DIM}{text}{Fore.RESET}"

    # CYAN

    def dim_cyan_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.CYAN}{Style.DIM}{text}{Fore.RESET}"

    def bright_cyan_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.CYAN}{Style.BRIGHT}{text}{Fore.RESET}"

    # MAGENTA

    def bright_magenta_text(
        self: Self,
        text: str,
    ) -> str:
        return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Fore.RESET}"

    # ===

    def not_a_repository(
        self: Self,
        text: str,
    ) -> str:
        return self.red_text(text)

    def error(
        self: Self,
        text: str,
    ) -> str:
        return self.bright_magenta_text(text)


# -----------------------


# TODO For now, it is assumed the git host server is GitHub

# TODO Use of colors assume dark (black) background


def latest_commit_is_pushed(repo: Repo) -> bool:
    """
    Local and remote (origin) are the same.

    :param repo: _description_
    :type repo: Repo
    :return: ``True`` if local and remote are the same; ``False`` otherwise
    :rtype: bool
    """
    remote: Remote = repo.remote("origin")
    remote.fetch()
    latest_remote_commit = remote.refs[repo.active_branch.name].commit
    latest_local_commit = repo.head.commit
    return latest_local_commit == latest_remote_commit


def prepare_table_for_print_repos() -> PrettyTable:
    """Return an empty table (header) with captions and alignment."""

    # Table headers

    SUMMARY = "M?UD>"
    DIR: str = "Local Directory"
    HEADS = "Heads"
    UNTRACKED_FILES: str = "Unt"
    MODIFIED_FILES: str = "Mod"
    STAGED_FILES: str = "Stg"

    table = PrettyTable(
        [
            SUMMARY,
            DIR,
            UNTRACKED_FILES,
            MODIFIED_FILES,
            STAGED_FILES,
            HEADS,
        ]
    )
    table.align[SUMMARY] = "l"
    table.align[DIR] = "l"
    table.align[HEADS] = "l"
    table.align[UNTRACKED_FILES] = "r"
    table.align[MODIFIED_FILES] = "r"
    table.align[STAGED_FILES] = "r"
    return table


def print_repos(
    dir_list: list[str],
    repos: ManagedRepoList,
) -> None:
    color_decorator: ColorDecorator = ColorDecorator(True)
    pretty_repo_table: PrettyTable = prepare_table_for_print_repos()

    max_len = 20  # TODO calculate
    pbar: tqdm = tqdm(dir_list, desc="Build", unit="rp")
    for dir_name in pbar:
        pbar.set_description(f"Build: {dir_name.ljust(max_len)}")

        try:
            repo = Repo(f"../{dir_name}")
        except InvalidGitRepositoryError:
            repo = None

        try:

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
                        color_decorator.green_text(head_name)
                        if head_name == active_branch_name
                        else color_decorator.dim_white_text(head_name)
                    )
                    for head_name in head_names
                ]

                # ---

                col_text_managed = (
                    color_decorator.green_text("M")
                    if local_managed
                    else color_decorator.dim_white_text(".")
                )

                col_text_is_repo: str = color_decorator.dim_white_text(".")

                col_text_dirty_repo: str = (
                    (
                        color_decorator.yellow_text("D")
                        if local_managed
                        else color_decorator.blue_text("D")
                    )
                    if repo.is_dirty()
                    else color_decorator.dim_white_text(".")
                )

                col_text_has_untracked_files: str = (
                    (
                        color_decorator.yellow_text("U")
                        if untracked_files != ""
                        else color_decorator.blue_text("U")
                    )
                    if untracked_files
                    else color_decorator.dim_white_text(".")
                )

                col_text_repo_name: str = (
                    (
                        color_decorator.yellow_text(dir_name)
                        if local_managed
                        else color_decorator.blue_text(dir_name)
                    )
                    if repo.is_dirty() or untracked_files
                    else (
                        color_decorator.green_text(dir_name)
                        if local_managed
                        else dir_name
                    )
                )

                col_text_untracked: str = (
                    (
                        color_decorator.yellow_text(untracked_files)
                        if local_managed
                        else color_decorator.blue_text(untracked_files)
                    )
                    if untracked_files
                    else ""
                )

                col_text_modified: str = (
                    (
                        color_decorator.yellow_text(modified_files)
                        if local_managed
                        else color_decorator.blue_text(modified_files)
                    )
                    if modified_files
                    else ""
                )

                col_text_staged: str = (
                    (
                        color_decorator.yellow_text(staged_files)
                        if local_managed
                        else color_decorator.blue_text(staged_files)
                    )
                    if staged_files
                    else ""
                )

                col_text_heads: str = ", ".join(colored_head_names)

                col_latest_commit_is_pushed: str = (
                    color_decorator.dim_white_text(".")
                    if latest_commit_is_pushed(repo)
                    else color_decorator.red_text(">")
                )

            else:

                col_text_managed: str = color_decorator.not_a_repository(".")
                col_text_is_repo: str = color_decorator.not_a_repository("N")
                col_text_dirty_repo: str = color_decorator.not_a_repository(".")
                col_text_has_untracked_files = color_decorator.not_a_repository(".")
                col_text_repo_name: str = color_decorator.not_a_repository(dir_name)
                col_text_untracked: str = color_decorator.not_a_repository(".")
                col_text_modified: str = color_decorator.not_a_repository(".")
                col_text_staged: str = color_decorator.not_a_repository(".")
                col_text_heads: str = color_decorator.not_a_repository(".")
                col_latest_commit_is_pushed: str = color_decorator.not_a_repository(".")

        except Exception as e:
            col_text_managed: str = color_decorator.bright_magenta_text("?")
            col_text_is_repo: str = color_decorator.bright_magenta_text("?")
            col_text_dirty_repo: str = color_decorator.bright_magenta_text("?")
            col_text_has_untracked_files = color_decorator.bright_magenta_text("?")
            col_text_repo_name: str = color_decorator.bright_magenta_text(dir_name)
            col_text_untracked: str = color_decorator.bright_magenta_text("?")
            col_text_modified: str = color_decorator.bright_magenta_text("?")
            col_text_staged: str = color_decorator.bright_magenta_text("?")
            col_text_heads: str = color_decorator.bright_magenta_text("?")
            col_latest_commit_is_pushed: str = color_decorator.bright_magenta_text("?")

        col_text_summary: str = (
            col_text_managed
            + col_text_is_repo
            + col_text_has_untracked_files
            + col_text_dirty_repo
            + col_latest_commit_is_pushed
        )
        pretty_repo_table.add_row(
            [
                col_text_summary,
                col_text_repo_name,
                col_text_untracked,
                col_text_modified,
                col_text_staged,
                col_text_heads,
            ]
        )

        pbar.set_description(f"Build: {''.ljust(max_len)}")

    print(pretty_repo_table)


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
    try:
        managed_repos.clone_managed_repos()
    except Exception:
        # ignore
        pass

    # Fetch all remotes (no merge or rebase)
    try:
        managed_repos.fetch_remotes()
    except Exception:
        # ignore
        pass

    # Sorted parent directory names, ignore case
    # Not all directories are repositories and not all are managed
    sorted_dirs: list[str] = sorted(next(os.walk(".."))[1], key=str.casefold)
    print_repos(sorted_dirs, managed_repos)


if __name__ == "__main__":
    main()
