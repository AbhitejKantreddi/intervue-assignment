import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    print("Error: GROQ_API_KEY not set. Add GROQ_API_KEY=your_key to your .env file")
    sys.exit(1)

MODEL = "llama-3.1-8b-instant"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are an expert interview analyst. Given a raw interview transcript, extract and return a structured summary in the following JSON format. Return ONLY valid JSON, no markdown, no explanation.

{
  "topics_covered": [
    "Topic 1 -- brief description",
    "Topic 2 -- brief description"
  ],
  "profile": {
    "role": "Job Title -- seniority level (e.g. Backend Engineer -- mid-level)",
    "justification": "2-3 sentences explaining why this profile fits based on the transcript."
  },
  "candidate_summary": "A single paragraph of 3-6 sentences covering: background, key strengths, notable concerns or gaps, and overall impression."
}

Guidelines:
- topics_covered: List 3-7 main themes actually discussed in the interview (not just mentioned). Be specific.
- profile: Infer the most fitting role and seniority from their experience, vocabulary, and the depth of answers. If the role is non-technical (e.g. operations, project management), reflect that accurately.
- candidate_summary: Be balanced and honest. Mention both strengths and weaknesses. Keep it professional.
- If the transcript is vague or short, do your best with what is available and note uncertainty in the justification.
- Do not invent information not present in the transcript."""


def summarize_transcript(transcript_text):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Here is the interview transcript:\n\n{transcript_text}"}
        ],
        "temperature": 0.3,
        "max_tokens": 1024
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()
    raw_text = result["choices"][0]["message"]["content"].strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.split("\n", 1)[1]
        if raw_text.endswith("```"):
            raw_text = raw_text.rsplit("```", 1)[0].strip()

    return json.loads(raw_text)


def format_output(summary):
    lines = []
    lines.append("=" * 60)
    lines.append("INTERVIEW SUMMARY")
    lines.append("=" * 60)

    lines.append("\nTOPICS COVERED")
    lines.append("-" * 40)
    for topic in summary.get("topics_covered", []):
        lines.append(f"  * {topic}")

    lines.append("\nCANDIDATE PROFILE")
    lines.append("-" * 40)
    profile = summary.get("profile", {})
    lines.append(f"  Role:          {profile.get('role', 'N/A')}")
    lines.append(f"  Justification: {profile.get('justification', 'N/A')}")

    lines.append("\nCANDIDATE SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  {summary.get('candidate_summary', 'N/A')}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python summarizer.py <transcript_file.txt>")
        print("       python summarizer.py <transcript_file.txt> --json")
        sys.exit(1)

    transcript_path = sys.argv[1]
    output_json = "--json" in sys.argv

    if not os.path.exists(transcript_path):
        print(f"Error: File '{transcript_path}' not found.")
        sys.exit(1)

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_text = f.read().strip()

    if not transcript_text:
        print("Error: Transcript file is empty.")
        sys.exit(1)

    print(f"Summarizing '{transcript_path}'...\n")

    try:
        summary = summarize_transcript(transcript_text)
    except json.JSONDecodeError as e:
        print(f"Error: Model returned invalid JSON. Details: {e}")
        sys.exit(1)
    except requests.HTTPError as e:
        print(f"API Error: {e.response.status_code} -- {e.response.text}")
        sys.exit(1)

    if output_json:
        print(json.dumps(summary, indent=2))
    else:
        print(format_output(summary))


if __name__ == "__main__":
    main()