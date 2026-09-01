#!/usr/bin/env python3
"""
Awesome Agentic Ecosystem - Grand Master Index & Multi-Directory Generator
Automated deep discovery, strict quality filter, multi-category directory builder,
and master index generator for AI Agents, MCP Servers, Agent Skills, Plugins, and Frameworks.

Maintained by: tech.anupam
Support / Donate: https://anupambuilds.store/donate
Store: https://anupambuilds.store
"""

import argparse
import datetime
import json
import os
import random
import sys
import time
from typing import Dict, List, Optional, Set, Tuple
import urllib.parse
import requests

# Ensure UTF-8 console output across all OS environments
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "tools.json")
README_FILE = os.path.join(BASE_DIR, "README.md")
CATEGORIES_DIR = os.path.join(BASE_DIR, "categories")
GITHUB_API_URL = "https://api.github.com"

# Quality thresholds & strict anti-junk gate
DEFAULT_MIN_STARS = 150
MAX_DAYS_INACTIVE = 180
MIN_DESC_LENGTH = 15

# Spam / low-quality blacklist keywords
SPAM_KEYWORDS = [
    "cheat", "hack", "crack", "keygen", "leak", "free-download",
    "homework", "assignment", "test-repo", "temp-repo", "coursework",
    "practice-repo", "tutorial-starter", "my-first-repo"
]

# Author & Branding config
AUTHOR_NAME = "tech-anupam"
AUTHOR_PROFILE = "https://github.com/tech-anupam"
REPO_URL = "https://github.com/tech-anupam/awesome-agentic-ecosystem"
DONATE_URL = "https://anupambuilds.store/donate"
STORE_URL = "https://anupambuilds.store"

