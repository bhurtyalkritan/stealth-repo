#!/usr/bin/env python3
"""
Secure Expense Tracker - Main CLI Application
A secure, encrypted expense tracking application with user authentication.
"""

import typer
from rich.console import Console
from rich.prompt import Prompt
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import init_db
from auth import signup, login
from expenses import (
    add_transaction, list_transactions, monthly_report, 
    get_categories, add_custom_category, delete_transaction,
    get_spending_summary
)
from ui import (
    display_welcome, display_main_menu, get_menu_choice,
    get_transaction_input, get_filter_options, display_categories,
    confirm_action, display_error, display_success, display_info,
    get_month_year_input, pause, clear_screen
)
from export import export_to_csv, export_to_pdf

app = typer.Typer(help="🔒 Secure Expense Tracker - Your finances, encrypted and secure")
console = Console()

# Global variable to store current user
current_user = None

def authenticate_user():
    """Handle user authentication (login/signup)."""
    global current_user
    
    while not current_user:
        console.print("\n[bold yellow]Authentication Required[/]")
        console.print("[cyan]1.[/] Login")
        console.print("[cyan]2.[/] Sign Up")
        console.print("[cyan]3.[/] Exit")
        
        choice = get_menu_choice(3)
        
        if choice == 1:
            username = Prompt.ask("Username")
            password = Prompt.ask("Password", password=True)
            user = login(username, password)
            if user:
                current_user = user
                display_success(f"Welcome back, {username}!")
        
        elif choice == 2:
            username = Prompt.ask("Choose username")
            password = Prompt.ask("Choose password", password=True)
            confirm_password = Prompt.ask("Confirm password", password=True)
            
            if password != confirm_password:
                display_error("Passwords don't match!")
                continue
            
            if signup(username, password):
                display_info("Please login with your new account.")
        
        elif choice == 3:
            console.print("[cyan]Goodbye! 👋[/]")
            raise typer.Exit()

def handle_add_transaction():
    """Handle adding a new transaction."""
    amount, category, description, date_str = get_transaction_input()
    
    if add_transaction(current_user, amount, category, description, date_str):
        display_success("Transaction added successfully!")
    else:
        display_error("Failed to add transaction.")

def handle_view_transactions():
    """Handle viewing transactions with optional filtering."""
    console.print("\n[bold blue]📊 View Transactions[/]")
    
    if confirm_action("Apply filters?"):
        category_filter, start_date, end_date = get_filter_options()
        list_transactions(current_user, category_filter, start_date, end_date)
    else:
        list_transactions(current_user)
    
    # Option to delete a transaction
    if confirm_action("\nDelete a transaction?"):
        try:
            tx_id = int(Prompt.ask("Transaction ID to delete"))
            if confirm_action(f"Are you sure you want to delete transaction {tx_id}?"):
                delete_transaction(current_user, tx_id)
        except ValueError:
            display_error("Invalid transaction ID.")

def handle_monthly_report():
    """Handle monthly report generation."""
    console.print("\n[bold green]📈 Monthly Report[/]")
    
    year, month = get_month_year_input()
    if year and month:
        monthly_report(current_user, year, month)
    else:
        display_error("Invalid month/year input.")

def handle_spending_summary():
    """Handle spending summary."""
    console.print("\n[bold cyan]📅 Spending Summary[/]")
    
    try:
        days = int(Prompt.ask("Number of days to analyze", default="30"))
        if days <= 0:
            display_error("Number of days must be positive.")
            return
        get_spending_summary(current_user, days)
    except ValueError:
        display_error("Please enter a valid number.")

def handle_manage_categories():
    """Handle category management."""
    console.print("\n[bold magenta]🏷️ Manage Categories[/]")
    
    categories = get_categories(current_user)
    display_categories(categories)
    
    console.print("\n[cyan]1.[/] Add new category")
    console.print("[cyan]2.[/] Back to main menu")
    
    choice = get_menu_choice(2)
    
    if choice == 1:
        category_name = Prompt.ask("New category name").strip()
        if category_name:
            add_custom_category(current_user, category_name)
        else:
            display_error("Category name cannot be empty.")

def handle_export_data():
    """Handle data export."""
    console.print("\n[bold yellow]📤 Export Data[/]")
    
    console.print("[cyan]1.[/] Export to CSV")
    console.print("[cyan]2.[/] Export to PDF")
    console.print("[cyan]3.[/] Back to main menu")
    
    choice = get_menu_choice(3)
    
    if choice == 1:
        filename = Prompt.ask("CSV filename", default="transactions.csv")
        if export_to_csv(current_user, filename):
            display_success(f"Data exported to {filename}")
        else:
            display_error("Export failed.")
    
    elif choice == 2:
        filename = Prompt.ask("PDF filename", default="expense_report.pdf")
        if export_to_pdf(current_user, filename):
            display_success(f"Report exported to {filename}")
        else:
            display_error("Export failed.")

def handle_settings():
    """Handle user settings."""
    console.print("\n[bold red]⚙️ Settings[/]")
    
    console.print("[cyan]1.[/] Change Password")
    console.print("[cyan]2.[/] View Account Info")
    console.print("[cyan]3.[/] Back to main menu")
    
    choice = get_menu_choice(3)
    
    if choice == 1:
        display_info("Password change feature - To be implemented")
    elif choice == 2:
        console.print(f"[green]Username: {current_user.username}[/]")
        console.print(f"[green]Account ID: {current_user.id}[/]")

@app.command()
def start():
    """🚀 Start the Secure Expense Tracker"""
    # Initialize database
    init_db()
    
    # Display welcome screen
    display_welcome()
    
    try:
        # Authenticate user
        authenticate_user()
        
        # Main application loop
        while True:
            console.print("\n")
            display_main_menu()
            
            choice = get_menu_choice(8)
            
            if choice == 1:
                handle_add_transaction()
            elif choice == 2:
                handle_view_transactions()
            elif choice == 3:
                handle_monthly_report()
            elif choice == 4:
                handle_spending_summary()
            elif choice == 5:
                handle_manage_categories()
            elif choice == 6:
                handle_export_data()
            elif choice == 7:
                handle_settings()
            elif choice == 8:
                if confirm_action("Are you sure you want to logout?"):
                    console.print("[cyan]Logged out successfully. Goodbye! 👋[/]")
                    break
            
            pause()
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/]")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {str(e)}[/]")
        console.print("[yellow]Please contact support if this problem persists.[/]")

@app.command()
def init():
    """🔧 Initialize the database"""
    init_db()
    console.print("[green]Database initialized successfully![/]")

@app.command()
def version():
    """📋 Show version information"""
    console.print("[cyan]Secure Expense Tracker v1.0.0[/]")
    console.print("[yellow]Created for Wells Fargo Interview - September 2025[/]")

if __name__ == "__main__":
    app()
