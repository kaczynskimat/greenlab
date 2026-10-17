"""
Equivalence tests for LeetCode #125 (Valid Palindrome), guideline G19.

Each baseline_N is compared with modified_N on the same inputs.
Passing these tests provides evidence of equivalence for the tested
inputs, but does not prove equivalence for all possible inputs.
"""

import pytest

from vp_baseline_1 import Solution as Baseline1
from vp_baseline_2 import Solution as Baseline2
from vp_baseline_3 import Solution as Baseline3
from vp_modified_1 import Solution as Modified1
from vp_modified_2 import Solution as Modified2
from vp_modified_3 import Solution as Modified3

PAIRS = [
    (Baseline1, Modified1),
    (Baseline2, Modified2),
    (Baseline3, Modified3),
]


@pytest.fixture(params=PAIRS, ids=["pair1", "pair2", "pair3"])
def pair(request):
    baseline_cls, modified_cls = request.param
    # Fresh instances per test so no state is shared
    return baseline_cls(), modified_cls()


def check(pair, s, expected):
    baseline, modified = pair
    result_baseline = baseline.isPalindrome(s)
    result_modified = modified.isPalindrome(s)
    assert result_baseline == result_modified == expected, (
        f"Input {s!r}: baseline={result_baseline}, "
        f"modified={result_modified}, expected={expected}"
    )


def test_typical_palindrome(pair):
    """Typical case: mixed case, spaces and punctuation, valid palindrome."""
    check(pair, "A man, a plan, a canal: Panama", True)


def test_typical_non_palindrome(pair):
    """Typical case: cleaned string is not a palindrome."""
    check(pair, "race a car", False)


def test_only_non_alphanumeric(pair):
    """Boundary: nothing remains after filtering, which counts as a palindrome."""
    check(pair, ".,  :;!?", True)


def test_single_character(pair):
    """Boundary: shortest valid input."""
    check(pair, "a", True)


def test_digits_and_letters(pair):
    """Edge case: digit vs letter, where alphanumeric filtering matters."""
    check(pair, "0P", False)