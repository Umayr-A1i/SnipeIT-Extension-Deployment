import requests
from dataclasses import dataclass


@dataclass
class SnipeItClient:
    """
    Minimal client for talking to the Snipe-IT API.
    Expects:
      - base_url like: http://18.132.137.45:8080/api/v1/
      - api_token: Snipe-IT API token string
    """
    base_url: str
    api_token: str

    def __post_init__(self) -> None:
        # Normalise base URL so we can safely append endpoints
        if not self.base_url.endswith("/"):
            self.base_url += "/"

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_token}",
                "Accept": "application/json",
            }
        )

    def version(self) -> dict:
        """
        Call the Snipe-IT /version endpoint.
        Used as the primary health check for the API.
        """
        resp = self.session.get(self.base_url + "version", timeout=10)
        resp.raise_for_status()
        return resp.json()

    def ping(self) -> dict:
        """
        Backwards-compatible 'ping' that just wraps the /version call.
        """
        data = self.version()
        return {"status": "success", "snipeit": data}

    def list_assets(self, search: str | None = None) -> dict:
        """
        List hardware assets from Snipe-IT.
        Optionally filter by a search term.
        """
        params: dict[str, str] = {}
        if search:
            params["search"] = search

        resp = self.session.get(self.base_url + "hardware", params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()


