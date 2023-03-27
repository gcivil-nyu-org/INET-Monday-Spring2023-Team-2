import os
import unittest

from voluncheer import environment


class EnvironmentTest(unittest.TestCase):
    """Tests the various environment combinations."""

    def setUp(self):
        self.current_env = os.getenv("ENVIRONMENT_TYPE")
        if self.current_env is not None:
            del os.environ["ENVIRONMENT_TYPE"]

            def reset_environment():
                os.environ["ENVIRONMENT_TYPE"] = self.current_env

            self.addCleanup(reset_environment)

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
            development = environment._Environment(type=environment._Type.DEVELOPMENT)
            self.assertTrue(development.is_aws)
            self.assertTrue(development.is_development)
            self.assertFalse(development.is_production)
            self.assertFalse(development.is_local)
        with self.subTest("production"):
            production = environment._Environment(type=environment._Type.PRODUCTION)
            self.assertTrue(development.is_aws)
            self.assertTrue(production.is_production)
            self.assertFalse(production.is_development)
            self.assertFalse(production.is_local)
        with self.subTest("local"):
            local = environment._Environment(type=environment._Type.LOCAL)
            self.assertFalse(local.is_aws)
            self.assertTrue(local.is_local)
            self.assertFalse(local.is_development)
            self.assertFalse(local.is_production)
        with self.subTest("continuous_integration"):
            continuous_integration = environment._Environment(
                type=environment._Type.CONTINUOUS_INTEGRATION
            )
            self.assertFalse(continuous_integration.is_aws)
            self.assertFalse(continuous_integration.is_local)
            self.assertFalse(continuous_integration.is_development)
            self.assertFalse(continuous_integration.is_production)
