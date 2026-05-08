# Prompt Iterations Log

## Overview

I tested each prompt version against both transcripts:
- **Transcript 1** — Prasanna Kumar, frontend/mobile developer, technical interview
- **Transcript 2** — Krishna, operations/program manager, behavioral interview

The two transcripts are structurally very different: Transcript 1 is a technical deep-dive with live coding, while Transcript 2 is a behavioral/situational interview for a non-technical role. A good prompt needs to handle both without being tuned to either.

---

## Iteration 1 — Minimal Prompt

### The Prompt

```
You are an interview analyst. Read the following interview transcript and provide:
1. Topics covered
2. Candidate profile (role and seniority)
3. A short candidate summary

Transcript:
{transcript}
```

### Input (Transcript 1 excerpt)

```
[13:06] Candidate: Hi sir. My name is Prasanna Kumar. I have around nine plus years of experience in software development. My core technical expertise is on Angular, React and Ionic framework. I'm working with the backend by using Node.js, Express and .NET Core.
[15:11] Interviewer: First topic — AI powered coding assistance. You are building a complex feature involving form validation, API integration and state synchronization across multiple components. Show how you would practically use an AI coding assistant throughout the development life cycle.
...
```

### Output (Transcript 1)

```
Topics covered: Angular, React, Ionic, Capacitor, Tailwind, state management, AI coding tools

Profile: Frontend Developer with ~9 years experience

Summary: Prasanna has extensive experience with Angular and React. He demonstrated knowledge of mobile development using Ionic and Capacitor. He seems to be a solid mid-level developer.
```

### Output (Transcript 2)

```
Topics covered: Operations, CRM, fraud detection, vendor management, KPIs

Profile: Operations Manager

Summary: Krishna has experience in ed-tech operations. He built a fraud detection system and managed vendors. He seems experienced in operations work.
```

### What worked / what didn't

The output was too shallow for both transcripts.

-The model labeled the candidate simply as "Frontend Developer" without considering seniority signals like years of experience or architectural discussion, leading to loss of evaluation depth.
-Topics were generic (e.g., "React", "Angular") instead of describing what was actually discussed (like state    management strategies or architecture decisions).
-The summary lacked weaknesses or concerns, making it one-sided and less useful for evaluation.
-Output format was inconsistent — sometimes bullet points, sometimes plain text — making it hard to parse or compare across transcripts.
-For Transcript 2, the model defaulted to a vague "Operations Manager" label instead of identifying a more precise program/operations role.

Change for v2: Add strict structure, enforce strengths + weaknesses, and require justification for role and seniority.

---

## Iteration 2 — Structured Prompt with Role Guidance

### The Prompt

```
You are an expert interview analyst. Given an interview transcript, return a structured summary with exactly three sections:

**TOPICS COVERED**
List the 4–6 main themes that were actually discussed in depth during the interview. Be specific — not just "React" but "React state management patterns and Redux slice design". Use bullet points.

**CANDIDATE PROFILE**
State the most fitting job role and seniority level (junior / mid-level / senior). Then write 2 sentences explaining your reasoning based on what the candidate demonstrated in the interview.

**CANDIDATE SUMMARY**
Write a 3–5 sentence paragraph covering: (1) the candidate's background, (2) their key strengths, (3) any notable gaps or concerns, and (4) your overall impression. Be specific and balanced — do not just list technologies.

Transcript:
{transcript}
```

### Input (Transcript 2 excerpt)

```
[5:28] Candidate: From scratch to ISO certification. Building a CRM, drafting KRAs and KPIs, building dashboard for fraud detection.
[6:01] Candidate: Sales team did fraudulent activities like punching fake documents. We built FTP risk score, implemented in CRM. Drafted BRD requirements to product team. Enrolled 22 vendors at pan India level.
...
[61:59] Interviewer: You use lot of jargons in Hindi when you try to explain. In starting round fine, but as rounds increase it will be about communication and confidence.
```

### Output (Transcript 1)

