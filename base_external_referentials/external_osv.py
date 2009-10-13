# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    Sharoon Thomas, Raphael Valyi
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

from osv import fields, osv

class external_osv(osv.osv):
    def extid_to_oeid(self, cr, uid, ids, external_referential_id):
        #First get the external key field name
        #conversion external id -> OpenERP object using Object mapping_column_name key!
        mapping_id = self.pool.get('external.mapping').search(cr, uid, [('model', '=', self._name), ('referential_id', '=', external_referential_id)])
        if mapping_id:
            #now get the external field name
            ext_field_name = self.pool.get('external.mapping').read(cr, uid, mapping_id[0], ['external_field'])['external_field']
            if ext_field_name:
                #now get the oe_id
                oe_id = self.search(cr, uid, [(ext_field_name, '=', ids)])
                if oe_id:
                    return oe_id[0]
    
    def where_i_belong(self,cr,uid,id):
        all_mapping_cols = self.pool.get('external.referential')._get_all_mappingcolnames(cr,uid)
        result = {}
        if all_mapping_cols:
            my_read = self.read(cr,uid,id,[])
            for each_key in all_mapping_cols:
                if each_key in my_read.keys() and my_read[each_key]:
                    result[each_key] = my_read[each_key]
        return result
        
    def ext_import(self,cr, uid, data, external_referential_id, defaults={}, context={}):
        #Inward data has to be list of dictionary
        #This function will import a given set of data as list of dictionary into Open ERP
        if data:
            write_ids = []  #Will record ids of records modified, not sure if will be used
            create_ids = [] #Will record ids of newly created records, not sure if will be used
            mapping_id = self.pool.get('external.mapping').search(cr,uid,[('model','=',self._name),('referential_id','=',external_referential_id)])
            if mapping_id:
                #If a mapping exists for current model, search for mapping lines
                mapping_line_ids = self.pool.get('external.mapping.line').search(cr,uid,[('mapping_id','=',mapping_id),('type','in',['in_out','in'])])
                mapping_lines = self.pool.get('external.mapping.line').read(cr,uid,mapping_line_ids,['external_field','external_type','in_function'])
                if mapping_lines:
                    #if mapping lines exist find the data conversion for each row in inward data
                    for each_row in data:
                        vals = {} #Dictionary for create record
                        for each_mapping_line in mapping_lines:
                            #Type cast if the expression exists
                            if each_mapping_line['external_type']:
                                type_casted_field = eval(each_mapping_line['external_type'])(each_row.get(each_mapping_line['external_field'],False))
                            else:
                                type_casted_field = each_row.get(each_mapping_line['external_field'],False)
                            #Build the space for expr
                            space = {
                                    'self':self,
                                    'cr':cr,
                                    'uid':uid,
                                    'data':data,
                                    'external_referential_id':external_referential_id,
                                    'defaults':defaults,
                                    'context':context,
                                    'ifield':type_casted_field
                                        }
                            #The expression should return value in list of tuple format
                            #eg[('name','Sharoon'),('age',20)] -> vals = {'name':'Sharoon', 'age':20}
                            exec each_mapping_line['in_function'] in space
                            result = space.get('result',False)
                            #If result exists and is of type list
                            if result and type(result)==list:
                                for each_tuple in result:
                                    if type(each_tuple)==tuple and len(each_tuple)==2:
                                        vals[each_tuple[0]] = each_tuple[1] 
                        #Every mapping line has now been translated into vals dictionary, now set defaults if any
                        for each_default_entry in defaults.keys():
                            vals[each_default_entry] = defaults[each_default_entry]
                        #Vals is complete now, perform a record check, for that we need foreign field
                        for_key_field = self.pool.get('external.mapping').read(cr,uid,mapping_id[0],['external_field'])['external_field']
                        vals[for_key_field] = external_referential_id
                        if vals and for_key_field in vals.keys():
                            #Check if record exists
                            existing_rec_ids = self.search(cr,uid,[(for_key_field,'=',vals[for_key_field])]) 
                            if existing_rec_ids:
                                if self.write(cr,uid,existing_rec_ids,vals,context):
                                    write_ids.append(existing_rec_ids)
                            else:
                                create_ids.append(self.create(cr,uid,vals,context))

    def ext_export_data(self,cr,uid,ids,external_referential_id,defaults={},context={}):
        #if ids is [] all records are selected or ids has to be a list of ids
        #return a list of dictionary of formatted items
        if external_referential_id:
            out_data = []
            if not ids:
                ids = self.search(cr,uid,[])#Get all records if ids is empty
            data = self.read(cr,uid,ids,[])
            #Find the mapping record now
            mapping_id = self.pool.get('external.mapping').search(cr,uid,[('model','=',self._name),('referential_id','=',external_referential_id)])
            if mapping_id:
                #If a mapping exists for current model, search for mapping lines
                mapping_line_ids = self.pool.get('external.mapping.line').search(cr,uid,[('mapping_id','=',mapping_id),('type','in',['in_out','out'])])
                mapping_lines = self.pool.get('external.mapping.line').read(cr,uid,mapping_line_ids,['external_field','out_function'])
                if mapping_lines:
                    #if mapping lines exist find the data conversion for each row in inward data
                    for each_row in data:
                        vals = {} #Dictionary for record
                        for each_mapping_line in mapping_lines:
                            #Build the space for expr
                            space = {
                                    'self':self,
                                    'cr':cr,
                                    'uid':uid,
                                    'data':data,
                                    'external_referential_id':external_referential_id,
                                    'defaults':defaults,
                                    'context':context,
                                    'record':each_row
                                        }
                            #The expression should return value in list of tuple format
                            #eg[('name','Sharoon'),('age',20)] -> vals = {'name':'Sharoon', 'age':20}
                            exec each_mapping_line['out_function'] in space
                            result = space.get('result',False)
                            #If result exists and is of type list
                            if result and type(result)==list:
                                for each_tuple in result:
                                    if type(each_tuple)==tuple and len(each_tuple)==2:
                                        vals[each_tuple[0]] = each_tuple[1]
                        #Every mapping line has now been translated into vals dictionary, now set defaults if any
                        for each_default_entry in defaults.keys():
                            vals[each_default_entry] = defaults[each_default_entry]
                        #If vals exist append it to the out_data list
                        if vals:
                            out_data.append(vals)
        return out_data