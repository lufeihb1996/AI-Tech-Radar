# 📡 AI Tech Radar — English Manual

**[🇨🇳 返回中文主页 (Chinese README)](./README.md)**

**AI Tech Radar** is a local-first AI intelligence radar that discovers playable new AI models, open-source repositories, ComfyUI/diffusion workflows, low-VRAM GPU hacks, and wild weekend builds across 5 developer platforms—without guessing keywords.

---

## 1. Architecture & 4-Stage Funnel

1. **Stage 1 — 5-Source Zero-Keyword Ingestion**
   - **X (Twitter)**: Pulls your personal `HomeTimeline` (For You), `HomeLatestTimeline` (Following), plus reverse X searches seeded dynamically by today's HuggingFace & GitHub trending names.
   - **HuggingFace Trending**: Top rising Models, Spaces, and Datasets.
   - **GitHub Surging Repos**: Newly created repositories (last 12 days) surging in stars.
   - **Reddit AI Communities**: Combined daily top feed from `r/LocalLLaMA`, `r/StableDiffusion`, and `r/comfyui`.
   - **Hacker News (`Show HN`)**: Builder-submitted AI tools and demos.

2. **Stage 2 — Signal Ranking, Cross-Source Deduplication & 1st-Reply Link Rescue**
   - Ranks X posts by **Bookmark-to-Like Ratio (`bookmarks / likes`)** rather than raw likes or follower count.
   - Merges duplicate discoveries pointing to the same GitHub/HuggingFace URL (`canonical_key`), combining source badges and boosting multi-platform items.
   - Automatically penetrates `TweetDetail` for fresh linkless X posts to rescue hidden GitHub/HF URLs placed in the author's first reply.

3. **Stage 3 — Official TypeSafe Jev System-1 Judge (New-First Priority)**
   - Scores items on 4 structured questions: `category`, `playability` (`READY_NOW` / `DEMO_PAPER` / `WAITLIST_HYPE`), `utility_score` (0–99), and `is_hype_bait`.
   - **New-First Queue**: Newly inserted items from the current scan always receive Jev evaluation slots first; leftover slots evaluate older backlog items. Evaluated items (`jev_evaluated = 1`) are never re-billed.

4. **Stage 4 — Bilingual UI, Streaming Media Proxy & On-Demand Digest**
   - Switch the entire UI between **中文** and **EN** at the top right.
   - Filter by **Last 24h / Last 3 Days / Last 7 Days / All Time** so all-time high scores never freeze your front page.
   - Built-in `/api/media` streaming proxy handles HTTP `Range` (`206 Partial Content`) video playback and anti-hotlink headers via your system proxy.
   - Manual per-card (`🌐 ZH`) and current-page (`🌐 Translate Page`) distillation powered by `deepseek/deepseek-v4-flash` via OpenRouter.

---

## 2. Installation & Setup

```bash
git clone https://github.com/lufeihb1996/AI-Tech-Radar.git
cd AI-Tech-Radar

# Windows (1-click auto-setup & launch):
start-ai-radar.bat

# macOS / Linux:
chmod +x start-ai-radar.sh
./start-ai-radar.sh
```

Then open **http://127.0.0.1:8096** and click **`⚙️ Keys & Cookies`** in the top-right corner to configure:
- **`TYPESAFE_API_KEY`**: Official TypeSafe Jev API key from `https://console.typesafe.ai`.
- **`TWITTER_AUTH_TOKEN` & `TWITTER_CT0`**: Copy from `https://x.com` browser DevTools (`F12 -> Application -> Cookies`).
- **`OPENROUTER_API_KEY`**: OpenRouter key from `https://openrouter.ai/keys` (used only when manually clicking Translate).

---

## 3. REST API Overview

| Method & Path | Description |
| :--- | :--- |
| `GET /api/status` | Returns credential status flags and per-source item counts. |
| `GET /api/items` | Paginated query (`source`, `category`, `playability`, `has_video`, `starred`, `hours`, `sort`, `q`, `page`, `page_size`). |
| `POST /api/scan` | Runs concurrent multi-source fetch, 1st-reply link rescue, deduplicated upsert, and new-first Jev scoring. |
| `POST /api/translate` | Manually distills specified item IDs (`ids`) into Chinese via `deepseek/deepseek-v4-flash`. |
| `POST /api/star` | Toggles bookmark/star state (`id`) in local SQLite. |
| `GET /api/media?url=...` | Allowlisted streaming media proxy supporting `Range` requests for X/Reddit/HF/GitHub assets. |
| `POST /api/settings` | Updates `.env` keys from the Web UI without overwriting blank fields. |
