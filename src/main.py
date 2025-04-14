import os
import json
import requests
from markdownify import markdownify
from dotenv import load_dotenv

def get_organizations(token):
    url = "https://api.github.com/user/orgs"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_repositories(token, org_name):
    url = f"https://api.github.com/orgs/{org_name}/repos"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_commit_count(token, owner, repo_name, username):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/stats/contributors"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 202:  # Stats still being calculated
        return 0
    response.raise_for_status()
    stats = response.json()
    for contributor in stats:
        if contributor["author"]["login"] == username:
            return contributor["total"]
    return 0

def aggregate_stats(token, username):
    total_commits = 0
    total_repos = 0
    organizations = get_organizations(token)

    for org in organizations:
        org_name = org["login"]
        print(f"Fetching repositories for organization: {org_name}")
        repos = get_repositories(token, org_name)
        total_repos += len(repos)

        for repo in repos:
            repo_name = repo["name"]
            print(f"Fetching commits for repository: {org_name}/{repo_name}")
            total_commits += get_commit_count(token, org_name, repo_name, username)

    return {
        "organizations": len(organizations),
        "repositories": total_repos,
        "total_commits": total_commits,
    }

def main():
    load_dotenv()
    token = os.getenv("INPUT_TOKEN")
    output_format = os.getenv("INPUT_OUTPUT_FORMAT", "JSON")
    username = os.getenv("GITHUB_ACTOR")  # GitHub Action username

    if not token:
        raise ValueError("Token is required to authenticate with GitHub API.")

    stats = aggregate_stats(token, username)

    if output_format.upper() == "MARKDOWN":
        stats_md = markdownify(json.dumps(stats, indent=4))
        print(stats_md)
        with open(os.getenv("GITHUB_OUTPUT", "stats.md"), "w") as md_file:
            md_file.write(stats_md)
    else:
        print(json.dumps(stats, indent=4))
        with open(os.getenv("GITHUB_OUTPUT", "stats.json"), "w") as json_file:
            json.dump(stats, json_file, indent=4)

if __name__ == "__main__":
    main()