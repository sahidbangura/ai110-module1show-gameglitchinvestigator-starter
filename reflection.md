# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran it, the game looked normal: a difficulty selector, a text box, and a Submit button. It was unplayable once I started guessing. The hints sent me the wrong way, they were sometimes inconsistent from one guess to the next, and New Game did not fully reset the round. Code locations below refer to the original, unfixed `app.py` (line numbers as they were before my edits).

**Bugs, with input/trigger, expected vs. actual, and code-level cause**

1. **Reversed hints.** Trigger: guess 60 when the secret is 50. Expected: "Too High" with a hint to go LOWER. Actual: "Too High" with "Go HIGHER!", and the reverse for low guesses. Cause: the return messages in `check_guess` (`app.py` lines 37-40) are swapped.
2. **Secret turns into a string on even attempts.** Trigger: submit a guess on attempt 2, 4, 6... Expected: every guess is compared as int vs. int. Actual: the hint is wrong or inconsistent on every other guess. Cause: in the submit block (`app.py` lines 158-161) the secret is converted with `str(...)` when `attempts % 2 == 0`, so `check_guess` falls into its `TypeError` branch and compares strings (`app.py` lines 41-47).
3. **New Game does not reset the game or respect difficulty.** Trigger: win or lose, then click New Game, or pick Easy and click New Game. Expected: a fresh round with score, history and status cleared, and a secret in the selected range (1-20 on Easy). Actual: the status stays "won"/"lost", so the game stays locked at "Game over", the score and history carry over, and the secret can be up to 100. Cause: the `if new_game:` block (`app.py` lines 134-138) only resets `attempts` and calls `random.randint(1, 100)`.
4. **Wrong range text and off-by-one attempts.** Trigger: select Easy and look at the banner. Expected: "between 1 and 20" and the full attempt allowance. Actual: always "between 1 and 100", and "Attempts left" is one too low at the start. Cause: the hardcoded text in `st.info` (`app.py` lines 109-112) and `attempts` initialised to 1 (`app.py` line 96).
5. **Hard is easier than Normal.** Trigger: select Hard. Expected: a harder, wider range than Normal. Actual: 1-50, narrower than Normal's 1-100. Cause: `get_range_for_difficulty` (`app.py` lines 9-10).

**Terminal trace of the starter code (commit f651d72), secret = 50**

I ran the starter's own functions with the same secret conversion the Submit block applied (secret becomes a string on even attempts). In the live game I saw the same wrong hints, e.g. "Go HIGHER!" after guessing above the secret.

```
== Starter code, Normal difficulty, secret = 50 ==
range for Hard: (1, 50) | range for Normal: (1, 100)
attempt 1: guess 60 vs secret 50 (int) -> Too High | 📈 Go HIGHER!
attempt 2: guess 40 vs secret '50' (str) -> Too Low | 📉 Go LOWER!
attempt 3: guess 60 vs secret 50 (int) -> Too High | 📈 Go HIGHER!
attempt 4: guess 9 vs secret '50' (str) -> Too High | 📈 Go HIGHER!
score after Win on attempt 1: 80
score after Too High on attempt 2: 5
parse_guess("3.7") -> (True, 3, None)
```

What this shows: both hints are backwards (60 vs 50 says HIGHER; 40 vs 50 says LOWER); on attempt 4 a guess of 9 is called "Too High" against 50 because "9" > "50" as strings; a wrong "Too High" guess on an even attempt *adds* 5 points; a win on attempt 1 scores 80 instead of 90; and 3.7 is silently truncated to 3.

**Bug Reproduction Log**

