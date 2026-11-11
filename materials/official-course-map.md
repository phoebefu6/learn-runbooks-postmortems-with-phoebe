# Official course map - learn-runbooks-postmortems-with-phoebe

"Runbooks & Postmortems". Two tracks: Writer (a1-a6, bench capstone a6) and Leader (b1-b4), 45 minutes
each. Built 2026-11-11 by the course lead. Internal build document: never linked from an audience page.

Question across the course: of every runbook and postmortem you have, how many would help the next
responder, and how many would mislead them?

Angle: the docs SYSTEM, not one document. Siblings teach one runbook and one postmortem; this course
owns the library (inventory, drift, coverage, drills at scale) and the corpus (many postmortems read
as one dataset, three readers, actions tracked to done).

## Evidence tiers

- **Read at source** = fetched and read on 2026-11-11 by the lead. Only these may be quoted, and only
  in short phrases (under 15 words, one per page at most, with attribution).
- **Reported** = the page could not be read (blocked or paywalled), or the claim comes from a book or a
  vendor blog; say "reported" and paraphrase.
- **Constructed** = Pellmoor and everything in its library, corpus and samples. Label "Constructed
  Pellmoor example" every time.

## Verified facts (read at source, 2026-11-11)

### Google SRE book, ch. 15 "Postmortem Culture: Learning from Failure" (Lunney, Lueder; ed. O'Connor)
URL https://sre.google/sre-book/postmortem-culture/
- Definition: a postmortem is "a written record of an incident, its impact, the actions taken to
  mitigate or resolve it", plus root causes and follow-up actions.
- Triggers listed (paraphrase): user-visible downtime or degradation beyond a threshold; data loss of
  any kind; on-call intervention such as a rollback or rerouting; resolution time above a threshold; a
  monitoring failure (usually meaning the incident was found by hand).
- Blameless: the write-up focuses on contributing causes and "assumes that everyone involved in an
  incident had good intentions".
- Best-practice headings: avoid blame and keep it constructive; no postmortem left unreviewed;
  visibly reward people for doing the right thing; ask for feedback on postmortem effectiveness.
- "An unreviewed postmortem might as well never have existed."
- Sharing rituals: postmortem of the month (a monthly newsletter); postmortem reading clubs on
  incidents months or years old; Wheel of Misfortune (a past postmortem re-enacted with engineers in
  the roles).

### Google SRE book, Introduction (Emergency Response)
URL https://sre.google/sre-book/introduction/
- Recording best practice ahead of time in a playbook "produces roughly a 3x improvement in MTTR"
  compared with "winging it". This is Google's own reported experience, not a controlled study: say so.

### Google SRE book, "Accelerating SREs to On-Call and Beyond"
URL https://sre.google/sre-book/accelerating-sre-on-call/
- Disaster role playing is "commonly referred to as" Wheel of Misfortune or Walk the Plank.
- Lists "training strictly through operator procedures, checklists, and playbooks" as an
  anti-pattern: playbooks do not replace understanding. (Used in a3: a drill tests the page AND the
  responder.)
- Section "Break Real Things, Fix Real Things": practise on a realistic instance diverted from live
  traffic or a borrowed staging stack (a3 paraphrases it). A game master presents a scenario, often
  drawn from a past outage, to the primary and secondary on-call (a3, b2).
- In a rapidly changing environment documentation "can fall out of date quickly"; newer engineers
  depend more on it than seniors who fill gaps from memory.

