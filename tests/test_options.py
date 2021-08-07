from src.options import Options

def test_parse_options():
    # exercise
    options = Options(["total=50", "orderBy=modified"])

    # post-conditions
    assert options.fields == 'files(name,mimeType,size)'
    assert options.filter_by == 'name'
    assert options.order_by == 'modified'
    assert options.query == None
    assert options.total == '50'
    assert options.is_descending is False
    assert options.fetch_all_files is False
    assert options.order_by_size is False

def test_parse_options_order_by_size_desc():
    # exercise
    options = Options(["total=all", "filterBy=mimeType", "orderBy=size", "desc"])

    # post-conditions
    assert options.fields == 'files(name,mimeType,size)'
    assert options.filter_by == 'mimeType'
    assert options.order_by == 'size'
    assert options.query == None
    assert options.total == 'all'
    assert options.is_descending is True
    assert options.fetch_all_files is True
    assert options.order_by_size is True

def test_parse_options_no_cli_args():
    # exercise
    options = Options()

    # post-conditions
    assert options.fields == 'files(name,mimeType,size)'
    assert options.filter_by == 'name'
    assert options.order_by == None
    assert options.query == None
    assert options.total == '10'
    assert options.is_descending is False
    assert options.fetch_all_files is False
    assert options.order_by_size is False