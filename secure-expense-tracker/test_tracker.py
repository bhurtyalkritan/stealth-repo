import pytest
import tempfile
import os
from datetime import datetime, timedelta
from db import init_db, get_db_session, User, Transaction
from auth import signup, login, hash_password, verify_password, generate_salt
from expenses import add_transaction, list_transactions
from crypto import encrypt_text, decrypt_text

class TestAuth:
    def setup_method(self):
        """Setup test database."""
        # Use in-memory database for testing
        os.environ['DATABASE_URL'] = 'sqlite:///test.db'
        init_db()
    
    def teardown_method(self):
        """Clean up test database."""
        if os.path.exists('test.db'):
            os.remove('test.db')
        if os.path.exists('secret.key'):
            os.remove('secret.key')
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "TestPassword123"
        salt = generate_salt()
        hashed = hash_password(password, salt)
        
        assert verify_password(password, hashed, salt)
        assert not verify_password("WrongPassword", hashed, salt)
    
    def test_user_signup(self):
        """Test user registration."""
        result = signup("testuser", "TestPass123")
        assert result == True
        
        # Test duplicate username
        result = signup("testuser", "AnotherPass123")
        assert result == False
    
    def test_user_login(self):
        """Test user login."""
        # First create a user
        signup("testuser", "TestPass123")
        
        # Test successful login
        user = login("testuser", "TestPass123")
        assert user is not None
        assert user.username == "testuser"
        
        # Test failed login
        user = login("testuser", "WrongPassword")
        assert user is None

class TestCrypto:
    def test_encryption_decryption(self):
        """Test text encryption and decryption."""
        original_text = "This is sensitive transaction data"
        
        encrypted = encrypt_text(original_text)
        assert encrypted != original_text
        
        decrypted = decrypt_text(encrypted)
        assert decrypted == original_text
    
    def test_empty_text_encryption(self):
        """Test encryption of empty strings."""
        encrypted = encrypt_text("")
        decrypted = decrypt_text(encrypted)
        assert decrypted == ""

class TestExpenses:
    def setup_method(self):
        """Setup test environment."""
        os.environ['DATABASE_URL'] = 'sqlite:///test.db'
        init_db()
        
        # Create test user
        session = get_db_session()
        salt = generate_salt()
        hashed_password = hash_password("TestPass123", salt)
        self.test_user = User(username="testuser", password=hashed_password, salt=salt)
        session.add(self.test_user)
        session.commit()
        session.close()
    
    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists('test.db'):
            os.remove('test.db')
        if os.path.exists('secret.key'):
            os.remove('secret.key')
    
    def test_add_transaction(self):
        """Test adding a transaction."""
        result = add_transaction(self.test_user, 50.0, "Food", "Test meal", "2025-09-20")
        assert result == True
        
        # Verify transaction was added
        session = get_db_session()
        transactions = session.query(Transaction).filter_by(user_id=self.test_user.id).all()
        assert len(transactions) == 1
        assert transactions[0].amount == 50.0
        assert transactions[0].category == "Food"
        session.close()
    
    def test_transaction_encryption(self):
        """Test that transaction descriptions are encrypted."""
        description = "Sensitive transaction details"
        add_transaction(self.test_user, 25.0, "Transport", description)
        
        session = get_db_session()
        transaction = session.query(Transaction).filter_by(user_id=self.test_user.id).first()
        
        # Description should be encrypted in database
        assert transaction.description != description
        
        # But should decrypt correctly
        decrypted = decrypt_text(transaction.description)
        assert decrypted == description
        session.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
