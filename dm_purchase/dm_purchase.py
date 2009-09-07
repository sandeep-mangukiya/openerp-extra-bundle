# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import fields
from osv import osv

class purchase_order(osv.osv):#{{{
    _name = "purchase.order"
    _inherit="purchase.order"

    _columns = {
        'campaign_id' : fields.many2one('dm.campaign', 'Campaign', select="1"),
        'po_confirm_do' : fields.boolean('Auto confirm purchase order'),
        'invoice_create_do' : fields.boolean('Auto create invoice'),
        'invoice_validate_do' : fields.boolean('Auto validate invoice'),
        'invoice_pay_do' : fields.boolean('Auto pay invoice'),
    }
purchase_order()#}}}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: