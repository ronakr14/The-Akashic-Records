---
domain: database
subdomain: distribution
note_type: concept
source_type: self
status: draft
level: advanced
---
# AI Summary

DRAFT — scaffold only. Synthesis pending. Scaling a database beyond one node: replication topologies, consistency models, and partitioning/sharding strategies.

---

## Replication

- Leader/follower (single-leader), multi-leader, leaderless (quorum)
- Sync vs async; replication lag and read-your-writes
- Failover, split-brain, fencing

## Consistency models

- Strong / linearizable vs eventual vs causal
- Quorum reads/writes (R + W > N)
- Ties to CAP / PACELC — see [[Distributed System]]

## Partitioning / sharding

- Range vs hash vs directory partitioning
- Hot partitions, rebalancing, consistent hashing
- Secondary indexes on partitioned data (local vs global)
- Contrast with lake-side [[Partitioning]]

## Routing & coordination

- Where the routing tier lives; request routing strategies
- Cross-shard queries and transactions (2PC, sagas)

## Keys

- Shard-key choice; avoiding monotonic hotspots — see [[UUIDv7 & ULID]]

## Open questions

- Single-leader + read replicas enough, or is multi-region write needed?
- Shard key candidate for the main entities?

## Reference

- [[Turso]] — embedded/edge SQLite replication
- [[MongoDB]] — sharding + replica sets
- [[_Database Reference Index]]

## See also

- [[_Database MOC]] · [[Distributed System]] · [[Partitioning]] · [[UUIDv7 & ULID]] · [[Database Design]]
