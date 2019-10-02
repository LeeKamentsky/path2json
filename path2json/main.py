import argparse
import base64
import json
import os
import sys


DESCRIPTION="""path2json is a program that scans a directory and converts
the contents of the files in that directory to JSON. It can be used, for
instance, to get a JSON output of /sys/class/net/<net-interface>/statistics
so that you can see how much stuff is happening on your network interface.
"""


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "path",
        help="The path to the directory to be JSONed"
    )
    parser.add_argument(
        "output",
        help="The file to be written"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recurse to subdirectories, creating a dictionary for each"
    )
    parser.add_argument(
        "-l",
        "--follow-links",
        action="store_true",
        help="Follow links when recursing"
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        help="Indent for JSON file. If not present, JSON will be a single line"
    )
    parser.add_argument(
        "-e",
        "--ignore-errors",
        action="store_true",
        help="Ignore errors - e.g. permission or read errors. The key for the "
        "file will not be included in the JSON."
    )
    return parser.parse_args(args)


def to_json(path, recursive, follow_links, ignore_errors):
    d = {}
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.islink(file_path) and not follow_links:
            continue
        if os.path.isdir(file_path):
            if recursive:
                d[filename] = to_json(file_path, recursive, follow_links,
                                      ignore_errors)
            continue
        try:
            with open(file_path, "rb") as fd:
                data = fd.read()
                try:
                    value = int(data)
                except ValueError:
                    try:
                        value = data.decode("ascii")
                    except UnicodeDecodeError:
                        value = base64.b64encode(data).decode("utf8")
                d[filename] = value
        except:
            if ignore_errors:
                continue
            else:
                print("Failed to open or read %s" % file_path)
                raise
    return d


def main(args=sys.argv[1:]):
    args = parse_args(args)
    d = to_json(args.path, args.recursive, args.follow_links,
                args.ignore_errors)
    with open(args.output, "w") as fd:
        json.dump(d, fd, indent=args.indent)