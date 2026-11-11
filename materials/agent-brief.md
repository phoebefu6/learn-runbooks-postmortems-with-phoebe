# Agent brief - shared by every fan-out page of learn-runbooks-postmortems-with-phoebe

Internal build document, filled from course-builder/references/agent-brief.template.md on
2026-11-11. Never link it from an audience page.

You are writing ONE static HTML session page. No servers, no npm. **If your target file already
exists on disk, do not write it; report that and stop.** Write the file, return its path and one
line of coverage, plus (a) any source you read that the course map lacks and (b) anything that
contradicts another page. No HTML in your reply.

## Read first, in this order

1. The template page for YOUR track. Copy its structure, classes, SVG grammar and quiz markup
   EXACTLY, including how many options each question has (4, lettered "A · ", "B · ", ...):
   - Writer: `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-runbooks-postmortems-with-phoebe/courses/a1-count-what-you-have.html`
   - Leader: `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-runbooks-postmortems-with-phoebe/courses/b1-which-docs-must-exist.html`
   Skim the bench page for the full widget and its printed lines:
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-runbooks-postmortems-with-phoebe/courses/a6-the-docs-kit-on-the-bench.html`
2. The source map: every verified number, its evidence tier, per-session coverage, the seams, and
   the exact lines each widget prints. Use ONLY its numbers; never invent a statistic; if a fact is
   missing, teach the uncertainty.
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-runbooks-postmortems-with-phoebe/materials/official-course-map.md`
3. The stylesheet `:root` block for the palette tokens (first 30 lines):
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-runbooks-postmortems-with-phoebe/assets/style.css`

## Page skeleton (keep every component)

toolbar (crumb EXACTLY `<a href="../index.html">learn-runbooks-postmortems-with-phoebe</a> / Writer
session N of 6` or `... / Leader session N of 4`, #toggle-all, #zoom-toggle) · masthead (eyebrow
"Learn Runbooks &amp; Postmortems with Phoebe · Writer session N of 6" or "· Leader session N of 4",
h1 "Title: <span class="accent">short accent phrase</span>", .sub, .chip-row with the level chip
"🟡 Writer" (a2, a3), "🟠 Writer" (a4, a5), "🟡 Leader" (b2), "🟠 Leader" (b3), "🔴 Leader" (b4),
plus the two audience chips and the time chip exactly as your template, .agenda a1-a4) · main.wrap ·
section#intro (Part 0 "Where we start": kicker, .lede, .legend pills as the template,
.callout.win "★ What you walk out with tonight.") · 3 Parts, each `section.section#part-N` with
section-kicker (klabel "Part N · covers ...", h2, `.tag.concept "N min live"`), a `.lede`, ONE
figure, `details.card` accordions (summary: `.mode.live` or `.mode.self`, title, `.mini`,
`.caret ▶`), at least one `.callout.example` with `span.ex-pill` "Real world" on the page ·
section#demo-1 Build-along (kicker `.tag.demo "★ 22 min · everyone builds"` on Writer pages,
`"★ 22 min · everyone works it through"` on Leader pages, .lede, the widget if your outline names
one, ONE figure, `.steps > .step`, each with a `.prompt-box.good` carrying a `span.label`) ·
section#exercise Homework (ol, 4 items) · section#quiz (3 x `.quiz-q data-answer="0-based"`,
`p.qtext`, 4 `button.qopt` "A · ...", `p.qwhy`; one `p.quiz-score` after the last; vary the correct
letter across the three) · section#official, h2 EXACTLY "What this session teaches, and where it
came from", `.covered > .covered-row` (pill solid ✓ / light ◐ + name + note), then the `.mono` line
EXACTLY "Every fact on this page, and its verification tier, is recorded in the course's source
map." · section.cheat#cheatsheet (h3 "Writer session N cheat sheet <span>· pin this</span>" or
"Leader session N cheat sheet ...", .grid-2 of six .cheat-item) · `.callout.next` with `.nx-pill`
"Next session" · footer.pagefoot · scripts.

Head: the template's social meta block with this page's own title/description/url;
`<title>Writer session N · <Title> - learn runbooks and postmortems with phoebe</title>` (or Leader);
`<link rel="stylesheet" href="../assets/style.css?v=1">`. Nothing else external.
Scripts at the end, exactly as the templates: `../assets/rbp-sample.js?v=1`, `../assets/rbp-live.js?v=1`,
`../assets/app.js?v=1` (keep all three even if the page has no widget).
The widget: `<div class="rbp-widget" data-mode="MODE" data-rung="RUNG" data-sample="SAMPLE"></div>`
right after the build-along .lede, before its figure. MODE is `library`, `linter`, `corpus` or `bench`
(bench = both tabs; add `data-tab="library"` to open on the Library tab). RUNG is r0-r5, t1, t2.
SAMPLE is s1 (RB-07 as found), s2 (RB-07 rewritten), s3 (PM-11 first draft), s4 (PM-11 team version).
Learners change rungs by clicking the ladder buttons; samples via the sample dropdown; levers by
checkboxes, two selects (drill rota: none / once a quarter / every 6 weeks / every 4 weeks; action
chase: nobody chases / every 4 weeks / every 2 weeks / every week) and the drift slider.

