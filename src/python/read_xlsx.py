# -*- coding: utf-8 -*-
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL')
import argparse
import csv
from datetime import datetime
import re
import sys
import xlrd 
import json
from pprint import pprint

output = None
delimiter = ','
quotechar = ''
datasetname = ''
resource = ''
cell_types = {
         0:'TEXT',
         1:'TEXT',
         2:'REAL',
         3:'TIMESTAMP',
         4:'BOOLEAN',
         5:'TEXT',
         6:'TEXT'
        }

def print_header():
    header = '''@prefix category: <https://vocabularies.clarin.eu/clavas/formats/categories#> .
@prefix family: <https://vocabularies.clarin.eu/clavas/formats/families#> .
@prefix type: <https://vocabularies.clarin.eu/clavas/formats/types#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix iana: <https://www.iana.org/assignments/media-types/media-types#> .
'''
    output.write(f'{header}\n')

def print_values(values):
    #output.write(f'{values}\n')
    for ext in re.split(',|;|/',values['Extension']):
        if values['Extension']!='??' and values['Extension']!='' \
            and values['Category']!='--':
            type_w_o_spaces = re.sub(r'[ ()/]','_',values['Name'])
            cat_w_o_spaces = re.sub(r'[ ()/]','_',values['Category'])
            if values['Family']!='':
                lines_family = f'''category:{cat_w_o_spaces} a skos:Concept;
  skos:prefLabel "{values['Category']}";
  skos:narrower family:{values['Family']}.

family:{values['Family']} a skos:Concept;
  skos:prefLabel "{values['Family']}";
  skos:narrower type:{type_w_o_spaces}.
 
type:{type_w_o_spaces} a skos:Concept;
  skos:prefLabel "{values['Name']}";
  iana:mimetype "{values['Mimetype']}";
  iana:extension "{ext.strip()}".

'''
                output.write(lines_family)
            else:
                lines_type = f'''category:{cat_w_o_spaces} a skos:Concept;
  skos:prefLabel "{values['Category']}";
  skos:narrower type:{type_w_o_spaces}.
 
type:{type_w_o_spaces} a skos:Concept;
  skos:prefLabel "{values['Name']}";
  iana:mimetype "{values['Mimetype']}";
  iana:extension "{ext.strip()}".

'''
                output.write(lines_type)


def get_labels(sheet,headerrow):
    stderr('get_labels')
    header_names = ['Category','Extension','Family','Mimetype','Name']
    result = {}
    for colnum in range(sheet.ncols):
        cell_value = sheet.cell_value(headerrow,colnum)
        if cell_value in header_names:
            result[cell_value] = colnum
    return result

def xls_file(inputfile, headerrow=0):
#        headers = read_sheets(filename)
        wb = xlrd.open_workbook(inputfile,headerrow,encoding_override="utf-8") 
        sheet = wb.sheet_by_name('Families')
        labels = get_labels(sheet,headerrow)
        for rownum in range(sheet.nrows):
            if(rownum>headerrow):
                values = {}
                for key in labels:
                    values[key] = sheet.cell_value(rownum,labels[key])
                print_values(values)
                stderr(values)

        '''                    
                cell_value = sheet.cell_value(rownum,colnum)
                cell_type = sheet.cell_type(rownum,colnum)
                if(cell_types[cell_type]=='TIMESTAMP'):
                    cell_date = xlrd.xldate.xldate_as_datetime(cell_value,0)
                    stderr(f'{cell_date.strftime("%d-%m-%Y")} ({cell_types[cell_type]})')
                else:
                    stderr(f'{cell_value} ({cell_types[cell_type]})')
'''
 


def clean_string(value):
    return value


def stderr(text):
    sys.stderr.write("{}\n".format(text))

def arguments():
    ap = argparse.ArgumentParser(description='Read file (csv, xls(x), sql_dump to make xml-rdf')
    ap.add_argument('-i', '--inputfile',
                    help="inputfile",
                    default = "../../data/Formats and Mimetypes.xlsx")
    ap.add_argument('-o', '--outputfile',
                    help="outputfile",
                    default = "../../data/formats_and_mimetypes.ttl")
    ap.add_argument('-q', '--quotechar',
                    help="quotechar",
                    default = "'" )
    ap.add_argument('-t', '--headerrow',
                    help="headerrow; 0=row 1 (default = 0)",
                    default = 0)
    args = vars(ap.parse_args())
    return args


def end_prog(code=0):
    stderr(datetime.today().strftime("einde: %H:%M:%S"))
    sys.exit(code)

 
if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))

    args = arguments()
    inputfile = args['inputfile']
    outputfile = args['outputfile']
    headerrow = args['headerrow']
    quotechar = args['quotechar']

    output = open(outputfile, "w", encoding="utf-8")
    print_header()
    
    xls_file(inputfile, headerrow)

    end_prog(0)

