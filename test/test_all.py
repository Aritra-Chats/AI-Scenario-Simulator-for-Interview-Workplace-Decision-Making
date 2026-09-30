import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""Master test suite executing all verifications from Day 1 through Day 10."""

from test_day1_day2 import test_day1_and_day2_all_subparts
from test_day3 import main as test_day3_main
from test_day4_day5 import main as test_day4_day5_main
from test_day6_to_10 import main as test_day6_to_10_main


def run_all():
    print("\n" + "=" * 65)
    print("RUNNING MASTER TEST SUITE: COMPLETE DAYS 1 - 10 IMPLEMENTATION")
    print("=" * 65)

    test_day1_and_day2_all_subparts()
    test_day3_main()
    test_day4_day5_main()
    test_day6_to_10_main()

    print("\n" + "*" * 65)
    print("CONGRATULATIONS! ALL DAYS (1 TO 10) AND ALL SUB-PARTS (A TO E)")
    print("ARE 100% IMPLEMENTED, INTEGRATED, AND FULLY VERIFIED!")
    print("*" * 65 + "\n")


if __name__ == "__main__":
    run_all()
