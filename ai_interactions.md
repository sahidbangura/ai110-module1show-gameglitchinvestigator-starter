# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7) / Challenge 1: Advanced Edge-Case Testing

> Tool: Claude Code. Edge cases were identified with the assistant, then turned into pytest cases in `tests/test_game_logic.py`.

**Prompt used:**

```
Challenge 1: Advanced Edge-Case Testing. Identify three potential edge-case inputs
(negative numbers, decimals, extremely large values) that might still break my game,
generate pytest cases that verify the game handles them gracefully, and fix the code
where they fail.
```

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative, zero and out-of-range numbers (`-5`, `0`, `101`, a 20-digit number) | Challenge 1 prompt above | `test_out_of_range_numbers_rejected` | Failed on the old code (accepted, cost an attempt); passes after `parse_guess(raw, low, high)` | The old code accepted any integer, so a guess like `-5` wasted an attempt. |
| Decimals (`3.7`, `0.5`, `-2.5`) and whole decimals (`5.0`) | Challenge 1 prompt above | `test_non_whole_decimals_rejected_not_truncated`, `test_in_range_boundaries_and_whole_decimals_accepted` | Failed on the old code (3.7 became 3); passes now | Silent truncation hides a typo from the player; `5.0` is still a clear whole-number guess. |
| Huge or special values (`1e999`, `inf`, `nan`, `1e3`) | Challenge 1 prompt above | `test_non_numeric_and_special_values_rejected` | Passes; `inf` would otherwise raise `OverflowError` | Float parsing can produce values `int()` cannot handle, so the function must return an error instead of crashing. |
| Blank input and whitespace (`""`, `"   "`, `None`) | Challenge 1 prompt above | `test_blank_input_rejected` | Passes | Whitespace-only input must be treated as blank, not as a number. |
| Boundaries (`1`, `100`) | Challenge 1 prompt above | `test_in_range_boundaries_and_whole_decimals_accepted` | Passes | Off-by-one errors are common at the edges of a range. |

**Note:** The "failed before" results are from reasoning about the previous `parse_guess` code, not from re-running it, so confirm by temporarily reverting if your instructor wants proof.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
