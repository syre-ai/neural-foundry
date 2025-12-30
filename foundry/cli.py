"""Main CLI entry point for Claude Foundry."""

import click
from rich.console import Console

from foundry import __version__
from foundry.engine.state import GameState

# Import tracks to register them
import foundry.tracks  # noqa: F401

from foundry.engine.runner import (
    start_mission,
    check_mission,
    complete_mission,
    list_missions,
    list_tracks,
)
from foundry.ui.display import show_welcome, show_status

console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version=__version__)
def cli(ctx):
    """Claude Foundry - Master Claude Code through hands-on missions."""
    ctx.ensure_object(dict)
    ctx.obj["state"] = GameState.load()

    if ctx.invoked_subcommand is None:
        show_welcome(ctx.obj["state"])


@cli.command()
@click.pass_context
def status(ctx):
    """Show your current progress and stats."""
    show_status(ctx.obj["state"])


@cli.command()
@click.option("--track", "-t", default=None, help="Filter by track")
@click.pass_context
def missions(ctx, track):
    """List available missions."""
    list_missions(ctx.obj["state"], track)


@cli.command()
def tracks():
    """List available learning tracks."""
    list_tracks()


@cli.command()
@click.argument("mission_id")
@click.pass_context
def play(ctx, mission_id):
    """Start a mission and set up its workspace."""
    start_mission(ctx.obj["state"], mission_id)


@cli.command()
@click.argument("mission_id")
@click.pass_context
def check(ctx, mission_id):
    """Check progress on a mission."""
    check_mission(ctx.obj["state"], mission_id)


@cli.command(name="complete")
@click.argument("mission_id")
@click.pass_context
def complete_cmd(ctx, mission_id):
    """Complete a mission and claim rewards."""
    complete_mission(ctx.obj["state"], mission_id)


def main():
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
