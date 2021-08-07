#!/usr/bin/python

from argparse import ArgumentParser
from hurry.filesize import size

from src.api_service import ApiService
from src.options import Options


def __display_items(items):
    if not items:
        print('No files found.')
    else:
        print('Files:')
        counter = 0

        for item in items:
            counter = counter + 1
            display_value = f"{counter}. {item['name']} | {item['mimeType']}"

            if 'size' in item:
                file_byte_size = int(item['size'])
                display_value += f" | {size(file_byte_size)}"

            print(display_value)


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--files", nargs='*',
                        help="Show most recent files.")
    parser.add_argument("-d", "--download", nargs='+',
                        help="Download file (must provide an id)")
    args = parser.parse_args()

    service = ApiService()

    if args.files is not None:
        items = service.get_files(Options(args.files))
        __display_items(items)
    elif args.download is not None:
        file_name = args.download[0] if len(args.download) > 0 else None
        download_path = args.download[1] if len(args.download) == 2 else "."
        service.download_file(file_name, download_path)
    else:
        print("No argument is selected. Pass -h or --help for details")


if __name__ == '__main__':
    main()
