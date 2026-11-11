// Run the browser engine (assets/rbp-live.js) in node on the shipped sample and print the canon as
// JSON, in the same shape as materials/rbp_reference.py --json. Usage: node materials/rbp-node.js <repo>
const fs = require("fs"), path = require("path"), vm = require("vm");
const repo = process.argv[2] || path.join(__dirname, "..");
const ctx = { console };
ctx.window = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(repo, "assets/rbp-sample.js"), "utf8"), ctx);
vm.runInContext(fs.readFileSync(path.join(repo, "assets/rbp-live.js"), "utf8"), ctx);
const R = ctx.RBP, S = ctx.RBP_SAMPLE, T = ctx.RBP_SAMPLES;
function one([rid, name, o]) { const r = JSON.parse(JSON.stringify(R.run(S, o))); r.rung = rid; r.name = name; return r; }
const lint = {};
Object.keys(T).forEach(k => { lint[k] = JSON.parse(JSON.stringify(R.lint(T[k].text))); });
console.log(JSON.stringify({ ladder: R.PRESETS.map(one), traps: R.TRAPS.map(one), moves: R.MOVES.map(one), lint }, null, 1));
