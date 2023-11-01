from solutions.CHK import checkout_solution


class TestCHK():
    def test_basket(self):
        assert checkout_solution.checkout.compute(['A','A','A','A','B','B','C']) == 245

    def test_basket_fail(self):
        assert checkout_solution.checkout.compute(['A','A','A','A','B','B','C','E']) == -1




