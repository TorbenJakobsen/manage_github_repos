import os
from functools import total_ordering
from typing import Any, Self

from git import Repo
from pydantic import BaseModel
from tqdm import tqdm

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
