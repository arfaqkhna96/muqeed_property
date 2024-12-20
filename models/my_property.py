from tokenize import String

from odoo import fields, models, api


class MyProperty(models.Model):
    _name = 'my.property'
    _description = 'Estate Property'

    name = fields.Char(string="Property Name", required=True, )
    description = fields.Text(string="Description")
    property_type = fields.Selection([('vacant_land','Vacant Land'),('villa','Villa'),('house','House'),('commercial_space','Commercial Space')],string="Property Type")
    city = fields.Char(string="City")
    sales_type = fields.Selection([('sale', 'Sale'), ('rent', 'Rent')],string="Sales Type",default='sale')
    property_area = fields.Char(string="Property Area")
    bedrooms = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')],string="Bedrooms",default='1')
    bathrooms = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')],
                                string="Bathrooms", default='1')
    availability = fields.Boolean(string="Availability", default=False)
    balcony = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')],string="Balcony",default='1')
    amount = fields.Integer(string="Amount")
    address = fields.Text(string="Address")

    features_ids=    fields.Many2many('property.features',String="Features")

    video_file = fields.Binary(string="Upload Video", max_width=1024, max_height=1024)

    image_ids = fields.One2many(
        'property.image', 'property_id', string='Property Images')



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

class Features(models.Model):
    _name = 'property.features'
    _description = 'Property Features'
    name= fields.Char(string="Features")
