def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Hard was 1-50 (easier than Normal); widened with Claude Code
        return 1, 200
    return 1, 100


def parse_guess(raw: str, low=None, high=None):
    """
    Parse user input into an int guess.

    Accepts whole numbers (including "5.0"); rejects blanks, text, non-whole
    decimals, inf/nan, and, when low/high are given, values outside that range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    try:
        number = float(raw) if "." in raw else int(raw)
    except (ValueError, OverflowError):
        return False, None, "That is not a number."

    if isinstance(number, float):
        if number != number or number in (float("inf"), float("-inf")):
            return False, None, "That is not a number."
        if not number.is_integer():
            return False, None, "Enter a whole number."
        number = int(number)

    if low is not None and high is not None and not low <= number <= high:
        return False, None, f"Enter a number between {low} and {high}."

    return True, number, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: Hint messages were swapped; refactored into logic_utils.py with Claude Code (agent mode)
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
