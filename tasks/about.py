from invoke import task, Context
from tasks.context import context

# Import rich components
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

@task(default=True)
def info(c):
    """
    Print information about the project context
    """
    console = Console()
    
    # 1. Print a header box
    console.print(Panel.fit(
        f"[bold cyan]Welcome to {context.project_name.title()}[/bold cyan] v[bold green]{context.version}[/bold green]",
        subtitle="[dim]Deployment CLI[/dim]",
        border_style="blue"
    ))
    
    # 2. Create a properties table
    table = Table(show_header=True, header_style="bold magenta", border_style="dim")
    table.add_column("Property", width=20)
    table.add_column("Value / Path", style="green")
    
    # 3. Add rows dynamically from our props context!
    table.add_row("Project Name", context.project_name)
    table.add_row("Version", context.version)
    table.add_row("AWS Region", context.aws_region)
    
    # 4. Render it to the terminal
    console.print(table)
    console.print("\n")