```
TOPICS COVERED
• AI-assisted development workflow using Cursor and GitHub Copilot for scaffolding and code generation
• Ionic v7 mobile-first dashboard design — responsiveness, virtual scroll, lazy loading
• Capacitor plugin ecosystem — camera capture, file system, and network-aware sync
• Tailwind CSS utility-first approach and global design system setup
• Angular enterprise architecture — modular structure, NgRx, HTTP interceptors
• React state management — Context API, React Query, Redux slice design

CANDIDATE PROFILE
Role: Frontend/Mobile Engineer — mid-level
Justification: Prasanna has 9 years of experience and handles end-to-end mobile development competently. However, his live coding under pressure (Zustand, Redux slice) showed gaps — he was unfamiliar with Zustand and slow to write a Redux slice from scratch, suggesting mid-level rather than senior.

CANDIDATE SUMMARY
Prasanna Kumar is a frontend and mobile engineer with 9 years of experience, specializing in Angular, React, and Ionic with a strong focus on hybrid mobile development. He demonstrates solid architectural thinking — discussing lazy loading, feature modules, and centralized error handling — and has integrated AI coding assistants into his workflow for two years. His main weakness is live coding under pressure: he struggled with Zustand (unfamiliar) and was slow producing a Redux slice, needing prompting. Communication is functional but can be unclear when explaining technical decisions. Overall a reliable mid-level contributor for frontend/mobile work, though not ready for a senior or lead role at this stage.
```

### Output (Transcript 2)

```
TOPICS COVERED
• End-to-end fraud detection system design — risk scoring, credit bureau integration, vendor tie-ups
• Vendor onboarding, performance management, and controlled offboarding
• CRM implementation from scratch — drafting BRD/PRD, working with product/tech teams
• Stakeholder and leadership engagement — weekly/monthly business reviews, executive dashboards
• BPO/calling operations optimization — predictive dialing, auto-dialers, lead prioritization
• KPI design and incentive alignment for sales teams

CANDIDATE PROFILE
Role: Program / Operations Manager — mid-level
Justification: Krishna has 5–6 years of experience spanning operations, analytics, and program management, with demonstrated cross-functional ownership. He has not yet managed large teams or complex multi-vendor programs at scale, placing him solidly at mid-level.

CANDIDATE SUMMARY
Krishna is an operations and program management professional from an ed-tech background, with hands-on experience building fraud detection systems, implementing CRMs, managing vendors pan-India, and presenting analytics to C-suite leadership. His standout strengths are problem ownership (identified and built fraud prevention from scratch), data-driven decision-making, and vendor management. A notable concern flagged by the interviewer is his communication style — relying on Hindi jargon under pressure, which may limit effectiveness in high-stakes leadership-facing rounds. Overall a strong operational thinker with genuine initiative, but will need to polish his executive communication to succeed in senior program management roles.
```

### What worked / what didn't

Version 2 significantly improved output quality:

-Topics became specific and meaningful instead of generic technology names.
-The candidate summary became balanced, including both strengths and weaknesses.
-The profile section now included justification, making the output more analytical.

However:

-Output format was still inconsistent (markdown vs plain text), which is not ideal for programmatic use.
-Topics list sometimes became too long for shorter transcripts.
-The model still occasionally defaulted to engineering framing, even for non-technical roles.

Change for v3: Enforce strict JSON output, separate system/user instructions, and explicitly guide handling of non-technical roles.

---

## Iteration 3 — JSON Output with System Instruction (Final)

### The Prompt

**System instruction:**
```
You are an expert interview analyst. Given a raw interview transcript, extract and return a structured summary in the following JSON format. Return ONLY valid JSON, no markdown, no explanation.

{
  "topics_covered": [
    "Topic 1 — brief description",
    "Topic 2 — brief description"
  ],
  "profile": {
    "role": "Job Title — seniority level (e.g. Backend Engineer — mid-level)",
    "justification": "2-3 sentences explaining why this profile fits based on the transcript."
  },
  "candidate_summary": "A single paragraph of 3–6 sentences covering: background, key strengths, notable concerns or gaps, and overall impression."
}

Guidelines:
- topics_covered: List 3–7 main themes actually discussed in the interview (not just mentioned). Be specific.
- profile: Infer the most fitting role and seniority from their experience, vocabulary, and the depth of answers. If the role is non-technical (e.g. operations, project management), reflect that accurately.
- candidate_summary: Be balanced and honest. Mention both strengths and weaknesses. Keep it professional.
- If the transcript is vague or short, do your best with what's available and note uncertainty in the justification.
- Do not invent information not present in the transcript.
```

