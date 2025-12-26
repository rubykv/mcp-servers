# Playwright MCP Server

MCP server for running Playwright tests.

## Prerequisites

Make sure Playwright and pytest are installed in your environment.

## Available Tools

- run_playwright_tests: Run Playwright tests via pytest

## Registering Python MCP Server

To register this Python MCP server with Windsurf, add the following to your Windsurf configuration:

```json
{
  "mcpServers": {
    "playwright-node": {
      "command": "python",
      "args": ["servers/playwright/server.py"],
      "disabled": false
    }
  }
}```