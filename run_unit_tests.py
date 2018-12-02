import pavement


def test_all_unit_tests():
    result = pavement._test_all()
    if result == 0:
        pavement.print_passed()
    else:
        pavement.print_failed()
