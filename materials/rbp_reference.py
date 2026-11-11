#!/usr/bin/env python3
"""Python reference for the Docs bench (assets/rbp-live.js). Constructed Pellmoor example.

Two engines, written independently of the JavaScript and required to agree with it on every value:
  1. lint(text)          the runbook / postmortem rule engine (9 rules)
  2. run(sample, opts)   the library + corpus model over one quarter (library) and one year (corpus)
Usage:
  python3 materials/rbp_reference.py <repo>           print the canon ladder, run the rule unit tests
  python3 materials/rbp_reference.py <repo> --json    canon as JSON (compare-ladder.py reads this)
The drift rate is a SIMULATED parameter (default 30 percent of system changes break a step on a
page they touch). The drift and catch rolls are shipped integers in assets/rbp-sample.js.
"""
import json, math, re, sys
from pathlib import Path

# ---------------------------------------------------------------- linter
JUDGE = ["check if", "check whether", "as appropriate", "as needed", "if needed", "if necessary", "investigate",
         "use your judgement", "use your judgment", "looks ok", "look ok", "looks high", "looks wrong",
         "looks normal", "make sure everything"]
ACT = re.compile(r"^(restart|run|scale|set|delete|drop|fail over|failover|roll back|rollback|deploy|purge|disable|"
                 r"enable|drain|kill|clear|flush|switch|re-run|rerun|replay|apply|reboot|stop|start)\b", re.I)
CONFIRM = re.compile(r"\b(confirm|expect|expected|you should see|verify that)\b", re.I)
STEP = re.compile(r"^\s*(\d+)[.)]\s+(.*)$")
HEAD = re.compile(r"^\s*#")
CMD = re.compile(r"^\s*\$\s+\S")
EXPECTED = re.compile(r"^\s*expected?:", re.I)
OWNER = re.compile(r"^\s*owner:\s*\S", re.I)
VERIFIED = re.compile(r"^\s*last (verified|updated):\s*\S", re.I)
RELATIVE = re.compile(r"\b(yesterday|this morning|last night|tonight|earlier today|later that day|a few minutes later|"
                      r"shortly after|around noon)\b", re.I)
CLOCK = re.compile(r"\b([01]?\d|2[0-3]):[0-5]\d(:[0-5]\d)?(?!\s*(UTC|Z)\b)(?![:\d])")
AMPM = re.compile(r"\b\d{1,2}(:\d\d)?\s?(am|pm)\b", re.I)
BLAMEW = re.compile(r"\b(careless|carelessly|human error|fault of|his fault|her fault|their fault|negligent|"
                    r"sloppy|mistake by|to blame)\b", re.I)
NAMED = re.compile(r"\b([A-Z][a-z]+) (pushed|deployed|forgot|missed|broke|ignored|changed|ran|deleted|merged|failed)\b")
NOT_NAMES = {"The", "We", "It", "A", "An", "This", "That", "Someone", "Nobody", "Everyone", "Team", "Pellmoor",
             "Supplier", "Pricing", "Finance", "Orders", "Picking", "Automation", "Validator", "Feed", "Job",
             "Scheduler", "Deploy", "Who", "Which", "Nothing", "Anyone"}
COUNTER = re.compile(r"\b(should have|should've|could have|would have|if only|failed to|ought to have)\b", re.I)
PM_HEAD = re.compile(r"^\s*#+\s*(impact|timeline|actions|action items)\b", re.I)
SEC = re.compile(r"^\s*#+\s*(.*)$")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
OWNER_IN = re.compile(r"owner:\s*\S", re.I)
BULLET = re.compile(r"^\s*[-*]\s+\S")

RULES = [
 ("judge", "Step needs judgement", "runbook"),
 ("confirm", "Action with no confirm step", "runbook"),
 ("expected", "Command with no expected output", "runbook"),
 ("owner", "No owner or last-verified line", "both"),
 ("time", "Relative or non-UTC timestamp", "both"),
 ("blame", "Blame language or a named person", "postmortem"),
 ("counter", "Counterfactual (\"should have\")", "postmortem"),
 ("wish", "Action without owner and date", "postmortem"),
 ("impact", "Impact with no number", "postmortem"),
]

def doc_type(lines):
    return "postmortem" if any(PM_HEAD.match(l) for l in lines) else "runbook"

