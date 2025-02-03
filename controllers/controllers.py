import logging

from odoo.http import request

from odoo import http

_logger = logging.getLogger(__name__)


class PropertyResale(http.Controller):
    @http.route('/', auth='public', website=True)
    def property_resale_page(self):
        properties = request.env['my.property'].sudo().search([])
        return request.render('muqeed_property.property_resale_template',
                              {
                                  'properties': properties
                              })


class Properties(http.Controller):
    @http.route('/properties', auth='public', website=True)
    def properties(self, sales=None, prop=None, min=None, max=None, minArea=None, maxArea=None, **kwargs):
        # Default filter values
        sales_filter = sales if sales in ['sale', 'rent'] else 'all'
        prop_filter = prop if prop in ['vacant_land', 'villa', 'house', 'commercial_space'] else 'all'

        # Build the domain for filtering properties
        domain = []

        # Sales type filter
        if sales_filter != 'all':
            domain.append(('sales_type', '=', sales_filter))

        # Property type filter
        if prop_filter != 'all':
            domain.append(('property_type', '=', prop_filter))

        # Price range filter
        if min and min.isdigit():
            domain.append(('amount', '>=', float(min)))
        if max and max.isdigit():
            domain.append(('amount', '<=', float(max)))

        # Area range filter
        if minArea and minArea.isdigit():
            domain.append(('property_area', '>=', float(minArea)))
        if maxArea and maxArea.isdigit():
            domain.append(('property_area', '<=', float(maxArea)))

        # Search for properties based on the constructed domain
        properties = request.env['my.property'].sudo().search(domain)

        # Pass data to the template
        return request.render('muqeed_property.my_property_template', {
            'properties': properties,
            'selected_sales_type': sales_filter,
            'selected_property_type': prop_filter,
            'min_price': min,
            'max_price': max,
            'min_area': minArea,
            'max_area': maxArea,
        })


class PropertyDetailController(http.Controller):
    @http.route('/property/detail/<int:property_id>', auth='public', website=True)
    def property_detail(self, property_id, **kwargs):
        properties = request.env['my.property'].sudo().search([])
        property = request.env['my.property'].sudo().browse(property_id)
        if not property:
            return request.not_found()

        return request.render('muqeed_property.property_detail_template', {
            'property': property,
            'properties': properties
        })


class PropertyController(http.Controller):

    @http.route('/properties/rent', type='http', auth='public', website=True)
    def properties_rent(self, **kwargs):
        properties = request.env['my.property'].search([('sales_type', '=', 'rent')])
        return request.render('muqeed_property.my_property_template', {
            'properties': properties,
            'filter_type': 'rent'
        })

    @http.route('/properties/sale', type='http', auth='public', website=True)
    def properties_sale(self, **kwargs):
        properties = request.env['my.property'].search([('sales_type', '=', 'sale')])
        return request.render('muqeed_property.my_property_template', {
            'properties': properties,
            'filter_type': 'sale'
        })

    @http.route('/properties/max_amount', type='json', auth='public')
    def get_max_amount(self):
        max_amount = request.env['my.property'].sudo().search([], limit=1, order='amount desc').amount
        return {'max_amount': max_amount or 0}


class MyPropertyController(http.Controller):

    @http.route('/properties/type/<string:property_type>', type='http', auth='public', website=True)
    def properties_by_type(self, property_type, **kwargs):
        if property_type == 'all':
            properties = request.env['my.property'].search([])
        else:
            properties = request.env['my.property'].search([('property_type', '=', property_type)])

        return request.render('muqeed_property.my_property_template', {
            'properties': properties,
            'selected_property_type': property_type  # Pass the selected property type
        })


class ContactUs(http.Controller):

    @http.route('/contact', type='http', auth='public', website=True)
    def contact_us(self, **kwargs):
        return request.render('muqeed_property.contact_us_template')

    @http.route('/contact/thanks', type='http', auth='public', website=True)
    def thanks_page(self, **kwargs):
        return request.render('muqeed_property.thanks_template')

    @http.route('/contact/submit', type='http', auth='public', website=True, csrf=False)
    def submit_contact(self, **kwargs):
        # Process form data
        name = kwargs.get('name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        message = kwargs.get('message')

        # Save the data to the `contact.us.message` model
        request.env['contact.us.message'].sudo().create({
            'name': name,
            'phone': phone,
            'email': email,
            'message': message,
        })

        return request.redirect('/contact/thanks')


class PropertyController1(http.Controller):
    @http.route('/properties/map', type='http', auth='public', website=True)
    def property_map(self, property_id=None):
        properties = request.env['my.property'].sudo().search([])
        selected_property = None
        if property_id:
            selected_property = request.env['my.property'].sudo().browse(int(property_id))
            if not selected_property.exist():
                selected_property = None

        return request.render('muqeed_property.property_detail_template', {
            'properties': properties,
            'selected_property': selected_property,
        })

class PropertyInterest(http.Controller):
    @http.route('/property_interest/submit', type='http', auth='public', methods=['POST'], csrf=True)
    def submit_interest(self, **post):
        request.env['property.interested.message'].create({
            'name': post.get('name'),
            'phone': post.get('phone'),
            'email': post.get('email'),
            'property_id': post.get('property_id'),
            'message': post.get('message'),
        })
        return request.redirect('/contact/thanks')
