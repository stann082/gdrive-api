from src.options import Options

def test_parse_options():
    # exercise
    options = Options(["total=50", "orderBy=size"])

    # post-conditions
    assert options.filter_by == None
    assert options.order_by == 'size'
    assert options.total == '50'
    assert options.are_defined is True

def test_parse_options_bad_value():
    # exercise
    options = Options(["total=50", "orderBy=size", "badvalue"])

    # post-conditions
    assert options.filter_by == None
    assert options.order_by == 'size'
    assert options.total == '50'
    assert options.are_defined is True

def test_parse_options_no_cli_args():
    # exercise
    options = Options()

    # post-conditions
    assert options.are_defined is False