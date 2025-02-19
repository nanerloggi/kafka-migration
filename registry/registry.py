from typing import Dict
from dataclasses import dataclass
from urllib.parse import quote

import requests
from requests.auth import HTTPBasicAuth


@dataclass
class Registry:
    url: str
    username: str
    password: str

    @staticmethod
    def _urlencode(url: str) -> str:
        return quote(url, safe="")

    def do(self, verb: str, endpoint: str, headers: Dict = {}, json: Dict = {}) -> Dict:
        response = (getattr(requests, verb)(
            url=f"{self.url}{endpoint}",
            auth=HTTPBasicAuth(self.username, self.password),
            headers={
                "Content-Type": "application/json",
                **headers,
            },
            json=json,
        ))

        # response.raise_for_status()
        return response.json(), response.status_code
    
    def subjects(self):
        response, _ = self.do("get", "/subjects")
        return response
    
    def versions(self, subject: str):
        response, _ = self.do("get", f"/subjects/{self._urlencode(subject)}/versions")
        return response
    
    def version(self, subject: str, version: str):
        response, _ = self.do("get", f"/subjects/{self._urlencode(subject)}/versions/{version}")
        return response

    def delete(self, subject: str):
        for version in self.do("get", f"/subjects/{self._urlencode(subject)}/versions"):
            self.do("delete", f"/subjects/{self._urlencode(subject)}/versions/{version}?permanent=true")

        return self.do("delete", f"/subjects/{self._urlencode(subject)}?permanent=true")
    
    def create(self, subject: str, schema: Dict):
        self.import_mode(subject)
        return self.do("post", f"/subjects/{self._urlencode(subject)}/versions", json=schema)

    def get_mode(self, subject: str):
        try:
            response, _ = self.do("get", f"/mode/{self._urlencode(subject)}")
            return response.get("mode", "UNKNOWN")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return "IMPORT"
            raise

    def set_mode(self, mode: str, subject=str()):
        endpoint = "/mode"

        if subject:
            endpoint += f"/{self._urlencode(subject)}"

        return self.do("put", endpoint, json={"mode": mode.upper()})

    def set_global_import_mode(self):
        return self.set_mode(mode="IMPORT")

    def set_import_mode_on_subject(self, subject: str):
        if self.get_mode(subject) != "IMPORT":
            return self.set_mode(mode="IMPORT", subject=subject)

    def set_readwrite_mode_on_subject(self, subject: str):
        return self.set_mode(mode="READWRITE", subject=subject)
