"""
manage_github_repos
"""

import os

from colorama import init as colorama_init
from git import Commit, InvalidGitRepositoryError, Remote, Repo
from prettytable import PrettyTable
from tqdm import tqdm

from color_decorator import ColorDecorator
from managed_repo import ManagedRepoList

# For Pydantic   :  https://docs.pydantic.dev/latest/
# For GitPython  :  https://gitpython.readthedocs.io/en/stable/intro.html
# For tqdm       :  https://tqdm.github.io/


# TODO Don't use color names - instead use decoration functions like: `decorate_color_as_missing_repo`


# -----------------------


# TODO For now, it is assumed the git host server is GitHub

# TODO Use of colors assume dark (black) background


def compare_latest_commits(repo: Repo) -> int:
    """
    Compares local and remote (origin).

    :param repo: local repository to check
    :type repo: Repo
    :return: ``0`` if local and remote are the same; -1 if local is behind, 1 if local is ahead
    :rtype: int
    """
    remote: Remote = repo.remote("origin")
    remote.fetch()
    latest_remote_commit: Commit = remote.refs[repo.active_branch.name].commit
    latest_local_commit: Commit = repo.head.commit
    if latest_local_commit == latest_remote_commit:
        return 0
    if latest_local_commit.committed_datetime < latest_remote_commit.committed_datetime:
        return -1
    # Fall through
    return 1

    # TODO Compare timestamps for comits


def prepare_table_for_print_repos() -> PrettyTable:
    """Return an empty table (header) with captions and alignment."""

    # Table headers

    SUMMARY = "MRUDC"
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
    USE_COLOR: bool = True
    color_decorator: ColorDecorator = ColorDecorator(USE_COLOR)
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
                        color_decorator.active_head(head_name)
                        if head_name == active_branch_name
                        else color_decorator.inactive_head(head_name)
                    )
                    for head_name in head_names
                ]

                # ---

                col_text_managed = (
                    color_decorator.managed_repo("M")
                    if local_managed
                    else color_decorator.unmanaged_repo(".")
                )

                col_text_is_repo: str = color_decorator.neutral(".")

                col_text_dirty_repo: str = (
                    (
                        color_decorator.bright_yellow_text("D")
                        if local_managed
                        else color_decorator.bright_blue_text("D")
                    )
                    if repo.is_dirty()
                    else color_decorator.neutral(".")
                )

                col_text_has_untracked_files: str = (
                    (
                        color_decorator.bright_yellow_text("U")
                        if untracked_files != ""
                        else color_decorator.bright_blue_text("U")
                    )
                    if untracked_files
                    else color_decorator.neutral(".")
                )

                col_text_repo_name: str = (
                    (
                        color_decorator.bright_yellow_text(dir_name)
                        if local_managed
                        else color_decorator.bright_blue_text(dir_name)
                    )
                    if repo.is_dirty() or untracked_files
                    else (
                        color_decorator.bright_green_text(dir_name)
                        if local_managed
                        else dir_name
                    )
                )

                col_text_untracked: str = (
                    (
                        color_decorator.bright_yellow_text(untracked_files)
                        if local_managed
                        else color_decorator.bright_blue_text(untracked_files)
                    )
                    if untracked_files
                    else ""
                )

                col_text_modified: str = (
                    (
                        color_decorator.bright_yellow_text(modified_files)
                        if local_managed
                        else color_decorator.bright_blue_text(modified_files)
                    )
                    if modified_files
                    else ""
                )

                col_text_staged: str = (
                    (
                        color_decorator.bright_yellow_text(staged_files)
                        if local_managed
                        else color_decorator.bright_blue_text(staged_files)
                    )
                    if staged_files
                    else ""
                )

                col_text_heads: str = ", ".join(colored_head_names)

                compare_repo_commits = compare_latest_commits(repo)
                col_latest_commit_is_pushed: str = (
                    color_decorator.local_and_remote_identical(".")
                    if compare_repo_commits == 0
                    else (
                        color_decorator.local_and_remote_different("<")
                        if compare_repo_commits == -1
                        else color_decorator.local_and_remote_different(">")
                    )
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
            col_text_managed: str = color_decorator.error("?")
            col_text_is_repo: str = color_decorator.error("?")
            col_text_dirty_repo: str = color_decorator.error("?")
            col_text_has_untracked_files = color_decorator.error("?")
            col_text_repo_name: str = color_decorator.error(dir_name)
            col_text_untracked: str = color_decorator.error("?")
            col_text_modified: str = color_decorator.error("?")
            col_text_staged: str = color_decorator.error("?")
            col_text_heads: str = color_decorator.error("?")
            col_latest_commit_is_pushed: str = color_decorator.error("?")

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

    cwd: str = os.getcwd()  # current working directory

    # Sanity checks
    if not os.path.exists(f"{cwd}/config/repos.csv"):
        print(os.getcwd())
        print(
            f"File 'config/repos.csv' not found in CWD ({cwd}) - copy/modify 'config/example.csv'"
        )
        return

    # Colors in terminal
    colorama_init()

    managed_repos: ManagedRepoList = ManagedRepoList.read_repos_from_csv_file(
        "config/repos.csv"
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