def sections(lines):
    """name of the heading each line sits under ('' before any heading), lower case"""
    cur, out = "", []
    for l in lines:
        m = SEC.match(l)
        if m: cur = m.group(1).strip().lower()
        out.append(cur)
    return out

def lint(text):
    lines = text.split("\n")
    kind = doc_type(lines)
    sec = sections(lines)
    f = {r[0]: [] for r in RULES}
    # step blocks: a numbered step runs until the next numbered step, a heading, or the end
    blocks, cur = [], None
    for i, l in enumerate(lines):
        if HEAD.match(l):
            cur = None; continue
        if STEP.match(l):
            cur = [i]; blocks.append(cur)
        elif cur is not None:
            cur.append(i)
    if kind == "runbook":
        for b in blocks:
            body = STEP.match(lines[b[0]]).group(2)
            low = body.lower()
            if any(p in low for p in JUDGE): f["judge"].append(b[0] + 1)
            if ACT.match(body) and not any(CONFIRM.search(lines[j]) for j in b): f["confirm"].append(b[0] + 1)
            for k, j in enumerate(b):
                if CMD.match(lines[j]):
                    nxt = [lines[x] for x in b[k + 1:] if lines[x].strip()][:2]
                    if not any(EXPECTED.match(x) for x in nxt): f["expected"].append(j + 1)
    if not (any(OWNER.match(l) for l in lines) and any(VERIFIED.match(l) for l in lines)):
        f["owner"].append(1)
    for i, l in enumerate(lines):
        if RELATIVE.search(l) or CLOCK.search(l) or AMPM.search(l): f["time"].append(i + 1)
    if kind == "postmortem":
        for i, l in enumerate(lines):
            if BLAMEW.search(l) or any(m.group(1) not in NOT_NAMES for m in NAMED.finditer(l)): f["blame"].append(i + 1)
            if COUNTER.search(l): f["counter"].append(i + 1)
            if sec[i].startswith("action") and BULLET.match(l) and not (OWNER_IN.search(l) and DATE.search(l)):
                f["wish"].append(i + 1)
        imp = [i for i, l in enumerate(lines) if SEC.match(l) and sec[i].startswith("impact")]
        if not imp:
            f["impact"].append(1)
        else:
            body = [l for i, l in enumerate(lines) if sec[i].startswith("impact") and not SEC.match(l)]
            if not any(re.search(r"\d", l) for l in body): f["impact"].append(imp[0] + 1)
    rows = []
    for rid, name, scope in RULES:
        applies = scope == "both" or scope == kind
        rows.append({"id": rid, "name": name, "applies": applies, "lines": f[rid] if applies else []})
    app = [r for r in rows if r["applies"]]
    passed = sum(1 for r in app if not r["lines"])
    return {"kind": kind, "rules": rows, "passed": passed, "applicable": len(app),
            "findings": sum(len(r["lines"]) for r in app), "score": rnd(100 * passed / len(app))}

# ---------------------------------------------------------------- library + corpus model
DEFAULTS = {"owners": False, "rewrite": False, "review": False, "drill": 0, "chase": 0, "drift": 30,
            "deleteStale": False, "autoClose": False}

def rnd(x):
    """half-up, to match JavaScript Math.round (Python round() is half-to-even)"""
    return int(math.floor(x + 0.5))

def median(xs):
    if not xs: return 0
    s = sorted(xs); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

