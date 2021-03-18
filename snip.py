# -*- coding: utf-8 -*-
"""A simple tool to help with snippets.

Usage:
    snip add lang prefix
"""


import argparse
import tempfile
import pathlib
import random
import string
import json
import os


SNIPPETS_PATH = pathlib.Path("/home/ihor/.config/Code/User/snippets")


def main():
    """Entry point of the application."""
    parser = _Parser().specify_args()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return
    _assemble_commands()[args.command](**vars(args))


class _Parser(argparse.ArgumentParser):

    def specify_args(self):
        subparsers = self.add_subparsers(dest="command")
        add = subparsers.add_parser("add")
        add.add_argument("lang")
        add.add_argument("prefix")
        # add.add_argument(
        #     "-r", "--review", help="help", action="store_true"
        # )
        # add.add_argument(
        #     "-e", "--edit-msg", help="help", action="store_true"
        # )
        # init = subparsers.add_parser("init")
        return self


def _assemble_commands():
    return {
        name: globals()[f"_{name}"]
        for name in {
            "add",
        }
    }


def _add(lang, prefix, **kwargs):
    snippet = _make_snippet(lang, prefix)
    if True:
        reviewed = _review_snippet(snippet)
    dest = SNIPPETS_PATH / f"{lang}.json"
    if not dest.exists():
        if input(f"{dest} does not exist.  Create? (y/n) ") != "y":
            return
        with open(dest, "w") as file:
            json.dump({}, file)
    _save_snippet(reviewed, dest)


def _save_snippet(snippet, dest):
    # Expects dest to exist
    with open(dest) as file:
        snippets = json.load(file)
    with open(dest, "w") as file:
        json.dump(snippets | snippet, file, indent=4)


def _make_snippet(lang, prefix):
    return {
        _make_random_name(): {
            "prefix": prefix,
            "body": [line for line in _request_body().splitlines()],
            "description": ""
        }
    }


def _request_body():
    _, name = tempfile.mkstemp()
    os.system(f"nano {name}")
    with open(name) as file:
        body = file.read()
    os.unlink(name)
    return body


def _review_snippet(snippet):
    _, name = tempfile.mkstemp()
    with open(name, "w") as file:
        json.dump(snippet, file, indent=4)
    os.system(f"nano {name}")
    with open(name) as file:
        snippet = json.load(file)
    os.unlink(name)
    return snippet


def _make_random_name():
    return "".join(
        random.choices(string.ascii_lowercase + string.digits, k=16)
    )


if __name__ == "__main__":
    main()
