import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("playwright-runner")

@mcp.tool()
def run_playwright_tests(
    test_path: str = "tests",
    project_dir: str = "tests"
) -> dict:
    """
    Run Playwright tests via pytest.

    Args:
        test_path: Path to test file or folder (relative to project_dir)
        project_dir: Root Playwright project directory

    Returns:
        Structured test results
    """

    project_dir = Path(project_dir).resolve()
    test_target = project_dir / test_path

    if not project_dir.exists():
        return {"status": "error", "message": "Playwright project directory not found"}

    if not test_target.exists():
        return {"status": "error", "message": f"Test path not found: {test_target}"}

    cmd = [
        "pytest",
        str(test_target),
        "-v"
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        return {
            "status": "success" if result.returncode == 0 else "failed",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "cwd": str(project_dir)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    mcp.run()
