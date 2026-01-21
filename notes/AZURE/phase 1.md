1️⃣ Fabric Workspace — EXAM CORE

Workspace = management + governance boundary

✔ Contains Fabric items (Lakehouse, Warehouse, Notebook, Pipeline, Semantic Model, etc.)
✔ Enforces access control (security boundary)
✔ Scopes workspace item events
✔ Holds workspace-level configuration

❌ Does NOT execute workloads
❌ Does NOT tune performance
❌ Does NOT control Spark/SQL runtime behavior

🧠 Exam hack

If question mentions performance, execution, runtime → NOT workspace

2️⃣ Workspace Item Events — MUST KNOW

✔ Emitted when Fabric item state changes

Refresh started / completed / failed

Pipeline run failed

Item created / deleted

❌ NOT emitted for:

Row-level data changes

Query execution

Pipeline activities

🧠 Event rule

Item = emits event
Activity = logs only

3️⃣ Events vs Logs vs Metrics (VERY TESTED)
Purpose	Use
Detect failure	Item event
Trigger automation	Item event
Error details / root cause	Logs
Duration / trends	Metrics
Impacted downstream items	Lineage

🧠 Hack

WHEN → Event
WHY → Log
HOW LONG → Metric
WHO BREAKS → Lineage

4️⃣ Real-Time Hub — EXAM TRAPS

✔ Aggregates real-time metadata & current state
✔ Discovers Eventstreams, KQL DBs, streaming sources
✔ Shows ingestion status NOW

❌ Does NOT:

Store data

Show historical trends

Execute queries

Trigger alerts

🧠 Hack

Real-Time Hub = WHO + NOW

5️⃣ Semantic Model Refresh Failure — INTERNAL FLOW

1️⃣ Item event → failure detected
2️⃣ Logs → error message
3️⃣ Metrics → duration / failure trends
4️⃣ Lineage → impacted reports

❌ Item event does NOT contain error details

6️⃣ Spark Workspace Settings — DP-700 CRITICAL

Spark workspace settings = DEFAULTS ONLY

✔ Apply to new Spark sessions only
✔ Define default Spark configuration
✔ Scoped to one workspace

❌ Do NOT:

Override notebook code

Improve performance automatically

Affect running jobs

Apply across workspaces

🧠 Hack

Spark workspace settings = template, not enforcement

7️⃣ Spark Settings Precedence (WRITE THIS)
Notebook spark.conf.set()
    ⬆ overrides
Spark workspace defaults

8️⃣ COMMON DP-700 TRAP PHRASES (AUTO-REJECT)

❌ “Improve Spark performance by changing workspace settings”
❌ “Workspace controls query execution”
❌ “Real-Time Hub shows historical trends”
❌ “Logs trigger alerts”
❌ “KQL can trigger pipelines”

🔥 ONE-LINE MASTER MEMORY (WRITE THIS)

Workspace = WHO + WHAT + WHO CAN
Spark settings = DEFAULTS ONLY
Event = WHEN
Log = WHY
Metric = HOW LONG
Lineage = WHO BREAKS

---


🧠 CRITICAL DP-700 MIND-HACK

Domain = BUSINESS VIEW 🏢
Workspace = TECHNICAL CONTAINER 📦

If the question is about:

business ownership → Domain

runtime behavior → ❌ Not domain
