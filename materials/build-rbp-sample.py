#!/usr/bin/env python3
"""Build assets/rbp-sample.js: Pellmoor's constructed incident docs library and corpus.

Constructed Pellmoor example. Nothing here is a real company's data. Every random draw is seeded,
and the drift / catch rolls are SHIPPED as integers (0-999) so the browser engine and the Python
reference read the same rolls and never need a shared hash. Serialised with json.dumps.
Usage: python3 materials/build-rbp-sample.py <repo>
"""
import json, random, sys
from pathlib import Path

rng = random.Random(20261111)
SYS = {"app": "Customer app", "pricing": "Pricing feed", "orders": "Order pipeline",
       "picking": "Warehouse picking", "finance": "Finance warehouse"}

# id, system, title, owned at start, days since last verified, paging alert bound (1/0)
PAGES = [
 ("RB-01","app","App login errors spike",1,40,1), ("RB-02","app","App crash rate above threshold",1,95,1),
 ("RB-03","app","Push notifications delayed",0,410,0), ("RB-04","app","Search returns empty results",1,220,1),
 ("RB-05","app","Basket totals mismatch",0,640,1), ("RB-06","app","Delivery slot picker blank",1,150,1),
 ("RB-07","app","Checkout payments failing",1,520,1), ("RB-08","app","App store release rollback",0,300,0),
 ("RB-09","pricing","Supplier price feed late",1,60,1), ("RB-10","pricing","Price feed rejected by validator",1,380,1),
 ("RB-11","pricing","Price change above 30 percent",0,700,1), ("RB-12","pricing","Promotion prices not applied",1,130,1),
 ("RB-13","pricing","Price cache stale",0,450,0), ("RB-14","pricing","Supplier feed schema changed",0,820,1),
 ("RB-15","pricing","Manual price override",1,25,0),
 ("RB-16","orders","Order queue backlog",1,30,1), ("RB-17","orders","Orders stuck in pending",1,200,1),
 ("RB-18","orders","Payment capture retries",0,390,1), ("RB-19","orders","Duplicate orders",1,170,1),
 ("RB-20","orders","Order events lagging",0,560,1), ("RB-21","orders","Refund job failed",1,260,1),
 ("RB-22","orders","Substitution service down",0,900,0), ("RB-23","orders","Order API error rate",1,75,1),
 ("RB-24","picking","Pick lists not generated",0,480,1), ("RB-25","picking","Handheld scanner sync failing",1,110,1),
 ("RB-26","picking","Picking wave late",1,340,1), ("RB-27","picking","Stock count mismatch",0,610,0),
 ("RB-28","picking","Cold chain sensor alert",1,55,1), ("RB-29","picking","Van loading manifest missing",0,430,0),
 ("RB-30","picking","Warehouse Wi-Fi outage",1,190,0), ("RB-31","picking","Label printer queue stuck",0,750,0),
 ("RB-32","finance","Nightly finance load failed",1,90,1), ("RB-33","finance","Revenue table late",1,280,1),
 ("RB-34","finance","Payment reconciliation gap",0,530,0), ("RB-35","finance","Supplier invoice match failing",1,160,0),
 ("RB-36","finance","Tax report export",0,680,0), ("RB-37","finance","Month-end close checklist",1,45,0),
 ("RB-38","finance","Warehouse credits exhausted",1,365,1),
]
# paging alerts that have no page at all (state: missing). Written as new pages on the inventory rung.
MISSING = [("NP-1","pricing","Feed row count drop"),("NP-2","orders","Payment webhook silent"),
           ("NP-3","picking","Freezer door open"),("NP-4","app","Delivery ETA wrong"),
           ("NP-5","finance","Duplicate revenue rows"),("NP-6","pricing","Feed currency mismatch")]
GAMEDAY = ["RB-16", "RB-23", "RB-32"]   # the one ad hoc game day Pellmoor already holds, week 6

pages = []
for pid, s, title, owned, age, alert in PAGES:
    if age > 365: nw = rng.choice([0, 1, 1, 2])
    elif age > 180: nw = rng.choice([0, 0, 1])
    else: nw = rng.choice([0, 0, 0, 0, 1])
    pages.append({"id": pid, "sys": s, "title": title, "owned": owned, "age": age, "alert": alert,
                  "steps": rng.randint(6, 14), "wrong": [rng.randint(0, 999) for _ in range(nw)], "isNew": 0})
for pid, s, title in MISSING:
    pages.append({"id": pid, "sys": s, "title": title, "owned": 0, "age": 0, "alert": 1,
                  "steps": rng.randint(5, 9), "wrong": [], "isNew": 1})