CATEGORIES = {
    "ai_ides_editors": {
        "slug": "ai-ides-code-editors",
        "icon": "💻",
        "title": "AI Code Editors & Native IDEs",
        "description": "Next-generation AI-first code editors, IDE forks, and intelligent developer workbenches (Cursor, Windsurf, Trae, Void, PearAI, Zed AI).",
        "keywords": [
            "ai-editor", "ai-ide", "code-editor", "cursor", "windsurf", "trae",
            "void-editor", "pearai", "zed", "developer-environment", "ide-fork"
        ]
    },
    "cli_terminal_agents": {
        "slug": "cli-terminal-agents",
        "icon": "📟",
        "title": "CLI & Terminal Agent Tools",
        "description": "Interactive command-line agents, terminal pair programmers, and shell automation copilots (Claude Code, Gemini CLI, Aider, Goose, Mentat).",
        "keywords": [
            "cli-agent", "terminal-agent", "claude-code", "gemini-cli", "aider",
            "goose", "terminal-assistant", "shell-copilot", "cli-tool", "cli"
        ]
    },
    "autonomous_dev_agents": {
        "slug": "autonomous-dev-agents",
        "icon": "🤖",
        "title": "Autonomous Software Engineering Agents",
        "description": "Full-stack autonomous software engineers, issue solvers, and end-to-end project builders (OpenHands, SWE-agent, GPT-Pilot, MetaGPT, Devika).",
        "keywords": [
            "coding-agent", "coding-assistant", "swe-bench", "pair-programming",
            "code-generation", "openhands", "swe-agent", "gpt-pilot", "metagpt",
            "devika", "software-engineering-agent", "dev-agent"
        ]
    },
    "mcp_servers": {
        "slug": "mcp-servers",
        "icon": "🔌",
        "title": "Model Context Protocol (MCP) Servers",
        "description": "Standardized MCP servers, tool connectors, protocol implementations, and registries for Claude Desktop, Cursor, and custom agents.",
        "keywords": [
            "mcp-server", "model-context-protocol", "mcp", "claude-desktop",
            "mcp-client", "smithery", "modelcontextprotocol"
        ]
    },
    "agent_skills": {
        "slug": "agent-skills",
        "icon": "⚡",
        "title": "Agent Skills & Action Toolkits",
        "description": "Function calling suites, tool integrations, external API bridges, and executable skillsets (Composio, Toolhouse, ToolJet).",
        "keywords": [
            "agent-skills", "agent-tools", "function-calling", "tool-use",
            "composio", "toolhouse", "action-toolkit", "agent-actions", "agent-toolkit"
        ]
    },
    "plugins_extensions": {
        "slug": "plugins-extensions",
        "icon": "🧩",
        "title": "AI Plugins & IDE Extensions",
        "description": "VS Code extensions, Cursor rules, JetBrains plugins, and environment enhancers for coding assistants (Continue, Roo-Cline, Cursorrules).",
        "keywords": [
            "cursorrules", "vscode-extension", "ai-plugin",
            "copilot-extension", "jetbrains", "llm-plugin", "cursor-tools", "continue"
        ]
    },
    "browser_automation": {
        "slug": "browser-automation",
        "icon": "🌐",
        "title": "Browser & Desktop Automation",
        "description": "Vision-guided web agents, OS-level controllers, Playwright integrations, and GUI agents (Browser-Use, Stagehand, Open-Interpreter, UI-TARS).",
        "keywords": [
            "browser-agent", "browser-automation", "web-agent", "desktop-agent",
            "gui-agent", "playwright", "stagehand", "browser-use", "open-interpreter",
            "ui-tars", "skyvern", "lavague", "computer-use"
        ]
    },
    "frameworks_orchestration": {
        "slug": "frameworks-orchestration",
        "icon": "🧠",
        "title": "Multi-Agent Frameworks & Orchestration",
        "description": "Graph-based workflows, conversational multi-agent systems, and stateful agent coordinators (LangGraph, CrewAI, AutoGen, Dify, Swarm).",
        "keywords": [
            "multi-agent", "agentic-framework", "orchestration", "langgraph",
            "crewai", "autogen", "swarm", "agent-framework", "llama-agents", "agentic", "dify"
        ]
    },
    "memory_context": {
        "slug": "memory-context",
        "icon": "💾",
        "title": "Memory, Context & RAG Engines",
        "description": "Long-term memory layers, graph-based RAG engines, and persistent context architectures (Mem0, Letta/MemGPT, GraphRAG, Cognee).",
        "keywords": [
            "agent-memory", "memory-engine", "graphrag", "graph-rag", "memgpt",
            "mem0", "letta", "knowledge-graph", "context-engine", "cognee"
        ]
    },
    "evals_sandboxes": {
        "slug": "evals-sandboxes",
        "icon": "🧪",
        "title": "Evals, Sandboxes & Observability",
        "description": "Safe code execution environments, agent tracing, cost analysis, and evaluation benchmarks (E2B, Langfuse, AgentOps, Helicone).",
        "keywords": [
            "agent-sandbox", "agent-eval", "observability", "llm-tracing",
            "langfuse", "agentops", "e2b", "sandboxing", "evals", "helicone", "phoenix"
        ]
    }
}

