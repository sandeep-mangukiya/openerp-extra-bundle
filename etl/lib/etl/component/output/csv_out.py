# -*- encoding: utf-8 -*-
##############################################################################
#
#    ETL system- Extract Transfer Load system
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
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


from etl import etl
import csv

class csv_out(etl.component):
    """
        This is an ETL Component that use to write data to csv file.

		Type: Data Component
		Computing Performance: Streamline
		Input Flows: 0-x
		* .* : the main data flow with input data
		Output Flows: 0-1
		* main : return all data
    """
    def __init__(self, filename, *args, **argv):
        super(csv_out, self).__init__(*args, **argv)
        self.filename=filename

    def process(self):
        fp2=None
        datas = []
        for channel,trans in self.input_get().items():
            for iterator in trans:
                for d in iterator:                    
                    if not fp2:
                        fp2 = file(self.filename, 'wb+')
                        fieldnames = d.keys()
                        fp = csv.DictWriter(fp2, fieldnames)
                        fp.writerow(dict(map(lambda x: (x,x), fieldnames)))
                    fp.writerow(d)
                    yield d, 'main'