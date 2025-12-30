"""Terminal display components."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from neural_foundry.game.state import GameState
from neural_foundry.game.tiers import TIER_INFO, get_next_tier

console = Console()

LOGO = """
[bold cyan]
 _   _                      _   _____                     _
| \ | | ___ _   _ _ __ __ _| | |  ___|__  _   _ _ __   __| |_ __ _   _
|  \| |/ _ \ | | | '__/ _` | | | |_ / _ \| | | | '_ \ / _` | '__| | | |
| |\  |  __/ |_| | | | (_| | | |  _| (_) | |_| | | | | (_| | |  | |_| |
|_| \_|\___|\__,_|_|  \__,_|_| |_|  \___/ \__,_|_| |_|\__,_|_|   \__, |
                                                                 |___/
[/bold cyan]
"""


def show_welcome(state: GameState) -> None:
    """Display the welcome screen."""
    console.print(LOGO)
    console.print(
        Panel(
            f"[bold]Welcome, {state.player_name}![/bold]\n\n"
            f"Learn Claude Code through training ART neural networks.\n"
            f"Complete missions to advance from Apprentice to Master.\n\n"
            f"[dim]Commands: status, missions, play[/dim]",
            title="Learn by Doing",
            border_style="cyan",
        )
    )
    console.print()
    _show_quick_status(state)


def _show_quick_status(state: GameState) -> None:
    """Show a compact status bar."""
    tier_info = TIER_INFO[state.tier]
    next_tier = get_next_tier(state.tier)

    progress_text = ""
    if next_tier:
        next_info = TIER_INFO[next_tier]
        completed = len(state.missions_completed)
        required = next_info.missions_required
        progress_text = f" | Progress: {completed}/{required} missions"

    console.print(
        f"[bold]{state.tier.value}[/bold] | "
        f"XP: {state.xp} | "
        f"Missions: {len(state.missions_completed)}"
        f"{progress_text}"
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
    table.add_row("Models Trained", str(state.total_models_trained))

    console.print(table)
    console.print()

    # Tier details
    console.print(Panel(
        f"[bold]{tier_info.description}[/bold]\n\n"
        f"[cyan]ART Models:[/cyan] {', '.join(tier_info.art_models)}\n"
        f"[green]Claude Skills:[/green]\n" +
        "\n".join(f"  - {skill}" for skill in tier_info.claude_skills),
        title=f"{state.tier.value} Tier",
        border_style="cyan",
    ))
