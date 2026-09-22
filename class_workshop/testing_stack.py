import unittest
from stack import Stack


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    def test_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty())

    def test_push(self):
        self.stack.push(10)

        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 1)

    def test_peek(self):
        self.stack.push(10)
        self.stack.push(20)

        self.assertEqual(self.stack.peek(), 20)
        self.assertEqual(self.stack.size(), 2)

    def test_pop(self):
        self.stack.push(10)
        self.stack.push(20)

        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.pop(), 10)
        self.assertTrue(self.stack.is_empty())

    def test_lifo(self):
        self.stack.push(10)
        self.stack.push(20)
        self.stack.push(30)

        self.assertEqual(self.stack.pop(), 30)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.pop(), 10)

    def test_pop_empty_stack(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek_empty_stack(self):
        with self.assertRaises(IndexError):
            self.stack.peek()


if __name__ == "__main__":
    unittest.main()