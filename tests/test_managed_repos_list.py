from src.manage_github_repos import ManagedRepo, ManagedRepoList

FILE_NAME = "example.csv"

repo_a: ManagedRepo = ManagedRepo(local_dir="a", repo_url="https://www.example.com/a")
repo_b: ManagedRepo = ManagedRepo(local_dir="b", repo_url="https://www.example.com/b")

l_ordered = [repo_a, repo_b]
l_inverse = [repo_b, repo_a]


def test_read_from_file() -> None:
    repos = ManagedRepoList.read_repos_from_csv_file(FILE_NAME)
    assert len(repos) == 6


def test_iter_ordered() -> None:
    s = ""
    for r in ManagedRepoList(l_ordered):
        s += r.local_dir
    assert s == "ab"


def test_iter_inverse() -> None:
    s = ""
    for r in ManagedRepoList(l_inverse):
        s += r.local_dir
    assert s == "ba"


def test_is_local_dir_managed() -> None:
    sut = ManagedRepoList(l_inverse)
    assert sut.is_local_dir_managed("a")
    assert sut.is_local_dir_managed("b")
    assert not sut.is_local_dir_managed("c")
