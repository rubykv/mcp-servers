# xray_client.py
import requests
from typing import List, Dict
import csv
import os
from datetime import datetime

class XrayClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://xray.cloud.getxray.app/api/v2"
        self.token = self._authenticate()

    def _authenticate(self) -> str:
        url = f"{self.base_url}/authenticate"
        response = requests.post(
            url,
            json={
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Xray auth failed: {response.status_code} - {response.text}"
            )

        return response.text.strip('"')

    def create_manual_test(
        self,
        project_key: str,
        summary: str,
        steps: List[Dict[str, str]]
    ) -> str:
        url = f"{self.base_url}/import/test"

        payload = {
            "tests": [
                {
                    "testType": "Manual",
                    "fields": {
                        "project": { "key": project_key },
                        "summary": summary
                    },
                    "steps": [
                        {
                            "action": step["action"],
                            "expectedResult": step["expected"]
                        }
                        for step in steps
                    ]
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Xray test creation failed: {response.status_code} - {response.text}"
            )

        data = response.json()
        return data["tests"][0]["key"]

    def generate_xray_test_cases(acceptance_criteria: str) -> List[Dict]:
        """
        Convert acceptance criteria text into structured Xray test steps.
        This is intentionally deterministic and simple.
        """
        tests = []

        # Simple heuristic split (you can improve later)
        lines = [l.strip("- ").strip() for l in acceptance_criteria.splitlines() if l.strip()]

        test_summary = "Auto-generated test from acceptance criteria"
        test_description = "Generated from Jira acceptance criteria"
        precondition = "System is available"

        for idx, line in enumerate(lines, start=1):
            tests.append({
                "Test Type": "Manual",
                "Test Summary": test_summary,
                "Test Description": test_description,
                "Precondition": precondition,
                "Step": f"Step {idx}: {line}",
                "Data": "",
                "Expected Result": f"{line} is successfully completed"
            })

        return tests


    def write_xray_csv(test_cases: List[Dict], output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)

        filename = f"xray-tests-{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"
        file_path = os.path.join(output_dir, filename)

        fieldnames = [
            "Test Type",
            "Test Summary",
            "Test Description",
            "Precondition",
            "Step",
            "Data",
            "Expected Result"
        ]

        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in test_cases:
                writer.writerow(row)

        return file_path
