---
note_type: glossary
status: reference
---
# Vault Dashboard

Dataview views over the vault. The deterministic version of these checks lives in [[Health Report]] (run `python .repo-metadata/health_report.py`); this note is the live, in-Obsidian view. Interactive editing of the same metadata: `Vault.base`.

Requires the Dataview plugin.

---

## Knowledge by status

```dataview
TABLE WITHOUT ID status AS "Status", length(rows) AS "Notes"
FROM "01-Knowledge"
WHERE note_type != "moc"
GROUP BY status
SORT length(rows) DESC
```

## Knowledge by domain

```dataview
TABLE WITHOUT ID domain AS "Domain", length(rows) AS "Notes"
FROM "01-Knowledge"
WHERE note_type != "moc"
GROUP BY domain
SORT length(rows) DESC
```

## Knowledge by level

```dataview
TABLE WITHOUT ID level AS "Level", length(rows) AS "Notes"
FROM "01-Knowledge"
WHERE note_type != "moc"
GROUP BY level
SORT length(rows) DESC
```

## Note types (whole vault)

```dataview
TABLE WITHOUT ID note_type AS "Type", length(rows) AS "Count"
FROM "01-Knowledge" OR "02-Projects" OR "03-Career" OR "06-Reference" OR "08-Prompts"
WHERE note_type
GROUP BY note_type
SORT length(rows) DESC
```

---

## Orphans — knowledge notes with no links in or out

```dataview
TABLE WITHOUT ID file.link AS "Note", domain AS "Domain", status AS "Status"
FROM "01-Knowledge"
WHERE note_type != "moc" AND length(file.inlinks) = 0 AND length(file.outlinks) = 0
SORT file.name ASC
```

## Weakly linked — fewer than 3 total links

```dataview
TABLE WITHOUT ID file.link AS "Note", length(file.inlinks) AS "In", length(file.outlinks) AS "Out", status AS "Status"
FROM "01-Knowledge"
WHERE note_type != "moc" AND (length(file.inlinks) + length(file.outlinks)) < 3
SORT (length(file.inlinks) + length(file.outlinks)) ASC
```

## Missing metadata — content notes lacking a schema key

```dataview
TABLE WITHOUT ID file.link AS "Note", domain, note_type, status, level
FROM "01-Knowledge" OR "02-Projects" OR "03-Career" OR "06-Reference" OR "08-Prompts"
WHERE (!domain OR !subdomain OR !note_type OR !source_type OR !status OR !level) AND note_type != "moc"
SORT file.folder ASC
```

---

## Promotion candidates — reference-status knowledge

```dataview
TABLE WITHOUT ID file.link AS "Note", domain AS "Domain", level AS "Level", length(file.inlinks) + length(file.outlinks) AS "Links", file.mtime AS "Modified"
FROM "01-Knowledge"
WHERE status = "reference" AND note_type != "moc"
SORT (length(file.inlinks) + length(file.outlinks)) DESC
```

## Drafts in progress

```dataview
TABLE WITHOUT ID file.link AS "Note", domain AS "Domain", file.mtime AS "Modified"
FROM "01-Knowledge" OR "02-Projects"
WHERE status = "draft"
SORT file.mtime DESC
```

## Stale ADRs / architecture (not touched in 180 days)

```dataview
TABLE WITHOUT ID file.link AS "Note", status AS "Status", file.mtime AS "Modified"
FROM "01-Knowledge" OR "05-Decisions"
WHERE (note_type = "adr" OR note_type = "architecture") AND file.mtime < date(today) - dur(180 days)
SORT file.mtime ASC
```

---

## Recently modified — last 7 days

```dataview
TABLE WITHOUT ID file.link AS "Note", domain AS "Domain", note_type AS "Type", status AS "Status", file.mtime AS "Modified"
FROM "01-Knowledge" OR "02-Projects" OR "03-Career" OR "04-Writing" OR "06-Reference"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 25
```

## Recently modified — last 30 days

```dataview
TABLE WITHOUT ID file.link AS "Note", domain AS "Domain", status AS "Status", file.mtime AS "Modified"
FROM "01-Knowledge"
WHERE file.mtime >= date(today) - dur(30 days)
SORT file.mtime DESC
LIMIT 40
```
