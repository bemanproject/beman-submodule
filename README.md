# beman-submodule

<!-- SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception -->

A pseudo-submodule tool for vendoring Git repositories in Beman projects.

## What is beman-submodule?

`beman-submodule` provides some of the features of `git submodule`, adding child git
repositories to a parent git repository, but unlike with `git submodule`, the entire child
repo is directly checked in, so only maintainers, not users, need to run this script. The
command line interface mimics `git submodule`'s.

## Installation

```sh
pip install beman-submodule
```

Or with [uv](https://github.com/astral-sh/uv):

```sh
uv tool install beman-submodule
```

## Usage

### Adding a beman submodule

```sh
beman-submodule add https://github.com/bemanproject/infra.git
```

This will clone the repository and create a `.beman_submodule` file tracking the remote and commit.

You can also specify a custom path:

```sh
beman-submodule add https://github.com/bemanproject/infra.git infra/
```

### Updating beman submodules

Update all beman submodules to match their `.beman_submodule` configuration:

```sh
beman-submodule update
```

Update all beman submodules to the latest from upstream:

```sh
beman-submodule update --remote
```

Update only a specific submodule:

```sh
beman-submodule update --remote infra/
```

### Checking status

Show the status of all beman submodules:

```sh
beman-submodule status
```

A `+` prefix indicates the submodule contents differ from the configured commit.

## How does it work?

Along with the files from the child repository, it creates a dotfile called
`.beman_submodule`, which looks like this:

```ini
[beman_submodule]
remote=https://github.com/bemanproject/infra.git
commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77
```

### Updating to a specific commit or changing the remote URL

Edit the corresponding lines in the `.beman_submodule` file and run
`beman-submodule update` to update the state of the beman submodule to the new
settings.

### Allow untracked files

If you need to add local files alongside the vendored content, use:

```sh
beman-submodule add --allow-untracked-files https://github.com/example/repo.git path/
```

This adds `allow_untracked_files=True` to the `.beman_submodule` config, preserving local
files during updates.

## CI Integration

Add this job to your CI workflow to ensure beman submodules are in a valid state:

```yaml
  beman-submodule-test:
    runs-on: ubuntu-latest
    name: "Check beman submodules for consistency"
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Install beman-submodule
        run: pip install beman-submodule
      - name: beman submodule consistency check
        run: |
          (set -o pipefail; beman-submodule status | grep -qvF '+')
```

This will fail if the contents of any beman submodule don't match what's specified in the
`.beman_submodule` file.

## Development

This project uses [uv](https://github.com/astral-sh/uv) for development:

```sh
# Install dependencies
uv sync --group dev

# Run tests
uv run pytest

# Run linter
uv run ruff check .

# Format code
uv run ruff format .
```

## License

Apache-2.0 WITH LLVM-exception
