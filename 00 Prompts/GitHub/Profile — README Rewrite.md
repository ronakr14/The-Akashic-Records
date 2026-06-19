---
description: Three-step Claude workflow to audit, rewrite, and visually upgrade a GitHub profile README.
use_when: When refreshing your GitHub profile bio + README from scratch.
inputs: [current bio, current README URL, role, target audience]
outputs: critique, rewritten bio, rewritten README, visual upgrade list with copy-paste code
related: [[Repo — Deep Analysis]]
tags: [prompt, github, branding, profile]
---
```table-of-contents
```

## 1. Audit your current profile

> Here is my GitHub profile bio and README. Be brutally honest with me.
> https://github.com/ronakr14
>
> Tell me exactly what is wrong with it. What would a recruiter or hiring manager think when they land on this page? What is missing, what is unclear, and what is making me look less credible than I actually am? Don't sugarcoat it.

## 2. Rewrite the bio and README

> Now rewrite my GitHub profile based on everything you just told me.
> I am a [your role] with experience in [your skills]. I want to attract [remote jobs / freelance clients]. Write me a sharp, professional bio under 150 characters.
> Then write a README that actually sells who I am — my skills, my best projects, what I am currently working on, and how to contact me. Make it human, not corporate.

## 3. Make it stand out visually

> I want my GitHub README to look impressive, not just read well.
> Suggest everything I can add to make it visually stand out — badges, stats widgets, project showcases, contribution graphs, anything that is free and easy to add. For each suggestion, tell me exactly what to do and give me the code or link I need to implement it right now.

---

Related: [[Repo — Deep Analysis]] — for analyzing repos *you visit*, not your own profile.