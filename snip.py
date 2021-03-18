# -*- coding: utf-8 -*-
"""A simple tool to help with snippets.

Usage:
    snip add lang prefix
"""


import argparse


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
    pass


if __name__ == "__main__":
    main()