### Google SRE workbook, ch. 10 "Postmortem Culture: Learning from Failure"
(Rogers, Suriar, Lueder, Deo, Sudhakar, with O'Connor and Rensin) URL https://sre.google/workbook/postmortem-culture/
- Worked case: one bad and one good postmortem of the same 2014 outage. Bad version faults: missing
  context, missing action-item detail, finger-pointing, animated language, many owners, limited
  audience, published four months late. Good version: written and circulated less than a week after
  the incident closed.
- Action items in the good version carry a type (investigate, prevent, mitigate, repair, detect), a
  priority, ONE owner and a tracking bug; 14 items in five themes. "It's better to have a single owner
  and multiple collaborators."
- Changing human behaviour "is less reliable than changing automated systems".
- Quantify impact; "a well-informed estimate is better than no data at all".
- Prompt postmortems "tend to be more accurate" (said of the good version, circulated within a week).
- Ben Treynor Sloss (quoted in the chapter): a postmortem "without subsequent action is
  indistinguishable from no postmortem".
- Google files action items as bugs in a central tracker so it can monitor their closure; rewards
  closing actions, not just writing; FixIt weeks twice a year.
- Warning signs of a failing culture include repeating incidents and leaders using blameful language.
- Storage and analysis: a searchable repository of thousands of postmortems since 2009, analysed for
  trends (postmortems per month, time to detect and resolve, blast radius).

### Google SRE workbook, "On-Call"
URL https://sre.google/workbook/on-call/
- "Details in playbooks go out of date at the same rate as production environment changes." THIS is
  the basis of the bench's drift model (each change is a chance a step stops being true).
- "Each alert should have a corresponding playbook entry"; when an alert is created a playbook entry
  usually is too.
- On-call engineers should update the playbook with fresh information when the page fires.
- CONTESTED (teach the disagreement, b1 and a2): teams disagree on detail; some keep entries general
  "so they change slowly", others prefer step-by-step. The workbook asks teams to agree a minimal
  structure. Neither side is resolved here.
- Playbooks "reduce stress, the mean time to repair (MTTR), and the risk of human error".

### PagerDuty Postmortem guide (Apache 2.0) URL https://docs.pagerduty.com/ops-guides/postmortem-best-practices
- Postmortem for every major incident (Sev-1 and Sev-2). Internal policy: complete within 3 calendar
  days for a Sev-1 and 5 business days for a Sev-2. The incident commander picks ONE owner, to avoid
  the bystander effect; writing is collaborative.
- Blameless page cites Dekker's Field Guide (old view vs new view: human error as a symptom of a
  systemic problem) and Allspaw's "The Infinite Hows" (ask how, not why). Hindsight bias: start the
  timeline before the incident and work forward.
- Effective postmortems: action items "actionable, specific, and bounded in scope"; do not call it an
  "outage" when it was less; very rarely is the mistake rooted in a person.
- Meeting: the document goes to attendees 24 hours ahead; the facilitator "speaks as little as
  possible", takes no sides; agenda: owner summarises causes and timeline, then actions, then the
  customer liaison summarises customer impact and the external message is reviewed and approved. The
  customer liaison attends for Sev-1 only (optional).
- Sharing: completed postmortems go to an "Incident Reports" list; meetings sit on a company-wide
  calendar anyone may join.
- Product note, dated: the guide states the PagerDuty Postmortems feature reached end of life on
  31 October 2026. Re-verify vendor docs before delivery.

### Google Cloud blog, "Fearless shared postmortems - CRE life lessons" (Hilton, Stockman, 2017-11-28)
URL https://cloud.google.com/blog/products/gcp/fearless-shared-postmortems-cre-life-lessons
- Sharing postmortems with customers can be good for both sides; the more of the customer's error
  budget an incident consumed, the more detail they want.
- Redact: names of people (say "a network engineer"), internal system names, other customers' details
  (Customer A, B); on graphs keep the time axis, drop absolute quantities or use percentages.
- Keep the "why did it happen" and "where we got lucky" sections close to as-is; write the least
  detailed background that still explains the incident.
- An incident report can be written as soon as the author is confident in the root cause; a shared
  postmortem waits for the internal one. With automation and practice, a shareable version costs about
  10% extra work plus review.
- The post does NOT discuss apologies. Apology vs explanation in b3 is taught as a judgement call with
  the disagreement shown, sourced as reported (vendor and comms blogs).

### Diataxis, "How-to guides" URL https://diataxis.fr/how-to-guides/
- A how-to guide serves "the work of the already-competent user"; it is goal-oriented, a sequence of
  actions, with no digression, explanation or teaching. Used only in the one-card anatomy recap (a1),
  which links tech-writing 93 for the full treatment.

