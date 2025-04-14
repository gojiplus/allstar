# Aggregate Organization Stats GitHub Action

This GitHub Action aggregates stats across all organizations you own, such as total commits, pull requests, and more.

## Features
- Retrieves stats across all organizations where you're an owner.
- Outputs stats in JSON or Markdown format.
- Easy integration with workflows.

## Inputs
| Input         | Description                                | Required | Default |
|---------------|--------------------------------------------|----------|---------|
| `token`       | GitHub Personal Access Token or GITHUB_TOKEN | Yes      | N/A     |
| `output-format` | The output format for stats (JSON or Markdown) | No       | JSON    |

## Outputs
| Output  | Description                              |
|---------|------------------------------------------|
| `stats` | Aggregated stats in the specified format |

## Example Usage
```yaml
name: Example Usage of Aggregate Organization Stats

on:
  workflow_dispatch:
    inputs:
      format:
        description: "Output format"
        required: false
        default: "JSON"

jobs:
  aggregate-stats:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run Aggregator Action
        uses: ./ # Use the action in the current repo
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          output-format: ${{ inputs.format }}
```

## License
MIT