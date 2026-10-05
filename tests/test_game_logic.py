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