### danluu/post-mortems (GitHub, README "A List of Post-mortems!")
URL https://github.com/danluu/post-mortems
- Structure and metadata only: entries grouped under Config Errors, Hardware/Power Failures,
  Conflicts, Time, Database, Uncategorized, plus other lists and analysis. Each entry is a company name
  linked to its write-up and a one-to-three sentence summary. Config errors is the largest named group
  (about 60 entries, counted by the lead; "about"). No licence is stated: quote nothing, link only.
  Used in b2 (the reading club) and a5 (a corpus is tagged by condition).

### incident.io blog, "Why do post-mortem action items fail?" (2026-04-16, vendor)
URL https://incident.io/blog/why-do-post-mortem-action-items-fail-how-to-make-incident-follow-ups-actually-get-done
- Vendor view (Self-study tier): five reasons actions fail: no individual owner, kept in the wrong
  place (the doc, not the team's tracker), vague wording, no follow-up cadence, systemic problems
  framed as technical tasks. No measured rates are given; quote no numbers from it.

## Reported (could not be read at source on 2026-11-11)

- John Allspaw, "Blameless PostMortems and a Just Culture", Etsy Code as Craft, 2012 (403 to the
  fetcher). Reported: engineers give detailed accounts without fear of punishment; accountability
  means giving that account. Paraphrase only.
- Sidney Dekker, The Field Guide to Understanding Human Error (book): old view vs new view;
  counterfactuals ("should have") describe a world that did not happen; hindsight bias. Reported
  (the old/new view framing is also cited on the PagerDuty blameless page, read at source).
- Learning from Incidents community (learningfromincidents.io; SSL failed): reported as a community
  of practitioners writing on incident analysis beyond root cause. Self-study link only.
- Atlassian incident handbook, postmortems (page body did not load). Atlassian's approver model and
  SLOs for priority actions are NOT used; nothing from it is quoted.
- Jeli (now part of PagerDuty) writing on incident analysis: not read; Self-study mention only.

## Contested, taught as disagreement

- Stale page vs no page (b1, a2): the workbook records teams that keep entries general so they change
  slowly versus step-by-step entries; some teams argue a stale page is worse than none because it is
  trusted. The bench trap t1 shows both sides: deleting stale pages lowers the share that misleads
  and raises alerts with no page.
- Root cause vs contributing conditions: PagerDuty and Dekker (reported) favour conditions; many
  templates still carry a root cause field. a4 links reliability a4 rather than re-arguing it.
- Apology vs explanation in a public note (b3): practitioner guidance disagrees on how early to
  apologise and how much to explain; legal review pulls toward less. Teach the trade-off.
- The 3x MTTR figure: Google's own experience, stated without method. Use as reported experience.

## The bench (computed in the browser, assets/rbp-live.js; reference materials/rbp_reference.py)

Constructed Pellmoor library: 38 runbooks across 5 systems (customer app 8, pricing feed 7, order
pipeline 8, warehouse picking 8, finance warehouse 7); 31 paging alerts, 25 bound to a page and 6 with
no page; 23 pages owned; 36 system changes over one 13-week quarter; one ad hoc game day in week 6
drilling 3 pages. Corpus: 11 postmortems over 52 weeks, 46 actions. Two repeat incidents: PM-09 (pick
lists missing again, week 36) repeats PM-03 through action PM-03.2; PM-11 (wrong prices shown to
customers for 3 hours, week 47) repeats PM-04 through action PM-04.1. Drift rate per change is
SIMULATED (default 30%), labelled on the widget.

Model, in words: a change that touches a page breaks one of its steps with the drift probability. An
owner reading a page (inventory, week 0) or reviewing it after a change catches a broken step 90% of
the time if the page is linter-clean and 40% if it is not (simulated, shipped rolls). A drill catches
every broken step on the page. A page misleads if it ends the quarter with any broken step. An action
is done only if it has an owner, a date and a clear definition of done; with a chase cadence it closes
at the first chase after its effort; without one it closes when history says it did, or never.
Auto-close marks an action closed at its due date without the work: closure rises, repeats do not fall.

python vs node: materials/compare-ladder.py, 2099 values, 0 differences, planted fault caught
(2026-11-11). Linter: 9 rules, 18 unit tests (one passing and one failing sample per rule) pass.

### Canon (default drift 30%)

| Rung | Misleading | Share | Alerts no page | No owner | Drill coverage | Broke a step | Wishes | Closed | Done | Median open age | Repeats |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R0 As found | 25 of 38 | 66% | 6 of 31 | 15 | 3 of 25 (12%) | 18 | 18 of 46 | 13 of 46 (28%) | 13 | 24 weeks | 2 of 2 |
| R1 Inventory + owners | 23 of 44 | 52% | 0 of 31 | 0 | 3 of 31 (10%) | 20 | 18 of 46 | 13 of 46 (28%) | 13 | 24 weeks | 2 of 2 |
| R2 Linter-clean rewrites | 18 of 44 | 41% | 0 of 31 | 0 | 3 of 31 (10%) | 20 | 0 of 46 | 13 of 46 (28%) | 13 | 24 weeks | 2 of 2 |
| R3 Change-triggered review | 6 of 44 | 14% | 0 of 31 | 0 | 3 of 31 (10%) | 20 | 0 of 46 | 13 of 46 (28%) | 13 | 24 weeks | 2 of 2 |
| R4 Drill rota | 2 of 44 | 5% | 0 of 31 | 0 | 31 of 31 (100%) | 20 | 0 of 46 | 13 of 46 (28%) | 13 | 24 weeks | 2 of 2 |
| R5 Action chase | 2 of 44 | 5% | 0 of 31 | 0 | 31 of 31 (100%) | 20 | 0 of 46 | 44 of 46 (96%) | 44 | 5 weeks | 0 of 2 |
| T1 Delete the stale pages | 10 of 22 | 45% | 14 of 31 | 1 | 3 of 17 (18%) | 9 | 18 of 46 | 13 of 46 (28%) | 13 | 24 weeks | 2 of 2 |
| T2 Auto-close at the due date | 18 of 44 | 41% | 0 of 31 | 0 | 3 of 31 (10%) | 20 | 0 of 46 | 46 of 46 (100%) | 13 | 0 weeks | 2 of 2 |

T1 also prints "Pages deleted by the trap: 16". R1 adds the 6 new pages (44 in the library).
Why R4 stops at 2: the drill rota covers paged pages only; the 2 that still mislead are unpaged pages
nobody drills (teaching point: coverage is of paged pages). R1-R4 do not move the corpus at all: an
owner and a date do not close an action; R5's chase does (teaching point for b4).

Learner moves (also in canon): m1 drift 50% with the full ladder: 2 of 44, 29 changes broke a step,
closed 44 of 46, repeats 0 of 2. m2 drill every 4 weeks with no change-triggered review: 6 of 44 (14%).
m3 chase every week with owners but no rewrites: closed 21 of 46 (46%), repeats 2 of 2 (wishes never
close). m4 review on with no owners: 20 of 38 (53%).

### Widget-printed lines (quote verbatim; nothing else)

Headline: "<n> of <N> pages would mislead at 2 a.m. (<p>%)". Stats lines: "Paging alerts with no page:
x of 31", "Pages with no owner: x", "Drill coverage: x of y paged pages drilled this quarter (z%)",
"System changes that broke a step: x (simulated drift 30%)", "Actions still written as wishes (no
clear done): x of 46", "Actions closed: x of 46 (y%) · really done: z", "Median age of open actions:
x weeks", "Repeat incidents traceable to an open action: x of 2", and on T1 "Pages deleted by the
trap: 16". Corpus table: per postmortem, week, conditions tagged, "d of t" actions done; repeat
badges "repeat: PM-03.2 still open" / "repeat avoided: PM-03.2 done in time".

