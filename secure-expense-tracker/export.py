import csv
import os
from datetime import datetime
from db import get_db_session, Transaction
from crypto import decrypt_text
from rich.console import Console
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from collections import defaultdict

console = Console()

def export_to_csv(user, filename: str = "transactions.csv") -> bool:
    """Export user transactions to CSV file."""
    try:
        session = get_db_session()
        transactions = session.query(Transaction).filter_by(user_id=user.id).order_by(Transaction.date.desc()).all()
        session.close()
        
        if not transactions:
            console.print("[yellow]No transactions to export.[/]")
            return False
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['ID', 'Date', 'Amount', 'Category', 'Description'])
            
            # Write transactions
            for tx in transactions:
                decrypted_desc = decrypt_text(tx.description) if tx.description else ""
                writer.writerow([
                    tx.id,
                    tx.date.strftime('%Y-%m-%d %H:%M:%S'),
                    tx.amount,
                    tx.category,
                    decrypted_desc
                ])
        
        console.print(f"[green]Exported {len(transactions)} transactions to {filename}[/]")
        return True
        
    except Exception as e:
        console.print(f"[red]Export failed: {str(e)}[/]")
        return False

def export_to_pdf(user, filename: str = "expense_report.pdf") -> bool:
    """Export user transactions and summary to PDF file."""
    try:
        session = get_db_session()
        transactions = session.query(Transaction).filter_by(user_id=user.id).order_by(Transaction.date.desc()).all()
        session.close()
        
        if not transactions:
            console.print("[yellow]No transactions to export.[/]")
            return False
        
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph(f"<b>Expense Report - {user.username}</b>", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Summary statistics
        total_amount = sum(tx.amount for tx in transactions)
        category_totals = defaultdict(float)
        for tx in transactions:
            category_totals[tx.category] += tx.amount
        
        summary_text = f"""
        <b>Summary:</b><br/>
        Total Transactions: {len(transactions)}<br/>
        Total Amount: ${total_amount:.2f}<br/>
        Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        summary = Paragraph(summary_text, styles['Normal'])
        story.append(summary)
        story.append(Spacer(1, 20))
        
        # Category breakdown
        category_text = "<b>Spending by Category:</b><br/>"
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_amount) * 100
            category_text += f"{category}: ${amount:.2f} ({percentage:.1f}%)<br/>"
        
        category_para = Paragraph(category_text, styles['Normal'])
        story.append(category_para)
        story.append(Spacer(1, 20))
        
        # Transactions table
        transactions_title = Paragraph("<b>All Transactions:</b>", styles['Heading2'])
        story.append(transactions_title)
        story.append(Spacer(1, 10))
        
        # Prepare table data
        table_data = [['Date', 'Amount', 'Category', 'Description']]
        for tx in transactions[:50]:  # Limit to first 50 transactions for PDF
            decrypted_desc = decrypt_text(tx.description) if tx.description else ""
            table_data.append([
                tx.date.strftime('%Y-%m-%d'),
                f"${tx.amount:.2f}",
                tx.category,
                decrypted_desc[:30] + "..." if len(decrypted_desc) > 30 else decrypted_desc
            ])
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        
        if len(transactions) > 50:
            note = Paragraph(f"<i>Note: Only showing first 50 transactions. Total: {len(transactions)}</i>", styles['Normal'])
            story.append(Spacer(1, 10))
            story.append(note)
        
        # Build PDF
        doc.build(story)
        
        console.print(f"[green]PDF report exported to {filename}[/]")
        return True
        
    except Exception as e:
        console.print(f"[red]PDF export failed: {str(e)}[/]")
        return False

def backup_database(backup_filename: str = None) -> bool:
    """Create a backup of the database."""
    try:
        if not backup_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"tracker_backup_{timestamp}.db"
        
        import shutil
        shutil.copy2("tracker.db", backup_filename)
        
        console.print(f"[green]Database backed up to {backup_filename}[/]")
        return True
        
    except Exception as e:
        console.print(f"[red]Backup failed: {str(e)}[/]")
        return False
