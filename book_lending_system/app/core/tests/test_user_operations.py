"""
Tests for user-related core operations
"""
import unittest
import sys
import os
from uuid import uuid4

# Add project root directory to path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.core.entities.user import User
from app.core.tests.test_mock_repositories import MockUserRepository

class TestUserOperations(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.user_repo = MockUserRepository()
    
    def tearDown(self):
        """Tear down test fixtures after each test method"""
        self.user_repo.clear()
    
    def test_add_user(self):
        """Test adding a user to the repository"""
        # Arrange
        user = User(name="John Doe")
        
        # Act
        self.user_repo.add(user)
        
        # Assert
        retrieved_user = self.user_repo.get(user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.name, "John Doe")
        self.assertEqual(retrieved_user.id, user.id)
    
    def test_get_user(self):
        """Test retrieving a user from the repository"""
        # Arrange
        user = User(name="Jane Smith")
        self.user_repo.add(user)
        
        # Act
        retrieved_user = self.user_repo.get(user.id)
        
        # Assert
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.name, "Jane Smith")
    
    def test_get_nonexistent_user(self):
        """Test retrieving a non-existent user"""
        # Act
        retrieved_user = self.user_repo.get(uuid4())
        
        # Assert
        self.assertIsNone(retrieved_user)
    
    def test_list_users(self):
        """Test listing all users"""
        # Arrange
        user1 = User(name="User One")
        user2 = User(name="User Two")
        user3 = User(name="User Three")
        
        self.user_repo.add(user1)
        self.user_repo.add(user2)
        self.user_repo.add(user3)
        
        # Act
        users = self.user_repo.list()
        
        # Assert
        self.assertEqual(len(users), 3)
        self.assertIn(user1, users)
        self.assertIn(user2, users)
        self.assertIn(user3, users)