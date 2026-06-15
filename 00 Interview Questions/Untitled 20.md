# 10. Error Handling
Most beginners ignore this.
Questions:
What happens when:
```text
999 good rows
1 bad row
```
Options:
### Fail Entire Job
Strict approach.
---
### Skip Bad Rows
Flexible approach.
---
### Quarantine
Very common.
```text
Valid rows → Target
Invalid rows → Error table
```