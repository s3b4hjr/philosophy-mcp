"""
MCP Server for the Philosophy corpus.
Exposes glossary, syntheses, thinker profiles, and articles as tools.
Runs via stdio — configure in VS Code or Claude Desktop.

Data source: public API at filosofiaemresumo.com.br
Override with FILOSOFIA_API_URL environment variable.
"""

import os
import json
from mcp.server.fastmcp import FastMCP
from philosophy_mcp.remote import RemoteCorpus

api_url = os.environ.get("FILOSOFIA_API_URL", "https://filosofiaemresumo.com.br/api")
corpus = RemoteCorpus(api_url)

mcp = FastMCP(
    "filosofia",
    instructions="Philosophy corpus: glossary, syntheses, thinker profiles, and articles in PT/EN/ES",
)


# ── Glossary ──────────────────────────────────────────────────

@mcp.tool()
def search_glossario(query: str, lang: str = "pt") -> str:
    """Search philosophical terms in the glossary by keyword.

    Args:
        query: Search term (e.g. 'eudaimonia', 'virtude', 'logos')
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    results = corpus.search_glossario(query, lang)
    if not results:
        return f"No glossary entries found for '{query}' in {lang}."
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_glossario(slug: str, lang: str = "pt") -> str:
    """Get the full definition of a glossary term by its slug.

    Args:
        slug: URL slug of the term (e.g. 'eudaimonia', 'imperativo-categorico')
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    result = corpus.get_glossario(slug, lang)
    if not result:
        return f"Glossary term '{slug}' not found in {lang}."
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def listar_glossario(lang: str = "pt") -> str:
    """List all available glossary terms.

    Args:
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    results = corpus.listar_glossario(lang)
    return json.dumps(results, ensure_ascii=False, indent=2)


# ── Syntheses ─────────────────────────────────────────────────

@mcp.tool()
def listar_sinteses(lang: str = "pt") -> str:
    """List all philosophical period syntheses (Pre-Socratics through 20th century).

    Args:
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    results = corpus.listar_sinteses(lang)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_sintese(slug: str, lang: str = "pt") -> str:
    """Get the full text of a period synthesis.

    Args:
        slug: Slug or partial match (e.g. 'pre-socraticos', '01', 'medieval')
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    result = corpus.get_sintese(slug, lang)
    if not result:
        return f"Synthesis '{slug}' not found in {lang}. Use listar_sinteses() to see available slugs."
    return json.dumps(result, ensure_ascii=False, indent=2)


# ── Thinkers ──────────────────────────────────────────────────

@mcp.tool()
def listar_pensadores(lang: str = "pt") -> str:
    """List all philosopher/thinker profiles available.

    Args:
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    results = corpus.listar_pensadores(lang)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def buscar_pensador(query: str, lang: str = "pt") -> str:
    """Search thinker profiles by name or keyword.

    Args:
        query: Search term (e.g. 'Sócrates', 'Kant', 'estoicismo')
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    results = corpus.buscar_pensador(query, lang)
    if not results:
        return f"No thinker found for '{query}' in {lang}."
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_pensador(slug: str, lang: str = "pt") -> str:
    """Get the full profile of a philosopher/thinker.

    Args:
        slug: Slug or name (e.g. 'socrates', 'Kant', 'aristoteles')
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    result = corpus.get_pensador(slug, lang)
    if not result:
        return f"Thinker '{slug}' not found in {lang}. Use buscar_pensador() to search."
    return json.dumps(result, ensure_ascii=False, indent=2)


# ── Articles ──────────────────────────────────────────────────

@mcp.tool()
def listar_artigos(lang: str = "pt") -> str:
    """List all available articles.

    Args:
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    results = corpus.listar_artigos(lang)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_artigo(slug: str, lang: str = "pt") -> str:
    """Get the full text of an article by slug.

    Args:
        slug: URL slug of the article (e.g. 'pre-socraticos-filosofia-grega')
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    result = corpus.get_artigo(slug, lang)
    if not result:
        return f"Article '{slug}' not found in {lang}."
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def search_artigos(query: str, lang: str = "pt") -> str:
    """Search articles by keyword in title or body.

    Args:
        query: Search term (e.g. 'niilismo', 'Butler', 'Maréchal')
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
    """
    results = corpus.search_artigos(query, lang)
    if not results:
        return f"No articles found for '{query}' in {lang}."
    return json.dumps(results, ensure_ascii=False, indent=2)


# ── General ───────────────────────────────────────────────────

@mcp.tool()
def search(query: str, lang: str = "pt", section: str = "") -> str:
    """Full-text search across the entire philosophy corpus.

    Args:
        query: Search term
        lang: Language code — 'pt', 'en', or 'es' (default: 'pt')
        section: Optional filter — 'glossario', 'sinteses', 'pensadores', or 'artigos'
    """
    sec = section if section else None
    results = corpus.search(query, lang, sec)
    if not results:
        return f"No results for '{query}' in {lang}."
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def corpus_stats() -> str:
    """Get statistics about the philosophy corpus (total entries, by section, by language)."""
    return json.dumps(corpus.stats(), ensure_ascii=False, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