First `details.card` in the FIRST Part is `open`; no other. Sentence case headings. Warm
practitioner voice, concrete, never dry. Inside prompt-boxes escape `&` `<` `>`. 450 to 650 lines
is guidance about depth, never a target: never collapse whitespace, dissolve a list into a
paragraph, or drop a component to fit.

## Hard rules (a violation is rework)

- NEVER an em dash or en dash, anywhere (prose, code, aria-labels, comments). Hyphen only.
- No meta text: never "this course", "in this course", "the course teaches", "banned here". State
  the professional norm directly with its reason. The two exact estate phrases above are the only
  self-references; "Writer session 5" cross-references are fine.
- Attribution "by Phoebe Fu". Never "built with" a tool.
- Every number comes from the map or is labelled constructed. Widget numbers: quote ONLY the lines
  listed under "Widget-printed lines", "Canon" and "Linter canon" in the map, verbatim, for the rung
  or sample named. If you want a number the widget does not print, do not use it. Constructed
  arithmetic you invent for a prompt-box (a drill rota schedule, a three-version note) must be
  labelled constructed and checked.
- The linter checks SHAPE, not truth: any page that shows a score says so.
- Contested or missing evidence: teach the disagreement; never resolve what the literature has not.
  The 3x MTTR figure is Google's own reported experience. Stale page vs no page, apology vs
  explanation, root cause vs contributing conditions are contested.
- Citations in the exact form of the map's appendix; anything marked reported is "reported".
  Quote at most ONE short phrase (under 15 words) from any source per page, with attribution.
  Never quote or summarise another company's public postmortem; the danluu index is linked,
  never quoted. No vendor named with a percentage.
- NEVER "lottery" or "lotteries"; say the mechanism.
- Default to the English word. No Chinese terms needed here.
- Titles, widget ids and class names must not collide with siblings. Do not reuse these sibling
  titles: "Postmortems that change something", "Runbooks a tired person can follow", "The incident
  package", "Ready before the next one", "Close with evidence", "What the record hands the
  write-up", "The first hour", "Anatomy of a runbook", "Runbooks and ops docs", "Blameless is the
  entry condition", "Three sections, generated not remembered", "Contributing conditions, not a
  root cause", "One runbook per page, kept true by being used", "The reader is tired, new, and
  holding a phone". Do not invent new CSS classes; use the template's classes only (inline
  style attributes are allowed sparingly, as the templates do).
- Running case: Pellmoor, a constructed same-day online grocer (customer app, pricing feed from
  suppliers, order pipeline, warehouse picking, finance warehouse). Say "Constructed Pellmoor
  example" for every Pellmoor story. Never Phoebe's employers, clients or projects. Never these
  names: Quarrybank, Harborlight, Halyard, Brightwater, Lumina, Marina, Himalaya, Fernhollow,
  Beacon, Tidewell, Callwell, Saltbox, Northwick, Cadence, Kettle, Marchmont, Pulse.
- People in Pellmoor stories are roles ("the pricing on-call", "the payments lead"), never names,
  except where a page shows the linter catching a named person in the s3 sample (Priya appears
  only inside that sample text, as the thing the rule flags).

## Figure grammar (hand-drawn, every figure)

Palette, ONLY these hexes (no invented greys): ink `#1E1A2E` · muted `#57526E` · accent `#281E51`
· accent-deep `#1A1338` · accent-mid `#3F3378` · accent-soft `#BDB7DC` · accent-50 `#EFEDF7` ·
faint `#CBC7DA` · hairline `#E6E3EF` · highlighter (contrast) `#FFE45C` · highlighter-ink `#6B5600`
· highlighter-50 `#FFF8D1` · `#FFFFFF` · universal reds `#991B1B` `#FEF2F2` `#FCA5A5` only for a
wrong-way or missing panel.

- `<figure class="zoomable">` > `<svg viewBox="0 0 880 H" xmlns="http://www.w3.org/2000/svg" role="img"
  aria-label="the data, not the shape">` > `<defs>` + `<style>` + content, then
  `<figcaption>🔍 Click to zoom - takeaway</figcaption>`. Grow H, never W.
- Prefix unique per figure, used for every class and id: `<page id><letter>`, e.g. `a2a`, `a2b`,
  `a2c`, `a2d`. Never reuse another page's prefix.