| Input Used | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|------------|-------------------|-----------------|------------------------|-------------------------|
| Guess 60, secret 50 | "Too High" outcome with a "Go LOWER!" hint | "Too High" outcome with "📈 Go HIGHER!" hint | none | `app.py`, `check_guess` (lines 37-40) |
| Guess 40, secret 50 | "Too Low" outcome with a "Go HIGHER!" hint | "Too Low" outcome with "📉 Go LOWER!" hint | none | `app.py`, `check_guess` (lines 37-40) |
| Any guess on attempt 2 (or any even attempt) | Hint based on int-vs-int comparison | Secret is converted to a string, so the comparison is string-based and the hint can be wrong (e.g. guess 9 vs. secret "50" reads as higher) | none (the `TypeError` is silently caught) | `app.py`, submit block (lines 158-161) and `check_guess` `except TypeError` (lines 41-47) |
| Win or lose, then click New Game | New round: score 0, history cleared, status "playing" | "You already won" / "Game over" still shown and the game stays locked; old score and history remain | none | `app.py`, `if new_game:` block (lines 134-138) |
| Difficulty Easy (range 1-20), click New Game | Secret between 1 and 20 | Secret can be up to 100; banner still says "1 and 100" | none | `app.py`, `new_game` block (line 136) and `st.info` (lines 109-112) |
| Difficulty Hard | Range larger than Normal's 1-100 | Range is 1-50 | none | `app.py`, `get_range_for_difficulty` (lines 9-10) |

---

## 2. How did you use AI as a teammate?

- **Tool:** I used Claude Code inside VS Code. I had it read the starter code, move the logic into `logic_utils.py`, write tests, and help me fill in the docs.
- **AI explanation of a bug:** I asked why the hints were so inconsistent. Claude Code found that `app.py` turned the secret into a string on every even attempt, so `check_guess` fell into its `except TypeError` branch and compared strings. As strings, `"9" > "50"`, so a guess of 9 came back "Too High". It also noticed the hint messages were swapped, which was a second, separate bug. I checked both by running the starter functions myself (the trace above matches).
- **Suggestion that was correct:** Claude Code suggested moving the four logic functions into `logic_utils.py`, swapping the hint messages, and deleting the `str(secret)` conversion. That was right because the problem lived in the logic, not the UI. I confirmed it with pytest: 60 vs. 50 gives "Too High" with a "LOWER" hint, and 9 vs. 50 gives "Too Low".
- **Suggestion I did not accept as written:** The starter tests expected `check_guess` to return a plain string, but the app unpacks an `(outcome, message)` pair. Changing the function to fit the tests would have broken the game, so I kept the tuple and rewrote the tests instead. I also dropped the old `try/except TypeError` string fallback, because it hid the real bug. I checked this by running pytest and playing a round.

---

## 3. Debugging and testing your fixes

- **How I knew a bug was fixed:** I reproduced it first (the table and trace in section 1), then ran the same input after the fix. For logic bugs I also wanted a pytest case that would have caught it.
- **A test that taught me something:** `test_check_guess_compares_numbers_not_strings` checks that 9 vs. 50 returns "Too Low". It is the exact case the even-attempt bug got wrong, so it proves that fix. I also added 24 edge-case tests for negative numbers, decimals, huge values and blank input. All 31 tests pass.
- **AI and tests:** Claude Code wrote the tests and pointed out that the starter tests compared a tuple to a string, so they could never pass as written. I read each test to make sure it targeted one specific bug.

---

## 4. What did you learn about Streamlit and state?

Every time you click a button or type in a box, Streamlit runs your whole script again from the top, so normal variables start over each time. `st.session_state` is like a notebook that survives those reruns, so anything that has to stick around, like the secret number, attempts and score, goes in there and is only created when it is missing. A few of my bugs came from this: some values were reset or changed on a rerun when they should have been kept, and New Game forgot to clear everything it stored.

---

## 5. Looking ahead: your developer habits

- **A habit I'll reuse:** Writing down exactly how to reproduce a bug before touching the code, then adding a test for it. It made it obvious when a fix really worked.
- **What I'd do differently:** Give the AI one bug at a time with the right files attached, and read the diff of every file it changes before accepting it.
- **How this changed my view of AI code:** AI-generated code can look finished and still hide small bugs, like a swapped message or a quiet type conversion, so I need to run it and test it instead of trusting it.