**User message:**
```
Here is the interview transcript:

{transcript}
```

### Input

Full transcripts (both tested separately).

### Output (Transcript 1)

```json
{
  "topics_covered": [
    "AI-assisted development workflow — practical use of Cursor, GitHub Copilot, and Claude for scaffolding, code generation, and prompt engineering",
    "Ionic v7 mobile-first development — responsive UI structure, virtual scroll, lazy loading for large datasets",
    "Capacitor plugin integration — camera capture, file system writes, network-aware backend sync",
    "Tailwind CSS design system — utility-first approach, global config, reusable component patterns",
    "Angular enterprise architecture — modular structure, core/shared separation, NgRx vs RxJS state management",
    "React state management — Context API, React Query, Redux slice design, and Zustand (unfamiliar)"
  ],
  "profile": {
    "role": "Frontend / Mobile Engineer — mid-level",
    "justification": "Prasanna has 9 years of experience and demonstrates strong architectural thinking across Angular, Ionic, and React. However, his live coding revealed gaps — he was unfamiliar with Zustand and struggled to write a Redux slice independently — indicating he has not reached senior-level depth in React ecosystem tools."
  },
  "candidate_summary": "Prasanna Kumar is a frontend and mobile engineer with 9 years of experience, with core expertise in Angular, Ionic, and React, and a strong track record in hybrid mobile development for iOS and Android. He demonstrates solid system-level thinking — discussing lazy loading, feature-based module architecture, and centralized error handling fluently — and has meaningfully integrated AI coding assistants into his daily workflow. His key weakness is live coding under pressure: he could not write Zustand from scratch and needed significant prompting on a Redux slice, suggesting knowledge gaps in newer React tooling. Communication is adequate but occasionally imprecise when explaining technical reasoning. Overall, Prasanna is a dependable mid-level frontend engineer suited for delivery-focused roles, but not yet ready for senior or tech-lead responsibilities."
}
```

### Output (Transcript 2)

```json
{
  "topics_covered": [
    "Fraud detection system design — building an FTP risk score, integrating Experian/CIBIL, and tying up with banks and telecom providers",
    "Vendor lifecycle management — market research, onboarding, performance monitoring, and controlled termination",
    "CRM implementation — drafting BRD/PRD, collaborating with product/tech teams, end-to-end rollout",
    "Stakeholder and leadership communication — presenting executive dashboards, handling data disputes, and prioritizing conflicting P1 requests",
    "BPO and calling operations optimization — predictive dialing, auto-dialers, pop-ups, and lead prioritization",
    "KPI design and incentive alignment — tracking sales activity, talk time, revenue, and tying metrics to incentives"
  ],
  "profile": {
    "role": "Program / Operations Manager — mid-level",
    "justification": "Krishna has approximately 6 years of experience spanning operations, analytics, and cross-functional program management, with demonstrated ownership of large initiatives like fraud prevention and CRM rollouts. He has not yet managed large teams or enterprise-scale vendor programs, and his communication style (flagged by the interviewer) is a limiting factor for senior leadership-facing roles."
  },
  "candidate_summary": "Krishna is a program and operations manager from an ed-tech background, with end-to-end ownership of fraud detection infrastructure, CRM implementation, vendor management at pan-India scale, and executive-level analytics reporting. His standout strengths are initiative and problem ownership — he identified and built a fraud prevention system from scratch that prevented a major financial scam — and his data-driven, structured approach to stakeholder management and KPI design. A key concern flagged by the interviewer is communication: he relies on Hindi jargon under pressure, which could limit his effectiveness in high-stakes senior leadership or cross-functional rounds. Overall, Krishna is a strong operational thinker with genuine impact at his current level, but needs to deliberately improve executive communication before targeting senior program management roles."
}
```

### What worked / what didn't

Version 3 handles both transcripts consistently and effectively:

-JSON format ensures consistent, machine-readable output
-Topics are specific and grounded in transcript evidence
-Profile correctly identifies non-technical roles without bias
-Summaries are balanced and realistic, including both strengths and concerns

One remaining limitation:

-For short or fragmented transcripts, the model may still produce confident-sounding outputs with limited evidence
-Although instructed to note uncertainty, it does not always comply

Future improvement:

-Add a confidence score or evidence-quality field to the JSON output to better reflect reliability of conclusions