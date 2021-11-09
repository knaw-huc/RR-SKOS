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

    res_file = open('../../data/csd.ttl','w')
    count_rp = 0   
    count_succes = 0
    count_total = 0
    res_file.write('''@prefix category: <https://vocabularies.clarin.eu/clavas/formats/categories#> .
@prefix family: <https://vocabularies.clarin.eu/clavas/formats/families#> .
@prefix type: <https://vocabularies.clarin.eu/clavas/formats/types#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix iana: <https://www.iana.org/assignments/media-types/media-types#> .

''')

    with open('../../data/CSD AnnotationType Element.txt', 'r') as invoer:
        for line in invoer:
            if(line.strip()!=''):
                count_total += 1
                matchdata = re.search(r'>([^<]*)<',line)
                try:
                    #stderr(f'{matchdata.group(1)}')
                    res = matchdata.group(1).split('/')
                    if(len(res)>1):
                        for r in res:
                            r2 = re.sub(r'[ -]','_',r)
                            if(r==res[-1]):
                                res_file.write(f'category:{r2} a skos:Concept;\n')
                                res_file.write(f'  skos:prefLabel "{r}".\n\n')
                            else:
                                res_file.write(f'category:{r2} a skos:Concept;\n')
                                res_file.write(f'  skos:prefLabel "{r}";\n')
                                n = re.sub(r'[ -]','_',res[res.index(r)+1])
                                res_file.write(f'  skos:narrower category:{n}.\n\n')
                except:
                    pass

    stderr(f'total: {count_total}')
    end_prog()
