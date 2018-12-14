from odoo.tests.common import TransactionCase




class TestROP(TransactionCase):

    def setUp(self):
        super(TestROP, self).setUp()

    def test_rop(self):
        # Test case #1
        test_case = 1
        category = self.env['product.category'].create({'id': test_case,
                                                        'name': 'Testing Category',
                                                        'enable_auto_rop': True})
        product = self.env['product.product'].create({'id': test_case,
                                                      'name': '{0} {1}'.format('Testing Product'),
                                                      'enable_auto_rop': True})
        orderpoint = self.env['stock.warehouse.orderpoint'].create({'id': test_case,
                                                                    'lead_days': 0,
                                                                    'product_min_qty': 0,
                                                                    'product_max_qty': 0,
                                                                    'product_safety_qty': 0,
                                                                    'product_id': product.id})
        results = product.compute_rop()
        self.assertEqual(0, orderpoint.lead_days)
        self.assertEqual(0, orderpoint.product_min_qty)
        self.assertEqual(0, orderpoint.product_max_qty)
        category.unlink()
        product.unlink()
        orderpoint.unlink()
        for result in results:
            result.unlink()

        # Test case #1a
        test_case = 10001
        product = self.env['product.product'].create({'id': test_case,
                                                      'name': '{0} {1}'.format('Testing Product')})
        orderpoint = self.env['stock.warehouse.orderpoint'].create({'id': test_case,
                                                                    'lead_days': 0,
                                                                    'product_min_qty': 0,
                                                                    'product_max_qty': 0,
                                                                    'product_safety_qty': 0,
                                                                    'product_id': product.id})
        results = product.compute_rop()
        self.assertEqual(0, orderpoint.lead_days)
        self.assertEqual(0, orderpoint.product_min_qty)
        self.assertEqual(0, orderpoint.product_max_qty)
        product.unlink()
        orderpoint.unlink()
        for result in results:
            result.unlink()

        # Test case #1b
        test_case = 10002
        category = self.env['product.category'].create({'id': test_case,
                                                        'name': 'Testing Category',
                                                        'enable_auto_rop': False})
        product = self.env['product.product'].create({'id': test_case,
                                                      'name': '{0} {1}'.format('Testing Product')})
        orderpoint = self.env['stock.warehouse.orderpoint'].create({'id': test_case,
                                                                    'lead_days': 0,
                                                                    'product_min_qty': 0,
                                                                    'product_max_qty': 0,
                                                                    'product_safety_qty': 0,
                                                                    'product_id': product.id})
        results = product.compute_rop()
        self.assertEqual(0, orderpoint.lead_days)
        self.assertEqual(0, orderpoint.product_min_qty)
        self.assertEqual(0, orderpoint.product_max_qty)
        category.unlink()
        product.unlink()
        orderpoint.unlink()
        for result in results:
            result.unlink()

        # Test case #1c
        test_case = 10003
        category = self.env['product.category'].create({'id': test_case,
                                                        'name': 'Testing Category',
                                                        'enable_auto_rop': True})
        product = self.env['product.product'].create({'id': test_case,
                                                      'name': '{0} {1}'.format('Testing Product'),
                                                      'enable_auto_rop': False})
        orderpoint = self.env['stock.warehouse.orderpoint'].create({'id': test_case,
                                                                    'lead_days': 0,
                                                                    'product_min_qty': 0,
                                                                    'product_max_qty': 0,
                                                                    'product_safety_qty': 0,
                                                                    'product_id': product.id})
        results = product.compute_rop()
        self.assertEqual(0, orderpoint.lead_days)
        self.assertEqual(0, orderpoint.product_min_qty)
        self.assertEqual(0, orderpoint.product_max_qty)
        category.unlink()
        product.unlink()
        orderpoint.unlink()
        for result in results:
            result.unlink()


