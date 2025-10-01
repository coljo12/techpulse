from django.test import TestCase, Client


class SmokeTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sources_list(self):
        """GET /api/news/sources/ should return 200 and a JSON list"""
        resp = self.client.get('/api/news/sources/', follow=True)
        self.assertEqual(resp.status_code, 200)
        # Basic content checks
        self.assertTrue(resp['Content-Type'].startswith('application/json'))
        data = resp.json()
        # Expect a list (DRF ListAPIView) or dict with 'results'
        self.assertTrue(isinstance(data, (list, dict)))

