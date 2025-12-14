# Jira MCP Server

A read-only MCP server for Jira, compatible with Windsurf.

## Required Environment Variables

- JIRA_BASE_URL
- JIRA_EMAIL
- JIRA_API_TOKEN

## Available Tools

- jira_get_issue
- jira_search_issues
- jira_whoami

## Run Locally

```bash
export JIRA_BASE_URL=...
export JIRA_EMAIL=...
export JIRA_API_TOKEN=...

python server.py
