from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSocialLinksModel(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})

    def test_profile_completed_all_urls(self):
        """Test that the profile is marked as complete when all URLs are present"""
        self.partner.write(
            {
                "facebook_url": "https://facebook.com/user",
                "linkedin_url": "https://linkedin.com/in/user",
                "x_url": "https://x.com/user",
            }
        )
        self.assertTrue(self.partner.is_profile_completed)

    def test_profile_completed_missing_one_url(self):
        """Test that the profile is not marked as complete when one URL is missing"""
        self.partner.write(
            {
                "facebook_url": "https://facebook.com/user",
                "linkedin_url": "https://linkedin.com/in/user",
                "x_url": False,
            }
        )
        self.assertFalse(self.partner.is_profile_completed)

    def test_profile_completed_no_urls(self):
        """Test that the profile is not marked as complete when no URLs are present"""
        self.partner.write(
            {"facebook_url": False, "linkedin_url": False, "x_url": False}
        )
        self.assertFalse(self.partner.is_profile_completed)

    def test_valid_urls_no_error(self):
        """Test that valid URLs do not raise errors"""
        valid_data = {
            "facebook_url": "https://facebook.com/user",
            "linkedin_url": "https://linkedin.com/in/user",
            "x_url": "https://x.com/user",
        }
        self.partner.write(valid_data)

    def test_invalid_facebook_url(self):
        """Test invalid Facebook URL"""
        with self.assertRaises(ValidationError) as context:
            self.partner.write({"facebook_url": "invalid-url"})
        self.assertIn("Invalid Facebook URL", context.exception.args[0])

    def test_invalid_linkedin_url(self):
        """Test invalid LinkedIn URL"""
        with self.assertRaises(ValidationError) as context:
            self.partner.write({"linkedin_url": "linkedin.com/invalid"})
        self.assertIn("Invalid LinkedIn URL", context.exception.args[0])

    def test_invalid_x_url(self):
        """Test invalid X URL"""
        with self.assertRaises(ValidationError) as context:
            self.partner.write({"x_url": "x.invalid/user"})
        self.assertIn("Invalid X URL", context.exception.args[0])

    def test_empty_urls_allowed(self):
        """Test that empty URLs are allowed"""
        self.partner.write({"facebook_url": False, "linkedin_url": None, "x_url": ""})

    def test_partial_urls_allowed(self):
        """Test that having some empty URLs is allowed"""
        self.partner.write(
            {
                "facebook_url": "https://facebook.com/user",
                "linkedin_url": False,
                "x_url": "https://x.com/user",
            }
        )
