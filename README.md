## 📊 GitHub Stats Aggregator

GitHub Action to aggregate and summarize statistics from public repositories across multiple GitHub organizations and user accounts.

### 🚀 Overview

GitHub Stats Aggregator collects statistics such as total repositories, stars, forks, and open issues from specified GitHub user accounts and organizations. The aggregated statistics are saved in both JSON and Markdown formats, perfect for integrating into README files or dashboards.

### ✨ Features

1. Summarizes data across multiple GitHub organizations and personal accounts.

2. Generates a Markdown summary report (stats.md).

3. Generates a JSON data file (stats.json) for further use or visualization.

### 🔧 Usage

Step 1: Create a Workflow File

Create a file .github/workflows/aggregate-stats.yml:

```yaml
name: Aggregate GitHub Stats

on:
  workflow_dispatch:
  schedule:
    - cron: "0 0 * * *"

jobs:
  aggregate:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    env:
      GITHUB_USER: "your-github-username"
      ORG_LIST: "USER, org1, org2, org3"
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - run: python -m pip install requests

      - run: python src/main.py

      - name: Commit and push
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add stats.json stats.md
          git commit -m "Update aggregated GitHub stats" || echo "No changes"
          git push
```

Replace your-github-username and org1, org2, org3 with your GitHub username and any organizations you want to include.

Step 2: Set up Python Script

Ensure the script (src/main.py) from this repository is present in your repository, along with any required files:
```
repo-root/
├── .github/
│   └── workflows/
│       └── aggregate-stats.yml
└── src/
    └── main.py
```

Step 3: Workflow Execution

The workflow runs daily (adjust cron as needed) and aggregates stats. Manually trigger the workflow via GitHub Actions UI if necessary.

### 📂 Example Output

The Action generates two files:

stats.md

# 📈 GitHub Aggregate Stats

- Total Entities: **4**
- Total Repositories: **120**
- Total Stars: **650**
- Total Forks: **210**
- Total Open Issues: **32**

## 🚀 Detailed Breakdown

### 🏢 [your-github-username](https://github.com/your-github-username)
- Repositories: 20
- Stars: 100
- Forks: 30
- Open Issues: 5

### 🏢 [org1](https://github.com/org1)
- Repositories: 40
- Stars: 200
- Forks: 80
- Open Issues: 12

stats.json

{
  "total_entities": 4,
  "total_repos": 120,
  "total_stars": 650,
  "total_forks": 210,
  "total_open_issues": 32,
  "details": [
    {
      "name": "your-github-username (User)",
      "total_repos": 20,
      "total_stars": 100,
      "total_forks": 30,
      "total_open_issues": 5
    },
    {
      "name": "org1",
      "total_repos": 40,
      "total_stars": 200,
      "total_forks": 80,
      "total_open_issues": 12
    }
  ]
}


