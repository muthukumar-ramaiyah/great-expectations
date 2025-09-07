import pytest_check as check

def test_soft_assertions():
    check.equal(1 + 1, 3, "Math is broken")
    check.is_true(False, "This should be true")
    check.greater(5, 2, "2 should not be greater than 5")

    print("✅ Test continued even after failures")
