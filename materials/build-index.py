#!/usr/bin/env python3
"""Writes index.html (landing page); the knowledge-map data is serialised with json.dumps.
Internal build script; never linked from an audience page."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
A = [("a1-count-what-you-have", "Count what you have", "Count what\nyou have", "#34D399", "📇",
      "The inventory: owner, last verified, alert bound, last drilled. Four states a page can be in, and the share of the library that would mislead tonight.",
      ["Four fields", "True, stale, orphaned", "Missing pages"], "start here"),
     ("a2-where-pages-go-stale", "Where pages go stale", "Where pages\ngo stale", "#FBBF24", "🍂",
      "Every system change is a chance a step stops being true. Change-triggered review against the calendar, and the linter rules a reviewer needs.",
      ["Drift with change", "Review on change", "Checkable steps"], None),
     ("a3-a-drill-is-the-only-test", "A drill is the only test", "A drill is the\nonly test", "#FBBF24", "⏱️",
      "Game days and paper drills, timing a newcomer through a page, what a failed step teaches, and a drill rota that fits one quarter.",
      ["Wheel of Misfortune", "Time a newcomer", "The drill rota"], None),
     ("a4-from-record-to-write-up", "From record to write-up", "From record\nto write-up", "#FB923C", "📝",
      "From the incident close-out record to the team postmortem: a UTC timeline, impact as numbers, conditions, actions as owner and date.",
      ["UTC timeline", "Impact in numbers", "Actions, not wishes"], None),
     ("a5-read-eleven-postmortems-as-one", "Read eleven postmortems as one", "Read eleven\npostmortems as one", "#FB923C", "🧵",
      "Tag the conditions across a year of incidents, find the repeat incident and the action that let it through, and read wishes for what they are.",
      ["Tag the conditions", "The repeat incident", "The corpus view"], None),
     ("a6-the-docs-kit-on-the-bench", "The docs kit on the bench", "The docs kit\non the bench", "#F87171", "⚖️",
      "The linter on a runbook and a postmortem, the whole library ladder, two traps that only look like progress, and the kit scored.",
      ["The ladder", "Two traps", "Kit scorecard"], "bench night")]
B = [("b1-which-docs-must-exist", "Which docs must exist", "Which docs\nmust exist", "#34D399", "📏",
      "A docs standard of three checkable rules, a severity line with deadlines, one owner each, and the open argument over stale pages.",
      ["Three rules", "Severity line", "Stale vs none"], "start here"),
     ("b2-the-review-people-come-to", "The review that people come to", "The review people\ncome to", "#FBBF24", "🪑",
      "The postmortem review ritual: who reads what before it, blameless facilitation in the room, and a reading club for other companies' incidents.",
      ["Read before the room", "The facilitator", "Reading club"], None),
     ("b3-writing-for-the-customer", "Writing for the customer", "Writing for\nthe customer", "#FB923C", "✉️",
      "One incident, three versions: team, executive, customer. What to say, what to redact, apology against explanation, timing and review.",
      ["Three readers", "What to redact", "Apology vs explanation"], None),
     ("b4-actions-that-close", "Actions that close", "Actions\nthat close", "#F87171", "✅",
      "Tracking actions to done: closure rate, the age of open actions, the repeat incident as the price of an open action, and the report you take upward.",
      ["Closed vs done", "Age of open actions", "Follow-through report"], "capstone")]

def card(f, title, icon, blurb, pill, track, n, tag):
    lab = f"{track} session {n}" + (f" · {tag}" if tag else "")
    return (f'      <a class="course-card" href="courses/{f}.html" style="--diff:{pill}"><span class="cicon">{icon}</span>'
            f'<span class="cnum">{lab}</span><h3>{title}</h3><p>{blurb}</p></a>')

cards_a = "\n".join(card(f, t, ic, bl, c, "Writer", i + 1, tg) for i, (f, t, _, c, ic, bl, _, tg) in enumerate(A))
cards_b = "\n".join(card(f, t, ic, bl, c, "Leader", i + 1, tg) for i, (f, t, _, c, ic, bl, _, tg) in enumerate(B))
mm = {"title": "Runbooks &\npostmortems", "centerColor": "#1A1338",
      "sessions": [{"label": l, "href": f"courses/{f}.html", "color": c,
                    "concepts": [{"label": x, "href": f"courses/{f}.html"} for x in cs]} for (f, _, l, c, _, _, cs, _) in A + B]}
tpl = open(os.path.join(HERE, "index.template.html")).read()
out = tpl.replace("{{CARDS_A}}", cards_a).replace("{{CARDS_B}}", cards_b).replace("{{MINDMAP}}", json.dumps(mm, indent=2, ensure_ascii=False))
open(os.path.join(HERE, "..", "index.html"), "w").write(out)
print("index.html written")
