import requests
import json
import os

def get_org_repo_stats(org):
    repos_url = f"https://api.github.com/orgs/{org}/repos?per_page=100"
    repos, page = [], 1

    while True:
        resp = requests.get(f"{repos_url}&page={page}")
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        page += 1

    org_stats = {
        "org_name": org,
        "total_repos": len(repos),
        "total_stars": sum(repo["stargazers_count"] for repo in repos),
        "total_forks": sum(repo["forks_count"] for repo in repos),
        "total_open_issues": sum(repo["open_issues_count"] for repo in repos),
    }
    return org_stats

def aggregate_all_orgs(orgs):
    aggregate = {
        "total_orgs": len(orgs),
        "total_repos": 0,
        "total_stars": 0,
        "total_forks": 0,
        "total_open_issues": 0,
        "org_details": [],
    }

    for org in orgs:
        stats = get_org_repo_stats(org)
        aggregate["total_repos"] += stats["total_repos"]
        aggregate["total_stars"] += stats["total_stars"]
        aggregate["total_forks"] += stats["total_forks"]
        aggregate["total_open_issues"] += stats["total_open_issues"]
        aggregate["org_details"].append(stats)

    return aggregate

def save_json(stats):
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=2)

def save_markdown(stats):
    md = "# 📈 GitHub Organization Stats\n\n"
    md += f"- Total Organizations: **{stats['total_orgs']}**\n"
    md += f"- Total Repositories: **{stats['total_repos']}**\n"
    md += f"- Total Stars: **{stats['total_stars']}**\n"
    md += f"- Total Forks: **{stats['total_forks']}**\n"
    md += f"- Total Open Issues: **{stats['total_open_issues']}**\n\n"

    md += "## 🚀 Organization Breakdown\n\n"
    for org in stats["org_details"]:
        md += f"### 🏢 [{org['org_name']}](https://github.com/{org['org_name']})\n"
        md += f"- Repositories: {org['total_repos']}\n"
        md += f"- Stars: {org['total_stars']}\n"
        md += f"- Forks: {org['total_forks']}\n"
        md += f"- Open Issues: {org['total_open_issues']}\n\n"

    with open("stats.md", "w") as f:
        f.write(md)

if __name__ == "__main__":
    org_list_str = os.getenv("ORG_LIST", "")
    if not org_list_str:
        raise ValueError("ORG_LIST environment variable is required.")

    orgs = [org.strip() for org in org_list_str.split(",") if org.strip()]
    stats = aggregate_all_orgs(orgs)
    save_json(stats)
    save_markdown(stats)
    print("✅ Stats aggregated successfully!")
