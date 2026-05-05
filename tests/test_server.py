"""Tests for MCP server tool functions."""

import json
from unittest.mock import patch, MagicMock

import pytest


@pytest.fixture
def mock_corpus():
    """Patch the corpus used by server tools."""
    with patch("philosophy_mcp.server.corpus") as mock:
        yield mock


@pytest.fixture(autouse=True)
def _import_tools(mock_corpus):
    """Import tool functions after patching corpus."""
    global search_glossario, get_glossario, listar_glossario
    global listar_sinteses, get_sintese
    global listar_pensadores, buscar_pensador, get_pensador
    global listar_artigos, get_artigo, search_artigos
    global search, corpus_stats

    from philosophy_mcp.server import (
        search_glossario,
        get_glossario,
        listar_glossario,
        listar_sinteses,
        get_sintese,
        listar_pensadores,
        buscar_pensador,
        get_pensador,
        listar_artigos,
        get_artigo,
        search_artigos,
        search,
        corpus_stats,
    )


class TestGlossarioTools:
    def test_search_glossario_found(self, mock_corpus):
        mock_corpus.search_glossario.return_value = [{"slug": "logos"}]
        result = search_glossario("logos")
        parsed = json.loads(result)
        assert parsed[0]["slug"] == "logos"

    def test_search_glossario_empty(self, mock_corpus):
        mock_corpus.search_glossario.return_value = []
        result = search_glossario("xyz")
        assert "No glossary entries found" in result

    def test_get_glossario_found(self, mock_corpus):
        mock_corpus.get_glossario.return_value = {"slug": "logos", "title": "Logos"}
        result = get_glossario("logos")
        parsed = json.loads(result)
        assert parsed["title"] == "Logos"

    def test_get_glossario_not_found(self, mock_corpus):
        mock_corpus.get_glossario.return_value = None
        result = get_glossario("nope")
        assert "not found" in result

    def test_listar_glossario(self, mock_corpus):
        mock_corpus.listar_glossario.return_value = [{"slug": "a"}, {"slug": "b"}]
        result = listar_glossario("pt")
        parsed = json.loads(result)
        assert len(parsed) == 2


class TestSinteseTools:
    def test_listar_sinteses(self, mock_corpus):
        mock_corpus.listar_sinteses.return_value = [{"slug": "medieval"}]
        result = listar_sinteses()
        assert "medieval" in result

    def test_get_sintese_found(self, mock_corpus):
        mock_corpus.get_sintese.return_value = {"slug": "medieval", "body": "..."}
        result = get_sintese("medieval")
        parsed = json.loads(result)
        assert parsed["slug"] == "medieval"

    def test_get_sintese_not_found(self, mock_corpus):
        mock_corpus.get_sintese.return_value = None
        result = get_sintese("xyz")
        assert "not found" in result


class TestPensadorTools:
    def test_listar_pensadores(self, mock_corpus):
        mock_corpus.listar_pensadores.return_value = [{"slug": "socrates"}]
        result = listar_pensadores()
        assert "socrates" in result

    def test_buscar_pensador_found(self, mock_corpus):
        mock_corpus.buscar_pensador.return_value = [{"name": "Kant"}]
        result = buscar_pensador("Kant")
        parsed = json.loads(result)
        assert parsed[0]["name"] == "Kant"

    def test_buscar_pensador_empty(self, mock_corpus):
        mock_corpus.buscar_pensador.return_value = []
        result = buscar_pensador("xyz")
        assert "No thinker found" in result

    def test_get_pensador_found(self, mock_corpus):
        mock_corpus.get_pensador.return_value = {"slug": "socrates"}
        result = get_pensador("socrates")
        parsed = json.loads(result)
        assert parsed["slug"] == "socrates"

    def test_get_pensador_not_found(self, mock_corpus):
        mock_corpus.get_pensador.return_value = None
        result = get_pensador("xyz")
        assert "not found" in result


class TestArtigoTools:
    def test_listar_artigos(self, mock_corpus):
        mock_corpus.listar_artigos.return_value = [{"slug": "art1"}]
        result = listar_artigos()
        assert "art1" in result

    def test_get_artigo_found(self, mock_corpus):
        mock_corpus.get_artigo.return_value = {"slug": "art1", "body": "text"}
        result = get_artigo("art1")
        parsed = json.loads(result)
        assert parsed["body"] == "text"

    def test_get_artigo_not_found(self, mock_corpus):
        mock_corpus.get_artigo.return_value = None
        result = get_artigo("xyz")
        assert "not found" in result

    def test_search_artigos_found(self, mock_corpus):
        mock_corpus.search_artigos.return_value = [{"title": "Niilismo"}]
        result = search_artigos("niilismo")
        parsed = json.loads(result)
        assert parsed[0]["title"] == "Niilismo"

    def test_search_artigos_empty(self, mock_corpus):
        mock_corpus.search_artigos.return_value = []
        result = search_artigos("xyz")
        assert "No articles found" in result


class TestGeneralTools:
    def test_search_found(self, mock_corpus):
        mock_corpus.search.return_value = [{"slug": "logos"}]
        result = search("logos")
        parsed = json.loads(result)
        assert len(parsed) == 1

    def test_search_empty(self, mock_corpus):
        mock_corpus.search.return_value = []
        result = search("xyz")
        assert "No results" in result

    def test_search_with_section(self, mock_corpus):
        mock_corpus.search.return_value = [{"slug": "logos"}]
        search("logos", section="glossario")
        mock_corpus.search.assert_called_with("logos", "pt", "glossario")

    def test_search_empty_section_becomes_none(self, mock_corpus):
        mock_corpus.search.return_value = []
        search("logos", section="")
        mock_corpus.search.assert_called_with("logos", "pt", None)

    def test_corpus_stats(self, mock_corpus):
        mock_corpus.stats.return_value = {"total": 648}
        result = corpus_stats()
        parsed = json.loads(result)
        assert parsed["total"] == 648
