# Interview Transcript Summarizer

A command-line script that takes an interview transcript as input and produces a structured summary: topics covered, candidate profile, and a balanced candidate summary.

---

## How to Run

### 1. Clone / download this repo

```bash
git clone <https://github.com/AbhitejKantreddi/intervue-assignment.git>
cd <repo-folder>
```

### 2. Install dependencies

```bash
pip install requests python-dotenv
```

### 3. Set up your API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_api_key_here
```

Get a free key at **https://console.groq.com** → API Keys → Create API Key (no credit card required).

> ⚠️ Never commit this file. It's already in `.gitignore`.

### Note on Rate Limits

The Groq API may return a `429` rate limit error due to token-per-minute limits. If this happens, wait a few seconds and retry — it resolves automatically.

### 4. Run the script

```bash
# Pretty-printed output (default)
python summarizer.py sample_transcript_assignment_1.txt

# Raw JSON output
python summarizer.py sample_transcript_assignment_2.txt --json
```

---

## LLM Provider and Model

- **Provider:** Groq
- **Model:** `llama-3.1-8b-instant`

Groq was chosen for its fast inference and generous free tier (14,400 requests/day, 500,000 tokens/day for this model) — more than sufficient for full-length interview transcripts in a single API call. The model is accessed via Groq's OpenAI-compatible chat completions endpoint.

---

## Reflection

### What surprised me

The biggest surprise was how much the *structure* of the output format mattered compared to the content of the instructions. My first two prompt iterations had good analytical instructions but produced inconsistent formatting across the two transcripts — markdown headers in one run, plain text in another. Switching to a strict JSON schema with a system instruction almost entirely eliminated that inconsistency. The model followed the schema reliably once it was given a concrete template to fill rather than a description of what to write.

The second surprise was how differently the model handled the two transcripts without explicit guidance. Transcript 1 is a technical interview; Transcript 2 is behavioral for an operations/PM role. My early prompts defaulted to "engineer" framing even for Transcript 2. Adding a single line — *"If the role is non-technical, reflect that accurately"* — was enough to fix this.

### What I'd improve with another day

1. **Confidence / evidence quality field** — Add a field to the JSON output indicating how much evidence supports the profile assessment (e.g., "high / medium / low" based on transcript length and specificity). The current prompt tells the model to "note uncertainty" but it doesn't always do so.

2. **Multi-turn follow-up** — A second API call that asks the model to critique its own first output ("What did you infer that isn't directly supported by the transcript?") could catch overconfident claims.

3. **Structured section detection** — For long transcripts, pre-processing to extract only candidate turns (filtering out interviewer lines) before sending to the model could reduce token usage and sharpen the summary.

4. **Output to file option** — Add a `--output results.json` flag to write structured results to disk, useful for batch processing multiple transcripts.

### Limitations of the final prompt

- **Fragmented speech:** Both sample transcripts contain incomplete sentences and filler words. The model handles this well in context, but very short or heavily fragmented transcripts may produce shallow summaries.
- **Hallucination risk:** The model occasionally infers seniority or role fit with more confidence than the transcript warrants. The instruction "do not invent information" reduces this but does not eliminate it.
- **Single-language assumption:** The prompt assumes the transcript is in English. Code-switched transcripts (e.g., Hindi-English mix) may produce lower quality output.
- **No ground truth:** There's no automated way to verify the summary quality — evaluation is subjective and manual.