- `<defs>` holds three things with the figure prefix P: a wobble filter `id="PSk"`
  (`feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="<int>"` +
  `feDisplacementMap scale="2.4" xChannelSelector="R" yChannelSelector="G"`, `x="-3%" y="-3%"
  width="106%" height="106%"`), a hachure pattern `id="PHc"` (7x7 userSpaceOnUse, rotate(-38), one
  `#281E51` line, opacity .5), an open arrowhead `id="PAr"` (path `M1 1 L9 5 L1 9`, fill none,
  `#1E1A2E` stroke 1.6). ALL shapes sit inside ONE `<g filter="url(#PSk)" fill="none"
  stroke="#1E1A2E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">`; rects carry a
  tiny rotation (-4 to 4 degrees for hand-placed items, under 1 for panels). Fills: white,
  accent-50, the hachure for "the pile" or "the data", accent `#281E51` for a dark box carrying white
  text, and the highlighter `#FFE45C` ONLY for the one thing the figure is about (a stale step, a
  failing rule, an open action). One doodle anchor per figure, simple strokes, never a mascot.
- Text classes (copy the template's `<style>` lines): `.PH` 800 12px ink heading · `.PL` 600 12px
  ink label · `.PS` 400 11px muted · `.PB` 800 11px highlighter-ink `#6B5600` · `.PV` 800 18px
  accent-deep value · `.PW` 800 12px white, ONLY on an `#281E51` or `#1A1338` fill (never on yellow) ·
  `.PN` 400 12px muted note. Text on the yellow highlighter fill is ink (`.PH`/`.PL`) only.
- Text over a hachure fill sits on a white rect placed OUTSIDE the filtered group.
- ALL `<text>` outside any filtered group, sans stack, never below 10.5px.
- Fit: max chars ≈ (box width - 20) / 7 at 12px, 6.4px/char at 11px; full-width note under 110
  chars; 40px between neighbouring point labels; bottom note 22px below the last row, H clears it by
  8px. No path may cross a text label (the gate flags line-through-text). Hand-stacked items must
  not overlap as painted rects (the gate flags a pile). When in doubt, shorten.
- Floor: one figure per Part plus one in the build-along. Draw the MECHANISM (the step that drifted
  from the system it describes, the alert with no page behind it, the action item that never closed
  and the repeat incident it let through, the drill timing a newcomer step by step, one incident
  rewritten for three readers), never a metaphor literally, never decoration.

## Voice and honesty

Every Part gets a real-world story: a read-at-source fact from the map where one exists, otherwise a
constructed Pellmoor story labelled "Constructed Pellmoor example". Pellmoor numbers a widget prints
are quoted from the map's canon; other Pellmoor numbers are constructed and say so. One-doc anatomy is
never retaught: link the sibling pages listed below.

## Cross-links (absolute URLs)

- Single runbook anatomy, one alert: https://phoebefu6.github.io/learn-data-reliability-with-phoebe/courses/b4-runbooks.html
- What a postmortem may conclude, blameless entry condition: https://phoebefu6.github.io/learn-data-reliability-with-phoebe/courses/a4-postmortems.html
- Generated incident package: https://phoebefu6.github.io/learn-data-reliability-with-phoebe/courses/b6-incident-package.html
- Runbook as a Diataxis how-to: https://phoebefu6.github.io/learn-tech-writing-with-phoebe/courses/93-runbooks.html
- Sentences, scanning: https://phoebefu6.github.io/learn-tech-writing-with-phoebe/courses/02-sentences-that-work.html ; https://phoebefu6.github.io/learn-tech-writing-with-phoebe/courses/03-structure-readers-scan.html
- The close-out record that hands off to a4: https://phoebefu6.github.io/learn-data-incident-response-with-phoebe/courses/b7-close-with-evidence.html
- Security incident first hour: https://phoebefu6.github.io/learn-cyber-security-with-phoebe/courses/a6-first-hour.html
- Diagram syntax: https://phoebefu6.github.io/learn-mermaid-with-phoebe/courses/05-plans-and-people.html
- Public postmortem index (link only, quote nothing): https://github.com/danluu/post-mortems
- Hub: https://phoebefu6.github.io/learn-with-phoebe/

## Footer chains and session titles

Writer: a1 Count what you have → a2 Where pages go stale → a3 A drill is the only test → a4 From
record to write-up → a5 Read eleven postmortems as one → a6 The docs kit on the bench.
Leader: b1 Which docs must exist → b2 The review that people come to → b3 Writing for the customer →
b4 Actions that close (b4's right side: "← Prev: Writing for the customer" and "Course home").
Files: a2-where-pages-go-stale.html, a3-a-drill-is-the-only-test.html, a4-from-record-to-write-up.html,
a5-read-eleven-postmortems-as-one.html, b2-the-review-people-come-to.html,
b3-writing-for-the-customer.html, b4-actions-that-close.html.
Footer left: "Writer session N of 6 · learn-runbooks-postmortems-with-phoebe · by Phoebe Fu
&nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a>"
Footer right: `<a href="PREV">← Prev: <title></a> &nbsp;·&nbsp; <a href="NEXT">Next: <title> →</a>`.

Session titles (exact, sentence case, one accent span in h1): as above.
