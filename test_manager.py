import os
import tempfile
import unittest

from manager import ExpenseManager, ValidationError
from storage import JsonStorage, StorageError


class ExpenseManagerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "expenses.json")
        self.manager = ExpenseManager(JsonStorage(self.path))

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_persist(self):
        self.manager.add(100, "food", "Lunch", "2026-11-01")
        reloaded = ExpenseManager(JsonStorage(self.path))
        self.assertEqual(len(reloaded.expenses), 1)
        self.assertEqual(reloaded.expenses[0].category, "Food")

    def test_rejects_non_positive_amount(self):
        with self.assertRaises(ValidationError):
            self.manager.add(0, "food")

    def test_rejects_bad_date(self):
        with self.assertRaises(ValidationError):
            self.manager.add(50, "food", date="01-11-2026")

    def test_delete_and_missing_id(self):
        e = self.manager.add(50, "travel")
        self.manager.delete(e.id)
        self.assertEqual(self.manager.expenses, [])
        with self.assertRaises(ValidationError):
            self.manager.delete(99)

    def test_ids_never_reused_after_delete_of_last(self):
        a = self.manager.add(10, "a")
        b = self.manager.add(20, "b")
        self.manager.delete(a.id)
        c = self.manager.add(30, "c")
        self.assertGreater(c.id, b.id)

    def test_summary_and_filter(self):
        self.manager.add(100, "food", date="2026-11-01")
        self.manager.add(50, "food", date="2026-10-05")
        self.manager.add(200, "rent", date="2026-11-02")
        nov = self.manager.filter(month="2026-11")
        self.assertEqual(self.manager.total(nov), 300)
        self.assertEqual(self.manager.by_category(self.manager.filter()),
                         {"Rent": 200.0, "Food": 150.0})

    def test_corrupt_file_raises_storage_error(self):
        with open(self.path, "w") as f:
            f.write("{not json")
        with self.assertRaises(StorageError):
            ExpenseManager(JsonStorage(self.path))


if __name__ == "__main__":
    unittest.main()
