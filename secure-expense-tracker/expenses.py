from datetime import datetime, timedelta
from db import get_db_session, Transaction, Category, User
from crypto import encrypt_text, decrypt_text
from rich.console import Console
from rich.table import Table
from rich.progress import track
from collections import defaultdict
import calendar

console = Console()

def add_transaction(user: User, amount: float, category: str, description: str, date_str: str = None) -> bool:
    """Add a new transaction for the user."""
    session = get_db_session()
    
    try:
        # Parse date if provided, otherwise use current date
        if date_str:
            transaction_date = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            transaction_date = datetime.utcnow()
        
        # Encrypt sensitive data
        encrypted_description = encrypt_text(description) if description else ""
        
        # Create transaction
        transaction = Transaction(
            user_id=user.id,
            amount=amount,
            category=category,
            description=encrypted_description,
            date=transaction_date
        )
        
        session.add(transaction)
        session.commit()
        session.close()
        
        console.print(f"[green]Transaction saved: ${amount:.2f} for {category} 🔐[/]")
        return True
        
    except ValueError:
        console.print("[red]Invalid date format. Please use YYYY-MM-DD.[/]")
        session.close()
        return False
    except Exception as e:
        console.print(f"[red]Error saving transaction: {str(e)}[/]")
        session.close()
        return False

def list_transactions(user: User, category_filter: str = None, start_date: str = None, end_date: str = None):
    """List transactions with optional filtering."""
    session = get_db_session()
    
    # Build query
    query = session.query(Transaction).filter_by(user_id=user.id)
    
    # Apply filters
    if category_filter:
        query = query.filter(Transaction.category.ilike(f"%{category_filter}%"))
    
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Transaction.date >= start_dt)
        except ValueError:
            console.print("[red]Invalid start date format. Use YYYY-MM-DD.[/]")
            return
    
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(Transaction.date < end_dt)
        except ValueError:
            console.print("[red]Invalid end date format. Use YYYY-MM-DD.[/]")
            return
    
    transactions = query.order_by(Transaction.date.desc()).all()
    session.close()
    
    if not transactions:
        console.print("[yellow]No transactions found.[/]")
        return
    
    # Create table
    table = Table(title="💰 Your Transactions")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Date", style="magenta")
    table.add_column("Amount", style="green", justify="right")
    table.add_column("Category", style="blue")
    table.add_column("Description", style="white")
    
    total = 0
    for tx in transactions:
        decrypted_desc = decrypt_text(tx.description) if tx.description else ""
        table.add_row(
            str(tx.id),
            tx.date.strftime("%Y-%m-%d"),
            f"${tx.amount:.2f}",
            tx.category,
            decrypted_desc[:50] + "..." if len(decrypted_desc) > 50 else decrypted_desc
        )
        total += tx.amount
    
    console.print(table)
    console.print(f"\n[bold]Total: ${total:.2f}[/]")

def monthly_report(user: User, year: int = None, month: int = None):
    """Generate monthly expense report with ASCII chart."""
    session = get_db_session()
    
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    
    # Get transactions for the specified month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    transactions = session.query(Transaction).filter(
        Transaction.user_id == user.id,
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).all()
    
    session.close()
    
    if not transactions:
        console.print(f"[yellow]No transactions found for {calendar.month_name[month]} {year}.[/]")
        return
    
    # Group by category
    category_totals = defaultdict(float)
    for tx in transactions:
        category_totals[tx.category] += tx.amount
    
    # Calculate total and percentages
    total_spent = sum(category_totals.values())
    
    console.print(f"\n[bold cyan]📊 Monthly Report - {calendar.month_name[month]} {year}[/]")
    console.print(f"[bold]Total Spent: ${total_spent:.2f}[/]\n")
    
    # Create ASCII bar chart
    max_bar_length = 40
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    
    for category, amount in sorted_categories:
        percentage = (amount / total_spent) * 100
        bar_length = int((amount / max(category_totals.values())) * max_bar_length)
        bar = "█" * bar_length
        
        console.print(f"{category:12} {bar:<40} ${amount:>8.2f} ({percentage:>5.1f}%)")

def get_categories(user: User):
    """Get all available categories (default + user-defined)."""
    session = get_db_session()
    
    # Get default categories
    default_cats = session.query(Category).filter_by(is_default=1).all()
    
    # Get user-defined categories
    user_cats = session.query(Category).filter_by(user_id=user.id, is_default=0).all()
    
    session.close()
    
    all_categories = [cat.name for cat in default_cats + user_cats]
    return sorted(all_categories)

def add_custom_category(user: User, category_name: str) -> bool:
    """Add a custom category for the user."""
    session = get_db_session()
    
    # Check if category already exists
    existing = session.query(Category).filter(
        Category.name.ilike(category_name),
        ((Category.user_id == user.id) | (Category.is_default == 1))
    ).first()
    
    if existing:
        console.print(f"[yellow]Category '{category_name}' already exists.[/]")
        session.close()
        return False
    
    # Add new category
    new_category = Category(user_id=user.id, name=category_name, is_default=0)
    session.add(new_category)
    session.commit()
    session.close()
    
    console.print(f"[green]Category '{category_name}' added successfully![/]")
    return True

def delete_transaction(user: User, transaction_id: int) -> bool:
    """Delete a transaction by ID."""
    session = get_db_session()
    
    transaction = session.query(Transaction).filter_by(
        id=transaction_id, 
        user_id=user.id
    ).first()
    
    if not transaction:
        console.print("[red]Transaction not found or you don't have permission to delete it.[/]")
        session.close()
        return False
    
    session.delete(transaction)
    session.commit()
    session.close()
    
    console.print(f"[green]Transaction {transaction_id} deleted successfully.[/]")
    return True

def get_spending_summary(user: User, days: int = 30):
    """Get spending summary for the last N days."""
    session = get_db_session()
    
    start_date = datetime.utcnow() - timedelta(days=days)
    transactions = session.query(Transaction).filter(
        Transaction.user_id == user.id,
        Transaction.date >= start_date
    ).all()
    
    session.close()
    
    if not transactions:
        console.print(f"[yellow]No transactions found in the last {days} days.[/]")
        return
    
    total = sum(tx.amount for tx in transactions)
    avg_daily = total / days
    avg_per_transaction = total / len(transactions)
    
    console.print(f"\n[bold cyan]📈 Spending Summary - Last {days} Days[/]")
    console.print(f"Total Spent: ${total:.2f}")
    console.print(f"Average per Day: ${avg_daily:.2f}")
    console.print(f"Average per Transaction: ${avg_per_transaction:.2f}")
    console.print(f"Total Transactions: {len(transactions)}")
