import unittest

from osint.input_validation import validate_target


class InputValidationTests(unittest.TestCase):
    def test_normalizes_domain(self):
        self.assertEqual(validate_target("Dominio", " Example.COM. "), "example.com")

    def test_normalizes_email_domain(self):
        self.assertEqual(validate_target("Email", "User@Example.COM"), "User@example.com")

    def test_accepts_username(self):
        self.assertEqual(validate_target("Usuario", "john_doe"), "john_doe")

    def test_rejects_unsafe_username_paths_and_options(self):
        for target in ("../user", r"..\\user", "--help"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                validate_target("Usuario", target)

    def test_rejects_bad_domain_and_email(self):
        for kind, target in (("Dominio", "https://example.com/path"), ("Email", "a..b@example.com"), ("Email", "missing-at")):
            with self.subTest(kind=kind, target=target), self.assertRaises(ValueError):
                validate_target(kind, target)
