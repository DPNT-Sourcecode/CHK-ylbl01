from solutions.CHK import checkout


class TestCHK():
    def test_basket(self):
        assert checkout.compute(['A','A','A','A','B','B','C']) == 245

    def test_basket_fail(self):
        assert checkout.compute(['A','A','A','A','B','B','C','E']) == -1



