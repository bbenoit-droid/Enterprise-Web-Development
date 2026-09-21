#!/usr/bin/python3
"""Tests for the BaseModel class."""

import unittest
from Models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel."""

    def test_create_object(self):
        """Test that a BaseModel object can be created."""

        my_model = BaseModel()

        self.assertIsInstance(my_model, BaseModel)

    def test_id(self):
        """Test that id is a string."""

        my_model = BaseModel()

        self.assertIsInstance(my_model.id, str)

    def test_created_at(self):
        """Test that created_at exists."""

        my_model = BaseModel()

        self.assertIsNotNone(my_model.created_at)

    def test_updated_at(self):
        """Test that updated_at exists."""

        my_model = BaseModel()

        self.assertIsNotNone(my_model.updated_at)

    def test_to_dict(self):
        """Test the to_dict method."""

        my_model = BaseModel()

        dictionary = my_model.to_dict()

        self.assertIsInstance(dictionary, dict)
        self.assertEqual(dictionary["__class__"], "BaseModel")
        self.assertEqual(dictionary["id"], my_model.id)

    def test_str(self):
        """Test the __str__ method."""

        my_model = BaseModel()

        result = str(my_model)

        self.assertIn("BaseModel", result)
        self.assertIn(my_model.id, result)

    def test_save(self):
        """Test that save updates updated_at."""

        my_model = BaseModel()

        old_updated_at = my_model.updated_at

        my_model.save()

        self.assertNotEqual(old_updated_at, my_model.updated_at)


if __name__ == "__main__":
    unittest.main()