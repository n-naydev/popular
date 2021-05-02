from fastapi.testclient import TestClient
from github import GithubException

import main

client = TestClient(main.app)


class GithubMock:
    class RepoMock:
        def __init__(self, totalCount=0):
            self.totalCount = totalCount

    def __init__(self, user=None, repo=None, forks=0, stars=0):
        self.user = user
        self.bio = None
        self.repo = repo
        self.forks = self.RepoMock(forks)
        self.stars = self.RepoMock(stars)

    def get_user(self, user=None):
        if not self.user:
            raise GithubException(404, "User not found", headers=None)
        return self

    def get_repo(self, repo):
        if not self.repo:
            raise GithubException(404, "Repo not found", headers=None)
        return self

    def get_forks(self):
        return self.forks

    def get_stargazers(self):
        return self.stars


def test_0_user_not_found(monkeypatch):
    user = "aaa"
    repo = "bbb"
    monkeypatch.setattr(main, "g", GithubMock())
    response = client.get(f"/users/{user}/{repo}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"{user}/{repo} not found"}


def test_1_repo_not_found(monkeypatch):
    user = "aaa"
    repo = "bbb"
    monkeypatch.setattr(main, "g", GithubMock(user=user))
    response = client.get(f"/users/{user}/{repo}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"{user}/{repo} not found"}


def test_2_repo_not_popular(monkeypatch):
    user = "aaa"
    repo = "bbb"
    monkeypatch.setattr(main, "g", GithubMock(user=user, repo=repo))
    response = client.get(f"/users/{user}/{repo}")
    assert response.status_code == 200
    assert response.json() == {
        "forks": 0,
        "popular": False,
        "stars": 0,
        "url": f"{user}/{repo}",
    }


def test_3_repo_popular(monkeypatch):
    user = "aaa"
    repo = "bbb"
    monkeypatch.setattr(main, "g", GithubMock(user=user, repo=repo, stars=500))
    response = client.get(f"/users/{user}/{repo}")
    assert response.status_code == 200
    assert response.json() == {
        "forks": 0,
        "popular": True,
        "stars": 500,
        "url": f"{user}/{repo}",
    }


def test_4_health_nok(monkeypatch):
    monkeypatch.setattr(main, "g", GithubMock())
    response = client.get("/health")
    assert response.status_code == 503


def test_5_health_ok(monkeypatch):
    monkeypatch.setattr(main, "g", GithubMock(user="aaa"))
    response = client.get("/health")
    assert response.status_code == 200
