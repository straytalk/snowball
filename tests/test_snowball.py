import unittest
import datetime

import sample_debts
from snowball import PaymentCalculator


class TestSnowball(unittest.TestCase):

    def test_pays_off_with_large_payment(self):
        debts = sample_debts.debts
        today = datetime.date.today()
        total_principal = sum(d['principal'] for d in debts.values())
        # make monthly payment large enough to pay down everything quickly
        model = PaymentCalculator(debts, total_principal * 2, today)
        schedule = model.activate()
        # all debts should be paid off
        self.assertEqual(model.debts, [])
        # schedule should be a list [header, rows]
        self.assertIsInstance(schedule, list)
        self.assertEqual(len(schedule), 2)
        header, rows = schedule
        for loan_name in debts.keys():
            self.assertIn(loan_name, header)

    def test_ordering_by_interest_then_principal(self):
        debts = {
            'a': {'principal': 100, 'interest': 0.05},
            'b': {'principal': 50, 'interest': 0.06},
            'c': {'principal': 75, 'interest': 0.05}
        }
        today = datetime.date.today()
        model = PaymentCalculator(debts, 1000, today)
        ordered = [loan.name for loan in model.debts]
        # expected order: highest interest first (b), then within same interest by principal ascending (c then a)
        self.assertEqual(ordered, ['b', 'c', 'a'])


if __name__ == "__main__":
    unittest.main()
