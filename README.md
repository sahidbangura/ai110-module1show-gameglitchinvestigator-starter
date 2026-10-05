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

**Fixes applied**

- Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score` into `logic_utils.py`; `app.py` imports them.
- Corrected hint direction, removed the string-secret branch, made Hard 1-200.
- Added a single `start_new_game()` that resets secret, attempts, score, status, and history, used on first load, difficulty change, and New Game.
- Banner now uses the real range; attempts start at 0.
- Simplified scoring: wins score `100 - 10 * attempts` (min 10), wrong guesses -5.
- `parse_guess` now strips whitespace.

## 📸 Demo Walkthrough

1. Run `python -m streamlit run app.py` and pick a difficulty in the sidebar; the banner shows the matching range.
2. Enter a guess and click Submit Guess; the hint tells you to go higher or lower correctly.
3. Keep guessing; attempts left counts down and the score drops 5 per miss.
4. Guess the secret to win (balloons, final score) or run out of attempts to lose.
5. Click New Game to reset everything, or change difficulty to start a fresh round.

## 🧪 Test Results

```
pytest
...... [100%]
6 passed
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
