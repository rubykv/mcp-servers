from mcp.server.fastmcp import FastMCP
from client import get_projects,get_issue, add_comment_to_issue


mcp = FastMCP("jira-mcp")

@mcp.tool()
def jira_projects(
    max_results: int = 50,
    start_at: int = 0,
    order_by: str = "lastIssueUpdatedDate",
    query: str | None = None,
    status: str | None = None,
) -> list[dict]:
    """
    List Jira projects the API token has access to.
    """
    return get_projects(
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
        query=query,
        status=status,
    )

@mcp.tool()
def jira_issue(issue_key: str) -> dict:
    """
    Get a Jira issue by key (e.g., PROJ-123).
    """
    return get_issue(issue_key)

@mcp.tool()
def write_comment_to_issue(comment: str, issue_key: str) -> dict:
    """
    Add a comment to a Jira issue.
    """
    return add_comment_to_issue(comment, issue_key)

if __name__ == "__main__":
    mcp.run()