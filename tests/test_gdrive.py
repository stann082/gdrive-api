import gdrive
from argparse import ArgumentParser
from src.api_service import ApiService

def test_get_files_get_files(monkeypatch):
    def mock_arg_parse_init(self):
        return None

    def mock_add_argument(self, *args, **kwargs):
        pass

    def mock_service_init(self):
        return None

    def mock_get_files(self, options):
        items = []
        for i in range(1, 5):
            item = {}
            item['name'] = f"{i}.txt"
            item['mimeType'] = "text-file"
            item['size'] = i + 100
            items.append(item)
        return items

    def mock_parse_args(self):
        args = Args()
        args.files = []
        return args

    monkeypatch.setattr(ArgumentParser, "__init__", mock_arg_parse_init)
    monkeypatch.setattr(ArgumentParser, "add_argument", mock_add_argument)
    monkeypatch.setattr(ArgumentParser, "parse_args", mock_parse_args)
    monkeypatch.setattr(ApiService, "__init__", mock_service_init)
    monkeypatch.setattr(ApiService, "get_files", mock_get_files)

    gdrive.main()

class Args(object):
    pass