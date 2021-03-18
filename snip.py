# -*- coding: utf-8 -*-
"""A simple tool to help with snippets.

Expects (not yet, but anyway) SNIPPETS_PATH to be a git repo.

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, description=__doc__)

    def specify_args(self):
        subparsers = self.add_subparsers(dest="command")
        add = subparsers.add_parser("add")
        add.add_argument("lang")
        add.add_argument("prefix")
        add.add_argument("-n", "--name", default=None)
        add.add_argument("-d", "--description", default="")
        add.add_argument("-s", "--skip-review", action="store_true")
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


def _add(lang, prefix, name, description, skip_review, **kwargs):
    snippet = _make_snippet(lang, prefix, name, description)
    if snippet is None:
        print("dismissing empty snippet...")
        return
    to_review = not skip_review and name is None or description == ""
    if to_review:
        snippet = _review_snippet(snippet)
        if snippet is None:
            print("dismissing snippet due to emptied message")
            return
    dest = SNIPPETS_PATH / f"{lang}.json"
    if not dest.exists():
        if input(f"{dest} does not exist.  Create? (y/n) ") != "y":
            print("not created, dismissing the snippet...")
            return
        with open(dest, "w") as file:
            json.dump({}, file)
    _save_snippet(snippet, dest)


def _save_snippet(snippet, dest):
    # Expects dest to exist
    with open(dest) as file:
        snippets = json.load(file)
    with open(dest, "w") as file:
        json.dump(snippets | snippet, file, indent=4)


def _make_snippet(lang, prefix, name, description):
    body = _request_body().splitlines()
    if not body:
        return None
    if name is None:
        name = _make_random_name()
    return {
        name: {
            "prefix": f"s-{prefix}",
            "body": body,
            "description": description
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
        contents = file.read()
        if not contents:
            snippet = None
        else:
            snippet = json.loads(contents)
    os.unlink(name)
    return snippet


def _make_random_name():
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=16)
    )


if __name__ == "__main__":
    main()
