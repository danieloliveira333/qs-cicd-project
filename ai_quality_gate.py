"""
AI Quality Gate - Uses Google Gemini to analyze Pull Request code
and decide if it should be approved or rejected.

Project #5: AI-Enabled Quality Gates in CI/CD
Qualidade de Software 2025/26 - Universidade da Beira Interior
"""

import os
import sys
import json
import urllib.request
import urllib.error


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY
)


def get_changed_files():
    """Read changed files from environment (set by the workflow)."""
    diff = os.environ.get("PR_DIFF", "")
    if not diff:
        print("WARNING: No diff found. Using placeholder.")
        diff = "No diff available."
    return diff


def analyze_with_gemini(diff: str) -> dict:
    """Send the diff to Gemini and get a quality analysis."""

    prompt = f"""
You are a strict but fair software quality gate for a Python project.
Analyze the following code diff from a Pull Request and return ONLY a JSON object.

Code diff:
{diff}

Return ONLY this JSON (no markdown, no explanation):
{{
  "decision": "APPROVED" or "REJECTED",
  "score": <integer 0-100>,
  "summary": "<one sentence overall assessment>",
  "issues": ["<issue 1>", "<issue 2>"],
  "positives": ["<positive 1>", "<positive 2>"],
  "recommendation": "<one sentence recommendation>"
}}

Rules for decision:
- APPROVED if score >= 70 and no critical bugs or security issues
- REJECTED if score < 70 or critical bugs/security issues found

Evaluate based on:
- Correctness (does the code work as intended?)
- Test coverage (are new functions tested?)
- Code quality (readable, no duplication, good naming)
- Security (no obvious vulnerabilities)
- Edge cases (are error cases handled?)
"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1024}
    }).encode("utf-8")

    req = urllib.request.Request(
        GEMINI_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            # Clean up in case Gemini adds markdown fences
            raw_text = raw_text.strip().strip("```json").strip("```").strip()
            return json.loads(raw_text)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        sys.exit(1)


def format_comment(analysis: dict) -> str:
    """Format the analysis as a GitHub PR comment in Markdown."""

    decision = analysis.get("decision", "UNKNOWN")
    score = analysis.get("score", 0)
    summary = analysis.get("summary", "")
    issues = analysis.get("issues", [])
    positives = analysis.get("positives", [])
    recommendation = analysis.get("recommendation", "")

    if decision == "APPROVED":
        badge = "## ✅ AI Quality Gate: APPROVED"
    else:
        badge = "## ❌ AI Quality Gate: REJECTED"

    issues_text = "\n".join(f"- ⚠️ {i}" for i in issues) if issues else "- None found"
    positives_text = "\n".join(f"- ✅ {p}" for p in positives) if positives else "- None noted"

    comment = f"""
{badge}

**Score:** {score}/100
**Summary:** {summary}

### 🔍 Issues Found
{issues_text}

### 👍 Positives
{positives_text}

### 💡 Recommendation
{recommendation}

---
*This review was generated automatically by the AI Quality Gate using Google Gemini.*
*For the QS 2025/26 project — Universidade da Beira Interior*
"""
    return comment.strip()


def main():
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    print("🤖 AI Quality Gate starting...")

    # Get the diff
    diff = get_changed_files()
    print(f"📄 Diff size: {len(diff)} characters")

    # Analyze with Gemini
    print("🔍 Sending to Gemini for analysis...")
    analysis = analyze_with_gemini(diff)
    print(f"📊 Analysis received: {json.dumps(analysis, indent=2)}")

    # Format comment
    comment = format_comment(analysis)

    # Save comment to file (workflow will post it to GitHub)
    with open("ai_gate_comment.md", "w") as f:
        f.write(comment)
    print("💬 Comment saved to ai_gate_comment.md")

    # Save decision for workflow
    decision = analysis.get("decision", "REJECTED")
    with open("ai_gate_decision.txt", "w") as f:
        f.write(decision)
    print(f"✅ Decision: {decision}")

    # Exit with error code if rejected (this will fail the pipeline)
    if decision == "REJECTED":
        print("❌ Quality gate REJECTED the PR.")
        sys.exit(1)
    else:
        print("✅ Quality gate APPROVED the PR.")
        sys.exit(0)


if __name__ == "__main__":
    main()
