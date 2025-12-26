# Xray MCP Server

MCP server for creating Xray tests in Jira Cloud.

## Available Tools

- create_xray_test: Create a manual Xray test in Jira Cloud

## Prerequisites

Make sure you have the following environment variables set:

- `XRAY_CLIENT_ID`: Your Xray client ID
- `XRAY_CLIENT_SECRET`: Your Xray client secret

You can obtain these from your Xray Cloud configuration.

## Registering Python MCP Server

To register this Python MCP server with Windsurf, add the following to your Windsurf configuration:

```json
{
  "mcpServers": {
    "xray": {
      "command": "python",
      "args": ["servers/xray/server.py"],
      "disabled": false
    }
  }
}```