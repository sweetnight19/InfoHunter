import unittest

from osint.config import Settings


class SettingsTests(unittest.TestCase):
    def test_reads_known_api_keys_from_injected_environment(self):
        settings = Settings.from_environment({"HIBP_API_KEY": "  test-secret  "})
        self.assertEqual(settings.api_key("HIBP_API_KEY"), "test-secret")
        self.assertIsNone(settings.api_key("VT_API_KEY"))

    def test_status_never_includes_secret_values(self):
        settings = Settings.from_environment({"HIBP_API_KEY": "private-secret"})
        self.assertEqual(settings.api_key_status()[0], {
            "Servicio": "Have I Been Pwned",
            "Estado": "Configurada",
        })
        self.assertNotIn("private-secret", repr(settings))
        self.assertNotIn("private-secret", repr(settings.api_key_status()))

    def test_unknown_key_is_a_programming_error(self):
        with self.assertRaises(KeyError):
            Settings.from_environment({}).api_key("UNKNOWN_KEY")


if __name__ == "__main__":
    unittest.main()
