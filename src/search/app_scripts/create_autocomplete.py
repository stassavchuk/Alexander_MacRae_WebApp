from ..models import *

def create():
    print "I have started"
    comp_array = Company.objects.values('name').distinct()
    sic_array = Company.objects.values('sic').distinct()
    sec_form_array = Filing.objects.values('sec_form').distinct()

    with open('./static/autocomplete.js', 'w') as f:
        f.write('$(function() {\n')

        f.write('var Companies = [\n')
        for item in comp_array:
            f.write('"' + item['name'] + '",\n')
        f.write('];\n')

        f.write('var SICs = [\n')
        for item in sic_array:
            f.write('"' + item['sic'] + '",\n')
        f.write('];\n')

        f.write('var Sec_Forms = [\n')
        for item in sec_form_array:
            f.write('"' + item['sec_form'] + '",\n')
        f.write('];\n')

        f.write(
'''$( "#id_company" ).autocomplete({
source: Companies
});
$( "#id_sic" ).autocomplete({
source: SICs
});
$( "#id_sec_form" ).autocomplete({
source: Sec_Forms
});'''
        )

        f.write('});')
    print "Work is done"
