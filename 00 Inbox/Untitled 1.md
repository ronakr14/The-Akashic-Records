create a plan since I am trying to create a test automation framework for my client.

Main goal: 
	understand excel requirement -> create simple english markdown to review -> generate test data in .sql file -> generate testcases in BDD scenarios -> html/pdf reports.

What I exactly want from this framework:
1. understand excel requriement, using claude generate a process.md file containing entire process overview, DDL statements, Assumptions, Key Rules, ETL transformations, Acceptance criteria, BDD scenarios. This will be onetime process. For further changes, user will manually update the process file.
2. Using this process.md file, create testcases and store it in sqlite.md, I need this for HITL, so user can review each testcase generated and flag it if its useful for the process or not. HITL review can be done using seperate process by iterating over all testcases in the file. Testcases should contain testcaseid, severity, title, description, expected, isactive, feedback. If user flag this not active, ask user for answer -> not needed, correction needed. If correction needed, ask in detail what is wrong with the testcase.
3. After HITL review of the testcase, generate testsql, 