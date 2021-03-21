# -*- coding: utf-8 -*-
"""Tool to help with snippets."""


import argparse
import tempfile
import pathlib
import random
import string
import json
import os


CONFIG = pathlib.Path(os.environ["HOME"]) / ".sniprc"


def main():
    """Entry point of the application."""
    parser = _Parser().specify_args()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return
    config = _read_config()
    if config is None and args.command != "init":
        print(f"no {CONFIG} - run init first")
        return
    _assemble_commands()[args.command](**vars(args), config=config)


def _read_config():
    if not CONFIG.exists():
        return None
    with open(CONFIG) as file:
        return argparse.Namespace(**json.load(file))


class _Parser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("description", __doc__)
        super().__init__(*args, **kwargs)

    def specify_args(self):
        subparsers = self.add_subparsers(dest="command")
        add = subparsers.add_parser("add", description=(
            "Add new snippet "
            "(or override the one with the same name)"
        ))
        add.add_argument("lang")
        add.add_argument("prefix")
        add.add_argument("-n", "--name", default=None)
        add.add_argument("-d", "--description", default="")
        add.add_argument("-s", "--skip-review", action="store_true")
        subparsers.add_parser("init", description=f"Make rcfile")
        subparsers.add_parser("config", description="Print config")
        return self


def _assemble_commands():
    return {
        name: globals()[f"_{name}"]
        for name in {
            "add",
            "init",
            "config",
        }
    }


def _config(config, **kwargs):
    print(json.dumps(vars(config), indent=4))


def _init(**kwargs):
    if CONFIG.exists():
        print(f"{CONFIG} exists, modify manually if needed")
        return
    config = dict(
        snippets=input("specify VS Code snippets folder: "),
        editor=input("specify editor: "),
    )
    with open(CONFIG, "w") as file:
        json.dump(config, file, indent=4)


def _add(lang, prefix, name, description, skip_review, config, **kwargs):
    dest = pathlib.Path(config.snippets) / f"{lang}.json"
    if not dest.exists():
        if input(f"{dest} does not exist.  Create? (y/n) ") != "y":
            print("not created, aborting...")
            return
        with open(dest, "w") as file:
            json.dump({}, file)
    snippet = _make_snippet(lang, prefix, name, description, config.editor)
    if snippet is None:
        print("dismissing empty snippet...")
        return
    to_review = not skip_review and (name is None or description == "")
    if to_review:
        snippet = _review_snippet(snippet, config.editor)
        if snippet is None:
            print("dismissing snippet due to emptied message")
            return
    _save_snippet(snippet, dest)
    print(f"saved to {dest}")


def _save_snippet(snippet, dest):
    # Expects dest to exist
    with open(dest) as file:
        snippets = json.load(file)
    with open(dest, "w") as file:
        json.dump(snippets | snippet, file, indent=4)


def _make_snippet(lang, prefix, name, description, editor):
    body = _request_body(editor).splitlines()
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


def _request_body(editor):
    _, name = tempfile.mkstemp()
    os.system(f"{editor} {name}")
    with open(name) as file:
        body = file.read()
    os.unlink(name)
    return body


def _review_snippet(snippet, editor):
    _, name = tempfile.mkstemp()
    with open(name, "w") as file:
        json.dump(snippet, file, indent=4)
    os.system(f"{editor} {name}")
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
