#Day 5 notes

##My topic and intended user

The agent answers a guitar player's questions about how guitars are built (neck construction, tonewoods, bracing, pickups, bridges, hollow vs. solid bodies, etc.), using only local knowledge files.

##Why I can evaluate this topic quickly

I play guitar and already know the basics of lutherie, so I can tell if the agent's answer is accurate, incomplete, or invented.

##Best one-file answer

"What's the difference between bolt-on and set-neck construction?" — answered correctly from neck_construction.md alone, with an accurate supporting quote.

##Best multi-file answer

"I want a bright guitar with easy string bending — what tonewood, scale length, and bridge type would work?" — the agent correctly pulled from tonewoods.md, fretboard_scale.md,bridge_types.md, and also setup_intonation.md.

##What the agent correctly refused to answer

"What's the current market price of a mahogany guitar body?" — the agent read index.md and tonewoods.md, confirmed no file contains pricing data, and said so directly instead of guessing a number.

##Contradicting-files test: did it read both files, or stop at the first?

Initially it stopped at finishing.md only and did not read tonewoods.md, even after I added a contradicting line to tonewoods.md about finish and tone. The problem was that index.md's description for tonewoods.md didn't mention that content, so the agent had no reason to open it. After updating the index description to reflect the new content, it now reads both files.

##Token usage I observed (shortest turn vs. a multi-document turn)

Shortest: 494 tokens (a simple hello). Longest: 13121 tokens (for the question meant to trigger the tool call overusage).

##What happened when I forced the tool-call budget to trigger

The agent told me the budget was exceeded and to try a narrower question.

##One stale, ambiguous, or adversarial test case

Ambiguous: "How do I fix the buzzing?" — the agent initially picked one interpretation (fret buzz) and answered fully. After altering the system prompt, it asked a further question about the source of the buzzing.

##One prompt or index change I made after testing

Updated index.md's description for tonewoods.md to mention the finish-vs-tone note, since the agent skipped that file on a relevant question due to the description not covering it. Also slightly altered the system prompt in order to tell the agent to ask follow-ups instead of asuming anything.

##What I would build next

A helper function that, given a new .md file, sends its contents to the model and asks it to generate a one-line description in the same style as the existing index.md rows. 