import bcrypt
import os
from datetime import datetime, timedelta
from db import get_db_session, User
from rich.console import Console

console = Console()

def generate_salt():
    """Generate a random salt for password hashing."""
    return bcrypt.gensalt().decode('utf-8')

def hash_password(password: str, salt: str) -> str:
    """Hash a password with salt using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

def verify_password(password: str, hashed: str, salt: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def is_user_locked(user: User) -> bool:
    """Check if user account is locked due to failed attempts."""
    if user.locked_until and datetime.utcnow() < user.locked_until:
        return True
    elif user.locked_until and datetime.utcnow() >= user.locked_until:
        # Unlock the user if lock period has expired
        session = get_db_session()
        user.failed_attempts = 0
        user.locked_until = None
        session.commit()
        session.close()
    return False

def lock_user(user: User):
    """Lock user account for 30 minutes after 3 failed attempts."""
    session = get_db_session()
    user.failed_attempts += 1
    
    if user.failed_attempts >= 3:
        user.locked_until = datetime.utcnow() + timedelta(minutes=30)
        console.print("[red]Account locked for 30 minutes due to multiple failed attempts.[/]")
    
    session.commit()
    session.close()

def reset_failed_attempts(user: User):
    """Reset failed login attempts on successful login."""
    session = get_db_session()
    user.failed_attempts = 0
    user.locked_until = None
    session.commit()
    session.close()

def signup(username: str, password: str) -> bool:
    """Create a new user account."""
    session = get_db_session()
    
    # Check if username already exists
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        console.print("[red]Username already exists. Please choose a different username.[/]")
        session.close()
        return False
    
    # Validate password strength
    if not is_password_strong(password):
        console.print("[red]Password must be at least 8 characters long and contain uppercase, lowercase, and numbers.[/]")
        session.close()
        return False
    
    # Create new user
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    
    new_user = User(username=username, password=hashed_password, salt=salt)
    session.add(new_user)
    session.commit()
    session.close()
    
    console.print(f"[green]Account created successfully for {username}![/]")
    return True

def login(username: str, password: str) -> User:
    """Authenticate user login."""
    session = get_db_session()
    user = session.query(User).filter_by(username=username).first()
    
    if not user:
        console.print("[red]Invalid username or password.[/]")
        session.close()
        return None
    
    if is_user_locked(user):
        remaining_time = (user.locked_until - datetime.utcnow()).seconds // 60
        console.print(f"[red]Account is locked. Try again in {remaining_time} minutes.[/]")
        session.close()
        return None
    
    if verify_password(password, user.password, user.salt):
        reset_failed_attempts(user)
        console.print(f"[green]Welcome back, {username}![/]")
        session.close()
        return user
    else:
        lock_user(user)
        console.print("[red]Invalid username or password.[/]")
        session.close()
        return None

def is_password_strong(password: str) -> bool:
    """Check if password meets security requirements."""
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit
