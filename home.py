import streamlit as st
from github_client import GitHubClient

# Streamlit App Configuration
st.set_page_config(page_title="GitHub Manager", layout="wide")

# Title
st.title("GitHub Repository Manager")

# Step 1: Authenticate via GitHub
st.header("Step 1: Authenticate via GitHub")
github_token = st.text_input("Enter your GitHub Token", type="password")

if github_token:
    try:
        client = GitHubClient(github_token)
        st.success("Authenticated successfully!")
    except Exception as e:
        st.error(f"Authentication failed: {e}")

# Step 2: Select Organization and Template Repositories
if github_token:
    st.header("Step 2: Select Organization and Template Repositories")
    organizations = client.list_organizations()
    org_names = [org["login"] for org in organizations]

    selected_org = st.selectbox("Select Organization", options=org_names)

    if selected_org:
        templates = client.list_template_repositories(selected_org, is_org=True)
        template_names = [template.name for template in templates]

        if template_names:
            selected_template = st.selectbox("Select a Template Repository", options=template_names)
            if selected_template:
                selected_template_repo = next(repo for repo in templates if repo.name == selected_template)
        else:
            st.warning("No template repositories found for the selected organization.")

# Step 3: Create a Repository Based on Template
if github_token and selected_template:
    st.header("Step 3: Create a Repository from Template")

    with st.form("Create Repo Form"):
        new_repo_name = st.text_input("Enter New Repository Name")
        is_private = st.checkbox("Make Private", value=True)
        include_branches = st.checkbox("Include Branches", value=True)

        submitted = st.form_submit_button("Create Repository")

        if submitted:
            try:
                st.text(f"{selected_template_repo.name} --> {new_repo_name}")
                # Create new repository
                new_repo = client.create_repo_from_template(
                    template_owner=selected_template_repo.owner,
                    template_repo=selected_template_repo.name,
                    new_repo_name=new_repo_name,
                    owner=selected_org,
                    private=is_private,
                    include_all_branches=include_branches
                )

                st.success(f"Repository '{new_repo_name}' created successfully")

                # Copy rulesets
                new_repo.copy_rulesets_from(selected_template_repo)
                st.success("Rulesets copied!")
            except Exception as e:
                st.error(f"Failed to create repository: {e}")
