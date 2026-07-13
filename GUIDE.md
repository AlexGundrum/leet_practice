# AlgoRep — Guide

## TLDR: what's actually in this repo now

AlgoRep started as a static drill site (`index.html` + `worker.js` + `algorithms.json`, Pyodide in the browser, `localStorage`) and is now a small local FastAPI app (`server.py`) with all state in flat JSON files under `data/`. Launch it with `AlgoRep.bat`, or `python -m uvicorn server:app --port 8000`. Nothing here talks to the internet except the CDN-hosted Pyodide/CodeMirror scripts and, optionally, Gmail for the pacing reminder.

**The atomic drill library** (`algorithms.json`) is now **87 entries**. The original 73 cover the standard interview-pattern curriculum (binary search, graphs, trees, DP, backtracking, etc.). 14 new hard-difficulty entries were added specifically to close the gap between "good at interviews" and "elite at contests": Fenwick tree, segment tree, sparse table, Z-function, Manacher's algorithm, digit DP, bitmask DP (Held-Karp TSP), matrix exponentiation, modular combinatorics, binary lifting, meet-in-the-middle, Rabin-Karp rolling hash, a binary trie for max-XOR-pair problems, and a 2D difference array. Every one of these was actually executed and cross-checked against brute force (and, for a few, 100–200 iteration randomized stress tests) before being written in — not just reasoned through.

**Smart Playlist topic grouping** was quietly broken for 61 of the original 73 entries (a narrow anchored regex meant most DP, backtracking, heap, and string-algorithm drills never got grouped into any topic bucket). It's been rebuilt as a verified token-classifier covering all 87 entries with zero misclassifications — see `TOPIC_CATEGORIES` in `js/app.js`.

**A "Path to Top 1%" curriculum playlist** (`data/playlists.json`) sequences all 26 hard-difficulty drills (the 14 new ones plus 12 pre-existing hard entries) in a deliberate order — data structures → string algorithms → number theory → advanced DP → advanced techniques → remaining hard polish. It's a normal custom playlist, so PB mode's Prev/Next buttons walk it in that exact order.

**The contest reflection loop** (new, `view-log-contest` → `view-generate-prompt` → `view-import-grading`): after a real LeetCode contest, capture every problem — title, patterns, every submission's code with your own comments, the failing test if any, your narrative of what you were actually thinking, and (new) **how many minutes it took you to solve**. The next day (deliberately delayed — see the spacing-effect note in the app itself), generate a rubric+data prompt, paste it into an external AI, and paste the JSON response back in. That import fans out into:
- a **per-category Elo rating** (`api/elo_engine.py`) blending your objective performance (solved/unsolved, submission count, and now your actual captured solve time vs. a difficulty-based expectation) with the AI's assessment of your thinking process, updated via a standard Elo expected-vs-actual formula
- **generalized flashcards** (retrieval-practice pattern-recognition cards)
- **edge-case drills** (quick-recall quizzes on what you actually missed)
- **specimen problem proposals** — specific non-atomic problems worth remembering, which you explicitly approve or reject into a separate curated library, keeping the atomic library pure

**Spaced repetition** (`api/srs_engine.py`) uses textbook SM-2 for flashcards and a simpler doubling scheme for edge cases. As of this batch, due-card selection is **mastery-weighted**: a card scheduled less than 21 days out (14 for edge cases) always shows when due; past that, its odds of appearing in a given session shrink smoothly the more "over-mastered" it is, floored at 15% so nothing fully vanishes. Well-known material gets out of your way without ever fully disappearing.

**A Recommended Practice Session** view pulls your single weakest Elo category and assembles matching atomic drills, relevant specimens, and due flashcards/edge-cases into one mixed session — interleaved, not blocked.

**A pacing reminder** (`scripts/pacing_reminder.py`) reads your logged contest dates and, if you're behind a tunable day-of-week threshold (default: 3/week), emails you via Gmail SMTP. It's a standalone script meant to be run daily via Windows Task Scheduler, independent of whether the app is open — see the docstring at the top of that file for setup.

