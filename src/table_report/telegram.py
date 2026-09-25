"""Sending the finished report to a Telegram chat."""

from __future__ import annotations

from pathlib import Path

import httpx

API_URL = "https://api.telegram.org"
CAPTION_LIMIT = 1024


class TelegramError(RuntimeError):
    pass


def send_document(token: str, chat_id: str, path: Path, caption: str = "", client: httpx.Client | None = None) -> None:
    """Uploads a file with sendDocument. Error messages never contain the token."""
    owns_client = client is None
    client = client or httpx.Client(timeout=60)
    try:
        with path.open("rb") as file:
            response = client.post(
                f"{API_URL}/bot{token}/sendDocument",
                data={"chat_id": chat_id, "caption": caption[:CAPTION_LIMIT]},
                files={"document": (path.name, file)},
            )
    except httpx.HTTPError as exc:
        raise TelegramError(f"Network error while sending to Telegram: {type(exc).__name__}") from None
    finally:
        if owns_client:
            client.close()

    try:
        payload = response.json()
    except ValueError:
        payload = {}
    if response.status_code != 200 or not payload.get("ok"):
        description = payload.get("description", f"HTTP {response.status_code}")
        raise TelegramError(f"Telegram rejected the report: {description}")
