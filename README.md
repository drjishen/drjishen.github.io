# drjishen.com — Personal Site & Blog

Personal website of **Jishen Pfeiffer** — MD, Digital Health Researcher, PhD Student.
Live at **[drjishen.com](https://drjishen.com)**.

Built with [Jekyll](https://jekyllrb.com/) using the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme (v7.5.0), hosted on GitHub Pages.

---

## Running Locally

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000`.

> **Note:** The local Ruby environment may have an older Chirpy gem cached. The server always uses the version pinned in `Gemfile.lock`. If you see discrepancies, run `bundle update jekyll-theme-chirpy` to sync.

---

## Project Structure

```
.
├── _config.yml                  # Site configuration (title, URL, social links, timezone)
├── _tabs/
│   └── about.md                 # About/CV page — rich HTML-in-Markdown layout
├── _posts/                      # Blog posts (YYYY-MM-DD-title.md)
├── _includes/
│   └── head.html                # Overrides Chirpy's <head> — adds custom.css link
├── assets/css/
│   └── custom.css               # Custom styles (teal palette, badges, timeline, etc.)
├── .github/
│   ├── workflows/
│   │   ├── pages-deploy.yml     # Builds & deploys site to GitHub Pages (CI/CD)
│   │   ├── monthly-prompt.yml   # Creates a monthly update issue on the 1st of each month
│   │   └── generate-from-issue.yml  # Generates blog post PR when issue is labeled ready-to-publish
│   └── ISSUE_TEMPLATE/
│       └── monthly-update.md    # Issue template for monthly updates
└── tools/
    └── generate_post.py         # Python script: parses issue body → Jekyll post draft
```

---

## Custom Styling

`assets/css/custom.css` provides the visual theme:

- **Accent colour:** deep teal `#0a7ea4`
- **Skill badges:** coloured pills grouped by category (Clinical, Digital Health, AI/ML, Tech, Security, Learning)
- **Language bars:** gradient progress bars
- **Work timeline:** vertical timeline with hover effects
- **Education cards:** bordered card layout
- **Dark mode:** all components have `[data-mode="dark"]` overrides

---

## Blog Posts

| File | Title | Date |
|---|---|---|
| `2024-05-26-hallo.md` | Welcome to my Digital Health Blog | May 2024 |
| `2024-09-01-medical-llms-intro.md` | Introduction to LLMs in Medicine | Sep 2024 |
| `2024-11-15-fhir-openehr-interoperability.md` | HL7 FHIR vs OpenEHR | Nov 2024 |
| `2025-02-01-knowledge-graphs-healthcare.md` | Knowledge Graphs in Healthcare | Feb 2025 |

---

## Monthly Update Agent

A GitHub-native workflow that automates keeping the site current.

### How it works

1. **On the 1st of every month** — `monthly-prompt.yml` creates a GitHub Issue with a structured template asking about:
   - Skills studied, courses completed, papers read
   - Projects worked on, events attended
   - Suggested blog post topic + outline
   - About page updates needed

2. **Fill in the issue** — answer the questions directly in the issue body.

3. **Label the issue `ready-to-publish`** — `generate-from-issue.yml` triggers automatically:
   - Runs `tools/generate_post.py` to parse the issue and generate a Jekyll post
   - Creates a new branch and commits the draft post
   - Opens a Pull Request for review

4. **Review and merge the PR** — edit the draft, then merge to publish.

### Manual trigger (for testing)

Go to **Actions → Monthly Update Prompt → Run workflow**.

### Required GitHub permissions

Go to **Settings → Actions → General → Workflow permissions** and set to **"Read and write permissions"**. Required for issue creation and PR opening.

---

## Deployment

Deploys automatically on push to `main` via `.github/workflows/pages-deploy.yml`.

**GitHub Pages must be set to "GitHub Actions" source:**
Settings → Pages → Build and deployment → Source → **GitHub Actions**

The workflow:
1. Builds with `bundle exec jekyll b`
2. Runs `htmlproofer` (external links disabled)
3. Uploads artifact → deploys via `actions/deploy-pages`

---

## Known Issues & Notes

### Chirpy 7.5.0 — `_includes/head.html` compatibility

The project overrides Chirpy's `head.html` (in `_includes/head.html`) to inject `custom.css`.
Chirpy 7.5.0 **removed** `mode-toggle.html` — the reference to it has been removed from our override.
If upgrading Chirpy in future, re-check `_includes/head.html` against the new theme version.

### GitHub Pages source must be "GitHub Actions"

If the source is set to "Deploy from a branch", GitHub tries to build Jekyll itself (without the Chirpy gem), fails, and serves raw `.md`/`.html` files. Always keep it on **GitHub Actions**.

### Empty commits don't trigger "Build and Deploy"

The `pages-deploy.yml` workflow only fires when actual files change. Empty commits (`git commit --allow-empty`) will not trigger a site rebuild.
