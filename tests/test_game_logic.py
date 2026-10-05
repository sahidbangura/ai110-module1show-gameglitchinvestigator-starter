from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_hard_range_is_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_parse_guess_valid_and_invalid():
    assert parse_guess("42") == (True, 42, None)
    assert parse_guess(" 7 ") == (True, 7, None)
    assert parse_guess("")[0] is False
    assert parse_guess(None)[0] is False
    assert parse_guess("abc")[0] is False


def test_score_win_and_miss():
    assert update_score(0, "Win", 1) == 90
    assert update_score(0, "Win", 20) == 10
    assert update_score(20, "Too High", 2) == 15
    assert update_score(20, "Too Low", 3) == 15


def test_check_guess_compares_numbers_not_strings():
    # As strings "9" > "50", which used to give a wrong hint on even attempts.
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"


# --- Edge cases (Challenge 1) ---

import pytest


@pytest.mark.parametrize("raw", ["-5", "0", "-0", "101", "99999999999999999999"])
def test_out_of_range_numbers_rejected(raw):
    # Negative, zero and huge values must not be accepted as guesses on 1-100.
    ok, value, error = parse_guess(raw, 1, 100)
    assert ok is False and value is None
    assert "between 1 and 100" in error


@pytest.mark.parametrize("raw", ["1", "100", " 50 ", "5.0"])
def test_in_range_boundaries_and_whole_decimals_accepted(raw):
    ok, value, error = parse_guess(raw, 1, 100)
    assert ok is True and error is None
    assert isinstance(value, int)


@pytest.mark.parametrize("raw", ["3.7", "0.5", "-2.5"])
def test_non_whole_decimals_rejected_not_truncated(raw):
    # 3.7 used to be silently truncated to 3.
    ok, value, error = parse_guess(raw, 1, 100)
    assert ok is False and value is None
    assert error == "Enter a whole number."


@pytest.mark.parametrize("raw", ["1e999", "inf", "-inf", "nan", "1e3", "abc", "4 2", "--5"])
def test_non_numeric_and_special_values_rejected(raw):
    # Must return an error tuple, never raise (e.g. OverflowError on int(inf)).
    ok, value, error = parse_guess(raw, 1, 100)
    assert ok is False and value is None
    assert error


@pytest.mark.parametrize("raw", ["", "   ", None])
def test_blank_input_rejected(raw):
    assert parse_guess(raw, 1, 100) == (False, None, "Enter a guess.")


def test_parse_guess_without_range_still_works():
    assert parse_guess("-5") == (True, -5, None)
