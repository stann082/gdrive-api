from src.api_service import ApiService
from src.options import Options

def test_get_files_basic():
    api_service = ApiService()
    options = Options(["total=50", "orderBy=name desc", "filterBy=name", "query=main.py"])
    files = api_service.get_files(options)

def test_get_files_all():
    api_service = ApiService()
    options = Options(["total=all", "orderBy=size desc"])
    files = api_service.get_files(options)