SEARCH_QUERIES = [
    # AI IDEs & Editors
    {"query": "topic:ai-editor stars:>100", "cat_hint": "ai_ides_editors", "sort": "stars"},
    {"query": "topic:ai-ide stars:>100", "cat_hint": "ai_ides_editors", "sort": "stars"},
    {"query": "ai code editor stars:>250", "cat_hint": "ai_ides_editors", "sort": "stars"},

    # CLI & Terminal Agents
    {"query": "topic:cli-agent stars:>100", "cat_hint": "cli_terminal_agents", "sort": "stars"},
    {"query": "topic:terminal-agent stars:>100", "cat_hint": "cli_terminal_agents", "sort": "stars"},
    {"query": "claude-code stars:>200", "cat_hint": "cli_terminal_agents", "sort": "stars"},
    {"query": "ai cli coding stars:>300", "cat_hint": "cli_terminal_agents", "sort": "stars"},

    # Autonomous Dev Agents
    {"query": "topic:coding-agent stars:>150", "cat_hint": "autonomous_dev_agents", "sort": "stars"},
    {"query": "topic:swe-bench stars:>100", "cat_hint": "autonomous_dev_agents", "sort": "stars"},
    {"query": "autonomous software engineer agent stars:>300", "cat_hint": "autonomous_dev_agents", "sort": "stars"},

    # MCP Ecosystem
    {"query": "topic:mcp-server stars:>100", "cat_hint": "mcp_servers", "sort": "stars"},
    {"query": "topic:model-context-protocol", "cat_hint": "mcp_servers", "sort": "updated"},
    {"query": "topic:mcp stars:>200", "cat_hint": "mcp_servers", "sort": "stars"},

    # Skills & Toolkits
    {"query": "topic:agent-skills stars:>80", "cat_hint": "agent_skills", "sort": "updated"},
    {"query": "topic:agent-tools stars:>100", "cat_hint": "agent_skills", "sort": "stars"},
    {"query": "topic:function-calling stars:>150", "cat_hint": "agent_skills", "sort": "stars"},

    # Plugins & Extensions
    {"query": "topic:cursorrules stars:>200", "cat_hint": "plugins_extensions", "sort": "stars"},
    {"query": "topic:vscode-extension ai agent stars:>200", "cat_hint": "plugins_extensions", "sort": "stars"},

    # Browser & Desktop Automation
    {"query": "topic:browser-agent stars:>100", "cat_hint": "browser_automation", "sort": "stars"},
    {"query": "topic:browser-automation ai stars:>200", "cat_hint": "browser_automation", "sort": "updated"},
    {"query": "topic:gui-agent stars:>80", "cat_hint": "browser_automation", "sort": "stars"},

    # Multi-Agent Frameworks
    {"query": "topic:multi-agent stars:>300", "cat_hint": "frameworks_orchestration", "sort": "stars"},
    {"query": "topic:agentic-framework stars:>150", "cat_hint": "frameworks_orchestration", "sort": "updated"},

    # Memory & Context
    {"query": "topic:agent-memory stars:>100", "cat_hint": "memory_context", "sort": "stars"},
    {"query": "topic:graphrag stars:>200", "cat_hint": "memory_context", "sort": "stars"},

    # Sandboxes, Evals & Observability
    {"query": "topic:agent-sandbox stars:>80", "cat_hint": "evals_sandboxes", "sort": "updated"},
    {"query": "topic:agent-eval stars:>80", "cat_hint": "evals_sandboxes", "sort": "stars"},

    # Broad high-signal queries
    {"query": "topic:ai-agent stars:>1000", "cat_hint": None, "sort": "updated"},
    {"query": "topic:autonomous-agent stars:>800", "cat_hint": None, "sort": "stars"}
]


def get_github_headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Awesome-Agentic-Ecosystem-Crawler"
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_search_results(query: str, sort: str, page: int, per_page: int, headers: Dict[str, str]) -> Tuple[List[Dict], bool]:
    """Execute GitHub search query with pagination and rate limit check."""
    url = f"{GITHUB_API_URL}/search/repositories?q={urllib.parse.quote(query)}&sort={sort}&order=desc&page={page}&per_page={per_page}"
    try:
        resp = requests.get(url, headers=headers, timeout=12)
        if resp.status_code == 403:
            reset_ts = resp.headers.get("X-RateLimit-Reset")
            print(f"[!] GitHub API rate limit reached. Reset at timestamp {reset_ts}", flush=True)
            return [], True
        if resp.status_code != 200:
            print(f"[!] Query failed ({resp.status_code}): {query}", flush=True)
            return [], False
        return resp.json().get("items", []), False
    except Exception as e:
        print(f"[!] Request error on '{query}': {e}", flush=True)
        return [], False


def is_quality_repo(repo: Dict, min_stars: int = DEFAULT_MIN_STARS) -> bool:
    """
    Strict Quality Gate:
    Filters out archived projects, spam, low-effort forks, dead repos, or empty toys.
    """
    if repo.get("archived", False):
        return False
    if repo.get("fork", False) and repo.get("stargazers_count", 0) < 500:
        return False
    if repo.get("stargazers_count", 0) < min_stars:
        return False

    desc = (repo.get("description") or "").strip()
    name = (repo.get("name") or "").lower()

    if len(desc) < MIN_DESC_LENGTH:
        return False

    full_check_str = f"{name} {desc.lower()}"
    for spam_kw in SPAM_KEYWORDS:
        if spam_kw in full_check_str:
            return False

    pushed_at_str = repo.get("pushed_at")
    if pushed_at_str:
        try:
            pushed_dt = datetime.datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
            age_days = (datetime.datetime.now(datetime.timezone.utc) - pushed_dt).days
            if age_days > MAX_DAYS_INACTIVE:
                return False
        except Exception:
            pass

    return True