**Known limitations, honestly:** this tool only covers the DSA/contest axis of interview prep — nothing here tracks system design or behavioral prep. Contest attendance is logged manually (no LeetCode API polling). See the "What this tool doesn't do" section below before you assume full coverage.

---

## How to actually use this to get great at competitive programming

### The weekly skeleton

You're doing 3 contests/week. Structure the week around that:

- **Contest day.** Do the real contest on leetcode.com. Immediately after, open **Log Contest** and capture everything while it's fresh: every problem, every submission's code with your own inline comments on what you were thinking, the failing test if one existed, your narrative (what you tried first, where you got stuck, what made you change approach), and your best estimate of how many minutes each problem actually took. Do **not** generate the grading prompt yet — that's tomorrow, on purpose. This capture step alone satisfies your weekly pacing.
- **Next day.** Generate the grading prompt, paste it into Claude/ChatGPT/whatever you use, paste the returned JSON into Import. Review the critique. Approve or reject any specimen proposals — be stingy; the point of that library is that everything in it is genuinely worth remembering, not everything you happened to solve. Then immediately do the **Recommended Practice Session** it just unlocked.
- **Non-contest days.** Open the app, clear Flashcards and Edge Case Drills first — they're due-gated and mastery-weighted now, so this is a genuinely fast 5–10 minutes, not a chore. Then work the **Path to Top 1%** curriculum playlist in order via PB mode, or pull from Smart Playlists if you want to target a specific topic.

### How to use the curriculum playlist specifically

Go in order — don't cherry-pick the ones that sound fun. For each entry: attempt it for real before opening "Insights & Solution." That panel is available immediately, and nothing currently stops you from peeking early, which defeats the entire point — treat the temptation to peek as a discipline problem, not a missing feature. Read the `when_to_use` note *after* you've genuinely attempted the problem, not before. If you solve one comfortably under a reasonable contest-pace time with no hints, don't linger — that's a real signal you already had it, move on.

### How to log time-to-solve honestly

Estimate it as accurately as you can, even roughly — "about 20 minutes" is far more useful to the Elo model than leaving it blank. A blank time is treated as neutral (neither helps nor hurts your rating for that problem); an honest number is what lets a fast clean solve on a hard problem actually move your rating up, and what lets a slow grind — even one you eventually solved — correctly flag that category as needing work.

### How to read the Dashboard without fooling yourself

Check it maybe twice a week, not daily. The number that matters is the **trend line**, not the absolute rating — a category climbing steadily from a low base is a better sign than a static high one. If the same category keeps coming up as your Recommended Session target three weeks running, that's a signal to stop drilling it blind and go actually study it from a reference source for an hour first. Grinding a pattern you don't fundamentally understand yet just builds fast, wrong instincts.

### The single most important discipline this tool can't enforce for you

Every practice mode here — Smart Playlists, the curriculum, even Recommended Session — tells you the pattern before you start. That trains execution of a known technique, not the harder skill that actually separates strong-but-not-elite competitors from the top tier: **cold pattern recognition from a bare problem statement**. Periodically, deliberately practice against this tool's grain: pick a random drill from the Problem Set list without reading its title bucket, cover the title, and force yourself to identify the pattern from the description alone before you look at anything else. This is more valuable than any new algorithm content and nothing here automates it for you yet.

### What this tool doesn't do — don't let it create false confidence

No system design practice. No behavioral-round tracking. No mock-interview / talk-out-loud simulation — contest problems are silent and timed, but real interview loops require narrating your thought process live, which is a distinct skill this tool never exercises. If your FAANG prep timeline includes those loops, they need a separate deliberate practice plan; this tool solving the DSA axis well doesn't mean the whole interview is covered.

### A short list of things worth adding later, in rough priority order

Rolling hash, XOR trie, and 2D difference arrays are now covered; string hashing's sibling techniques (suffix array/automaton), coordinate compression, sqrt decomposition, Mo's algorithm, network flow, and lazy-propagation segment trees remain real gaps if you want to keep extending the hard set. On the process side: a "blind drill" mode (pattern hidden until you commit to an approach) would be the highest-leverage single addition, followed by extending spaced repetition to the atomic drill library itself, not just flashcards.
