# xray_client.py
import requests
from typing import List, Dict

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
