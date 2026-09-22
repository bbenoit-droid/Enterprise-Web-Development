import unittest
from queue import Queue


class TestQueue(unittest.TestCase):

    def setUp(self):
        self.queue = Queue()

    def test_queue_is_empty(self):
        self.assertTrue(self.queue.is_empty())

    def test_enqueue(self):
        self.queue.enqueue(10)

        self.assertFalse(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 1)

    def test_peek(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)

        self.assertEqual(self.queue.peek(), 10)
        self.assertEqual(self.queue.size(), 2)

    def test_dequeue(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)

        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.dequeue(), 20)
        self.assertTrue(self.queue.is_empty())

    def test_fifo(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.enqueue(30)

        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.dequeue(), 20)
        self.assertEqual(self.queue.dequeue(), 30)

    def test_dequeue_empty_queue(self):
        with self.assertRaises(IndexError):
            self.queue.dequeue()

    def test_peek_empty_queue(self):
        with self.assertRaises(IndexError):
            self.queue.peek()


if __name__ == "__main__":
    unittest.main()