Corpus facts the table prints (as found): condition "silent job failure" is tagged on PM-02, PM-03,
PM-08, PM-09 and PM-10 (5 of 11); "stale runbook step" on PM-03, PM-04, PM-07, PM-09 (4 of 11);
"unvalidated supplier input" on PM-04 and PM-11.

### Linter canon (the four Pellmoor samples)

- s1 RB-07 checkout runbook, as found: "Runbook · 0 of 5 rules pass · score 0 · 8 findings";
  judgement lines 4, 7, 10; no confirm line 5; no expected output lines 6, 9; owner line 1; time line 8.
- s2 RB-07 rewritten: "Runbook · 5 of 5 rules pass · score 100 · 0 findings".
- s3 PM-11 pricing-feed postmortem, first draft: "Postmortem · 0 of 6 rules pass · score 0 · 11
  findings"; owner line 1; time lines 5, 6, 7; blame lines 6, 13; counterfactual line 13; wishes
  lines 16, 17, 18; impact line 9.
- s4 PM-11 team version: "Postmortem · 6 of 6 rules pass · score 100 · 0 findings".
- The linter is a rule engine, not a judge of truth: a page can score 100 and still be wrong (it
  drifted). That is why a3 says a drill is the only test. Say this on every page that shows a score.

## Per-session coverage

