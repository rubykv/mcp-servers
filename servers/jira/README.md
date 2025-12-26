# Jira MCP Server

MCP server for Jira, compatible with Windsurf.

## Required Environment Variables

- JIRA_BASE_URL
- JIRA_EMAIL
- JIRA_API_TOKEN

## Available Tools

- jira_projects
- jira_issue
- write_comment_to_issue

## Registering a Dockerized MCP Server with Windsurf

```json
{
  "mcpServers": {
    "jira-mcp": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e", "JIRA_BASE_URL=https://your-domain.atlassian.net",
        "-e", "JIRA_EMAIL=you@example.com",
        "-e", "JIRA_API_TOKEN=YOUR_API_TOKEN",
        "jira-mcp:latest"
      ]
    }
  }
}```

## Registering Python MCP Server

To register this Python MCP server with Windsurf, add the following to your Windsurf configuration:

```json
{
  "mcpServers": {
    "jira-mcp": {
      "command": "python",
      "args": ["servers/jira/server.py"],
      "env": {
        "JIRA_BASE_URL": "https://your-domain.atlassian.net",
        "JIRA_EMAIL": "you@example.com",
        "JIRA_API_TOKEN": "YOUR_API_TOKEN"
      },
      "disabled": false
    }
  }
}
```
