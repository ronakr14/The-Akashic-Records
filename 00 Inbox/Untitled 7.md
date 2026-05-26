I need to create a test automation framework for my client.
Goal : understand requriements -> create testdata/ testsql -> run script -> report in html format

Techstack: databricks, SQL, excel, txt file, python notebook/scripts

Phase 1:
1. convert excel requirements to markdown file using caveman mode.
2. Extract scope, assumptions, requirement, process stages, BDD scenarios, DDL
3. This will only happen onetime, so I can use claude code for conversion.
4. For future, it will be HITL everytime, unless we get complete new requirement.
5. I am ready to remove striked out part from the excel before sharing.
6. Excel is not structures, it is just detailed instructions.

Phase 2:
1. Based on markdown file extracted from phase 1, use claude code to generate testcases, test sql, test data.
2. testcases should cover happy path, edge cases, negative scenarios. Each testcase should provide testID, testcase, test description, acceptance criteria, generic sql
3. test sql should only use DDL provided in markdown. I do not want anything extra.
4. testdata should cover all testcases.
5. All this we can store in sqlite.md file with proper metadata. We will do HITL scenario to get feedback if sql, testdata is correct or not, and if not then why its not.

phase 3:
1. a python notebook which prepares test environment by performing following steps.
	1. create test env by taking backups and truncating original table.
	2. ingest test data
	3. run the original process script
	4. run test sql and then capture all test details, sql, result and status in html report.
	5. once all testcases done, then reload the original table using backup table.

Before starting, grill me if I am clear about my requirement, do not assume anything