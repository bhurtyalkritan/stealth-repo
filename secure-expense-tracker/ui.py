from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.text import Text
from datetime import datetime
import re

console = Console()

def display_welcome():
    """Display welcome screen."""
    welcome_text = Text("🔒 Secure Expense Tracker", style="bold cyan", justify="center")
    welcome_panel = Panel(
        welcome_text,
        subtitle="Your finances, encrypted and secure",
        border_style="cyan"
    )
    console.print("\n")
    console.print(welcome_panel)
    console.print("\n")

def display_main_menu():
    """Display the main menu options."""
    menu_options = """
[bold yellow]📋 Main Menu[/]

[cyan]1.[/] 💰 Add Transaction
[cyan]2.[/] 📊 View Transactions
[cyan]3.[/] 📈 Monthly Report
[cyan]4.[/] 📅 Spending Summary
[cyan]5.[/] 🏷️  Manage Categories
[cyan]6.[/] 📤 Export Data
[cyan]7.[/] ⚙️  Settings
[cyan]8.[/] 🚪 Logout
"""
    console.print(Panel(menu_options, border_style="yellow"))

def get_menu_choice(max_choice: int = 8) -> int:
    """Get and validate menu choice."""
    while True:
        try:
            choice = int(Prompt.ask("Choose an option", default="1"))
            if 1 <= choice <= max_choice:
                return choice
            else:
                console.print(f"[red]Please enter a number between 1 and {max_choice}.[/]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/]")

def get_transaction_input():
    """Get transaction details from user with validation."""
    console.print("\n[bold green]💰 Add New Transaction[/]")
    
    # Get amount
    while True:
        try:
            amount = float(Prompt.ask("Amount ($)"))
            if amount <= 0:
                console.print("[red]Amount must be greater than 0.[/]")
                continue
            break
        except ValueError:
            console.print("[red]Please enter a valid amount.[/]")
    
    # Get category
    category = Prompt.ask("Category", default="Other")
    
    # Get description
    description = Prompt.ask("Description (optional)", default="")
    
    # Get date
    while True:
        date_input = Prompt.ask("Date (YYYY-MM-DD, or press Enter for today)", default="")
        if not date_input:
            date_input = None
            break
        
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_input):
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                break
            except ValueError:
                console.print("[red]Invalid date. Please use YYYY-MM-DD format.[/]")
        else:
            console.print("[red]Invalid date format. Please use YYYY-MM-DD.[/]")
    
    return amount, category, description, date_input

def get_filter_options():
    """Get filtering options for transaction list."""
    console.print("\n[bold blue]🔍 Filter Options[/]")
    
    category = Prompt.ask("Filter by category (optional)", default="")
    start_date = Prompt.ask("Start date (YYYY-MM-DD, optional)", default="")
    end_date = Prompt.ask("End date (YYYY-MM-DD, optional)", default="")
    
    return (
        category if category else None,
        start_date if start_date else None,
        end_date if end_date else None
    )

def display_categories(categories: list):
    """Display available categories in a nice format."""
    console.print("\n[bold blue]🏷️ Available Categories[/]")
    
    # Split into columns for better display
    cols = 3
    rows = (len(categories) + cols - 1) // cols
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    for _ in range(cols):
        table.add_column()
    
    for i in range(rows):
        row_data = []
        for j in range(cols):
            idx = i + j * rows
            if idx < len(categories):
                row_data.append(f"• {categories[idx]}")
            else:
                row_data.append("")
        table.add_row(*row_data)
    
    console.print(table)

def confirm_action(message: str) -> bool:
    """Get confirmation from user."""
    return Confirm.ask(message)

def display_error(message: str):
    """Display error message."""
    console.print(f"[red]❌ {message}[/]")

def display_success(message: str):
    """Display success message."""
    console.print(f"[green]✅ {message}[/]")

def display_info(message: str):
    """Display info message."""
    console.print(f"[blue]ℹ️  {message}[/]")

def display_warning(message: str):
    """Display warning message."""
    console.print(f"[yellow]⚠️  {message}[/]")

def get_month_year_input():
    """Get month and year for reports."""
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    year_input = Prompt.ask(f"Year", default=str(current_year))
    month_input = Prompt.ask(f"Month (1-12)", default=str(current_month))
    
    try:
        year = int(year_input)
        month = int(month_input)
        
        if not (1 <= month <= 12):
            console.print("[red]Month must be between 1 and 12.[/]")
            return None, None
        
        if year < 2000 or year > 2100:
            console.print("[red]Please enter a valid year.[/]")
            return None, None
            
        return year, month
    except ValueError:
        console.print("[red]Please enter valid numbers.[/]")
        return None, None

def display_loading(message: str = "Processing..."):
    """Display loading message."""
    console.print(f"[yellow]⏳ {message}[/]")

def clear_screen():
    """Clear the console screen."""
    console.clear()

def pause():
    """Pause execution until user presses Enter."""
    Prompt.ask("\nPress Enter to continue", default="")
    
def display_stats_table(stats: dict):
    """Display statistics in a formatted table."""
    table = Table(title="📊 Statistics", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="green", justify="right")
    
    for key, value in stats.items():
        table.add_row(key, str(value))
    
    console.print(table)
