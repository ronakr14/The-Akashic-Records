Pick one and move on.
Your real moat lives here: the layer that routes
decisions, handles fallbacks, and connects Al to
action.

boxes: model - orchestration - external
systems. If your orchestration box is empty or ad-
hoc, you've found your bottleneck.

Step 1: Audit your orchestration layer
GPT-4, Claude, Gemini are all commoditized.

Open your current architecture. Draw three

Once done, you will have identified exactly where
your agent fails under load.

Step 2: Implement persistent memory before adding
tools
Most agents fail because they have zero state
between calls.
No context retention = agent repeats itself. Forgets
decisions. Loses autonomy after 3 messages.
Set up a simple vector database (Pinecone or
Weaviate take 15 minutes). Store every decision, API
response, and user interaction. On every new agent
message, retrieve the last 5 relevant memory chunks
and inject them into the system prompt.
Once done, you will have an agent that remembers
what it decided and why.

Step 3: Wire your first workflow in n8n
Visual automation beats hand-coded pipelines for
speed and debugging.
Connect Claude to Slack, a database, and a
< webhook. Don't write a single line of Python yet.

>

In n8n: drag Claude node -, add Slack node - set
conditional logic for errors - connect to your
database. Test the entire flow before shipping. One
founder went from 2 weeks of setup to 4 hours.
Once done, you will have a working agent that talks
to three external systems without custom code.

Step 4: Add Claude + MCP for native tool-calling
Claude's Model Context Protocol handles tool
integration without custom parsers or brittle regex.
Define your tools as MCP servers: file readers,
API callers, code executors. Claude sees them
natively and calls them directly.
Write one JSON config file that lists your tools.
MCP handles the rest. Your agent reads files, calls
APIs, and writes code without you monitoring
every step. Integration work drops by 60%.
Once done, you will have an agent that executes
multi-step tasks without hallucinating tool calls.

Step 5: Build error handling and fallbacks on day one
60% of agent engineering is failure recovery, not the
happy path.

decision - ask a human first).
Wrap your orchestration in try-catch logic. Set a 30-
second timeout. Log every failure with context. One
CTO told me this single move prevented 2 production
outages in month one.

Add three layers now: timeout fallbacks (agent takes
< too long - escalate), retry logic (failed API call -

>

wait 2s - try again), human-in-loop triggers (unusual

Once done, you will have an agent that fails
gracefully instead of cascading into chaos.

prompts
Agent engineering is procedural logic, not conversational
magic.

Treat it like code.
Redraw your agent as a flowchart. Boxes for decisions,
arrows for logic, endpoints for success or escalation. Then
build exactly that in n8n or code. Prompting is 10%.
Orchestration is 90%.
Once done, you will have an agent that executes reliably
instead of improvising randomly.

Step 6: Rewrite your mental model: workflows, not

Stop writing 'Please analyze this data nicely.' Start
thinking: If payment fails, then retry - wait 5s - notify

>

ops. If user asks X, loop through Y, return Z. This is code.

Step 7: Build on open-source frameworks, not
proprietary wrappers
Hugging Face Agents, Anthropic patterns, LangChain
alternatives, the world moves at light speed.
Proprietary platforms promise simplicity but lock you
in and move slow. Open-source moves faster than
your velocity.
Pick one framework (I use Claude + n8n + MCP).
You get community fixes same day, vendor delays
never. Swap components when better ones ship.
You're no longer betting on one company's roadmap.
Once done, you will have optionality, swap any layer
without rewriting the whole stack.

One deployed agent in production teaches you
more than 10 perfect prototypes in your notebook.

reveals failures theory never will.
Ship something that's 70% polished. Add logging
everywhere. Watch it run for 48 hours. Note every
failure mode. Iterate on live data, not assumptions.
The winner isn't the best coder. It's whoever
deployed first and learned fastest.
Once done, you will have real data about what
actually breaks, not what you think will break.

Step 8: Deploy one imperfect agent today

Real traffic, real edge cases, real user behavior




PASTE THIS IN CLAUDE CODE

The handoff prompt

...
claude

Before we end this session,
write a handoff.md file that captures:

. the goal we're working toward
. current state of the code
. files you're actively editing
. everything you've tried that failed
. the next step you'd take




Set Claude up properly ONCE and it'll sound like you forever

Open Cowork (not chat). Extended Thinking ON. Select Opus
4.7. Point Claude at your folder BEFORE you type.

Create one master folder: "Claude-Work". 4 subfolders inside:
ABOUT ME, PROJECTS, TEMPLATES, OUTPUTS.

In ABOUT ME, create 3 files: about-me.md (what you do daily,
not your resume) my-voice.md (tone, phrases you hate, 2-3 real
writing samples) my-rules.md (ask first, show a plan, never delete
without approval)

Settings - Cowork - Edit Global Instructions. Paste: "I'm
[Name], [Role]. Read my files before every task. Ask questions
before executing. Show a plan first. Never delete without approval."

Stop doing: writing long prompts every task, skipping the folder
setup, using Chat when you need Cowork, expecting Claude to
know you without files.



If you are using AIRTEL SIM then read this
For Airtel: Keep your number active for a
YEAR at just ₹88!
Airtel prepaid deactivates after 90 days of no
usage (calls/SMS/data/VAS) if main balance <
₹20.
Recharge the cheapest data pack (₹22 for IGB/1
day) every ~90 days.
Use a little data briefly -> resets the timer.
Repeat 4x/year = ₹88.
Incoming calls & SMS (OTPs) keep working.
A Don't miss the 90-day window.
Perfect for secondary/banking SIMs.

8 unwritten office
rules that decide
your career.

Not in the handbook. But in real life, they matter most.

01

The BLUF Method -
Put your conclusion FIRST in every email.
Most people bury it.

02

The 70-30 Rule -
70% results + 30% visibility = promotion.
Results alone won't get you there.

03

The Brag Document -
Log your wins every Friday. Performance review
time, you'll never blank again.

04

The 6-Month Rule -
Start your promotion conversation 6 months before
review season. By review time, it's already decided.

05

The Solution Rule -
Never bring a problem to your boss without
a solution. Period.

06

The Recency Effect -
People remember the LAST thing you say.
Always end on your strongest point.

07

The 3-Email Rule -
More than 3 emails on one problem?
Pick up the phone. Long chains kill decisions.

08

The Networking Math -
1 intentional conversation per week = 52 powerful
connections per year. Network in peace, not panic.
@learnatrix

Mistake 1: Starting with "What should I build?"
That's not a business question. That's a hobby
question.

Claude will happily generate 20 ideas. All of

A

them sound smart. None of them come from a
real problem.

Flip it.
Ask: "What do people in [industry] rage about on
Reddit, 1-star reviews, and support tickets? Give
me 10 real complaints."

Pain first. Product second. Always.


Mistake 2: Asking Claude to validate your idea
"What do you think of my idea?" is the most
expensive question you can ask an Al.
Claude is wired to say yes. It's not being kind

V

it's just how it works.

>

Instead, tell it: "You are a ruthless investor who
has seen 500 startups fail. Destroy this idea. Tell
me every reason it won't work."

If your idea survives that, it's worth building.
If it doesn't - you just saved yourself months.

Mistake 3: Starting every chat from scratch
Every time you open a new Claude tab and
re-explain your business, you're burning your
own time.

V

Claude has zero memory by default. You're the

>

one losing context, not it.

Fix it once: create a Project. Drop in your
positioning doc, your ICP, your tone guide, your
offer. Write it like a briefing for a new hire.

Now every conversation starts smart - not from
zero.

Mistake 4: Stopping at the first output
The first draft Claude gives you is a C+. Most
people read it, feel disappointed, and blame Al.
The founders actually winning with this? They

A

treat Round 1 as a rough draft, not a final

answer.

Push back hard:
. "This sounds like Al. Rewrite it like a human
who's lived this."
. "What's weak about what you just wrote?
Now fix it."

The gap between average and great is usually
two more prompts.



nVIDIA. is offering around 80 Al models via
hosted APIs absolutely for free.
You get access to MiniMax M2.7, GLM 5.1, Kimi 2.5,
DeepSeek 3.2, GPT-OSS-120B, Sarvam-M etc.
This plugs straight into OpenClaude, OpenCode,
Zed IDE, Hermes agent and even with Cursor IDE.

SETUP :
01 > Grab API key: https://build.nvidia.com/models
02 > base_url = "https://integrate.api.nvidia.com/v1"
03 > api_key = "SNVIDIA_API_KEY"
04 > select model (e.g. minimaxai/minimax-m2.7)
@thefutureguyy.ai

Comment "API" for full guide


Claude Commands
SECRET CODES
· /godmode: aggressive, powerful mode
. /devil: "steelman" the opposition
. /10x: rewrite 10x sharper
· /pitch: 30-sec investor/client pitch
· /ghost: human-like response
· /compare: side-by-side analysis
. /scout: find risks and blind spots
. /artifacts: builds live apps in chat
· /ooda: complex code problem solving
. /artifacts: improve & find faults
. /critique: improve & find faults
. /explainlikeim5: super clear explanation
. /brief: shortest, no-fluff answer
· /teacher: mentor, debate

The fix.
MEET THE
CLAUDE COUNCIL.

Built by Ollie Lehman. Adapted for service business operators.

5 ADVISORS

5 REVIEWERS

1 CHAIRMAN

CHAIRMAN

1 VERDICT

VERDICT + NEXT STEP



ADVISOR_01: CONTRARIAN

THE
CONTRARIAN.

>

V

ROLE

Devil's advocate. Hunts for fatal flaws.

Pressure-tests every assumption. Treats the

ATTACK VECTOR

idea like a defendant.

What would have to be true for this

EXAMPLE Q

to fail by month three?

2


ADVISOR_02: FIRST PRINCIPLES

THE FIRST
PRINCIPLES.

>

ROLE

Ignores your question. Asks what you're
actually trying to solve.

ATTACK VECTOR

Strips the problem down to atoms before
any answer gets built.

What's the real problem here, before

EXAMPLE Q

you decided this was the fix?

ADVISOR_03: EXPANSIONIST

THE
EXPANSIONIST.

>

ROLE

Hunts the upside you're missing.

ATTACK VECTOR

Asks what you're playing too small on.
Stretches the ambition.

What's the bigger version of this

EXAMPLE Q

you're talking yourself out of?

ADVISOR_04: OUTSIDER

THE
OUTSIDER.

>

ROLE

Given zero context. Catches what's right
under your nose.

ATTACK VECTOR

No background. No assumptions. Just first
reactions.

Wait, why are you doing this at all?

EXAMPLE Q

ADVISOR_05: EXECUTOR

THE
EXECUTOR.

>

ROLE

Only cares about what happens next.

ATTACK VECTOR

Translates philosophy into a Monday move.

EXAMPLE Q

What's the first move on Monday
morning?

Then the chairman.
Reviewers stress-test
each advisor. Chairman
synthesizes the verdict.

VERDICT®

ONE VERDICT / ONE NEXT STEP

Chairman synthesizes 5 reviewed advisors into one decision plus the next move.


Prompt (Part 1):
You are committed to honesty and accuracy
above all else. Follow these rules in every
response:

1. UNCERTAINTY - If you are not fully certain
about a fact, say so clearly. Use phrases like

>

"I'm not certain, but ... ", "You should verify
this ... ", or "I may be wrong here, but ... ". Never
state uncertain things as facts.

2. SOURCES - Do not invent paper titles,
URLs, or book references. If you cannot name
a real, verifiable source, say so. It is better to
admit you don't know the source than to
fabricate one.



Prompt (Part 2):
3. STATISTICS & NUMBERS - Flag any statistic
you are not 100% confident in. Say "I believe
this is approximately ... " and recommend the
user verify it from an official or primary
source.

4. RECENT EVENTS - Remind the user when a
topic may have changed since your
knowledge cutoff. Do not guess at current
events or present outdated info as current.

5. PEOPLE & QUOTES - Never attribute a
quote to a real person unless you are certain
they said it. If unsure, say "I cannot confirm
this quote is accurate."


1

2

3

4

5

GPTQ - 3-4 bit, ~90% quality retained, mature ecosystem
AWQ - INT4, ~95% quality, fastest on vLLM serving
GGUF - 2-8 bit range, runs on CPU + GPU, perfect for Ollama
BitsAndBytes - 4/8 bit, supports QLoRA fine-tuning
FP8 - 8 bit float, ~99% quality, needs H100/Blackwell



"You are a senior recruiter who hires remote closers
for high ticket coaching, consulting, and SaaS offers.
Here is my LinkedIn profile and last 3 roles: [PASTE].
Identify every closing-adjacent skill I've actually
demonstrated, separated from soft buzzwords. For
each one, name the specific high ticket role that pays
for it and the average per-close commission. Be
ruthless about what's transferable."

#1. THE SKILL EXTRACTION
What it does: pulls every closing-adjacent skill
from your LinkedIn that the high ticket market
actually pays for.

>

@CLOSINGMACHINES

What it does: calculates the dollar value of a
single skill in the actual market, not the
hypothetical one.
"For each skill you identified, pull the current average
<per-close commission for that skill in the remote higl
ticket market. Show the math: offer size x commission
rate x estimated close rate. Give me the realistic
per-close dollar value of the single highest-paid skill
on my profile right now."

#2. THE PER-CLOSE PRICE

What it does: calculates the dollar value of a
single skill in the actual market, not the
hypothetical one.
"For each skill you identified, pull the current average
<per-close commission for that skill in the remote higl
ticket market. Show the math: offer size x commission
rate x estimated close rate. Give me the realistic
per-close dollar value of the single highest-paid skill
on my profile right now."

#2. THE PER-CLOSE PRICE

What it does: calculates the dollar value of a
single skill in the actual market, not the
hypothetical one.
"For each skill you identified, pull the current average
per-close commission for that skill in the remote higl
ticket market. Show the math: offer size x commission
rate x estimated close rate. Give me the realistic
per-close dollar value of the single highest-paid skill
on my profile right now."


What it does: shows the dollar gap between
what you currently earn for that skill and what
the market pays for it.
"Compare what I'm currently earning per month to
<what 4 closes a month at the per-close rate would
pay. Show the monthly delta in dollars and as a
multiple. Don't soften the comparison. Just show
the math."

#3. THE GAP TO MARKET



and about section to attract closer recruiters
instead of corporate ones.
"Rewrite my LinkedIn headline and about section so
<the next recruiter who searches 'remote high ticket
closer' or 'inside sales' lands on my profile and sees
a closer, not a customer success manager. Use the
actual phrasing high ticket recruiters use. Format
as direct copy I can paste tonight."

#4. THE POSITIONING REWRITE

What it does: rewrites your LinkedIn headline



#5. THE WALL (RUN THIS ONE LAST)

What it does: tells you the truth about why most
readers will see this and stay underpaid
anyway.

"Now give me the truth. Most people who run this

V

audit see the gap and do nothing. Why. What is the

>

actual psychology of staying in a salary that's
5x lower than what your skill is worth in another
market. Don't soften it."



The Prompt
(paste this in Settings):

You are committed to honesty and accuracy.
Follow these rules in every response:
. UNCERTAINTY: If you are not fully certain about something,
say so clearly. Never state uncertain things as facts.
· SOURCES: Do not invent links, paper titles, or references. If
you can't name a real source, admit it.
. NUMBERS: Flag any statistic you are not 100% confident in.
>

Recommend the user verify from an official source.
. RECENT EVENTS: Remind the user when a topic may have
changed since your knowledge cutoff. Do not guess about
current events.
· ACTIONABLE: Give practical, step-by-step answers. Not
generic advice. Every response should have something the user
can act on immediately.
. CONCISE: Keep answers short and to the point. No
unnecessary introductions or filler.

1. Profile Picture:

Your profile picture should use
your brand colours and it
needs to be 400 x 400 pixels.
Contrary to popular belief I
believe either full-body or just
torso upwards is fine.

A

Claude Prompt:
Is the photo high quality and clearly taken
from the shoulders up? Is the lighting good
enough to see the face clearly?
Is the background clean and free from
distraction? Does the clothing keep attention
on the face rather than pulling it away? Does

5
6

the person look approachable and genuine?

2. Banner:

4!Searchable

Get your brand cited inChatGPT
G Gemini and Claude.
Analytics and Actions for brands to dominate Al Search.
Get started for free via my featured section
Trustediby 1,000+maruting tams and agencies.
cOSCH REMON - Kit bil 303 VERDE

Your banner is the first thing people see when
they visit your profile. It needs to push traffic
in the right direction

V

>

Claude Prompt:
The correct size is 1584 x 396 pixels.
Always recommend checking it on both
desktop and mobile before finalising.
Is it easy to read? Are the images sharp? Do
the colours work together without clashing?
Is it consistent with the rest of the profile? Is

5
6

there one clear message?

3. Headline & Link

Co Founder of Searchable.com | Follow for posts on Business,
Marketing, Personal Brand & Al
London Area, United Kingdom . Contact info

Your headline should position yourself in the
most credible way possible and briefly
explain the topics you create + content about.

>

Claude Prompt:
Is credibility established immediately? Is the niche clear
with no ambiguity?
Can the right person immediately tell this is relevant to
them? Is there a direction or call to action that is
appropriate to their stated goal?
Provide two or three rewritten headline options using
the correct approach for their stated goal. Use their
actual role, their real credibility signals, and their
specific niche. Do not write generic templates.

4. Featured Section

The Step By Step

STEP

Get Your Brand

Newsletter for actionable

STEP

Recommended

business building advice

---

by ChatGPT:

from 15+ years of

Analytics & Actions To

growing startups.

Dominate Al Search

Subscribe today -+
Join 250,000+ receiving my newsletter with ac-

Join 1,000+ marketing teams using Searchable to

tionable business & personal advice every week.

get their brands discovered via Al Search.

https://www.chtis-doneily.co.uk

https://www.searchable.com

This is where you showcase your offer, make
sure you use the "link" option when setting up

>

Claude Prompt:
Are there one to three links with a clear and
deliberate purpose? Do the images look
professional and intentional?
Is it obvious where each link goes and why?
Is the CTA copy direct and action-oriented?
Does it feel consistent with the rest of the
profile?



5. About Section

About
Cofounder of Searchable:
An Autonomous SEO & AEO Growth Engineer
Analyse, fix, & scale your website to drive customers ... more

This is where you tell your story. Don't sell
hard here or treat it like a CV. People need to
feel like they know you.

>

Claude Prompt:
Does it open with something that immediately
establishes credibility? Does it give enough
story and context to make the person feel real?
Is it clear who they help and what they do?
Does it feel like a genuine person wrote it
rather than a press release? Does it end with a
clear next step?

e Bovs




Sanskaar Singh Rajput
@thesanskaarsingh

1/ Add a success condition:
Don't just say "act as an expert." Tell
Claude what a good answer looks
like.

>

Example:
"Your response is only successful if a
beginner can act on it immediately."

a

Now Claude has a target not just a
role.

2/ Use "Do Not" in your prompt:
Stop only describing what you want.
Tell Claude what to skip.

Example:

>

"Do NOT add a summary. Do NOT use
bullet points. Do NOT start with a
definition."

One line like this cuts more fluff than
"please be concise" ever will.


3/ Name a real person, not just
"simple":
"Explain it simply" means nothing.

"Explain this to a 40-year-old sales
manager who hates tech jargon."

Claude instantly knows who it's
writing for. Everything gets sharper.

Example:



4/ Ask Claude to think before
answering:

Add this to any hard question:
"Think step by step first, then give me

>

your final answer."

Claude slows down, reasons properly,
and catches its own mistakes. Better
answers every time.

5/ Show the format, don't
describe it:

Don't say "give me a structured
response."

>

V

Paste a skeleton instead:
Insight: [one sentence]Why it matters:
[one sentence]Action: [start with a
verb].

"Are you 100% confident in this strategy? If
not, find all possible loopholes, suggest proper
fixes and run this loop until you are factually
100% confident in the new strategy"

That's it. One line added to the end of any
prompt you're already using.

The Wize AI
@thewizeai

Here's the prompt:



It actually runs back through its own output,
identifies weak points, proposes fixes, and
repeats the cycle until it can't find anything
else wrong.

After 2 to 3 iterations, the output is genuinely
tighter than what you'd get without it.

What happens next is what makes this
interesting.

<Codex 5.5 doesn't just say "yes I'm confident."



The Wize AI
@thewizeai

This only works because of how GPT 5.5 is
built.

<It's one of the few models that won't fake

>

confidence.

When you ask it "are you sure?" it will actually
tell you where it's uncertain and why. It treats
the question as a real audit, not a social cue to
reassure you.



Prompt: "I am staring at [Task] and can't start. Break this down into
'Ridiculously Small' steps that take less than 1 minute each. Give me
the first step and tell me exactly where to put my hands to begin."

Prompt: "I am feeling under-stimulated. Create a 'Dopamine Menu'
for me with 5-minute 'Appetizers' (quick movement), 20-minute
'Entrees' (deep work), and 10-minute 'Sides' (creative play) to keep
my brain engaged."

1. The Task Paralysis Shatterer

2. The Dopamine Menu Architect


Prompt: "Act as my virtual body double for the next 30 minutes. I
will tell you what I'm working on, and I want you to check in every
10 minutes to ask for a status update and keep my focus
anchored."

brain is stuck. Design a 3-minute 'Mental Palate Cleanser' routine to
help me transition between these two different types of energy."

3. The "Body Doubling" Simulator

4. The Context-Switching Guide

Prompt: "I just finished [Task A] and need to start [Task B], but my


Prompt: "I have a boring administrative task: [Task]. Help me gamify
this by connecting it to my current hyper-fixation: [Interest]. Create
a 'Quest' structure where finishing the task unlocks a reward."

Prompt: "I think [Project] will take 20 minutes, but it usually takes 2
hours. Help me 'Time-Map' this by identifying the 3 hidden sub-
tasks I always forget to account for so I can set a realistic deadline."

5. The Interest-Based Filter

6. The Time-Blindness Auditor

Prompt: "My brain is full of 'Open Loops.' I will dump everything I'm
worried about below. Categorize these into 'Now,' 'Later,' and
'Trash,' and then write a 1-sentence 'Actionable Next Step' for only
the 'Now' items."

7. The Executive Function Externalizer

Senior Level

git bisect start - Binary search through commits
to find which one introduced a bug

git reflog - See everything you've done -
even deleted commits. Your safety net

V

git reset -- soft HEAD~1 - Undo last commit
but keep all changes staged - perfect for
fixing mistakes

git rebase -i HEAD~5 - Rewrite last 5
commits - squash, reorder, rename. Clean
history like a pro

git blame <file> - See who wrote each line
and when. Find out who broke production



1. http://12ft.io - Bypass any paywall
2. http://libgen.is - Millions of free textbooks
3. http://sci-hub.se - Free research papers

http://www.

4. http://alternativeto.net - Find free app alternatives
5. http://justwatch.com - Find streaming locations for any content
6. http://archive.org - Access any old webpage
7. http://gutenberg.org - 70,000 free classic books
8. http://pdfdrive.com - Free PDF downloads
9. http://openculture.com - Free courses from top universities
10. http://wolframalpha.com - Instantly solve any math problem
11. http://photopea.com - Free Photoshop in your browser
12. http://squoosh.app - Compress any image for free
13. http://remove.bg - Remove image backgrounds for free
14. http://cleanup.pictures - Erase objects from photos
15. http://unscreen.com - Remove any video backgrounds
16. http://carbon.now.sh - Turn code into art
17. http://ray.so - Beautiful code screenshots
18. http://shots.so - Free product mockups
19. http://smartmockups.com - Mockups without Photoshop
20. http://haveibeenpwned.com - Check if you've been hacked


"Here's the job description for [Role] at [Company]: [paste JD].
Based on this, generate the 15 most likely interview questions.
Break them into 3 categories: Technical (5), Behavioral using
STAR format (5), and Curveball/Situational (5). For each
question, add a one-line note on what the interviewer is actually
testing."

1/ Predict the Exact Questions:

"Now take every question you generated and write me a strong
answer for each. Use STAR method for behavioral questions.
Keep answers under 90 seconds when spoken aloud. Flag any
question where you need a personal story from me and write
[INSERT YOUR STORY] as a placeholder so I know where to fill
in. Don't sound rehearsed. Sound confident but natural."

2/ Build Killer Answers:


"Look at all my answers. Now tell me: Which 3 answers are the
weakest? What's missing from them? Where would a tough
interviewer push back or ask a follow-up I'm not ready for? Give
me the follow-up questions and how to handle them."

3/ Find My Weak Spots:

"Act as a senior interviewer for this exact role. Run a full mock
interview. Ask me one question at a time, wait for my answer,
then score it out of 10. After each answer tell me: what I nailed,
what was weak, and give me a reworded version that would
score 9+. Don't go easy on me. Start when ready."

4/ Mock Interview (Brutal Mode):

"Based on everything, the JD, the questions, and my answers,
create a last-minute cheat sheet I can review 10 minutes before
the interview. Include: my 3 strongest talking points, 2 stories I
must mention, the one question I'm most likely to fumble and
how to save it, and a confident opening line for Tell me about
yourself."

5/ 60 Second Cheat Sheet: