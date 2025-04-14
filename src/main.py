import requests
import json
import os

GITHUB_USER = os.getenv("GITHUB_USER", "")  # GitHub username

def get_repos(url):
    repos, page = [], 1
    while True:
        resp = requests.get(f"{url}&page={page}")
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_repo_stats(entity, is_user=False):
    """Fetch stats for a user's or organization's repositories."""
    if is_user:
        url = f"https://api.github.com/users/{entity}/repos?per_page=100"
    else:
        url = f"https://api.github.com/orgs/{entity}/repos?per_page=100"

    repos = get_repos(url)

    stats = {
        "name": entity if not is_user else f"{entity} (User)",
        "total_repos": len(repos),
        "total_stars": sum(r["stargazers_count"] for r in repos),
        "total_forks": sum(r["forks_count"] for r in repos),
        "total_open_issues": sum(r["open_issues_count"] for r in repos),
    }
    return stats

def aggregate_stats(entities):
    aggregate = {
        "total_entities": len(entities),
        "total_repos": 0,
        "total_stars": 0,
        "total_forks": 0,
        "total_open_issues": 0,
        "details": [],
    }

    for entity, is_user in entities:
        stats = get_repo_stats(entity, is_user)
        aggregate["total_repos"] += stats["total_repos"]
        aggregate["total_stars"] += stats["total_stars"]
        aggregate["total_forks"] += stats["total_forks"]
        aggregate["total_open_issues"] += stats["total_open_issues"]
        aggregate["details"].append(stats)

    return aggregate

def save_json(stats):
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=2)

def save_markdown(stats):
    md = "# 📈 GitHub Aggregate Stats\n\n"
    md += f"- Total Entities: **{stats['total_entities']}**\n"
    md += f"- Total Repositories: **{stats['total_repos']}**\n"
    md += f"- Total Stars: **{stats['total_stars']}**\n"
    md += f"- Total Forks: **{stats['total_forks']}**\n"
    md += f"- Total Open Issues: **{stats['total_open_issues']}**\n\n"

    md += "## 🚀 Detailed Breakdown\n\n"
    for detail in stats["details"]:
        name = detail["name"]
        link = f"https://github.com/{name.replace(' (User)', '')}"
        md += f"### 🏢 [{name}]({link})\n"
        md += f"- Repositories: {detail['total_repos']}\n"
        md += f"- Stars: {detail['total_stars']}\n"
        md += f"- Forks: {detail['total_forks']}\n"
        md += f"- Open Issues: {detail['total_open_issues']}\n\n"

    with open("stats.md", "w") as f:
        f.write(md)

if __name__ == "__main__":
    org_list_str = os.getenv("ORG_LIST", "")
    if not org_list_str or not GITHUB_USER:
        raise ValueError("ORG_LIST and GITHUB_USER environment variables are required.")

    entities = []
    for org in [o.strip() for o in org_list_str.split(",")]:
        if org.upper() == "USER":
            entities.append((GITHUB_USER, True))
        else:
            entities.append((org, False))

    stats = aggregate_stats(entities)
    save_json(stats)
    save_markdown(stats)
    print("✅ Stats aggregated successfully!")
