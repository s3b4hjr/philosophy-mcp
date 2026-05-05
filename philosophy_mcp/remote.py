"""
Remote client for the Filosofia API.
Used by the MCP server when no local hugo_content/ is available.
"""

import urllib.request
import urllib.parse
import json
import ssl
from typing import Optional

try:
    import certifi
    _ssl_ctx = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _ssl_ctx = ssl.create_default_context()


DEFAULT_API_URL = "https://filosofiaemresumo.com.br/api"


class RemoteCorpus:
    """Queries the public Filosofia API instead of local files."""

    def __init__(self, api_url: str = DEFAULT_API_URL):
        self.api_url = api_url.rstrip("/")

    def _get(self, path: str, params: Optional[dict] = None) -> any:
        url = f"{self.api_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "philosophy-mcp/0.1",
        })
        with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # ── Glossary ──────────────────────────────────────────

    def search_glossario(self, query: str, lang: str = "pt") -> list[dict]:
        try:
            return self._get("/glossario/search", {"q": query, "lang": lang})
        except Exception:
            return []

    def get_glossario(self, slug: str, lang: str = "pt") -> Optional[dict]:
        try:
            return self._get(f"/glossario/{urllib.parse.quote(slug)}", {"lang": lang})
        except Exception:
            return None

    def listar_glossario(self, lang: str = "pt") -> list[dict]:
        try:
            return self._get("/glossario", {"lang": lang})
        except Exception:
            return []

    # ── Syntheses ─────────────────────────────────────────

    def listar_sinteses(self, lang: str = "pt") -> list[dict]:
        try:
            return self._get("/sinteses", {"lang": lang})
        except Exception:
            return []

    def get_sintese(self, slug: str, lang: str = "pt") -> Optional[dict]:
        try:
            return self._get(f"/sinteses/{urllib.parse.quote(slug)}", {"lang": lang})
        except Exception:
            return None

    # ── Thinkers ──────────────────────────────────────────

    def listar_pensadores(self, lang: str = "pt") -> list[dict]:
        try:
            return self._get("/pensadores", {"lang": lang})
        except Exception:
            return []

    def buscar_pensador(self, query: str, lang: str = "pt") -> list[dict]:
        try:
            return self._get("/pensadores/search", {"q": query, "lang": lang})
        except Exception:
            return []

    def get_pensador(self, slug: str, lang: str = "pt") -> Optional[dict]:
        try:
            return self._get(f"/pensadores/{urllib.parse.quote(slug)}", {"lang": lang})
        except Exception:
            return None

    # ── Articles ──────────────────────────────────────────

    def listar_artigos(self, lang: str = "pt") -> list[dict]:
        try:
            return self._get("/artigos", {"lang": lang})
        except Exception:
            return []

    def get_artigo(self, slug: str, lang: str = "pt") -> Optional[dict]:
        try:
            return self._get(f"/artigos/{urllib.parse.quote(slug)}", {"lang": lang})
        except Exception:
            return None

    def search_artigos(self, query: str, lang: str = "pt") -> list[dict]:
        try:
            return self._get("/artigos/search", {"q": query, "lang": lang})
        except Exception:
            return []

    # ── General ───────────────────────────────────────────

    def search(self, query: str, lang: str = "pt", section: Optional[str] = None) -> list[dict]:
        params = {"q": query, "lang": lang}
        if section:
            params["section"] = section
        try:
            return self._get("/search", params)
        except Exception:
            return []

    def stats(self) -> dict:
        try:
            return self._get("/stats")
        except Exception:
            return {"error": "API unavailable"}
