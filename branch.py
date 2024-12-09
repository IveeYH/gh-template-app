import requests

class Branch:
    def __init__(self, repository, name):
        self.repository = repository
        self.name = name

    def get_rules(self):
        url = f"{self.repository.client.base_url}/repos/{self.repository.owner}/{self.repository.name}/rules/branches/{self.name}"
        response = requests.get(url, headers=self.repository.client.headers)
        response.raise_for_status()
        return response.json()
