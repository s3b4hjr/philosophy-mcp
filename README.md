# philosophy-mcp

An [MCP](https://modelcontextprotocol.io) server for a multilingual philosophy corpus — glossary, syntheses, thinker profiles, and articles in **Portuguese**, **English**, and **Spanish**.

**648 entries**: ~270 glossary terms, 11 period syntheses, ~107 thinker profiles, and articles from [Filosofia em Resumo](https://filosofiaemresumo.com.br).

---

## Quick Start

### Install from PyPI

```bash
pip install philosophy-mcp
```

### Use with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filosofia": {
      "command": "uvx",
      "args": ["philosophy-mcp"]
    }
  }
}
```

### Use with VS Code

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "filosofia": {
      "command": "uvx",
      "args": ["philosophy-mcp"]
    }
  }
}
```

That's it. The server connects to the public API automatically — no local files needed.

---

## What can it do?

Ask your AI assistant anything about philosophy. The MCP tools give it access to a curated corpus:

- *"O que é eudaimonia?"* → searches the glossary
- *"Tell me about Kant"* → fetches the thinker profile
- *"¿Cuáles son las síntesis disponibles?"* → lists period syntheses
- *"Search 'logos' across everything"* → full-text search

### Available Tools

| Tool | Description |
|---|---|
| `search_glossario(query, lang)` | Search glossary terms by keyword |
| `get_glossario(slug, lang)` | Full definition of a term by slug |
| `listar_glossario(lang)` | List all glossary terms |
| `listar_sinteses(lang)` | List period syntheses |
| `get_sintese(slug, lang)` | Full text of a period synthesis |
| `listar_pensadores(lang)` | List all thinker profiles |
| `buscar_pensador(query, lang)` | Search thinkers by name/keyword |
| `get_pensador(slug, lang)` | Full thinker profile |
| `listar_artigos(lang)` | List all articles |
| `get_artigo(slug, lang)` | Full article by slug |
| `search_artigos(query, lang)` | Search articles by keyword |
| `search(query, lang, section)` | Full-text search across corpus |
| `corpus_stats()` | Corpus statistics |

**`lang`**: `pt` (default), `en`, `es`

---

## Languages

All content is available in three languages:

| Language | Glossary | Syntheses | Thinkers | Articles |
|---|---|---|---|---|
| Português (pt) | ✓ | ✓ | ✓ | ✓ |
| English (en) | ✓ | ✓ | ✓ | ✓ |
| Español (es) | ✓ | ✓ | ✓ | ✓ |

---

## Data Source

The server connects to the public API at `filosofiaemresumo.com.br/api` automatically.

---

## Content Coverage

### Periods (Syntheses)

1. Pre-Socratics & Sophists (~600–400 BC)
2. Socrates, Plato & Aristotle
3. Hellenistic Philosophy
4. Medieval Philosophy
5. Humanism & Renaissance
6. Scientific Revolution
7. Rationalism & Empiricism
8. Contractualism, Enlightenment & Kant
9. German Idealism
10. 19th Century Philosophy
11. 20th Century Philosophy

### Thinkers (~107 profiles)

From Thales of Miletus to Judith Butler — including Socrates, Plato, Aristotle, Descartes, Kant, Hegel, Marx, Nietzsche, Heidegger, Sartre, Foucault, and many more.

### Glossary (~90 terms per language)

Key philosophical concepts: arché, eudaimonia, logos, phronesis, noumeno, Aufhebung, categorical imperative, will to power, and more.

---

## License

MIT