Writer
- a1 Count what you have: inventory fields (owner, last verified, alert bound, last drilled); four
  states (true, stale, orphaned, missing); one-card anatomy recap linking tech-writing 93 and
  reliability b4; SRE workbook "each alert should have a corresponding playbook entry"; bench library
  R0 then R1. Artifact: library inventory.
- a2 Where pages go stale: workbook "go out of date at the same rate as production environment
  changes"; change-triggered vs calendar review; linter rules judge, confirm, expected; contested
  general vs step-by-step; build-along rewrite s1 to s2 on the linter, then library R2 to R3.
  Artifact: one rewritten runbook.
- a3 A drill is the only test: Wheel of Misfortune (SRE book), training only through playbooks as an
  anti-pattern, timing a newcomer, what a failed step teaches; drill rota for 31 paged pages in one
  quarter; bench R3 to R4, m2. Artifact: drill log.
- a4 From record to write-up: opens from IR b7's close-out record; team postmortem: UTC timeline,
  impact as numbers, contributing conditions, actions as owner + date; SRE book triggers; PagerDuty
  deadlines; workbook bad vs good; linter s3 to s4. Artifact: team postmortem.
- a5 Read eleven postmortems as one: tagging conditions; the repeat incident; wishes vs actions;
  workbook's repository analysed for trends; danluu index grouped by condition type (structure only);
  corpus table, find PM-09 and PM-11. Artifact: cross-incident read.
- a6 The docs kit on the bench: whole ladder R0-R5, traps T1 and T2, drift slider; capstone.

Leader
- b1 Which docs must exist: docs standard (every paging alert has a page, a severity line for
  postmortems, one owner per page and per postmortem); SRE book triggers; PagerDuty Sev-1/Sev-2 and
  3 days / 5 business days; contested stale vs no page with T1; links cyber a6. Artifact: docs standard.
- b2 The review that people come to: no postmortem unreviewed; PagerDuty meeting (24 hours ahead,
  facilitator speaks little, agenda); reading clubs, postmortem of the month, Wheel of Misfortune;
  reading club built on the danluu index (link only). Artifact: review ritual.
- b3 Writing for the customer: CRE shared postmortems (redaction, error budget, timing, about 10%
  extra work); one incident, three versions; apology vs explanation (contested, reported); Pellmoor
  PM-11 public note; linter s4 as the team base. Artifact: public postmortem.
- b4 Actions that close: Treynor Sloss line; single owner; tracked as bugs; closure rate, median age;
  incident.io's five reasons (vendor, Self-study); bench R4 vs R5 vs T2. Artifact: follow-through report.

## Seams (link out with absolute https; never reteach)