idx = {p["id"]: i for i, p in enumerate(pages)}

NCH = {"app": 9, "pricing": 8, "orders": 8, "picking": 6, "finance": 5}
changes = []
for s, n in NCH.items():
    cand = [i for i, p in enumerate(pages) if p["sys"] == s]
    for k in range(n):
        wk = rng.randint(1, 13)
        t = rng.sample(cand, rng.choice([1, 2, 2, 3]))
        changes.append({"wk": wk, "sys": s, "touch": [[i, rng.randint(0, 999), rng.randint(0, 999)] for i in sorted(t)]})
changes.sort(key=lambda c: (c["wk"], c["sys"]))
for n, c in enumerate(changes): c["id"] = "CH-%02d" % (n + 1)

# ---- corpus: 11 postmortems, 46 actions over the last 52 weeks ----
PMS = [
 ("PM-01",3,2,"orders","Order queue backlog after a deploy",["deploy without rollback check","queue alert too late"]),
 ("PM-02",6,2,"finance","Nightly finance load failed twice",["silent job failure","credits not watched"]),
 ("PM-03",10,2,"picking","Pick lists missing for the morning wave",["silent job failure","stale runbook step"]),
 ("PM-04",14,1,"pricing","Supplier feed schema change broke validation",["unvalidated supplier input","stale runbook step"]),
 ("PM-05",19,2,"app","Login errors after a certificate expiry",["expiry not tracked","queue alert too late"]),
 ("PM-06",24,3,"orders","Duplicate orders from a retry storm",["retry without idempotency","deploy without rollback check"]),
 ("PM-07",28,2,"app","Delivery slot picker blank for an hour",["config pushed untested","stale runbook step"]),
 ("PM-08",32,2,"finance","Revenue table two days late",["silent job failure","credits not watched"]),
 ("PM-09",36,2,"picking","Pick lists missing again",["silent job failure","stale runbook step"]),
 ("PM-10",41,3,"orders","Refund job silently skipped a day",["silent job failure","no alert on silent job"]),
 ("PM-11",47,1,"pricing","Wrong prices shown to customers for 3 hours",["unvalidated supplier input","no alert on price outliers"]),
]
NACT = [4, 4, 5, 6, 4, 3, 4, 4, 5, 3, 4]
assert sum(NACT) == 46
ACT_TEXT = {
 "wish": ["Improve monitoring", "Be more careful with deploys", "Look into the alerting", "Make validation better",
          "Review the runbook", "Communicate better with suppliers", "Investigate retries", "Think about capacity"],
 "act": ["Add a rollback check to the deploy pipeline", "Page on queue depth above 5,000", "Alert when the nightly load writes zero rows",
         "Watch warehouse credits at 80 percent", "Reject supplier files whose schema differs from the contract",
         "Track certificate expiry with a 30-day page", "Make order retries idempotent", "Test config pushes in staging first",
         "Add an outlier check against the last accepted feed", "Rewrite the pick-list runbook after the scheduler move",
         "Bind the refund alert to a runbook", "Drill the price-feed runbook once a quarter"],
}
pms, actions = [], []
for (pid, wk, sev, s, title, tags), n in zip(PMS, NACT):
    pms.append({"id": pid, "wk": wk, "sev": sev, "sys": s, "title": title, "tags": tags, "repeatOf": None})
    for k in range(n):
        wish = 1 if rng.random() < 0.3 else 0
        owner = 0 if (wish and rng.random() < 0.6) or rng.random() < 0.15 else 1
        due = 0 if wish or rng.random() < 0.25 else 1
        effort = rng.randint(2, 14)
        # what history did with nobody chasing: proper actions often closed late, some never
        neglect = None if (wish or not owner or not due or rng.random() < 0.35) else rng.randint(2, 20)
        tag = tags[k % len(tags)]
        text = rng.choice(ACT_TEXT["wish"] if wish else ACT_TEXT["act"])
        actions.append({"id": "%s.%d" % (pid, k + 1), "pm": len(pms) - 1, "wk": wk, "owner": owner, "due": due,
                        "wish": wish, "effort": effort, "neglect": neglect, "tag": tag, "text": text})
# action texts written by hand per postmortem (the draw above only fills the field)
ACT_BY_ID = {'PM-01.1': 'Add a rollback check to the order service deploy', 'PM-01.2': 'Page on order queue depth above 5,000', 'PM-01.3': 'Block deploys that skip the canary step', 'PM-01.4': 'Look into the queue alerting', 'PM-02.1': 'Alert when the nightly finance load writes zero rows', 'PM-02.2': 'Watch warehouse credits at 80 percent', 'PM-02.3': 'Retry the finance load once, then page', 'PM-02.4': 'Add warehouse credits to the weekly capacity review', 'PM-03.1': 'Improve monitoring of the picking jobs', 'PM-03.2': 'Look into the pick-list job', 'PM-03.3': 'Make the scheduler more reliable', 'PM-03.4': 'Review the pick-list runbook', 'PM-03.5': 'Alert when no pick list exists by 05:00 UTC', 'PM-04.1': 'Make validation better', 'PM-04.2': 'Rewrite RB-14 for the new schema contract', 'PM-04.3': 'Reject supplier files whose schema differs from the contract', 'PM-04.4': 'Keep the runbooks up to date', 'PM-04.5': 'Communicate better with suppliers', 'PM-04.6': 'Bind RB-10 to the validator alert', 'PM-05.1': 'Track certificate expiry with a 30-day page', 'PM-05.2': 'Page on login error rate above 2 percent for 5 minutes', 'PM-05.3': 'Automate certificate renewal for the app gateway', 'PM-05.4': 'Add login errors to the app dashboard alert set', 'PM-06.1': 'Make order retries idempotent', 'PM-06.2': 'Be more careful with deploys', 'PM-06.3': 'Cap order retries at three per minute', 'PM-07.1': 'Test slot-picker config pushes in staging first', 'PM-07.2': 'Review the slot picker runbook', 'PM-07.3': 'Think about config safety', 'PM-07.4': 'Add a config rollback step to RB-06', 'PM-08.1': 'Improve monitoring of the revenue load', 'PM-08.2': 'Watch warehouse credits at 80 percent', 'PM-08.3': 'Look into the revenue pipeline', 'PM-08.4': 'Move the revenue load ahead of the credit reset', 'PM-09.1': 'Investigate the picking jobs again', 'PM-09.2': 'Rewrite RB-24 after the scheduler move', 'PM-09.3': 'Alert when no pick list exists by 05:00 UTC', 'PM-09.4': 'Keep the picking runbooks current', 'PM-09.5': 'Drill RB-24 with a newcomer', 'PM-10.1': 'Improve job monitoring', 'PM-10.2': 'Bind the refund job alert to RB-21', 'PM-10.3': 'Look into silent jobs', 'PM-11.1': 'Add an outlier check against the last accepted feed', 'PM-11.2': 'Page on more than 50 price changes above 30% in one file', 'PM-11.3': 'Make the feed safer', 'PM-11.4': 'Drill RB-11 with a newcomer'}
for a in actions:
    a["text"] = ACT_BY_ID[a["id"]]
# the two repeat incidents: PM-09 repeats PM-03, PM-11 repeats PM-04, each through one action never done
def fix(aid, **kw):
    a = next(x for x in actions if x["id"] == aid); a.update(kw)
fix("PM-03.2", owner=0, due=0, wish=1, effort=5, neglect=None, tag="silent job failure", text="Look into the pick-list job")
fix("PM-04.1", owner=1, due=0, wish=1, effort=8, neglect=None, tag="unvalidated supplier input", text="Make validation better")
pms[8]["repeatOf"] = "PM-03.2"
pms[10]["repeatOf"] = "PM-04.1"

out = {"meta": {"case": "Constructed Pellmoor example", "systems": SYS, "weeks": 13, "yearWeeks": 52,
                "note": "Constructed. Drift and catch rolls are shipped integers 0-999."},
       "pages": pages, "gameday": [idx[g] for g in GAMEDAY], "changes": changes, "pms": pms, "actions": actions}
repo = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1])
js = ("/* rbp-sample.js - Constructed Pellmoor example: 38 runbooks (+6 alerts with no page), 35 system changes in one\n"
      "   quarter, 11 postmortems and 46 actions over a year. Generated by materials/build-rbp-sample.py (json.dumps). */\n"
      "window.RBP_SAMPLE = " + json.dumps(out, separators=(",", ":")) + ";\n"
      "window.RBP_SAMPLES = " + json.dumps(json.loads((repo / "materials/rbp-samples.json").read_text()), separators=(",", ":")) + ";\n")
(repo / "assets/rbp-sample.js").write_text(js)
print("pages", len(pages), "changes", len(changes), "pms", len(pms), "actions", len(actions), "bytes", len(js))
print("owned", sum(p["owned"] for p in pages[:38]), "alert-bound", sum(p["alert"] for p in pages[:38]),
      "wrong at start", sum(1 for p in pages if p["wrong"]), "wishes", sum(a["wish"] for a in actions),
      "no owner", sum(1 - a["owner"] for a in actions), "no due", sum(1 - a["due"] for a in actions))
