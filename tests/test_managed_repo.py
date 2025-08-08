from src.manage_github_repos import ManagedRepo

repo_a: ManagedRepo = ManagedRepo(local_dir="a", repo_url="https://www.example.com/a")
repo_b: ManagedRepo = ManagedRepo(local_dir="b", repo_url="https://www.example.com/b")

l_ordered = [repo_a, repo_b]
l_inverse = [repo_b, repo_a]


def test_equality() -> None:
    assert repo_a == repo_a


def test_non_equality() -> None:
    assert repo_a != repo_b


def test_ordering() -> None:
    assert repo_a < repo_b


def test_sorted() -> None:
    assert sorted(l_ordered)[0] == repo_a
    assert sorted(l_inverse)[0] == repo_a
