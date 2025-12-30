"""Mission runner - handles mission execution and validation."""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

from foundry.engine.state import GameState, SAVE_DIR
from foundry.engine.base import (
    get_mission,
    get_all_missions,
    get_missions_for_tier,
    get_missions_for_track,
    get_all_tracks,
    Mission,
    CheckpointStatus,
)

console = Console()

# Default workspace location
WORKSPACE_BASE = SAVE_DIR / "workspace"


def get_workspace(mission_id: str) -> Path:
    """Get workspace path for a mission."""
    return WORKSPACE_BASE / mission_id


def start_mission(state: GameState, mission_id: str) -> bool:
    """Start a mission, setting up its workspace."""
    mission_class = get_mission(mission_id)
    if not mission_class:
        console.print(f"[red]Mission not found: {mission_id}[/red]")
        return False

    mission = mission_class()
    workspace = get_workspace(mission_id)

    # Setup workspace
    console.print(f"[cyan]Setting up mission workspace...[/cyan]")
    mission.setup(workspace)

    # Show mission briefing
    console.print()
    console.print(Panel(
        Markdown(mission.get_instructions()),
        title=f"[bold]{mission.info.title}[/bold]",
        border_style="cyan",
    ))

    console.print()
    console.print(f"[green]Workspace created at:[/green] {workspace}")
    console.print()
    console.print("[bold]Next steps:[/bold]")
    console.print(f"  1. cd {workspace}")
    console.print("  2. Start working with Claude Code!")
    console.print(f"  3. Run [cyan]nf check {mission_id}[/cyan] to validate progress")

    return True


def check_mission(state: GameState, mission_id: str) -> None:
    """Check progress on a mission."""
    mission_class = get_mission(mission_id)
    if not mission_class:
        console.print(f"[red]Mission not found: {mission_id}[/red]")
        return

    mission = mission_class()
    workspace = get_workspace(mission_id)

    if not workspace.exists():
        console.print(f"[yellow]Mission not started. Run:[/yellow] nf play {mission_id}")
        return

    mission.workspace = workspace

    # Check each checkpoint
    table = Table(title=f"Mission Progress: {mission.info.title}", border_style="cyan")
    table.add_column("Status", width=8)
    table.add_column("Checkpoint")
    table.add_column("Details")

    all_complete = True
    for cp in mission.get_checkpoints():
        success, message = mission.validate_checkpoint(cp.id)

        if success:
            status = "[green]✓[/green]"
            cp.status = CheckpointStatus.COMPLETED
        else:
            status = "[yellow]○[/yellow]"
            all_complete = False

        table.add_row(status, cp.title, message)

    console.print(table)

    if all_complete:
        console.print()
        console.print(Panel(
            f"[bold green]Mission Complete![/bold green]\n\n"
            f"XP Earned: +{mission.info.xp_reward}\n\n"
            f"Run [cyan]nf complete {mission_id}[/cyan] to claim rewards.",
            border_style="green",
        ))
    else:
        # Show hint for current checkpoint
        current = mission.get_current_checkpoint()
        if current:
            console.print()
            console.print(f"[dim]Hint: {current.hint}[/dim]")


def complete_mission(state: GameState, mission_id: str) -> bool:
    """Mark a mission as complete and award XP."""
    mission_class = get_mission(mission_id)
    if not mission_class:
        console.print(f"[red]Mission not found: {mission_id}[/red]")
        return False

    mission = mission_class()
    workspace = get_workspace(mission_id)

    if not workspace.exists():
        console.print(f"[yellow]Mission not started.[/yellow]")
        return False

    mission.workspace = workspace

    # Verify all checkpoints
    for cp in mission.get_checkpoints():
        success, _ = mission.validate_checkpoint(cp.id)
        if not success:
            console.print(f"[red]Mission not complete. Run 'nf check {mission_id}' to see progress.[/red]")
            return False

    # Award completion
    if mission_id in state.missions_completed:
        console.print(f"[yellow]Mission already completed.[/yellow]")
        return False

    old_tier = state.tier
    state.complete_mission(mission_id, mission.info.xp_reward)

    console.print(Panel(
        f"[bold green]Mission Complete: {mission.info.title}[/bold green]\n\n"
        f"XP Earned: +{mission.info.xp_reward}\n"
        f"Total XP: {state.xp}",
        border_style="green",
    ))

    if state.tier != old_tier:
        console.print(Panel(
            f"[bold magenta]TIER UP![/bold magenta]\n\n"
            f"You are now: [bold]{state.tier.value}[/bold]",
            border_style="magenta",
        ))

    return True


def list_missions(state: GameState, track: str | None = None) -> None:
    """List available missions, optionally filtered by track."""
    missions = get_all_missions()

    if not missions:
        console.print("[yellow]No missions available yet.[/yellow]")
        return

    # Filter by track if specified
    if track:
        missions = {k: v for k, v in missions.items() if v.info.track == track}

    table = Table(title="Available Missions", border_style="cyan")
    table.add_column("ID", style="cyan")
    table.add_column("Title")
    table.add_column("Track")
    table.add_column("Tier")
    table.add_column("XP")
    table.add_column("Status")

    for mission_id, mission_class in missions.items():
        info = mission_class.info

        if mission_id in state.missions_completed:
            status = "[green]✓ Complete[/green]"
        elif info.tier.value == state.tier.value:
            status = "[yellow]Available[/yellow]"
        else:
            status = "[dim]Locked[/dim]"

        table.add_row(
            info.id,
            info.title,
            info.track,
            info.tier.value,
            str(info.xp_reward),
            status,
        )

    console.print(table)
    console.print()
    console.print("[dim]Start a mission with: nf play <mission_id>[/dim]")


def list_tracks() -> None:
    """List all available learning tracks."""
    tracks = get_all_tracks()

    if not tracks:
        console.print("[yellow]No tracks registered.[/yellow]")
        return

    table = Table(title="Learning Tracks", border_style="cyan")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Missions")

    for track_id, track_info in tracks.items():
        mission_count = len(get_missions_for_track(track_id))
        table.add_row(
            track_id,
            track_info["name"],
            track_info["description"],
            str(mission_count),
        )

    console.print(table)
