# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Purpose:** A Streamlit number-guessing game. The player picks a difficulty, guesses the secret number within a limited number of attempts, gets Higher/Lower hints, and earns a score.

**Bugs found**

- Hints were reversed ("Too High" said "Go HIGHER!").
- On every even attempt the secret was converted to a string, so comparisons were string-vs-int and gave wrong hints.
- Attempts started at 1, so "attempts left" was off by one and New Game set it inconsistently.
- New Game ignored the difficulty range (always 1-100) and did not reset score, status, or history, so a finished game stayed locked.
- The info banner always said "1 to 100" regardless of difficulty.
- Hard (1-50) was easier than Normal (1-100).
- Scoring rewarded wrong "Too High" guesses on even attempts and over-penalised wins (`attempt + 1`).
- Changing difficulty kept the old secret, which could be outside the new range.
- The "Attempts left" banner and debug panel were drawn before the submit logic ran, so they lagged one guess behind.

**Fixes applied**

- Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score` into `logic_utils.py`; `app.py` imports them.
- Corrected hint direction, removed the string-secret branch, made Hard 1-200.
- Added a single `start_new_game()` that resets secret, attempts, score, status, and history, used on first load, difficulty change, and New Game.
- Banner now uses the real range; attempts start at 0.
- Simplified scoring: wins score `100 - 10 * attempts` (min 10), wrong guesses -5.
- `parse_guess` now strips whitespace, rejects out-of-range numbers, non-whole decimals (3.7 used to become 3), and inf/nan, and invalid input no longer costs an attempt (Challenge 1).
- The banner and debug panel render after the submit logic, so they show current values.

## 📸 Demo Walkthrough

Sample game on **Normal** (range 1-100, 8 attempts). The secret is 63, visible in "Developer Debug Info".

1. The sidebar shows "Range: 1 to 100" and "Attempts allowed: 8"; the banner says "Guess a number between 1 and 100. Attempts left: 8", and the score is 0.
2. User enters a guess of **40** and clicks Submit. The game shows "📈 Go HIGHER!" (Too Low). Attempts left drops to 7 and the score becomes **-5**.
3. User enters **80**. The game shows "📉 Go LOWER!" (Too High). Attempts left is 6 and the score becomes **-10**.
4. User enters **abc** (or **-5**, **500**, **3.7**). The game shows an error ("That is not a number.", "Enter a number between 1 and 100.", "Enter a whole number.") and no hint is given. The invalid entry does not use up an attempt, so attempts left stays at 6.
5. User enters **63** on attempt 3. The game shows balloons and "You won! The secret was 63. Final score: 60" (win = 100 - 10 x 3 = 70 points, added to -10).
6. Further submits show "You already won. Start a new game to play again." Clicking **New Game** resets the score, attempts, history and status, and picks a new secret in the current difficulty's range.

If the player uses all 8 attempts without guessing the number, the game shows "Out of attempts!" with the secret and the final score, and locks until New Game is clicked.

## 🧪 Test Results

Includes Challenge 1 (advanced edge-case tests for negatives, decimals, huge/special values, blanks and boundaries).

```
$ pytest -v
collected 31 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  3%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [  6%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [  9%]
tests/test_game_logic.py::test_hard_range_is_wider_than_normal PASSED    [ 12%]
tests/test_game_logic.py::test_parse_guess_valid_and_invalid PASSED      [ 16%]
tests/test_game_logic.py::test_score_win_and_miss PASSED                 [ 19%]
tests/test_game_logic.py::test_check_guess_compares_numbers_not_strings PASSED [ 22%]
tests/test_game_logic.py::test_out_of_range_numbers_rejected[-5] PASSED  [ 25%]
tests/test_game_logic.py::test_out_of_range_numbers_rejected[0] PASSED   [ 29%]
tests/test_game_logic.py::test_out_of_range_numbers_rejected[-0] PASSED  [ 32%]
tests/test_game_logic.py::test_out_of_range_numbers_rejected[101] PASSED [ 35%]
tests/test_game_logic.py::test_out_of_range_numbers_rejected[99999999999999999999] PASSED [ 38%]
tests/test_game_logic.py::test_in_range_boundaries_and_whole_decimals_accepted[1] PASSED [ 41%]
tests/test_game_logic.py::test_in_range_boundaries_and_whole_decimals_accepted[100] PASSED [ 45%]
tests/test_game_logic.py::test_in_range_boundaries_and_whole_decimals_accepted[ 50 ] PASSED [ 48%]
tests/test_game_logic.py::test_in_range_boundaries_and_whole_decimals_accepted[5.0] PASSED [ 51%]
tests/test_game_logic.py::test_non_whole_decimals_rejected_not_truncated[3.7] PASSED [ 54%]
tests/test_game_logic.py::test_non_whole_decimals_rejected_not_truncated[0.5] PASSED [ 58%]
tests/test_game_logic.py::test_non_whole_decimals_rejected_not_truncated[-2.5] PASSED [ 61%]
tests/test_game_logic.py::test_non_numeric_and_special_values_rejected[1e999] PASSED [ 64%]
tests/test_game_logic.py::test_non_numeric_and_special_values_rejected[inf] PASSED [ 67%]
tests/test_game_logic.py::test_non_numeric_and_special_values_rejected[-inf] PASSED [ 70%]
tests/test_game_logic.py::test_non_numeric_and_special_values_rejected[nan] PASSED [ 74%]
tests/test_game_logic.py::test_non_numeric_and_special_values_rejected[1e3] PASSED [ 77%]
tests/test_game_logic.py::test_non_numeric_and_special_values_rejected[abc] PASSED [ 80%]
tests/test_game_logic.py::test_non_numeric_and_special_values_rejected[4 2] PASSED [ 83%]
tests/test_game_logic.py::test_non_numeric_and_special_values_rejected[--5] PASSED [ 87%]
tests/test_game_logic.py::test_blank_input_rejected[] PASSED             [ 90%]
tests/test_game_logic.py::test_blank_input_rejected[   ] PASSED          [ 93%]
tests/test_game_logic.py::test_blank_input_rejected[None] PASSED         [ 96%]
tests/test_game_logic.py::test_parse_guess_without_range_still_works PASSED [100%]
============================= 31 passed in 0.08s ==============================
```

## 🚀 Stretch Features

- [x] **Challenge 1: Advanced Edge-Case Testing.** 24 parametrized pytest cases in `tests/test_game_logic.py` cover negative numbers, zero, out-of-range and huge values, non-whole decimals, `inf`/`nan`, blanks and the range boundaries. `parse_guess` in `logic_utils.py` was hardened to pass them. Output is in Test Results above; prompts and rationale are in `ai_interactions.md`.
