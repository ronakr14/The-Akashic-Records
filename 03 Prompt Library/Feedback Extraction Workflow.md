---
domain: pkm
subdomain: feedback
note_type: template
source_type: self
status: evergreen
level: beginner
tags:
  - prompt
---
# AI Summary
Reusable prompt template for extracting lessons from an AI conversation. Instructs the AI to review the entire conversation, identify user corrections, stated preferences, recurring feedback, and improvements for future sessions, then generate a structured feedback.md file for reuse in later conversations. Also references complementary workflows for end-of- session handoffs and daily note updates.

---
> "Read our whole conversation, extract every correction I made, every preference I stated, anything you'd do differently next time and format it to a feedback file you'll reload in future sessions."

Paste that output into a `feedback.md` file and load it into your Claude project.

---

Related: [[End of Session Handoff]] — for full session handoff. [[Daily Note — Update]] — for the lightweight daily-note route.