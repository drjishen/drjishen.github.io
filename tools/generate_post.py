#!/usr/bin/env python3
"""
generate_post.py
----------------
Parses a monthly-update GitHub issue body and generates a Jekyll blog post draft.

Usage:
    python tools/generate_post.py \
        --issue-body /tmp/issue_body.txt \
        --issue-title /tmp/issue_title.txt \
        --issue-number /tmp/issue_number.txt \
        --output-dir _posts
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path


# ── Section headings as they appear in the issue template ──────────────────
SECTIONS = {
    "skills":       r"###\s+1\.\s+Skills.*?This Month",
    "resources":    r"###\s+2\.\s+Courses.*?Resources",
    "research":     r"###\s+3\.\s+Research.*?Papers",
    "projects":     r"###\s+4\.\s+Projects.*?On",
    "events":       r"###\s+5\.\s+Events.*?Conferences",
    "topic_title":  r"###\s+6\.\s+Blog.*?Suggestion",
    "about":        r"###\s+7\.\s+About.*?Updates",
}


def extract_section(body: str, heading_pattern: str) -> str:
    """Return the text between the matched heading and the next --- or ### or EOF."""
    # Build a pattern that captures everything after the heading until the next section
    pattern = heading_pattern + r".*?\n(.*?)(?=\n---|\n###|\Z)"
    match = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
    if not match:
        return ""
    raw = match.group(1)
    # Strip HTML comments (the template placeholders)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
    return raw.strip()


def extract_blog_topic(body: str) -> tuple[str, str]:
    """Return (suggested_title, outline) from section 6."""
    section = extract_section(body, SECTIONS["topic_title"])
    title = ""
    outline = ""

    title_match = re.search(r"\*\*Suggested Title:\*\*\s*\n(.+)", section)
    if title_match:
        title = title_match.group(1).strip()

    outline_match = re.search(r"\*\*Outline:\*\*\s*\n(.*)", section, re.DOTALL)
    if outline_match:
        outline = outline_match.group(1).strip()

    return title, outline


def slugify(text: str) -> str:
    """Convert a title to a URL-safe slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def build_tags(skills_text: str) -> list[str]:
    """Heuristically extract short tags from the skills section."""
    # Take first few meaningful words as tags
    words = re.findall(r"\b[A-Za-z][A-Za-z0-9+#-]{2,}\b", skills_text)
    tags = list(dict.fromkeys(w.lower() for w in words[:8]))  # deduplicated, max 8
    return tags or ["monthly-update"]


def render_post(
    issue_number: int,
    suggested_title: str,
    outline: str,
    skills: str,
    resources: str,
    research: str,
    projects: str,
    events: str,
    about_updates: str,
    post_date: str,
    tags: list[str],
) -> str:
    """Render the Jekyll front matter + post body."""

    title = suggested_title if suggested_title else f"Monthly Update — {post_date}"

    def section_block(heading: str, content: str) -> str:
        if not content:
            return ""
        return f"\n## {heading}\n\n{content}\n"

    body_parts = []

    if outline:
        body_parts.append(
            f"## Overview\n\n*This post covers my learning and research highlights for the month.*\n\n"
            f"**Post outline:**\n\n{outline}\n\n"
            f"> ✏️ *Expand each section below — this draft was auto-generated from the monthly update issue.*"
        )

    body_parts.append(section_block("What I Studied This Month", skills))
    body_parts.append(section_block("Courses & Resources", resources))
    body_parts.append(section_block("Research Highlights", research))
    body_parts.append(section_block("Projects", projects))
    body_parts.append(section_block("Events & Conferences", events))

    if about_updates:
        body_parts.append(
            f"\n---\n\n## Site Updates\n\n{about_updates}\n\n"
            f"*(About page has been updated accordingly.)*"
        )

    body_parts.append(
        f"\n---\n\n*Auto-generated from [monthly update issue #{issue_number}]"
        f"(https://github.com/drjishen/drjishen.github.io/issues/{issue_number}). "
        f"Edited and published by Jishen Pfeiffer.*"
    )

    body = "\n".join(b for b in body_parts if b)

    return f"""---
title: "{title}"
date: {post_date}
categories: [Monthly Update]
tags: [{", ".join(tags)}]
---

{body}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Jekyll post from GitHub issue")
    parser.add_argument("--issue-body", required=True)
    parser.add_argument("--issue-title", required=True)
    parser.add_argument("--issue-number", required=True)
    parser.add_argument("--output-dir", default="_posts")
    args = parser.parse_args()

    body = Path(args.issue_body).read_text(encoding="utf-8")
    issue_number = int(Path(args.issue_number).read_text(encoding="utf-8").strip())

    skills    = extract_section(body, SECTIONS["skills"])
    resources = extract_section(body, SECTIONS["resources"])
    research  = extract_section(body, SECTIONS["research"])
    projects  = extract_section(body, SECTIONS["projects"])
    events    = extract_section(body, SECTIONS["events"])
    about     = extract_section(body, SECTIONS["about"])

    suggested_title, outline = extract_blog_topic(body)

    today = date.today().isoformat()
    tags = build_tags(skills)

    post_slug = slugify(suggested_title) if suggested_title else "monthly-update"
    filename = f"{today}-{post_slug}.md"

    output_path = Path(args.output_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = render_post(
        issue_number=issue_number,
        suggested_title=suggested_title,
        outline=outline,
        skills=skills,
        resources=resources,
        research=research,
        projects=projects,
        events=events,
        about_updates=about,
        post_date=today,
        tags=tags,
    )

    output_path.write_text(content, encoding="utf-8")
    print(f"Generated: {output_path}")

    # Write filename for the workflow step to pick up
    Path("/tmp/generated_filename.txt").write_text(filename, encoding="utf-8")


if __name__ == "__main__":
    main()
