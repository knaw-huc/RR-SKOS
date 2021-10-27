import csv
import glob
from datetime import datetime
import os
import re
import sys




def stderr(text='',nl='\n'):
    sys.stderr.write('{}{}'.format(text,nl))

def end_prog(code=0):
    stderr(datetime.today().strftime("einde: %H:%M:%S"))
    if(code!=0):
        stderr('code: {}'.format(code))
    sys.exit(code)


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))

    res_file = open('../../data/formats_and_mimetypes.ttl','w')
    count_rp = 0   
    count_succes = 0
    count_total = 0
    res_file.write('''@prefix category: <https://vocabularies.clarin.eu/clavas/formats/categories#> .
@prefix family: <https://vocabularies.clarin.eu/clavas/formats/families#> .
@prefix type: <https://vocabularies.clarin.eu/clavas/formats/types#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix iana: <https://www.iana.org/assignments/media-types/media-types#> .

''')

    with open('../../data/Formats and Mimetypes - Families.csv', 'r') as csvfile:
        linereader = csv.DictReader(csvfile, delimiter='\t')
        for row in linereader:
            count_total += 1
            lines_family = f'''category:{row['Category']} a skos:Concept,
  skos:prefLabel "{row['Category']}",
  skos:narrower family:{row['Family']}.

family:{row['Family']} a skos:Concept,
  skos:prefLabel "{row['Family']}",
  skos:narrower type:{row['Name']}.
 
type:{row['Name']} a skos:Concept,
  skos:prefLabel "{row['Name']}",
  iana:mimetype "{row['Mimetype']}",
  iana:extension "{row['Extension']}".

'''
            lines_type = f'''category:{row['Category']} a skos:Concept,
  skos:prefLabel "{row['Category']}",
  skos:narrower type:{row['Name']}.
 
type:{row['Name']} a skos:Concept,
  skos:prefLabel "{row['Name']}",
  iana:mimetype "{row['Mimetype']}",
  iana:extension "{row['Extension']}".

'''

            if row['Family']=='':
                res_file.write(lines_type)
            else:
                res_file.write(lines_family)

    stderr(f'total: {count_total}')
    end_prog()

