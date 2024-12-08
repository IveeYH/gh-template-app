import streamlit as st
from github import Github
from github.Repository import Repository
from github.Organization import Organization

# Step 1: Authenticate via GitHub
def authenticate_github(token):
    try:
        return Github(token)
    except Exception as e:
        st.error(f"Authentication failed: {e}")
        return None

# Step 2: Fetch organizations and repositories
def fetch_organizations(g):
    try:
        return g.get_user().get_orgs()
    except Exception as e:
        st.error(f"Failed to fetch organizations: {e}")
        return []

def fetch_template_repos(org):
    try:
        return [repo for repo in org.get_repos() if repo.is_template]
    except Exception as e:
        st.error(f"Failed to fetch template repositories: {e}")
        return []

# Step 3: Copy branch rules to the new repository
def copy_branch_rules(source_repo: Repository, target_repo: Repository):
    try:
        branch_rules = source_repo.get_branch_protection("main")
        target_repo.get_branch("main").edit_protection(
            enforce_admins=branch_rules.enforce_admins,
            required_status_checks=branch_rules.required_status_checks,
            restrictions=branch_rules.restrictions,
            required_pull_request_reviews=branch_rules.required_pull_request_reviews
        )
    except Exception as e:
        st.warning(f"Failed to copy branch rules: {e}")

# Step 4: Create new repository from template
def create_repo_from_template(template_repo: Repository, org: Organization, new_repo_name):
    try:
        new_repo = org.create_repo_from_template(
            name=new_repo_name,
            repo=template_repo,
            include_all_branches=True,
            private=True
        )
        copy_branch_rules(template_repo, new_repo)
        st.success(f"Repository {new_repo_name} created successfully!")
        return new_repo
    except Exception as e:
        st.error(f"Failed to create repository: {e}")

# Streamlit App Layout
st.title("GitHub Repository Creator")

# GitHub Token Input 
github_token = st.text_input("Enter your GitHub token:", type="password")
if github_token:
    github_client = authenticate_github(github_token)
    if github_client:
        organizations = fetch_organizations(github_client)
        if organizations:
            org_names = [org.login for org in organizations]
            selected_org_name = st.selectbox("Select an organization:", org_names)

            selected_org = next((org for org in organizations if org.login == selected_org_name), None)
            if selected_org:
                template_repos = fetch_template_repos(selected_org)

                if template_repos:
                    template_names = [repo.name for repo in template_repos]
                    selected_template_name = st.selectbox("Select a template repository:", template_names)

                    selected_template = next((repo for repo in template_repos if repo.name == selected_template_name), None)

                    if selected_template:
                        new_repo_name = st.text_input("Enter the name for the new repository:")

                        if st.button("Create Repository") and new_repo_name:
                            create_repo_from_template(selected_template, selected_org, new_repo_name)
                        elif st.button("Create Repository"):
                            st.warning("Please enter a repository name before proceeding.")
