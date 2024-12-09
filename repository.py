from branch import Branch
import requests

class Repository:
    def __init__(self, owner, name, client):
        self.owner = owner
        self.name = name
        self.client = client
        self._is_template = None

    @property
    def is_template(self):
        if self._is_template is None:
            url = f"{self.client.base_url}/repos/{self.owner}/{self.name}"
            response = requests.get(url, headers=self.client.headers)
            response.raise_for_status()
            repo_data = response.json()
            self._is_template = repo_data.get('is_template', False)
        return self._is_template

    def get_rulesets(self):
        url = f"{self.client.base_url}/repos/{self.owner}/{self.name}/rulesets"
        response = requests.get(url, headers=self.client.headers)
        if response.status_code != 200:
            raise ValueError(f"Es aquí: {response.raise_for_status()}")
        return response.json()

    def create_ruleset(self, ruleset):
        url = f"{self.client.base_url}/repos/{self.owner}/{self.name}/rulesets"
        response = requests.post(url, headers=self.client.headers, json=ruleset)
        if response.status_code != 200:
            raise ValueError(f"O aquí: {response.raise_for_status()}")
        return response.json()

    def copy_rulesets_from(self, template_repo):
        rulesets = template_repo.get_rulesets()
        print(rulesets)
        for ruleset in rulesets:
            for field in ['id', 'creator', 'created_at', 'updated_at', 'url']:
                ruleset.pop(field, None)
            self.create_ruleset(ruleset)

    def get_branches(self):
        url = f"{self.client.base_url}/repos/{self.owner}/{self.name}/branches"
        response = requests.get(url, headers=self.client.headers)
        response.raise_for_status()
        branches_data = response.json()
        return [Branch(self, branch['name']) for branch in branches_data]
