import unittest
from types import SimpleNamespace as N
from core import answer, redact, PRODUCTS
from media import banner
class FakeClient:
    chat=N(completions=N(create=lambda **kwargs:N(choices=[N(message=N(content='Verified response'))])))
class Tests(unittest.TestCase):
    def test_price(self): self.assertEqual(answer('Price of mouse?',FakeClient()),'Mouse: ₹599')
    def test_budget(self): self.assertEqual(answer('Product under 1000',FakeClient()),'Mouse: ₹599\nKeyboard: ₹999')
    def test_order(self): self.assertIn('Shipped',answer('Where is ORD001?',FakeClient()))
    def test_unknown(self): self.assertIn('HUMAN_HANDOFF',answer('Where is ORD999?',FakeClient()))
    def test_return(self): self.assertTrue(answer('Return after 15 days?',FakeClient()).startswith('No.'))
    def test_redact(self): self.assertNotIn('test@example.com',redact('test@example.com'))
    def test_banner(self): self.assertTrue(banner(PRODUCTS[0]).startswith(b'\x89PNG'))
if __name__=='__main__': unittest.main()
