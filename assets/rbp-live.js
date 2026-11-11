/* rbp-live.js - the Docs bench for learn-runbooks-postmortems-with-phoebe.
   Two engines, both computed in your browser:
     RBP.lint(text)          a real rule engine for runbooks and postmortems (9 rules)
     RBP.run(sample, opts)   Pellmoor's library over one quarter and its corpus over one year
   Constructed Pellmoor example. The drift rate is a SIMULATED parameter, labelled on the widget.
   materials/rbp_reference.py is an independent Python copy that must print the same numbers.
   Widget: <div class="rbp-widget" data-mode="library|linter|corpus|bench" data-rung="r0" data-sample="s1"></div> */
(function () {
  "use strict";

  /* ------------------------------------------------------------ linter */
  var JUDGE = ["check if", "check whether", "as appropriate", "as needed", "if needed", "if necessary", "investigate",
    "use your judgement", "use your judgment", "looks ok", "look ok", "looks high", "looks wrong",
    "looks normal", "make sure everything"];
  var ACT = /^(restart|run|scale|set|delete|drop|fail over|failover|roll back|rollback|deploy|purge|disable|enable|drain|kill|clear|flush|switch|re-run|rerun|replay|apply|reboot|stop|start)\b/i;
  var CONFIRM = /\b(confirm|expect|expected|you should see|verify that)\b/i;
  var STEP = /^\s*(\d+)[.)]\s+(.*)$/;
  var HEAD = /^\s*#/;
  var CMD = /^\s*\$\s+\S/;
  var EXPECTED = /^\s*expected?:/i;
  var OWNER = /^\s*owner:\s*\S/i;
  var VERIFIED = /^\s*last (verified|updated):\s*\S/i;
  var RELATIVE = /\b(yesterday|this morning|last night|tonight|earlier today|later that day|a few minutes later|shortly after|around noon)\b/i;
  var CLOCK = /\b([01]?\d|2[0-3]):[0-5]\d(:[0-5]\d)?(?!\s*(UTC|Z)\b)(?![:\d])/;
  var AMPM = /\b\d{1,2}(:\d\d)?\s?(am|pm)\b/i;
  var BLAMEW = /\b(careless|carelessly|human error|fault of|his fault|her fault|their fault|negligent|sloppy|mistake by|to blame)\b/i;
  var NAMED = /\b([A-Z][a-z]+) (pushed|deployed|forgot|missed|broke|ignored|changed|ran|deleted|merged|failed)\b/g;
  var NOT_NAMES = ["The", "We", "It", "A", "An", "This", "That", "Someone", "Nobody", "Everyone", "Team", "Pellmoor",
    "Supplier", "Pricing", "Finance", "Orders", "Picking", "Automation", "Validator", "Feed", "Job",
    "Scheduler", "Deploy", "Who", "Which", "Nothing", "Anyone"];
  var COUNTER = /\b(should have|should've|could have|would have|if only|failed to|ought to have)\b/i;
  var PM_HEAD = /^\s*#+\s*(impact|timeline|actions|action items)\b/i;
  var SEC = /^\s*#+\s*(.*)$/;
  var DATE = /\b\d{4}-\d{2}-\d{2}\b/;
  var OWNER_IN = /owner:\s*\S/i;
  var BULLET = /^\s*[-*]\s+\S/;

  var RULES = [
    ["judge", "Step needs judgement", "runbook", "A step that asks the reader to judge (\"check if\", \"as appropriate\", \"investigate\") hands the decision to the most tired person in the building. Name the reading and the threshold."],
    ["confirm", "Action with no confirm step", "runbook", "Every action needs a way to tell it worked. Without a confirm line, the reader moves on after a restart that did nothing."],
    ["expected", "Command with no expected output", "runbook", "A command with no expected output cannot be checked, by the reader at 2 a.m. or by the reviewer who should notice it drifted."],
    ["owner", "No owner or last-verified line", "both", "Without an owner and a last-verified (or last-updated) date, nobody answers for the page and the reader cannot tell how old it is."],
    ["time", "Relative or non-UTC timestamp", "both", "\"Yesterday\" and a clock time with no zone stop meaning anything once the document is read in another place or another week. Write UTC."],
    ["blame", "Blame language or a named person", "postmortem", "Blame words, or a person's name as the subject of a mistake, make the next account less honest. Name the role and the condition."],
    ["counter", "Counterfactual (\"should have\")", "postmortem", "\"Should have\" describes a world that did not happen. Describe what people saw and why their action made sense at the time."],
    ["wish", "Action without owner and date", "postmortem", "An action with no owner and no date is a wish. Wishes do not get done, and the incident they would have prevented comes back."],
    ["impact", "Impact with no number", "postmortem", "Impact without a number cannot be compared or prioritised. Count customers, orders, products, minutes or money."]
  ];

  function docType(lines) {
    for (var i = 0; i < lines.length; i++) if (PM_HEAD.test(lines[i])) return "postmortem";
    return "runbook";
  }
  function sections(lines) {
    var cur = "", out = [];
    lines.forEach(function (l) { var m = l.match(SEC); if (m) cur = m[1].trim().toLowerCase(); out.push(cur); });
    return out;
  }
  function lint(text) {
    var lines = String(text).split("\n");
    var kind = docType(lines), sec = sections(lines), f = {};
    RULES.forEach(function (r) { f[r[0]] = []; });
    var blocks = [], cur = null;
    lines.forEach(function (l, i) {
      if (HEAD.test(l)) { cur = null; return; }
      if (STEP.test(l)) { cur = [i]; blocks.push(cur); }
      else if (cur !== null) cur.push(i);
    });
    if (kind === "runbook") {
      blocks.forEach(function (b) {
        var body = lines[b[0]].match(STEP)[2], low = body.toLowerCase();
        if (JUDGE.some(function (p) { return low.indexOf(p) !== -1; })) f.judge.push(b[0] + 1);
        if (ACT.test(body) && !b.some(function (j) { return CONFIRM.test(lines[j]); })) f.confirm.push(b[0] + 1);
        b.forEach(function (j, k) {
          if (CMD.test(lines[j])) {
            var nxt = b.slice(k + 1).map(function (x) { return lines[x]; }).filter(function (x) { return x.trim(); }).slice(0, 2);
            if (!nxt.some(function (x) { return EXPECTED.test(x); })) f.expected.push(j + 1);
          }
        });
      });
    }
    if (!(lines.some(function (l) { return OWNER.test(l); }) && lines.some(function (l) { return VERIFIED.test(l); }))) f.owner.push(1);
    lines.forEach(function (l, i) { if (RELATIVE.test(l) || CLOCK.test(l) || AMPM.test(l)) f.time.push(i + 1); });
    if (kind === "postmortem") {
      lines.forEach(function (l, i) {
        var named = false, m;
        NAMED.lastIndex = 0;
        while ((m = NAMED.exec(l)) !== null) { if (NOT_NAMES.indexOf(m[1]) === -1) named = true; }
        if (BLAMEW.test(l) || named) f.blame.push(i + 1);
        if (COUNTER.test(l)) f.counter.push(i + 1);
        if (sec[i].indexOf("action") === 0 && BULLET.test(l) && !(OWNER_IN.test(l) && DATE.test(l))) f.wish.push(i + 1);
      });
      var imp = [];
      lines.forEach(function (l, i) { if (SEC.test(l) && sec[i].indexOf("impact") === 0) imp.push(i); });
      if (!imp.length) f.impact.push(1);
      else {
        var body = lines.filter(function (l, i) { return sec[i].indexOf("impact") === 0 && !SEC.test(l); });
        if (!body.some(function (l) { return /\d/.test(l); })) f.impact.push(imp[0] + 1);
      }
    }
    var rows = RULES.map(function (r) {
      var applies = r[2] === "both" || r[2] === kind;
      return { id: r[0], name: r[1], applies: applies, lines: applies ? f[r[0]] : [] };
    });
    var app = rows.filter(function (r) { return r.applies; });
    var passed = app.filter(function (r) { return !r.lines.length; }).length;
    var findings = app.reduce(function (s, r) { return s + r.lines.length; }, 0);
    return { kind: kind, rules: rows, passed: passed, applicable: app.length, findings: findings,
      score: Math.round(100 * passed / app.length) };
  }

  /* ------------------------------------------------------------ library + corpus model */
  var DEFAULTS = { owners: false, rewrite: false, review: false, drill: 0, chase: 0, drift: 30, deleteStale: false, autoClose: false };
  function median(xs) {
    if (!xs.length) return 0;
    var s = xs.slice().sort(function (a, b) { return a - b; }), n = s.length;
    return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
  }
  function run(S, opts) {
    var o = {}, k;
    for (k in DEFAULTS) o[k] = DEFAULTS[k];
    for (k in (opts || {})) o[k] = opts[k];
    var P = S.pages, n = P.length, i;
    var active = P.map(function (p) { return !p.isNew || !!o.owners; });
    if (o.deleteStale) active = active.map(function (a, i) { return a && !(!P[i].isNew && P[i].age > 365); });
    var owned = P.map(function (p, i) { return active[i] && !!(p.owned || o.owners || p.isNew); });
    var clean = owned.map(function (w) { return w && !!o.rewrite; });
    var thr = clean.map(function (c) { return c ? 900 : 400; });
    var wrong = P.map(function (p, i) { return active[i] ? p.wrong.slice() : []; });
    var caught = 0;
    if (o.owners || o.rewrite) {
      for (i = 0; i < n; i++) if (owned[i]) {
        var keep = wrong[i].filter(function (u) { return u >= thr[i]; });
        caught += wrong[i].length - keep.length; wrong[i] = keep;
      }
    }
    var drillable = [];
    for (i = 0; i < n; i++) if (active[i] && owned[i] && P[i].alert) drillable.push(i);
    var plan = {};
    if (o.drill) drillable.forEach(function (pi, kk) {
      for (var w = 1 + (kk % o.drill); w <= S.meta.weeks; w += o.drill) (plan[w] = plan[w] || []).push(pi);
    });
    var drilled = P.map(function () { return false; }), drills = 0, drifted = 0;
    for (var wk = 1; wk <= S.meta.weeks; wk++) {
      S.changes.forEach(function (c) {
        if (c.wk !== wk) return;
        c.touch.forEach(function (t) {
          var pi = t[0], ud = t[1], uc = t[2];
          if (!active[pi] || ud >= o.drift * 10) return;
          drifted++;
          if (o.review && owned[pi] && uc < thr[pi]) caught++;
          else wrong[pi].push(uc);
        });
      });
      var todo = (plan[wk] || []).slice();
      if (wk === 6) S.gameday.forEach(function (gi) { if (active[gi]) todo.push(gi); });
      todo.forEach(function (pi) { drilled[pi] = true; drills++; wrong[pi] = []; });
    }
    var actIdx = [], bound = [];
    for (i = 0; i < n; i++) if (active[i]) { actIdx.push(i); if (P[i].alert) bound.push(i); }
    var mis = actIdx.filter(function (i) { return wrong[i].length > 0; }).length;
    var states = P.map(function (p, i) {
      if (!active[i]) return p.alert ? "missing" : "deleted";
      if (wrong[i].length) return "stale";
      if (!owned[i]) return "orphaned";
      return "true";
    });
    var drilledBound = bound.filter(function (i) { return drilled[i]; }).length;
    var lib = {
      pages: actIdx.length, misleading: mis, share: actIdx.length ? Math.round(100 * mis / actIdx.length) : 0,
      alertsTotal: P.reduce(function (s, p) { return s + p.alert; }, 0),
      alertsNoPage: P.filter(function (p, i) { return p.alert && !active[i]; }).length,
      orphaned: actIdx.filter(function (i) { return !owned[i]; }).length,
      boundPages: bound.length, drilledBound: drilledBound,
      drillCoverage: bound.length ? Math.round(100 * drilledBound / bound.length) : 0,
      drills: drills, drifted: drifted, caughtByReview: caught,
      wrongSteps: actIdx.reduce(function (s, i) { return s + wrong[i].length; }, 0), states: states,
      deleted: P.filter(function (p, i) { return !p.isNew && !active[i]; }).length
    };
    var Y = S.meta.yearWeeks, A = S.actions, done = [], marked = [];
    A.forEach(function (a) {
      var hasOwner = a.owner || o.owners, hasDue = a.due || o.rewrite, wish = a.wish && !o.rewrite;
      var proper = hasOwner && hasDue && !wish, d = null;
      if (proper) {
        var t = a.wk + a.effort;
        if (o.chase) d = Math.ceil(t / o.chase) * o.chase;
        else if (a.neglect !== null) d = t + a.neglect;
      }
      if (d !== null && d > Y) d = null;
      var mk = d;
      if (o.autoClose && hasDue && a.wk + 4 <= Y) mk = mk === null ? a.wk + 4 : Math.min(mk, a.wk + 4);
      done.push(d); marked.push(mk);
    });
    var closed = marked.filter(function (m) { return m !== null; }).length;
    var ages = [];
    A.forEach(function (a, j) { if (marked[j] === null) ages.push(Y - a.wk); });
    var repeats = [];
    S.pms.forEach(function (pm) {
      if (!pm.repeatOf) return;
      var j = A.findIndex(function (a) { return a.id === pm.repeatOf; });
      if (done[j] === null || done[j] >= pm.wk) repeats.push(pm.id);
    });
    var cor = {
      actions: A.length, closed: closed, closure: Math.round(100 * closed / A.length),
      reallyDone: done.filter(function (d) { return d !== null; }).length, open: ages.length, medianOpenAge: median(ages),
      wishes: A.filter(function (a) { return a.wish && !o.rewrite; }).length,
      repeats: repeats.length, repeatIds: repeats, repeatsPossible: S.pms.filter(function (p) { return p.repeatOf; }).length,
      done: done, marked: marked
    };
    return { library: lib, corpus: cor };
  }

  var PRESETS = [
    ["r0", "As found", {}],
    ["r1", "Inventory + owners", { owners: true }],
    ["r2", "Linter-clean rewrites", { owners: true, rewrite: true }],
    ["r3", "Change-triggered review", { owners: true, rewrite: true, review: true }],
    ["r4", "Drill rota", { owners: true, rewrite: true, review: true, drill: 13 }],
    ["r5", "Action chase", { owners: true, rewrite: true, review: true, drill: 13, chase: 2 }]
  ];
  var TRAPS = [
    ["t1", "Delete the stale pages", { deleteStale: true }],
    ["t2", "Auto-close at the due date", { owners: true, rewrite: true, autoClose: true }]
  ];
  var MOVES = [
    ["m1", "Drift 50, full ladder", { owners: true, rewrite: true, review: true, drill: 13, chase: 2, drift: 50 }],
    ["m2", "Drill monthly, no review", { owners: true, rewrite: true, drill: 4 }],
    ["m3", "Chase weekly, no rewrites", { owners: true, chase: 1 }],
    ["m4", "Review on, no owners", { review: true }]
  ];

  window.RBP = { lint: lint, run: run, RULES: RULES, DEFAULTS: DEFAULTS, PRESETS: PRESETS, TRAPS: TRAPS, MOVES: MOVES };

  /* ------------------------------------------------------------ widget */
  if (typeof document === "undefined") return;
  var SAMPLES = window.RBP_SAMPLES || {};
  function h(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function findRung(id) {
    var all = PRESETS.concat(TRAPS);
    for (var i = 0; i < all.length; i++) if (all[i][0] === id) return all[i];
    return null;
  }
  var registry = [];

  function buildLinter(root, sampleId) {
    var box = h("div", "rbp-pane rbp-linter");
    box.appendChild(h("p", "rbp-clabel", "Linter · paste or edit a runbook or a postmortem"));
    var bar = h("div", "rbp-bar");
    var sel = h("select", "rbp-select"); sel.setAttribute("aria-label", "Load a Pellmoor sample");
    Object.keys(SAMPLES).forEach(function (k) { var op = h("option", null, SAMPLES[k].label); op.value = k; sel.appendChild(op); });
    bar.appendChild(sel);
    box.appendChild(bar);
    var ta = h("textarea", "rbp-text"); ta.setAttribute("aria-label", "Document to lint"); ta.spellcheck = false; ta.rows = 14;
    box.appendChild(ta);
    var head = h("p", "rbp-lhead"), list = h("div", "rbp-rules");
    box.appendChild(head); box.appendChild(list);
    function paint() {
      var r = lint(ta.value);
      head.textContent = (r.kind === "runbook" ? "Runbook" : "Postmortem") + " · " + r.passed + " of " + r.applicable +
        " rules pass · score " + r.score + " · " + r.findings + (r.findings === 1 ? " finding" : " findings");
      list.innerHTML = "";
      r.rules.forEach(function (row, i) {
        var d = h("div", "rbp-rule " + (!row.applies ? "is-na" : row.lines.length ? "is-fail" : "is-pass"));
        var top = h("div", "rbp-rtop");
        top.appendChild(h("span", "rbp-rstat", !row.applies ? "n/a" : row.lines.length ? "fails" : "passes"));
        top.appendChild(h("b", null, row.name));
        top.appendChild(h("span", "rbp-rlines", !row.applies ? (RULES[i][2] === "runbook" ? "runbooks only" : "postmortems only")
          : row.lines.length ? "line" + (row.lines.length > 1 ? "s " : " ") + row.lines.join(", ") : "clean"));
        d.appendChild(top);
        d.appendChild(h("p", "rbp-rwhy", RULES[i][3]));
        list.appendChild(d);
      });
      root.dataset.lintScore = r.score;
    }
    sel.addEventListener("change", function () { ta.value = SAMPLES[sel.value].text; paint(); });
    ta.addEventListener("input", paint);
    var first = SAMPLES[sampleId] ? sampleId : Object.keys(SAMPLES)[0];
    if (first) { sel.value = first; ta.value = SAMPLES[first].text; }
    paint();
    return { el: box, setSample: function (id) { if (SAMPLES[id]) { sel.value = id; ta.value = SAMPLES[id].text; paint(); } },
      lint: function () { return lint(ta.value); } };
  }

  function buildLibrary(root, rungId, mode) {
    var S = window.RBP_SAMPLE;
    var box = h("div", "rbp-pane rbp-library");
    box.appendChild(h("p", "rbp-clabel", "Ladder · each rung adds one practice to the one before"));
    var ladder = h("div", "rbp-ladder");
    var btns = {};
    PRESETS.concat(TRAPS).forEach(function (p) {
      var b = h("button", "rbp-rung" + (p[0].charAt(0) === "t" ? " rbp-trap" : "")); b.type = "button";
      b.appendChild(h("b", null, p[0].toUpperCase())); b.appendChild(document.createTextNode(" " + p[1]));
      b.addEventListener("click", function () { setRung(p[0]); });
      btns[p[0]] = b; ladder.appendChild(b);
    });
    box.appendChild(ladder);
    var lev = h("div", "rbp-levers");
    function check(key, label) {
      var l = h("label", "rbp-lever" + (key === "deleteStale" || key === "autoClose" ? " rbp-lever-trap" : ""));
      var c = h("input"); c.type = "checkbox"; c.dataset.key = key;
      l.appendChild(c); l.appendChild(h("span", null, label)); lev.appendChild(l);
      c.addEventListener("change", function () { state[key] = c.checked; current = null; paint(); });
      return c;
    }
    function pick(key, label, opts) {
      var l = h("label", "rbp-lever"); l.appendChild(h("span", null, label));
      var s = h("select", "rbp-select"); s.dataset.key = key;
      opts.forEach(function (op) { var e = h("option", null, op[1]); e.value = op[0]; s.appendChild(e); });
      l.appendChild(s); lev.appendChild(l);
      s.addEventListener("change", function () { state[key] = parseInt(s.value, 10); current = null; paint(); });
      return s;
    }
    var ctl = {
      owners: check("owners", "Owners: every page and action gets a named owner; the 6 unpaged alerts get a page"),
      rewrite: check("rewrite", "Linter-clean rewrites: owned pages pass the linter; wishes become owner + date"),
      review: check("review", "Change-triggered review: a change that touches a page sends it to its owner"),
      drill: pick("drill", "Drill rota for paged pages", [["0", "none"], ["13", "once a quarter"], ["6", "every 6 weeks"], ["4", "every 4 weeks"]]),
      chase: pick("chase", "Action chase", [["0", "nobody chases"], ["4", "every 4 weeks"], ["2", "every 2 weeks"], ["1", "every week"]]),
      deleteStale: check("deleteStale", "Trap: delete every page not verified in a year"),
      autoClose: check("autoClose", "Trap: mark actions closed when their due date passes")
    };
    box.appendChild(lev);
    var dl = h("label", "rbp-drift");
    dl.appendChild(h("span", null, "Drift rate per system change (SIMULATED): "));
    var dr = h("input"); dr.type = "range"; dr.min = "0"; dr.max = "100"; dr.step = "5";
    dr.setAttribute("aria-label", "Simulated drift rate per system change, percent");
    var dv = h("b", null, "30%");
    dl.appendChild(dr); dl.appendChild(dv); box.appendChild(dl);
    dr.addEventListener("input", function () { state.drift = parseInt(dr.value, 10); current = null; paint(); });

    var head = h("div", "rbp-headline"), stats = h("ul", "rbp-stats");
    box.appendChild(head); box.appendChild(stats);
    var grid = h("div", "rbp-grid"); grid.setAttribute("aria-label", "Pellmoor's pages, coloured by state");
    var legend = h("div", "rbp-legend");
    [["true", "true"], ["stale", "would mislead"], ["orphaned", "no owner"], ["missing", "alert with no page"], ["deleted", "deleted"]].forEach(function (x) {
      var s = h("span", "rbp-lg"); s.appendChild(h("i", "rbp-tile is-" + x[0])); s.appendChild(document.createTextNode(x[1])); legend.appendChild(s);
    });
    var corpus = h("div", "rbp-corpus");
    if (mode !== "corpus") { box.appendChild(h("p", "rbp-clabel", "The library at the end of the quarter")); box.appendChild(grid); box.appendChild(legend); }
    box.appendChild(h("p", "rbp-clabel", "The corpus: 11 postmortems, 46 actions, one year"));
    box.appendChild(corpus);
    var state = {}, current = null;

    function setRung(id) {
      var p = findRung(id); if (!p) return;
      state = {}; for (var k in DEFAULTS) state[k] = DEFAULTS[k];
      for (k in p[2]) state[k] = p[2][k];
      current = id; paint();
    }
    function paint() {
      ctl.owners.checked = !!state.owners; ctl.rewrite.checked = !!state.rewrite; ctl.review.checked = !!state.review;
      ctl.deleteStale.checked = !!state.deleteStale; ctl.autoClose.checked = !!state.autoClose;
      ctl.drill.value = String(state.drill); ctl.chase.value = String(state.chase);
      dr.value = String(state.drift); dv.textContent = state.drift + "%";
      Object.keys(btns).forEach(function (k) { btns[k].classList.toggle("is-on", k === current); });
      var r = run(S, state), L = r.library, C = r.corpus;
      head.innerHTML = "";
      head.appendChild(h("b", null, L.misleading + " of " + L.pages));
      head.appendChild(h("span", null, " pages would mislead at 2 a.m. (" + L.share + "%)"));
      stats.innerHTML = "";
      [
        "Paging alerts with no page: " + L.alertsNoPage + " of " + L.alertsTotal,
        "Pages with no owner: " + L.orphaned,
        "Drill coverage: " + L.drilledBound + " of " + L.boundPages + " paged pages drilled this quarter (" + L.drillCoverage + "%)",
        "System changes that broke a step: " + L.drifted + " (simulated drift " + state.drift + "%)",
        "Actions still written as wishes (no clear done): " + C.wishes + " of " + C.actions,
        "Actions closed: " + C.closed + " of " + C.actions + " (" + C.closure + "%) · really done: " + C.reallyDone,
        "Median age of open actions: " + C.medianOpenAge + " weeks",
        "Repeat incidents traceable to an open action: " + C.repeats + " of " + C.repeatsPossible
      ].concat(L.deleted ? ["Pages deleted by the trap: " + L.deleted] : []).forEach(function (t) { stats.appendChild(h("li", null, t)); });
      grid.innerHTML = "";
      S.pages.forEach(function (p, i) {
        var st = L.states[i];
        var own = st !== "missing" && st !== "deleted" && !!(p.owned || state.owners || p.isNew);
        var t = h("span", "rbp-tile is-" + st + (own || st === "missing" || st === "deleted" ? "" : " is-noowner"), p.id);
        t.title = p.id + " " + p.title + " (" + S.meta.systems[p.sys] + "): " +
          { "true": "true", stale: "would mislead", orphaned: "no owner", missing: "paging alert with no page", deleted: "deleted" }[st] + (own || st === "missing" || st === "deleted" ? "" : ", no owner");
        grid.appendChild(t);
      });
      corpus.innerHTML = "";
      var tb = h("table", "clean rbp-ctable");
      var tr = h("tr"); ["Postmortem", "Week", "Conditions tagged", "Actions done"].forEach(function (x) { tr.appendChild(h("th", null, x)); });
      tb.appendChild(tr);
      S.pms.forEach(function (pm, pi) {
        var row = h("tr");
        var c1 = h("td"); c1.appendChild(h("b", null, pm.id + " ")); c1.appendChild(document.createTextNode("SEV" + pm.sev + " · " + pm.title));
        if (pm.repeatOf) {
          var rep = C.repeatIds.indexOf(pm.id) !== -1;
          c1.appendChild(h("span", "rbp-rep" + (rep ? " is-hit" : ""), rep ? "repeat: " + pm.repeatOf + " still open" : "repeat avoided: " + pm.repeatOf + " done in time"));
        }
        row.appendChild(c1); row.appendChild(h("td", null, String(pm.wk)));
        row.appendChild(h("td", null, pm.tags.join("; ")));
        var c4 = h("td"), dots = h("span", "rbp-dots"), nd = 0, nt = 0;
        S.actions.forEach(function (a, j) {
          if (a.pm !== pi) return; nt++;
          var cls = C.done[j] !== null ? "is-done" : C.marked[j] !== null ? "is-marked" : "is-open";
          if (C.done[j] !== null) nd++;
          var d = h("i", "rbp-dot " + cls); d.title = a.id + " " + a.text + (cls === "is-done" ? ": done" : cls === "is-marked" ? ": marked closed, not done" : ": open");
          dots.appendChild(d);
        });
        c4.appendChild(dots); c4.appendChild(document.createTextNode(" " + nd + " of " + nt));
        row.appendChild(c4); tb.appendChild(row);
      });
      corpus.appendChild(tb);
      root.dataset.rung = current || "custom";
      root.dataset.share = L.share;
    }
    setRung(findRung(rungId) ? rungId : "r0");
    return { el: box, setRung: setRung, set: function (o) { for (var k in o) state[k] = o[k]; current = null; paint(); },
      result: function () { return run(S, state); } };
  }

  function mount(root) {
    if (root.dataset.rbpMounted) return; root.dataset.rbpMounted = "1";
    var mode = root.dataset.mode || "bench";
    var w = h("div", "rbp-bench");
    var hd = h("div", "rbp-head");
    hd.appendChild(h("h4", null, mode === "linter" ? "Docs bench · linter" : mode === "library" ? "Docs bench · library" : mode === "corpus" ? "Docs bench · corpus" : "Docs bench"));
    hd.appendChild(h("p", "rbp-rail", "Constructed Pellmoor example. The rule engine is real and runs on any text you paste. The library is 38 constructed runbooks, 36 system changes in one quarter, 11 postmortems and 46 actions in one year; the drift rate is a simulated parameter you can move. Your numbers will differ on your own library."));
    w.appendChild(hd);
    var api = { root: root };
    var lin = null, lib = null;
    if (mode === "linter" || mode === "bench") lin = buildLinter(root, root.dataset.sample || "s1");
    if (mode !== "linter") lib = buildLibrary(root, root.dataset.rung || "r0", mode);
    if (lin && lib) {
      var tabs = h("div", "rbp-tabs");
      var t1 = h("button", "rbp-tab is-on", "Linter"), t2 = h("button", "rbp-tab", "Library");
      t1.type = t2.type = "button";
      tabs.appendChild(t1); tabs.appendChild(t2); w.appendChild(tabs);
      w.appendChild(lin.el); w.appendChild(lib.el); lib.el.hidden = true;
      var show = function (which) { lin.el.hidden = which !== "linter"; lib.el.hidden = which !== "library"; t1.classList.toggle("is-on", which === "linter"); t2.classList.toggle("is-on", which === "library"); };
      t1.addEventListener("click", function () { show("linter"); }); t2.addEventListener("click", function () { show("library"); });
      api.show = show;
      if (root.dataset.tab === "library") show("library");
    } else {
      w.appendChild((lin || lib).el);
    }
    root.appendChild(w);
    api.linter = lin; api.library = lib;
    registry.push(api);
  }
  function boot() { Array.prototype.forEach.call(document.querySelectorAll(".rbp-widget"), mount); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();

  window.RBP_BENCH = {
    widgets: registry,
    setRung: function (id, n) { registry.forEach(function (a, i) { if (a.library && (n == null || n === i)) a.library.setRung(id); }); },
    setSample: function (id, n) { registry.forEach(function (a, i) { if (a.linter && (n == null || n === i)) a.linter.setSample(id); }); },
    set: function (o, n) { registry.forEach(function (a, i) { if (a.library && (n == null || n === i)) a.library.set(o); }); }
  };
})();
