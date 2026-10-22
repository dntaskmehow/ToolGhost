import json
from typing import List
from rich.console import Console
from rich.table import Table
from .engine import GhostFinding

console = Console()

class GhostReporter:
    @staticmethod
    def print_terminal_report(findings: List[GhostFinding]):
        if not findings:
            console.print("[green]? No tool-use parameter anomalies or execution vulnerabilities detected.[/green]")
            return

        table = Table(title="[bold red]ToolGhost LLM Tool-Use Vulnerability Findings[/bold red]")
        table.add_column("Tool", style="cyan", no_wrap=True)
        table.add_column("Parameter", style="yellow")
        table.add_column("Payload", style="magenta")
        table.add_column("Status", style="bold green")
        table.add_column("Reasoning / Impact", style="white")

        for f in findings:
            table.add_row(
                f.tool,
                f.parameter,
                f.payload,
                str(f.status_code),
                f.reason
            )
        console.print(table)

    @staticmethod
    def save_json_report(findings: List[GhostFinding], filepath: str):
        data = [f.model_dump() for f in findings]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        console.print(f"[bold green]? JSON report saved to {filepath}[/bold green]")
