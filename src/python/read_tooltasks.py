# -*- coding: utf-8 -*-
import locale
import argparse
from datetime import datetime
import os
import re
import sys
import xlrd 



def print_header():
    header = '''@prefix category: <https://vocabularies.clarin.eu/clavas/formats/categories#> .
@prefix family: <https://vocabularies.clarin.eu/clavas/formats/families#> .
@prefix type: <https://vocabularies.clarin.eu/clavas/formats/types#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix iana: <https://www.iana.org/assignments/media-types/media-types#> .
'''
    output.write(f'{header}\n')


def print_values(values):
    stderr(f'{values}\n')
    prefLabel = re.search(r'>([^<]*)<',values['Item']).group(1)
    output.write(f"category:{re.sub(r'  *','_',values['Cat1'])} a skos:Concept;\n")
    output.write(f'  skos:prefLabel "{prefLabel}"')
    if(values['Cat2']):
        output.write(f";\n  skos:narrower category:{re.sub(r'  *','_',values['Cat2'])}.\n\n")
        output.write(f"category:{re.sub(r'  *','_',values['Cat2'])} a skos:Concept;\n")
        output.write(f'  skos:prefLabel "{prefLabel}"')
        if(values['Cat3']):
            output.write(f",\n  skos:narrower category:{re.sub(r'  *','_',values['Cat3'])}.\n\n")
            output.write(f"category:{re.sub(r'  *','_',values['Cat3'])} a skos:Concept;\n")
            output.write(f'  skos:prefLabel "{prefLabel}"')
            if(values['Cat4']):
                output.write(f"m\n  skos:narrower category:{re.sub(r'  *','_',values['Cat4'])}.\n\n")
                output.write(f"category:{re.sub(r'  *','_',values['Cat4'])} a skos:Concept;\n")
                output.write(f'  skos:prefLabel "{prefLabel}"')
    output.write(f'.\n\n')


def get_labels(sheet,headerrow):
    stderr('get_labels')
    header_names = ['Category','Extension','Family','Mimetype','Name']
    result = {}
    for colnum in range(sheet.ncols):
        cell_value = sheet.cell_value(headerrow,colnum)
        result[cell_value] = colnum
    return result


def xls_file(inputfile, headerrow=0):
#        headers = read_sheets(filename)
        wb = xlrd.open_workbook(inputfile,headerrow,encoding_override="utf-8") 
        sheet = wb.sheet_by_name('Sheet1')
        labels = get_labels(sheet,headerrow)
        for rownum in range(sheet.nrows):
            if(rownum>headerrow):
                values = {}
                for key in labels:
                    values[key] = sheet.cell_value(rownum,labels[key])
                print_values(values)


def arguments():
    ap = argparse.ArgumentParser(description='Read file (csv, xls(x), sql_dump to make xml-rdf')
    ap.add_argument('-i', '--inputfile',
                    help="inputfile",
                    default = "../../data/Tooltasks Ontology 2021-05-07.xlsx")
    ap.add_argument('-o', '--outputfile',
                    help="outputfile",
                    default = "../../data/tooltasks_ontology.ttl")
    ap.add_argument('-t', '--headerrow',
                    help="headerrow; 0=row 1 (default = 0)",
                    default = 0)
    args = vars(ap.parse_args())
    return args


def stderr(text='',nl='\n'):
    sys.stderr.write('{}{}'.format(text,nl))

def end_prog(code=0):
    stderr(datetime.today().strftime("einde: %H:%M:%S"))
    sys.exit(code)

 
if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))

    args = arguments()
    inputfile = args['inputfile']
    outputfile = args['outputfile']
    headerrow = args['headerrow']

    output = open(outputfile, "w", encoding="utf-8")
    print_header()
    
    xls_file(inputfile, headerrow)

    end_prog()

