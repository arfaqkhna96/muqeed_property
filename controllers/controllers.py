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
    def properties(self, sales=None, prop=None, min=None, max=None, **kwargs):
        # Default filter values
        sales_filter = sales if sales in ['sale', 'rent'] else 'all'
        prop_filter = prop if prop in ['vacant_land', 'villa', 'house', 'commercial_space'] else 'all'

        # Build the domain for filtering properties
        domain = []
        if sales_filter != 'all':
            domain.append(('sales_type', '=', sales_filter))
        if prop_filter != 'all':
            domain.append(('property_type', '=', prop_filter))

        # Handle price range filtering
        if min and min.isdigit():
            domain.append(('amount', '>=', float(min)))
        if max and max.isdigit():
            domain.append(('amount', '<=', float(max)))

        # Search for properties based on the constructed domain
        properties = request.env['my.property'].sudo().search(domain)

        # Pass data to the template
        return request.render('muqeed_property.my_property_template', {
            'properties': properties,
            'selected_sales_type': sales_filter,
            'selected_property_type': prop_filter,
            'min_price': min,
            'max_price': max,
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

