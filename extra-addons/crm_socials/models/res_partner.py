import validators as validate
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SocialLinks(models.Model):
    _inherit = "res.partner"

    facebook_url = fields.Char(string="Facebook URL", translate=True)
    linkedin_url = fields.Char(string="LinkedIn URL", translate=True)
    x_url = fields.Char(string="X URL", translate=True)
    is_profile_completed = fields.Boolean(
        compute="_compute_profile_completed", index=True, store=True
    )

    @api.depends("facebook_url", "linkedin_url", "x_url")
    def _compute_profile_completed(self) -> None:
        for record in self:
            record.is_profile_completed = all(
                [record.facebook_url, record.linkedin_url, record.x_url]
            )

    @api.constrains("facebook_url", "linkedin_url", "x_url")
    def _check_social_urls(self) -> None:
        for record in self:
            if record.facebook_url and not validate.url(record.facebook_url):
                raise ValidationError(_("Invalid Facebook URL"))
            if record.linkedin_url and not validate.url(record.linkedin_url):
                raise ValidationError(_("Invalid LinkedIn URL"))
            if record.x_url and not validate.url(record.x_url):
                raise ValidationError(_("Invalid X URL"))
