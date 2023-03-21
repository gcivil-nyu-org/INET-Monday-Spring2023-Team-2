import unittest

from voluncheer import environment


class EnvironmentTest(unittest.TestCase):
    """Tests the various environment combinations."""

    def test_default_environment(self):
        """Tests the default environment initializes correctly."""
        default = environment._Environment()

        with self.subTest("type"):
            got = default.type
            want = environment._Type.LOCAL
            self.assertEqual(got, want)
            self.assertTrue(default.is_local)
            self.assertFalse(default.is_development)
            self.assertFalse(default.is_production)

    def test_type(self):
        """Tests environment types and type properties are mutually exclusive."""
        with self.subTest("development"):
            development = environment._Environment(
                type=environment._Type.DEVELOPMENT, secret_key="other"
            )
            self.assertTrue(development.is_development)
            self.assertFalse(development.is_production)
            self.assertFalse(development.is_local)
        with self.subTest("production"):
            production = environment._Environment(
                type=environment._Type.PRODUCTION, secret_key="other"
            )
            self.assertTrue(production.is_production)
            self.assertFalse(production.is_development)
            self.assertFalse(production.is_local)
        with self.subTest("local"):
            local = environment._Environment(type=environment._Type.LOCAL, secret_key="other")
            self.assertTrue(local.is_local)
            self.assertFalse(local.is_development)
            self.assertFalse(local.is_production)
