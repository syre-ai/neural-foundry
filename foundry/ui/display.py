"""Terminal display components."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from foundry.engine.state import GameState
from foundry.engine.tiers import TIER_INFO, get_next_tier

console = Console()

LOGO = """
[bold cyan]
  _____ _                 _        _____                      _
 / ____| |               | |      |  ___|                    | |
| |    | | __ _ _   _  __| | ___  | |_ ___  _   _ _ __   __ _| |_ __ _   _
| |    | |/ _` | | | |/ _` |/ _ \ |  _/ _ \| | | | '_ \ / _` | __/ _` | | |
| |____| | (_| | |_| | (_| |  __/ | || (_) | |_| | | | | (_| | || (_| |_| |
 \_____|_|\__,_|\__,_|\__,_|\___| \_| \___/ \__,_|_| |_|\__,_|\__\__,_(_)_|
[/bold cyan]
"""


def show_welcome(state: GameState) -> None:
    """Display the welcome screen."""
    console.print(LOGO)
    console.print(
        Panel(
            f"[bold]Welcome, {state.player_name}![/bold]\n\n"
            f"Master Claude Code through hands-on missions.\n"
            f"Progress through tiers from Apprentice to Master.\n\n"
            f"[dim]Commands: status, missions, tracks, play[/dim]",
            title="Learn by Doing",
            border_style="cyan",
        )
    )
    console.print()
    _show_quick_status(state)


def _show_quick_status(state: GameState) -> None:
    """Show a compact status bar."""
    next_tier = get_next_tier(state.tier)

    progress_text = ""
    if next_tier:
        next_info = TIER_INFO[next_tier]
        completed = len(state.missions_completed)
        required = next_info.missions_required
        progress_text = f" | Progress: {completed}/{required} missions"

    track_text = f" | Track: {state.current_track}" if state.current_track != "default" else ""

    console.print(
        f"[bold]{state.tier.value}[/bold] | "
        f"XP: {state.xp} | "
        f"Missions: {len(state.missions_completed)}"
        f"{progress_text}{track_text}"
    )


def show_status(state: GameState) -> None:
    """Display detailed player status."""
    tier_info = TIER_INFO[state.tier]

    table = Table(title="Player Status", border_style="cyan")
    table.add_column("Attribute", style="bold")
    table.add_column("Value")

    table.add_row("Name", state.player_name)
    table.add_row("Tier", f"[cyan]{state.tier.value}[/cyan]")
    table.add_row("XP", str(state.xp))
    table.add_row("Missions Completed", str(len(state.missions_completed)))
    table.add_row("Current Track", state.current_track)

    console.print(table)
    console.print()

    # Tier details
    console.print(Panel(
        f"[bold]{tier_info.description}[/bold]\n\n"
        f"[green]Claude Code Skills:[/green]\n" +
        "\n".join(f"  - {skill}" for skill in tier_info.claude_skills),
        title=f"{state.tier.value} Tier",
        border_style="cyan",
    ))
