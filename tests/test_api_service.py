from src.api_service import ApiService
from src.options import Options

def test_get_files_get_files():
    # exercise
    api_service = ApiService()
    options = Options(["total=5"])
    files = api_service.get_files(options)

    # post-conditions
    assert len(files) == 5
