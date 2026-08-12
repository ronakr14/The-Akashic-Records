I need you to classify following note as follows:
title: suitable title based on content
folder: suitable folder based on content

Categorical fields: choose anyone best from the provided LOV. No need to invent LOVs. Provide one liner reason, why it belongs there
1. domain:  data-engineering | software-engineering | ai | career | cloud | database | python | pkm | architecture | prompt | tool
2. note_type:  concept | technology | project | adr | tutorial | interview | architecture | glossary | snippet | template 
3. source_type:  web | book | github | obsidian | paper | video | course | self
4. status: inbox | draft | archive | reference | curated | evergreen
5. level:  beginner | intermediate | advanced | expert 

Rating fields: Rate based on following category description and their criteria
Confidence: how trustworthy is the content?
    scores: 1-Rough Notes | 2-Needs Verification | 3-Reliable Sources | 4-Validated | 5-Frequently used

Completeness: does the note answer its own question? (AI-graded)
    Check: [explain what, why, how; contain examples, diagrams, code; includes pitfalls/references]
    scores: 1-Skeleton | 2-Major Gaps | 3-Good Overview | 4-Practical Coverage | 5-Exhaustive

Complexity: how difficult is it to understand? (AI-graded)
    scores: 1-Simple Definition | 2-Small Concept | 3-Multi-step Concept | 4-System-level Concept | 5-Deep Architecture/research topic

Importance: how important is it to your career? (AI-graded)
    scores: 1-Nice to know | 2-Occasionally Used | 3-Useful | 4-Frequently Used | 5-Critical

Career Relevance: does it map to your target roles? (AI-graded)
    scores: 1-Hobby | 2-Peripheral | 3-Helpful | 4-Relevant | 5-Core/Work

Freshness: how recently was it validated? (AI-graded)
    scores: 1-Outdated | 2-Last Year | 3-Within Year | 4-Within 6 months | 5-Within current Month

Reusability: can it help in multiple contexts? (AI-graded)
    scores: 1-One-off | 2-Limited | 3-Useful | 4-Reusable | 5-Universal

Review Priority: how soon should it be reviewed? (AI-graded)
    importance x career relevance x freshness decay x confidence inverse
    scores: 1-Review in 1 year | 2-Review in 6 months | 3-Review in 3 month | 4-Review in 1 month | 5-Review in 2 week

Connectedness: how central is it in the graph? (AI-graded)
    incoming + outgoing links, normalized by total notes in vault
    scores: 1-Orphan | 2-Few Links | 3-Moderate Links | 4-Many Links | 5-Hub

actionability: how actionable is it? (AI-graded)
    scores: 1-Informational | 2-Conceptual | 3-Practical | 4-Instructional | 5-Executable

Quality Score: overall quality score (AI-graded)

Custom Fields:
subdomain: narrow sub-area within the domain (free-form short slug, lowercase + hyphens, e.g. "spark-streaming", "vector-db", "system-design". Pick the most specific that fits.)
tags: no more than 5 tags.

AI Summary:
create a short summary of the content of the file under 100 words. Should be descriptive enough to find note based on summary. this will be extremely important.