import requests
from repository import Repository

class GitHubClient:
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def create_repo_from_template(self, template_owner, template_repo, new_repo_name, owner=None, private=False, include_all_branches=False):
        url = f"{self.base_url}/repos/{template_owner}/{template_repo}/generate"
        data = {
            "name": new_repo_name,
            "owner": owner,
            "private": private,
            "include_all_branches": include_all_branches
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        repo_data = response.json()
        return Repository(repo_data['owner']['login'], repo_data['name'], self)

    def list_organizations(self):
        url = f"{self.base_url}/user/orgs"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_user_repositories(self, username):
        url = f"{self.base_url}/users/{username}/repos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        repos_data = response.json()
        return [Repository(repo['owner']['login'], repo['name'], self) for repo in repos_data]

    def list_organization_repositories(self, organization):
        url = f"{self.base_url}/orgs/{organization}/repos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        repos_data = response.json()
        return [Repository(repo['owner']['login'], repo['name'], self) for repo in repos_data]

    def list_template_repositories(self, owner, is_org=False):
        if is_org:
            repos = self.list_organization_repositories(owner)
        else:
            repos = self.list_user_repositories(owner)
        return [repo for repo in repos if repo.is_template]
