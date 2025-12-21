# server.py
from mcp.server.fastmcp import FastMCP
from xray_client import XrayClient
import os

mcp = FastMCP("xray-mcp")

xray_client = XrayClient(
    client_id=os.environ["XRAY_CLIENT_ID"],
    client_secret=os.environ["XRAY_CLIENT_SECRET"]
)

@mcp.tool()
def create_xray_test(
    project_key: str,
    summary: str,
    steps: list
) -> dict:
    """
    Create a Manual Xray Test in Jira Cloud.
    """
    test_key = xray_client.create_manual_test(
        project_key=project_key,
        summary=summary,
        steps=steps
    )

    return {
        "status": "success",
        "test_key": test_key
    }

@mcp.tool()
def generate_xray_csv_from_acceptance_criteria(
    acceptance_criteria: str,
    output_dir: str = "./artifacts/xray"
) -> dict:
    """
    Generate Xray test cases in CSV format from Jira acceptance criteria.
    """
    test_cases = generate_xray_test_cases(acceptance_criteria)
    csv_path = write_xray_csv(test_cases, output_dir)

    return {
        "status": "success",
        "test_count": len(test_cases),
        "csv_path": csv_path
    }

if __name__ == "__main__":
    mcp.run()
