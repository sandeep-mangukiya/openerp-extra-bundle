# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

import wizard
import pooler
    
def selection_list(self, cr, uid, context):
    temp = pooler.get_pool(cr.dbname).get('dm.workitem').SELECTION_LIST 
    return temp

parameter_form = '''<?xml version="1.0"?>
<form string="Modify Workitem" colspan="4">
    <field name="by_state" colspan="4"/>
    <field name="action_time" colspan="4"/>
    <field name="state" colspan="4"/>
    <field name="in_state" colspan="4" attrs="{'readonly':[('by_state','=',False)]}"/>/>
</form>'''

parameter_fields = {
     'by_state': {'string': 'Change State of all workitem in state',
                   'type': 'boolean'},     
    'action_time': {'string': 'Action Time', 'type': 'datetime', 
                    'required': True},
    'state': {'string': 'New State', 'type': 'selection', 
              'selection': selection_list, 'required': True},
    'in_state': {'string': 'State', 'type': 'selection',
              'selection': [('pending', 'Pending'), ('error', 'Error'), 
                            ('freeze', 'Frozen'),('done', 'Done')],
                            'default': lambda *a: 'error' },
                       
}

def _change_state_action_time(self, cr, uid, data, context):
    workitem_obj = pooler.get_pool(cr.dbname).get('dm.workitem')
    if data['form']['by_state']:
        workitem_ids=workitem_obj.search(cr,uid,[('state','=',data['form']['in_state'])])
        workitem_obj.write(cr, uid, workitem_ids, {'state': data['form']['state'],
                                    'action_time': data['form']['action_time']})
    else:
        workitem_obj.write(cr, uid, data['ids'], {'state': data['form']['state'],
                                    'action_time': data['form']['action_time']})
    return {}

class wizard_workitem(wizard.interface):
    states = {
        'init': {
            'actions': [],
            'result': {'type': 'form', 'arch': parameter_form, 
                       'fields': parameter_fields, 
                       'state': [('end', 'Cancel'), ('done', 'Modify')]}

        },
        'done': {
            'actions': [],
            'result': {
                'type': 'action',
                'action': _change_state_action_time,
                'state': 'end'
            }
        },
    }
wizard_workitem("wizard.workitem")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: