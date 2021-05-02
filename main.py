from fastapi import FastAPI, HTTPException
from github import Github, GithubException
from pydantic import AnyUrl, BaseModel, BaseSettings, Field


class Settings(BaseSettings):
    github_token: str = Field(..., env="github_token")


settings = Settings()
g = Github(settings.github_token)

app = FastAPI()


class RepoInfo(BaseModel):
    url: str
    forks: int
    stars: int
    popular: bool


@app.get("/users/{user}/{repo}", response_model=RepoInfo)
async def repo(user: str, repo: str):
    """Endpoint to return repo info"""
    try:
        r = g.get_user(user).get_repo(repo)
    except GithubException:
        raise HTTPException(status_code=404, detail=f"{user}/{repo} not found")
    num_forks = r.get_forks().totalCount
    num_stars = r.get_stargazers().totalCount
    score = num_stars * 1 + num_forks * 2
    popular = score >= 500
    return RepoInfo(
        url=f"{user}/{repo}", forks=num_forks, stars=num_stars, popular=popular
    )


@app.get("/health")
async def health():
    try:
        r = g.get_user().bio
    except GithubException:
        raise HTTPException(status_code=503)
    return None
