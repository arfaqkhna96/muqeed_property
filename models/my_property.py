from odoo import fields, models, api


class MyProperty(models.Model):
    _name = 'my.property'
    _description = 'Estate Property'

    name = fields.Char(string="Property Name", required=True, )
    description = fields.Text(string="Description")
    property_type = fields.Selection([('vacant_land','Vacant Land'),('villa','Villa'),('house','House'),('commercial_space','Commercial Space')],string="Property Type")
    sales_type = fields.Selection([('sale', 'Sale'), ('rent', 'Rent')],string="Sales Type",default='sale')
    utilities = fields.Boolean(string="Utilities", default=False)
    electric_meter = fields.Boolean(string=" Electric Meter", default=False)
    water_meter = fields.Boolean(string="Water Meter", default=False)
    generator = fields.Boolean(string=" Generator", default=False)
    solar_water_heater = fields.Boolean(string="Solar Water Heater", default=False)
    amount = fields.Float(string="Amount")

    video_file = fields.Binary(string="Upload Video", max_width=1024, max_height=1024)

    image_ids = fields.One2many(
        'property.image', 'property_id', string='Property Images')

    def _process_ondelete(self):
        _logger.info("Processing ondelete for: %s", self)
        ondelete = (self.field.ondelete or {}).get(self.selection.value)
        _logger.info("ondelete value: %s", ondelete)

    @api.onchange('utilities')
    def _onchange_utilities(self):
        """Reset utility fields when 'utilities' is deselected"""
        if not self.utilities:
            self.electric_meter = False
            self.water_meter = False
            self.generator = False
            self.solar_water_heater = False

    def _compute_property_image_name(self):
        for record in self:
            # Get the file name from the image field (if available)
            if record.property_image:
                # Extract file name from binary data (base64 encoded)
                record.property_image_name = f"image_{record.id}.jpg"  # Default filename if no specific name is provided
            else:
                record.property_image_name = ''


class BranchImage(models.Model):
    _name = 'property.image'
    _description = 'Property Image'

    property_id = fields.Many2one('my.property', string='Property', required=True)
    image = fields.Binary('Image', required=True, help="Upload an image for the property.")