def run(S, opts=None):
    o = dict(DEFAULTS); o.update(opts or {})
    P = S["pages"]; n = len(P)
    active = [(not p["isNew"]) or o["owners"] for p in P]
    if o["deleteStale"]:
        active = [a and not (not p["isNew"] and p["age"] > 365) for a, p in zip(active, P)]
    owned = [active[i] and (P[i]["owned"] or o["owners"] or P[i]["isNew"]) for i in range(n)]
    clean = [owned[i] and o["rewrite"] for i in range(n)]
    thr = [900 if clean[i] else 400 for i in range(n)]
    wrong = [list(P[i]["wrong"]) if active[i] else [] for i in range(n)]
    caught = 0
    if o["owners"] or o["rewrite"]:                   # week 0: each owner reads their page once
        for i in range(n):
            if owned[i]:
                keep = [u for u in wrong[i] if u >= thr[i]]
                caught += len(wrong[i]) - len(keep); wrong[i] = keep
    drillable = [i for i in range(n) if active[i] and owned[i] and P[i]["alert"]]
    plan = {}
    if o["drill"]:
        for k, i in enumerate(drillable):
            w = 1 + (k % o["drill"])
            while w <= S["meta"]["weeks"]:
                plan.setdefault(w, []).append(i); w += o["drill"]
    drilled, drills, drifted, missed = [False] * n, 0, 0, 0
    for wk in range(1, S["meta"]["weeks"] + 1):
        for c in S["changes"]:
            if c["wk"] != wk: continue
            for i, ud, uc in c["touch"]:
                if not active[i] or ud >= o["drift"] * 10: continue
                drifted += 1
                if o["review"] and owned[i] and uc < thr[i]: caught += 1
                else: wrong[i].append(uc)
        todo = list(plan.get(wk, []))
        if wk == 6: todo += [i for i in S["gameday"] if active[i]]
        for i in todo:
            drilled[i] = True; drills += 1; wrong[i] = []
    act_idx = [i for i in range(n) if active[i]]
    mis = sum(1 for i in act_idx if wrong[i])
    bound = [i for i in act_idx if P[i]["alert"]]
    states = []
    for i in range(n):
        if not active[i]: st = "missing" if P[i]["alert"] else "deleted"
        elif wrong[i]: st = "stale"
        elif not owned[i]: st = "orphaned"
        else: st = "true"
        states.append(st)
    lib = {"pages": len(act_idx), "misleading": mis, "share": rnd(100 * mis / len(act_idx)) if act_idx else 0,
           "alertsTotal": sum(p["alert"] for p in P), "alertsNoPage": sum(1 for i in range(n) if P[i]["alert"] and not active[i]),
           "orphaned": sum(1 for i in act_idx if not owned[i]),
           "boundPages": len(bound), "drilledBound": sum(1 for i in bound if drilled[i]),
           "drillCoverage": rnd(100 * sum(1 for i in bound if drilled[i]) / len(bound)) if bound else 0,
           "drills": drills, "drifted": drifted, "caughtByReview": caught,
           "wrongSteps": sum(len(wrong[i]) for i in act_idx), "states": states,
           "deleted": sum(1 for i in range(n) if not P[i]["isNew"] and not active[i])}
    # corpus over the year
    Y = S["meta"]["yearWeeks"]
    done, marked = [], []
    for a in S["actions"]:
        has_owner = a["owner"] or o["owners"]; has_due = a["due"] or o["rewrite"]; wish = a["wish"] and not o["rewrite"]
        proper = has_owner and has_due and not wish
        d = None
        if proper:
            t = a["wk"] + a["effort"]
            if o["chase"]: d = int(math.ceil(t / o["chase"]) * o["chase"])
            elif a["neglect"] is not None: d = t + a["neglect"]
        if d is not None and d > Y: d = None
        mk = d
        if o["autoClose"] and has_due and a["wk"] + 4 <= Y:
            mk = a["wk"] + 4 if mk is None else min(mk, a["wk"] + 4)
        done.append(d); marked.append(mk)
    A = S["actions"]
    closed = sum(1 for m in marked if m is not None)
    ages = [Y - A[k]["wk"] for k in range(len(A)) if marked[k] is None]
    repeats = []
    for pm in S["pms"]:
        if pm["repeatOf"]:
            k = next(j for j, a in enumerate(A) if a["id"] == pm["repeatOf"])
            if done[k] is None or done[k] >= pm["wk"]: repeats.append(pm["id"])
    cor = {"actions": len(A), "closed": closed, "closure": rnd(100 * closed / len(A)),
           "reallyDone": sum(1 for d in done if d is not None), "open": len(ages), "medianOpenAge": median(ages),
           "wishes": sum(1 for a in A if a["wish"] and not o["rewrite"]),
           "repeats": len(repeats), "repeatIds": repeats, "repeatsPossible": sum(1 for p in S["pms"] if p["repeatOf"]),
           "done": done, "marked": marked}
    return {"library": lib, "corpus": cor}