- Single runbook anatomy, tired reader, binding one alert: https://phoebefu6.github.io/learn-data-reliability-with-phoebe/ (b4)
- Runbook as a Diataxis how-to: https://phoebefu6.github.io/learn-tech-writing-with-phoebe/ (93), sentence craft (02, 03)
- What a postmortem may conclude, blameless entry condition: learn-data-reliability a4
- Generated incident package: learn-data-reliability b6
- Live response and close-out record: https://phoebefu6.github.io/learn-data-incident-response-with-phoebe/ (b7 hands off here)
- First hour of a security incident: https://phoebefu6.github.io/learn-cyber-security-with-phoebe/ (a6)
- Diagram syntax: https://phoebefu6.github.io/learn-mermaid-with-phoebe/ (s5)

## Not covered (honest list)

Vendor tool walkthroughs (PagerDuty, incident.io, Confluence, Notion templates): Self-study only.
Runbook automation (executable runbooks) beyond one sentence. Incident command and live response
(IR course). Security incident and breach notification rules (cyber, privacy courses). Legal advice on
public statements. Formal accident models (STAMP, FRAM) beyond a mention. Any measured industry base
rate for runbook staleness: none found at source, so every library rate is constructed or simulated.

## Citation appendix (use this form on coverage rows)

- Google, Site Reliability Engineering (2016), ch. 15 "Postmortem Culture", sre.google, read at source
- Google, Site Reliability Engineering (2016), Introduction, sre.google, read at source
- Google, Site Reliability Engineering (2016), "Accelerating SREs to On-Call and Beyond", sre.google, read at source
- Google, The Site Reliability Workbook (2018), ch. 10 "Postmortem Culture", sre.google, read at source
- Google, The Site Reliability Workbook (2018), "On-Call", sre.google, read at source
- PagerDuty, Postmortem guide (Apache 2.0), docs.pagerduty.com, read at source 2026-11-11
- Hilton and Stockman, "Fearless shared postmortems", Google Cloud blog, 2017, read at source
- Diataxis, "How-to guides", diataxis.fr, read at source
- danluu/post-mortems, GitHub index, structure read at source, no licence stated
- incident.io, "Why do post-mortem action items fail?", 2026, vendor blog, read at source
- Allspaw, "Blameless PostMortems and a Just Culture", Etsy, 2012, reported
- Dekker, The Field Guide to Understanding Human Error, book, reported

### Exact cross-link URLs
- https://phoebefu6.github.io/learn-data-reliability-with-phoebe/courses/b4-runbooks.html
- https://phoebefu6.github.io/learn-data-reliability-with-phoebe/courses/a4-postmortems.html
- https://phoebefu6.github.io/learn-data-reliability-with-phoebe/courses/b6-incident-package.html
- https://phoebefu6.github.io/learn-tech-writing-with-phoebe/courses/93-runbooks.html
- https://phoebefu6.github.io/learn-tech-writing-with-phoebe/courses/02-sentences-that-work.html
- https://phoebefu6.github.io/learn-tech-writing-with-phoebe/courses/03-structure-readers-scan.html
- https://phoebefu6.github.io/learn-data-incident-response-with-phoebe/courses/b7-close-with-evidence.html
- https://phoebefu6.github.io/learn-cyber-security-with-phoebe/courses/a6-first-hour.html
- https://phoebefu6.github.io/learn-mermaid-with-phoebe/courses/05-plans-and-people.html

## Fan-out notes (2026-11-11)

- a3 uses per-system paged-page counts (customer app 7, pricing feed 7, order pipeline 8, warehouse
  picking 5, finance warehouse 4 = 31) read from assets/rbp-sample.js and labelled constructed; the
  quarterly rota (5 weeks of 3 drills, 8 weeks of 2) matches the engine's drill schedule.
- NP-1 renamed "Feed row count drop" (was "Price outlier against last feed", which contradicted the
  s4 condition "No alert watched for a price jump"). Action texts written by hand per postmortem;
  canon unchanged (2099 values re-compared).
- b3: a customer note with no Impact/Timeline/Actions heading is linted as a runbook; with them,
  the owner and wish rules misfit a public note. The page says so in words and quotes no score.
- b4 paraphrases Goodhart's law without citation.
