#!/bin/bash
set -e

# Stop Odoo service
sudo systemctl stop odoo

# Navigate to Odoo directory
cd /opt/odoo/odoo/custom_modules/muqeed_property

# Pull latest code from the specified branch
git pull origin master



# Apply migrations (if necessary)
./odoo-bin -c /etc/odoo.conf -d real_estate --stop-after-init -u all

# Start Odoo service
sudo systemctl start odoo