PRESETS = [
 ("r0", "As found", {}),
 ("r1", "Inventory + owners", {"owners": True}),
 ("r2", "Linter-clean rewrites", {"owners": True, "rewrite": True}),
 ("r3", "Change-triggered review", {"owners": True, "rewrite": True, "review": True}),
 ("r4", "Drill rota", {"owners": True, "rewrite": True, "review": True, "drill": 13}),
 ("r5", "Action chase", {"owners": True, "rewrite": True, "review": True, "drill": 13, "chase": 2}),
]
TRAPS = [
 ("t1", "Delete the stale pages", {"deleteStale": True}),
 ("t2", "Auto-close at the due date", {"owners": True, "rewrite": True, "autoClose": True}),
]
MOVES = [
 ("m1", "Drift 50, full ladder", {"owners": True, "rewrite": True, "review": True, "drill": 13, "chase": 2, "drift": 50}),
 ("m2", "Drill monthly, no review", {"owners": True, "rewrite": True, "drill": 4}),
 ("m3", "Chase weekly, no rewrites", {"owners": True, "chase": 1}),
 ("m4", "Review on, no owners", {"review": True}),
]

def load_sample(repo):
    js = (Path(repo) / "assets/rbp-sample.js").read_text()
    start = js.index("window.RBP_SAMPLE = ") + len("window.RBP_SAMPLE = ")
    return json.JSONDecoder().raw_decode(js[start:])[0]

def canon(repo):
    S = load_sample(repo)
    samples = json.loads((Path(repo) / "materials/rbp-samples.json").read_text())
    def one(t):
        rid, name, o = t; r = run(S, o); r["rung"] = rid; r["name"] = name; return r
    return {"ladder": [one(t) for t in PRESETS], "traps": [one(t) for t in TRAPS], "moves": [one(t) for t in MOVES],
            "lint": {k: lint(v["text"]) for k, v in samples.items()}}

# ---------------------------------------------------------------- rule unit tests (pass AND fail per rule)
TESTS = [
 ("judge", "1. Check if the queue looks high.", "1. Read the queue depth on the panel."),
 ("confirm", "1. Restart the adapter.", "1. Restart the adapter.\n   Confirm the error rate falls below 2%."),
 ("expected", "1. Run the check.\n   $ ./check.sh\n   Then carry on.", "1. Run the check.\n   $ ./check.sh\n   Expected: OK\n   Confirm OK."),
 ("owner", "# RB\n1. Read the panel.", "# RB\nOwner: a\nLast verified: 2026-01-01\n1. Read the panel."),
 ("time", "## Timeline\nAt 09:40 the feed arrived yesterday.", "## Timeline\n2026-10-28 09:40 UTC the feed arrived."),
 ("blame", "## Timeline\nPriya pushed the feed.", "## Timeline\nThe feed was accepted by the validator."),
 ("counter", "## Impact\n3 orders. The validator should have caught it.", "## Impact\n3 orders. The validator checks columns, not values."),
 ("wish", "## Actions\n- Make validation better", "## Actions\n- Add an outlier check. Owner: pricing lead. Due: 2026-11-25"),
 ("impact", "## Impact\nSome customers saw wrong prices.", "## Impact\n1,140 products wrong for 3 hours."),
]

def self_test():
    bad = []
    for rid, failing, passing in TESTS:
        def hit(t):
            return bool(next(r for r in lint(t)["rules"] if r["id"] == rid)["lines"])
        if not hit(failing): bad.append(rid + " missed its failing sample")
        if hit(passing): bad.append(rid + " flagged its passing sample")
    return bad

if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else str(Path(__file__).resolve().parents[1])
    c = canon(repo)
    if "--json" in sys.argv:
        print(json.dumps(c)); sys.exit(0)
    bad = self_test()
    print("rule unit tests:", "all 18 pass" if not bad else bad)
    for grp in ("ladder", "traps", "moves"):
        for r in c[grp]:
            L, C = r["library"], r["corpus"]
            print(f"{r['rung']:3} {r['name']:28} mislead {L['misleading']:2}/{L['pages']} ({L['share']}%) nopage {L['alertsNoPage']} "
                  f"orphan {L['orphaned']:2} drill {L['drilledBound']}/{L['boundPages']} ({L['drillCoverage']}%) drifted {L['drifted']} | "
                  f"closed {C['closed']}/46 ({C['closure']}%) done {C['reallyDone']} medAge {C['medianOpenAge']} repeats {C['repeats']}/2")
    for k, v in c["lint"].items():
        print(k, v["kind"], f"{v['passed']}/{v['applicable']} score {v['score']} findings {v['findings']}",
              {r['id']: r['lines'] for r in v['rules'] if r['lines']})
    sys.exit(1 if bad else 0)