def categorize_repo(repo: Dict, cat_hint: Optional[str] = None) -> str:
    """Intelligently score and classify repository into one of the 10 canonical categories."""
    topics = [t.lower() for t in repo.get("topics", [])]
    name = (repo.get("name") or "").lower()
    description = (repo.get("description") or "").lower()

    scores: Dict[str, int] = {k: 0 for k in CATEGORIES}

    if cat_hint and cat_hint in CATEGORIES:
        scores[cat_hint] += 5

    for cat_key, cat_meta in CATEGORIES.items():
        for kw in cat_meta["keywords"]:
            if kw in topics:
                scores[cat_key] += 6
            if kw in name:
                scores[cat_key] += 4
            if kw in description:
                scores[cat_key] += 2

    best_category = max(scores, key=lambda k: scores[k])
    if scores[best_category] == 0:
        best_category = "frameworks_orchestration"

    return best_category


def load_tools() -> List[Dict]:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_tools(tools: List[Dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tools, f, indent=2, ensure_ascii=False)
        f.write("\n")


def update_and_discover(min_stars: int, limit: int, pages: int = 2, clean: bool = False) -> List[Dict]:
    """Execute dynamic discovery across rotated queries with strict deduplication."""
    existing_tools = [] if clean else load_tools()
    tools_by_name: Dict[str, Dict] = {t["full_name"].strip().lower(): t for t in existing_tools}
    headers = get_github_headers()

    auth_label = "Authenticated" if "Authorization" in headers else "Unauthenticated"
    print(f"[*] Starting Discovery Pipeline ({auth_label})", flush=True)
    print(f"[*] Base registry has {len(existing_tools)} tools.", flush=True)

    new_discoveries = 0
    updated_records = 0

    queries_to_run = list(SEARCH_QUERIES)
    random.shuffle(queries_to_run)

    stop_all = False
    for idx, q_entry in enumerate(queries_to_run, 1):
        if stop_all:
            break

        query = q_entry["query"]
        cat_hint = q_entry["cat_hint"]
        sort_by = q_entry.get("sort", "stars")

        print(f" [{idx}/{len(queries_to_run)}] Querying: '{query}' (sort={sort_by})...", flush=True)

        for page in range(1, pages + 1):
            items, is_rate_limited = fetch_search_results(
                query=query,
                sort=sort_by,
                page=page,
                per_page=limit,
                headers=headers
            )

            if is_rate_limited:
                print(f"[!] Stopping crawler early due to GitHub API rate limit.", flush=True)
                stop_all = True
                break

            if not items:
                break

            for item in items:
                full_name = (item.get("full_name") or "").strip()
                if not full_name:
                    continue

                if not is_quality_repo(item, min_stars=min_stars):
                    continue

                fn_key = full_name.lower()
                stars = item.get("stargazers_count", 0)
                forks = item.get("forks_count", 0)
                desc = item.get("description") or "No description provided."
                desc = desc.replace("\n", " ").replace("\r", "").replace("|", "-").strip()
                lang = item.get("language") or "Multi"

                if fn_key in tools_by_name:
                    tools_by_name[fn_key]["stars"] = stars
                    tools_by_name[fn_key]["forks"] = forks
                    tools_by_name[fn_key]["description"] = desc
                    tools_by_name[fn_key]["last_updated"] = datetime.date.today().isoformat()
                    # Re-verify category to match updated 10-category taxonomy
                    tools_by_name[fn_key]["category"] = categorize_repo(item, cat_hint=cat_hint)
                    updated_records += 1
                else:
                    cat = categorize_repo(item, cat_hint=cat_hint)
                    new_entry = {
                        "full_name": full_name,
                        "name": item.get("name", full_name.split("/")[-1]),
                        "url": item.get("html_url", f"https://github.com/{full_name}"),
                        "description": desc,
                        "category": cat,
                        "stars": stars,
                        "forks": forks,
                        "language": lang,
                        "topics": item.get("topics", [])[:6],
                        "added_at": datetime.date.today().isoformat(),
                        "last_updated": datetime.date.today().isoformat()
                    }
                    tools_by_name[fn_key] = new_entry
                    new_discoveries += 1
                    print(f"    [+] New Quality Discovery: {full_name} ({stars} stars) -> {cat}", flush=True)

            time.sleep(0.6)

    merged_tools = list(tools_by_name.values())
    merged_tools.sort(key=lambda x: x.get("stars", 0), reverse=True)
    save_tools(merged_tools)

    print(f"[*] Complete: {len(merged_tools)} total unique tools (+{new_discoveries} new, {updated_records} updated).", flush=True)
    return merged_tools


def format_star_count(stars: int) -> str:
    if stars >= 1000:
        return f"{stars / 1000:.1f}k"
    return str(stars)


def generate_category_readmes(tools: List[Dict], by_cat: Dict[str, List[Dict]], last_sync: str):
    """Generate individual detailed README.md files in each category directory."""
    os.makedirs(CATEGORIES_DIR, exist_ok=True)

    for cat_key, cat_meta in CATEGORIES.items():
        cat_folder = os.path.join(CATEGORIES_DIR, cat_meta["slug"])
        os.makedirs(cat_folder, exist_ok=True)
        cat_file = os.path.join(cat_folder, "README.md")

        cat_tools = by_cat.get(cat_key, [])
        cat_stars = sum(t.get("stars", 0) for t in cat_tools)

        lines = []
        lines.append(f"# {cat_meta['icon']} {cat_meta['title']}")
        lines.append("")
        lines.append(f"> {cat_meta['description']}")
        lines.append("")
        lines.append(f"[← Back to Grand Master Index](../../README.md) • [⭐ Star Repository]({REPO_URL})")
        lines.append("")
        lines.append(f"[![Tools in Category](https://img.shields.io/badge/Tools-{len(cat_tools)}-blue.svg?style=for-the-badge)](./) ")
        lines.append(f"[![Category Stars](https://img.shields.io/badge/Category%20Stars-{format_star_count(cat_stars)}+-yellow.svg?style=for-the-badge)]({REPO_URL}) ")
        lines.append(f"[![Updated](https://img.shields.io/badge/Updated-{last_sync}-orange.svg?style=for-the-badge)]({REPO_URL})")
        lines.append("")
        lines.append("---")
        lines.append("")

        if not cat_tools:
            lines.append("*No tools currently catalogued in this category.*")
        else:
            lines.append("## 🏆 Curated Collection")
            lines.append("")
            lines.append("| Tool | Description | Stars | Language | Direct Link |")
            lines.append("| :--- | :--- | :---: | :---: | :---: |")
            for t in cat_tools:
                badge = f"[![Stars](https://img.shields.io/github/stars/{t['full_name']}?style=flat&label=⭐)]({t['url']})"
                lang = t.get("language") or "Multi"
                lines.append(f"| [**`{t['name']}`**]({t['url']}) | {t['description']} | {badge} | `{lang}` | [Explore ↗]({t['url']}) |")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"[← Back to Grand Master Index](../../README.md) • [💖 Support & Donate]({DONATE_URL})")

        with open(cat_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    print(f"[*] Successfully generated {len(CATEGORIES)} category directory READMEs in {CATEGORIES_DIR}.", flush=True)


def generate_master_readme(tools: List[Dict]):
    """Build Grand Master Index README linking directly to category directories and trending tools."""
    # Re-verify and update any category mapping changes
    for t in tools:
        if t.get("category") not in CATEGORIES:
            t["category"] = categorize_repo(t)

    total_tools = len(tools)
    total_stars = sum(t.get("stars", 0) for t in tools)
    last_sync = datetime.date.today().isoformat()

    trending_top = sorted(tools, key=lambda x: x.get("stars", 0), reverse=True)[:10]

    by_cat: Dict[str, List[Dict]] = {k: [] for k in CATEGORIES}
    for t in tools:
        cat = t.get("category", "frameworks_orchestration")
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(t)

    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: x.get("stars", 0), reverse=True)

    # First, generate all category subfolders & sub-readmes
    generate_category_readmes(tools, by_cat, last_sync)

    lines = []

    # Title & Hero
    lines.append("# ⚡ Awesome Agentic Ecosystem")
    lines.append("")
    lines.append("> A curated, fully automated grand master index of high-impact **AI Agents**, **Model Context Protocol (MCP) Servers**, **AI IDEs & Editors**, **CLI Agent Tools**, **Agent Skills**, and **Multi-Agent Frameworks**. Only useful, battle-tested tools — zero junk. 🤖🔌💻")
    lines.append("")

    # Badges Row 1: Metrics
    lines.append(f"[![Total Tools](https://img.shields.io/badge/Total%20Tools-{total_tools}-blue.svg?style=for-the-badge&logo=github)](./tools.json) ")
    lines.append(f"[![Total Stars Tracked](https://img.shields.io/badge/Total%20Stars-{format_star_count(total_stars)}+-yellow.svg?style=for-the-badge&logo=apachespark)]({REPO_URL}) ")
    lines.append(f"[![Auto Sync](https://img.shields.io/badge/Auto%20Sync-Daily%20Cron-brightgreen.svg?style=for-the-badge&logo=githubactions)](./.github/workflows/update.yml) ")
    lines.append(f"[![Last Updated](https://img.shields.io/badge/Updated-{last_sync}-orange.svg?style=for-the-badge)]({REPO_URL}) ")
    lines.append(f"[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg?style=for-the-badge)](./LICENSE)")
    lines.append("")

    # Badges Row 2: Author & Donate
    lines.append(f"[![Maintainer](https://img.shields.io/badge/Maintainer-{AUTHOR_NAME}-00C7B7.svg?style=for-the-badge&logo=github)]({AUTHOR_PROFILE}) ")
    lines.append(f"[![Support & Donate](https://img.shields.io/badge/Support-Donate%20Here-FF5E5B.svg?style=for-the-badge&logo=kofi&logoColor=white)]({DONATE_URL}) ")
    lines.append(f"[![Store](https://img.shields.io/badge/Store-anupambuilds.store-7952B3.svg?style=for-the-badge&logo=shopify&logoColor=white)]({STORE_URL})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Interactive Category Hub / Directory Index Cards
    lines.append("## 📂 Explore by Category Directory")
    lines.append("")
    lines.append("| Category Directory | Folder Link | Curated Tools | Focus Area |")
    lines.append("| :--- | :--- | :---: | :--- |")
    for cat_key, cat_meta in CATEGORIES.items():
        count = len(by_cat.get(cat_key, []))
        folder_link = f"[`categories/{cat_meta['slug']}/`](./categories/{cat_meta['slug']}/)"
        lines.append(f"| {cat_meta['icon']} **{cat_meta['title']}** | {folder_link} | `{count} tools` | {cat_meta['description']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Top 10 Trending
    lines.append("## 🔥 Top 10 Starred & Trending Tools")
    lines.append("")
    lines.append("| Rank | Tool | Category Directory | Stars | Language | Description |")
    lines.append("| :---: | :--- | :--- | :---: | :---: | :--- |")
    for idx, t in enumerate(trending_top, 1):
        cat_meta = CATEGORIES.get(t.get("category", ""), {})
        cat_slug = cat_meta.get("slug", "frameworks-orchestration")
        cat_icon = cat_meta.get("icon", "📦")
        cat_label = f"[{cat_icon} {cat_meta.get('title', 'Tools')}](./categories/{cat_slug}/)"
        stars_formatted = format_star_count(t.get("stars", 0))
        lines.append(f"| **#{idx}** | [**`{t['name']}`**]({t['url']}) | {cat_label} | ⭐ `{stars_formatted}` | `{t.get('language', 'Multi')}` | {t['description']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Recently Added
    recent_tools = sorted(tools, key=lambda x: x.get("added_at", "2000-01-01"), reverse=True)[:6]
    lines.append("## 🆕 Recently Discovered")
    lines.append("")
    lines.append("| Tool | Discovered Date | Stars | Category Directory |")
    lines.append("| :--- | :---: | :---: | :--- |")
    for t in recent_tools:
        cat_meta = CATEGORIES.get(t.get("category", ""), {})
        cat_slug = cat_meta.get("slug", "frameworks-orchestration")
        cat_icon = cat_meta.get("icon", "📦")
        cat_link = f"[{cat_icon} {cat_meta.get('title', 'Category')}](./categories/{cat_slug}/)"
        lines.append(f"| [**`{t['name']}`**]({t['url']}) | `{t.get('added_at', 'N/A')}` | ⭐ `{format_star_count(t.get('stars', 0))}` | {cat_link} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Strict Quality Standards Policy
    lines.append("## 🛡️ Strict Quality & Anti-Junk Gate")
    lines.append("")
    lines.append("Every repository tracked in this collection must pass automated quality benchmarks:")
    lines.append("")
    lines.append("- ✅ **High Community Signal**: Minimum star threshold (>= 150-200+ stars).")
    lines.append("- ✅ **Active Maintenance**: Discards archived, abandoned, or stale repositories (>180 days inactive).")
    lines.append("- ✅ **Original Utility**: Excludes empty forks, tutorial copies, assignment homework, and placeholder toys.")
    lines.append("- ✅ **Strict Deduplication**: Verified against canonical repository identifiers to ensure clean, unique listings.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # How It Works & Automation
    lines.append("## 🛠️ How It Works & Automation")
    lines.append("")
    lines.append("This repository updates **automatically every day at 00:00 UTC** via GitHub Actions.")
    lines.append("")
    lines.append("1. **Deep Discovery**: Rotates queries across GitHub API topics (`mcp-server`, `ai-editor`, `cli-agent`, `coding-agent`, `agent-skills`, `browser-agent`, etc.).")
    lines.append("2. **Quality Gate & Filter**: Evaluates metadata, stars, push activity, and description quality.")
    lines.append("3. **Category Directory Generation**: Automatically updates both `tools.json` and 10 per-category directory READMEs in [`categories/`](./categories/).")
    lines.append("4. **Auto-Commit**: Changes are cleanly pushed to GitHub daily.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Support & Donate
    lines.append("## 💖 Support & Donate")
    lines.append("")
    lines.append("If this collection helps you find top-tier tools for your AI stack, please consider supporting the project:")
    lines.append("")
    lines.append(f"- ☕ **Donate / Support:** [{DONATE_URL}]({DONATE_URL})")
    lines.append(f"- 🛒 **Store & Projects:** [{STORE_URL}]({STORE_URL})")
    lines.append(f"- 👤 **Maintained by:** **{AUTHOR_NAME}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Contributing
    lines.append("## 🤝 Contributing")
    lines.append("")
    lines.append("Have you built or discovered an awesome AI Agent, MCP Server, or Tool?")
    lines.append("")
    lines.append("1. Fork this repository.")
    lines.append("2. Add your tool entry directly to `tools.json` with the proper category.")
    lines.append("3. Run `python sync.py --render-only` to regenerate all category directories and the master index.")
    lines.append("4. Submit a Pull Request!")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("⭐ **Star this repository** to stay updated with the fastest-growing tools in the Agentic AI universe!")

    content = "\n".join(lines) + "\n"
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[*] Successfully regenerated Grand Master Index at {README_FILE}.", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Sync and update the Awesome Agentic Ecosystem collection.")
    parser.add_argument("--render-only", action="store_true", help="Only render READMEs from tools.json without API queries.")
    parser.add_argument("--clean", action="store_true", help="Start discovery with an empty database from scratch.")
    parser.add_argument("--min-stars", type=int, default=DEFAULT_MIN_STARS, help="Minimum stars threshold.")
    parser.add_argument("--limit", type=int, default=10, help="Max items per query page.")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to crawl per query.")
    args = parser.parse_args()

    if args.render_only:
        tools = load_tools()
        print(f"[*] Rendering Master Index and 10 Category Folders from {len(tools)} tools...", flush=True)
        generate_master_readme(tools)
    else:
        tools = update_and_discover(
            min_stars=args.min_stars,
            limit=args.limit,
            pages=args.pages,
            clean=args.clean
        )
        generate_master_readme(tools)


if __name__ == "__main__":
    main()
