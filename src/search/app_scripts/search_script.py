from ..models import *
from django.db.models import F, Q
from django.db import connection


def SEC_filings_search(sec_form, date0, date1, primary_only):
    documents = Document.objects.filter(
        Q(filing__fil_date__gte=date0, filing__fil_date__lte=date1) |
        Q(filing__fil_date_ch__gte=date0, filing__fil_date_ch__lte=date1) |
        Q(filing__accepted__gte=date0, filing__accepted__lte=date1),
        doc_type__contains='EX',
    )

    if sec_form:
        documents.filter(filing__sec_form__iexact=sec_form)

    return documents.distinct()


def search_by_company(company, sic, sec_form, agr_type, search_type, primary):
    if search_type == "4":
        # return do_serch(company, sic, sec_form)
        cursor = connection.cursor()
        SQL_TEXT = '''
            SELECT DISTINCT
            search_filing.fil_date, search_company.name, search_filing.sec_form, search_filing.sec_form_det, search_document.doc_type, search_document.url, search_document.description
            FROM search_filing
            INNER JOIN search_document ON
                search_document.filing_id=search_filing.id AND
                search_document.doc_type LIKE '%EX%' AND
                search_filing.sec_form ILIKE'%<SEC_FORM_DATA>%'
            INNER JOIN search_company ON
                search_document.filing_id = search_company.filing_id AND
                search_company.sic ILIKE '%<SIC_DATA>%' AND
                search_company.name ILIKE '%<COMPANY_DATA>%'
            '''
        SQL_TEXT = SQL_TEXT.replace('<SEC_FORM_DATA>', sec_form).replace('<COMPANY_DATA>', company).replace('<SIC_DATA>', sic)
        print SQL_TEXT
        if primary:
            SQL_TEXT += ' AND \nsearch_company.primary IS True'
        cursor.execute(SQL_TEXT)
        return cursor.fetchall()

    if search_type == "3":
        cursor = connection.cursor()
        SQL_TEXT = '''
            SELECT DISTINCT
            search_filing.fil_date, search_company.name, search_document.agr_name, search_document.agr_type, search_filing.sec_form, search_document.other_info
            FROM search_filing
            INNER JOIN search_document ON
                search_document.filing_id=search_filing.id AND
                search_filing.sec_form ILIKE '%<SEC_FORM_DATA>%'
            INNER JOIN search_company ON
                search_document.filing_id = search_company.filing_id AND
                search_company.sic ILIKE '%<SIC_DATA>%' AND
                search_company.name ILIKE '%<COMPANY_DATA>%'
                '''
        SQL_TEXT = SQL_TEXT.replace('<SIC_DATA>', sic).replace('<SEC_FORM_DATA>', sec_form).replace('<COMPANY_DATA>', company)
        if primary:
            SQL_TEXT += ' AND \nsearch_company.primary IS True'
        print SQL_TEXT
        cursor.execute(SQL_TEXT)
        return cursor.fetchall()


def do_serch(company, sic, sec_form):
    filing = Filing.objects.filter(
        sec_form=sec_form,
    )
    filing.select_related('company')
    filing.select_related('document')
    return filing


def search_1(agr_name, agr_type, date_start, date_end, party, capacity, pr_only):
    cursor = connection.cursor()
    SQL_TEXT = 'SELECT DISTINCT search_filing.fil_date, ' \
               'search_company.name, search_document.agr_name, ' \
               'search_document.agr_type, search_filing.sec_form, ' \
               'search_document.other_info'
    # if party:
    #     SQL_TEXT += ', search_party.name, search_party.capacity'

    SQL_TEXT += '\nFROM search_filing\n' \
                'INNER JOIN search_document ON\n' \
                'search_document.filing_id=search_filing.id AND\n' \
                "search_document.agr_date >= '" + str(date_start) + "' AND\n" \
                "search_document.agr_date <= '" + str(date_end) + "'"

    if agr_name:
        SQL_TEXT += " AND\n" + "search_document.agr_name ILIKE '%" + agr_name + "%'"
    if agr_type:
        SQL_TEXT += " AND\n" + "search_document.agr_type ILIKE '%" + agr_type + "%'"

    # if party:
    #     SQL_TEXT += "\n INNER JOIN search_party ON search_party.document_id = search_document.id"

    SQL_TEXT += "\nINNER JOIN search_company ON\nsearch_document.filing_id = search_company.filing_id"
    if pr_only:
        SQL_TEXT += " AND\nsearch_company.primary IS TRUE"

    print '-------------------SQL REQUEST----------------------'
    print SQL_TEXT
    print '----------------------------------------------------'

    cursor.execute(SQL_TEXT)
    return cursor.fetchall()

def search_2(company, sec_form, date_0, date_1, pr_only):
    cursor = connection.cursor()
    SQL_TEXT = "SELECT DISTINCT search_filing.fil_date, search_company.name," \
               "search_filing.sec_form, search_filing.sec_form_det, search_document.doc_type," \
               "search_document.url, search_document.description"

    SQL_TEXT += "\nFROM search_filing"

    SQL_TEXT += "\nINNER JOIN search_document ON" \
                "\nsearch_document.filing_id=search_filing.id" \
                "\nAND search_document.doc_type LIKE '%EX%'" \
                "\nAND search_filing.sec_form ILIKE '%" + sec_form + "%'" \
                "\nAND search_filing.fil_date >= '" + str(date_0) + "'" \
                "\nAND search_filing.fil_date <= '" + str(date_1) + "'"

    SQL_TEXT += "\nINNER JOIN search_company ON" \
                "\nsearch_document.filing_id = search_company.filing_id"

    if pr_only:
        SQL_TEXT += "\nAND search_company.primary IS TRUE"
    if company:
        SQL_TEXT += "\nAND search_company.name ILIKE'%" + company + "%'"

    print '-------------------SQL REQUEST----------------------'
    print SQL_TEXT
    print '----------------------------------------------------'

    cursor.execute(SQL_TEXT)
    return cursor.fetchall()
