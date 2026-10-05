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

- **Tools:** Claude Code (agent mode in VS Code). I used it to read the starter code, refactor the logic, write tests, and fill in the documentation.
- **Correct suggestion:** Claude Code suggested moving `check_guess`, `parse_guess`, `get_range_for_difficulty` and `update_score` into `logic_utils.py`, swapping the reversed hint messages, and deleting the `str(secret)` conversion on even attempts. That was correct because the root cause was in the logic and the string conversion made the comparison string-based. I verified it with pytest (`check_guess(60, 50)` returns "Too High" with a "LOWER" hint, and `check_guess(9, 50)` returns "Too Low"). I still need to confirm the hints in the live game with `streamlit run app.py`.
- **Suggestion not accepted as written:** The starter tests expected `check_guess` to return a plain string, while the function returns an `(outcome, message)` pair that `app.py` unpacks. Changing the function to match the tests would have broken the app, so I kept the tuple and rewrote the tests to unpack it. I also did not keep the AI's original `try/except TypeError` string-comparison fallback in `check_guess`. It hid the real bug instead of fixing it. I verified my version by running pytest and confirming all tests pass.

---

## 3. Debugging and testing your fixes

- **How I decided a bug was fixed:** I reproduced it first using the Bug Reproduction Log above, then re-ran the same input after the fix and checked that the expected result appeared. For logic bugs I also required a pytest case that failed before the fix and passed after.
- **Test that showed something:** `test_check_guess_compares_numbers_not_strings` checks that a guess of 9 against a secret of 50 returns "Too Low". Compared as strings, "9" > "50", so this is exactly the wrong answer the even-attempt bug produced. `test_guess_too_high` checks that 60 vs. 50 returns "Too High" with a "LOWER" hint. All 7 tests pass with `pytest`.
- **AI and tests:** Claude Code wrote the test cases and pointed out that the starter tests compared a tuple to a string, which is why they could never pass as written. I reviewed each test to make sure it targeted a specific bug.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the whole script from top to bottom every time you click a button or type in a box, so ordinary variables are reset on each run. `st.session_state` is a dictionary that survives those reruns, so anything that has to persist, like the secret number, attempts, score and history, belongs there and should only be created when it is missing. The original bugs came from mishandling this: values were reset or changed on a rerun when they should have been kept (and the New Game reset missed some of the stored values).

---

## 5. Looking ahead: your developer habits

- **Habit to reuse:** Writing a small reproduction log and a failing test before fixing, so I can prove each fix worked.
- **Do differently next time:** Give the AI one bug per chat with the relevant files attached, and review the diff of every file it touches before accepting it.
- **How this changed my view of AI code:** AI-generated code can look complete and still contain subtle bugs, such as a swapped hint or a hidden type conversion, so I need to test and read it instead of trusting it.
