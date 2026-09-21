import unittest
from Models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def test_id(self):
        model = BaseModel()

        self.assertIsNotNone(model.id)
        self.assertIsInstance(model.id, str)

    def test_created_at(self):
        model = BaseModel()

        self.assertIsNotNone(model.created_at)

    def test_updated_at(self):
        model = BaseModel()

        self.assertEqual(model.created_at, model.updated_at)

    def test_to_dict(self):
        model = BaseModel()

        data = model.to_dict()

        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], model.id)
        self.assertEqual(data["created_at"], model.created_at.isoformat())
        self.assertEqual(data["updated_at"], model.updated_at.isoformat())


if __name__ == "__main__":
    unittest.main()