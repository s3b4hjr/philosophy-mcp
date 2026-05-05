"""Tests for RemoteCorpus client."""

import json
import urllib.error
from unittest.mock import patch, MagicMock

import pytest

from philosophy_mcp.remote import RemoteCorpus


@pytest.fixture
def corpus():
    return RemoteCorpus("https://example.com/api")


def _mock_response(data):
    """Create a mock urlopen context manager returning JSON data."""
    body = json.dumps(data).encode("utf-8")
    resp = MagicMock()
    resp.read.return_value = body
    resp.__enter__ = lambda s: s
    resp.__exit__ = MagicMock(return_value=False)
    return resp


class TestRemoteCorpusInit:
    def test_strips_trailing_slash(self):
        c = RemoteCorpus("https://example.com/api/")
        assert c.api_url == "https://example.com/api"

    def test_default_url(self):
        c = RemoteCorpus()
        assert c.api_url == "https://filosofiaemresumo.com.br/api"


class TestGet:
    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_simple(self, mock_urlopen, corpus):
        mock_urlopen.return_value = _mock_response({"key": "value"})
        result = corpus._get("/test")
        assert result == {"key": "value"}
        call_args = mock_urlopen.call_args
        req = call_args[0][0]
        assert req.full_url == "https://example.com/api/test"

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_with_params(self, mock_urlopen, corpus):
        mock_urlopen.return_value = _mock_response([])
        corpus._get("/test", {"q": "logos", "lang": "pt"})
        call_args = mock_urlopen.call_args
        req = call_args[0][0]
        assert "q=logos" in req.full_url
        assert "lang=pt" in req.full_url


class TestGlossario:
    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_search_glossario(self, mock_urlopen, corpus):
        data = [{"slug": "logos", "title": "Logos"}]
        mock_urlopen.return_value = _mock_response(data)
        result = corpus.search_glossario("logos", "pt")
        assert result == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_search_glossario_error_returns_empty(self, mock_urlopen, corpus):
        mock_urlopen.side_effect = urllib.error.URLError("fail")
        result = corpus.search_glossario("logos", "pt")
        assert result == []

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_glossario(self, mock_urlopen, corpus):
        data = {"slug": "logos", "title": "Logos", "body": "..."}
        mock_urlopen.return_value = _mock_response(data)
        result = corpus.get_glossario("logos", "pt")
        assert result == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_glossario_error_returns_none(self, mock_urlopen, corpus):
        mock_urlopen.side_effect = urllib.error.URLError("fail")
        result = corpus.get_glossario("logos", "pt")
        assert result is None

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_listar_glossario(self, mock_urlopen, corpus):
        data = [{"slug": "a"}, {"slug": "b"}]
        mock_urlopen.return_value = _mock_response(data)
        result = corpus.listar_glossario("en")
        assert len(result) == 2


class TestSinteses:
    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_listar_sinteses(self, mock_urlopen, corpus):
        data = [{"slug": "pre-socraticos"}]
        mock_urlopen.return_value = _mock_response(data)
        result = corpus.listar_sinteses("pt")
        assert result == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_sintese(self, mock_urlopen, corpus):
        data = {"slug": "medieval", "body": "..."}
        mock_urlopen.return_value = _mock_response(data)
        result = corpus.get_sintese("medieval", "pt")
        assert result == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_sintese_error_returns_none(self, mock_urlopen, corpus):
        mock_urlopen.side_effect = urllib.error.URLError("fail")
        assert corpus.get_sintese("x", "pt") is None


class TestPensadores:
    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_listar_pensadores(self, mock_urlopen, corpus):
        data = [{"slug": "socrates"}, {"slug": "platao"}]
        mock_urlopen.return_value = _mock_response(data)
        assert len(corpus.listar_pensadores("pt")) == 2

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_buscar_pensador(self, mock_urlopen, corpus):
        data = [{"slug": "kant", "name": "Immanuel Kant"}]
        mock_urlopen.return_value = _mock_response(data)
        result = corpus.buscar_pensador("Kant", "pt")
        assert result[0]["name"] == "Immanuel Kant"

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_buscar_pensador_error_returns_empty(self, mock_urlopen, corpus):
        mock_urlopen.side_effect = urllib.error.URLError("fail")
        assert corpus.buscar_pensador("Kant", "pt") == []

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_pensador(self, mock_urlopen, corpus):
        data = {"slug": "socrates", "bio": "..."}
        mock_urlopen.return_value = _mock_response(data)
        result = corpus.get_pensador("socrates", "pt")
        assert result == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_pensador_error_returns_none(self, mock_urlopen, corpus):
        mock_urlopen.side_effect = urllib.error.URLError("fail")
        assert corpus.get_pensador("x", "pt") is None


class TestArtigos:
    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_listar_artigos(self, mock_urlopen, corpus):
        data = [{"slug": "art1"}]
        mock_urlopen.return_value = _mock_response(data)
        assert corpus.listar_artigos("pt") == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_artigo(self, mock_urlopen, corpus):
        data = {"slug": "art1", "body": "content"}
        mock_urlopen.return_value = _mock_response(data)
        assert corpus.get_artigo("art1", "pt") == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_get_artigo_error_returns_none(self, mock_urlopen, corpus):
        mock_urlopen.side_effect = urllib.error.URLError("fail")
        assert corpus.get_artigo("x", "pt") is None

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_search_artigos(self, mock_urlopen, corpus):
        data = [{"slug": "art1", "title": "Niilismo"}]
        mock_urlopen.return_value = _mock_response(data)
        result = corpus.search_artigos("niilismo", "pt")
        assert result == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_search_artigos_error_returns_empty(self, mock_urlopen, corpus):
        mock_urlopen.side_effect = urllib.error.URLError("fail")
        assert corpus.search_artigos("x", "pt") == []


class TestSearch:
    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_search_all(self, mock_urlopen, corpus):
        data = [{"slug": "logos", "section": "glossario"}]
        mock_urlopen.return_value = _mock_response(data)
        result = corpus.search("logos", "pt")
        assert result == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_search_with_section(self, mock_urlopen, corpus):
        data = [{"slug": "logos"}]
        mock_urlopen.return_value = _mock_response(data)
        corpus.search("logos", "pt", "glossario")
        req = mock_urlopen.call_args[0][0]
        assert "section=glossario" in req.full_url

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_search_error_returns_empty(self, mock_urlopen, corpus):
        mock_urlopen.side_effect = urllib.error.URLError("fail")
        assert corpus.search("x", "pt") == []


class TestStats:
    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_stats(self, mock_urlopen, corpus):
        data = {"total": 648}
        mock_urlopen.return_value = _mock_response(data)
        assert corpus.stats() == data

    @patch("philosophy_mcp.remote.urllib.request.urlopen")
    def test_stats_error(self, mock_urlopen, corpus):
        mock_urlopen.side_effect = urllib.error.URLError("fail")
        result = corpus.stats()
        assert "error" in result
