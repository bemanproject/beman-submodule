#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import argparse
import sys

from beman_submodule.lib.core import (
    add_command,
    check_for_git,
    status_command,
    update_command,
)


def get_parser():
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(description='Beman pseudo-submodule tool')
    subparsers = parser.add_subparsers(dest='command', help='available commands')

    parser_update = subparsers.add_parser('update', help='update beman_submodules')
    parser_update.add_argument(
        '--remote',
        action='store_true',
        help='update a beman_submodule to its latest from upstream',
    )
    parser_update.add_argument(
        'beman_submodule_path',
        nargs='?',
        help='relative path to the beman_submodule to update',
    )

    parser_add = subparsers.add_parser('add', help='add a new beman_submodule')
    parser_add.add_argument('repository', help='git repository to add')
    parser_add.add_argument('path', nargs='?', help='path where the repository will be added')
    parser_add.add_argument(
        '--allow-untracked-files',
        action='store_true',
        help='the beman_submodule will not occupy the subdirectory exclusively',
    )

    parser_status = subparsers.add_parser('status', help='show the status of beman_submodules')
    parser_status.add_argument('paths', nargs='*')

    return parser


def parse_args(args):
    """Parse command line arguments."""
    return get_parser().parse_args(args)


def usage():
    """Return the help text."""
    return get_parser().format_help()


def run_command(args):
    """Execute the appropriate command based on parsed arguments."""
    if args.command == 'update':
        update_command(args.remote, args.beman_submodule_path)
    elif args.command == 'add':
        add_command(args.repository, args.path, args.allow_untracked_files)
    elif args.command == 'status':
        status_command(args.paths)
    else:
        raise Exception(usage())


def main():
    """Main entry point for the CLI."""
    try:
        if not check_for_git(None):
            raise Exception('git not found in PATH')
        args = parse_args(sys.argv[1:])
        run_command(args)
    except Exception as e:
        print('Error:', e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
