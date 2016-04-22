import urllib
from bs4 import BeautifulSoup
from collections import namedtuple
import re
from tqdm import tqdm
from ..models import *


def read_csv(num=None, maxlength=None):
    filename = r'C:\Users\Stanislav\PycharmProjects\Alex_MacRae_Web_App\documents\April4.csv'
    with open(filename) as csv_file:
        # head = [next(csv_file) for x in xrange(num)]
        head = []
        for idx, line in enumerate(csv_file):
            head.append(line)
            if idx == num - 1:
                break
    head = [[item.replace('"', '')[:maxlength if maxlength else None] for item in line.split('","')] for line in head]

    return head


class Scraper(object):

    @staticmethod
    def scrap(url):
        htmltext = urllib.urlopen(url).read()

        soup = BeautifulSoup(htmltext, "html.parser")
        (access_no, fil_data, fil_data_ch, accepted, doc_count) = Scraper._form_data(soup)
        documents = Scraper._documents_data(soup)
        companies = Scraper._companies_data(soup)

        return Scraper.Data(access_no, fil_data, fil_data_ch, accepted, doc_count, documents, companies)

    Company = namedtuple("Company", "name, "
                                    "cik, "
                                    "irs_no, "
                                    "state_of_incorp, "
                                    "fiscal_year_end, "
                                    "type, "
                                    "act, "
                                    "file_no, "
                                    "film_no, "
                                    "sic")

    Document = namedtuple("Document", "seq, "
                                      "description, "
                                      "doc_name, "
                                      "url, "
                                      "type, "
                                      "size")

    Data = namedtuple("Data", "access_no, "
                              "fil_data, "
                              "fil_data_ch, "
                              "accepted, "
                              "doc_count, "
                              "documents, "
                              "companies")

    @staticmethod
    def _form_data(soup):
        try:
            data = soup.find(id="formDiv").text.split("\n")
        except:
            return ("", "", "", "", "")

        (access_no, filling_date, filling_date_changed, accepted, documents) = ("",)*5
        try:
            access_no = soup.find(id="secNum").text.split("\n")[1].split(' ')[-1]
        except:
            pass
        try:
            filling_date = data[data.index("Filing Date") + 1]
        except:
            pass
        try:
            filling_date_changed = data[data.index("Filing Date Changed") + 1]
        except:
            pass
        try:
            accepted = data[data.index("Accepted") + 1]
        except:
            pass
        try:
            documents = data[data.index("Documents") + 1]
        except:
            pass

        return (access_no, filling_date, filling_date_changed, accepted, documents)

    @staticmethod
    def _documents_data(soup):
        try:
            rows = soup.find("table", {"class": "tableFile"}).findAll("tr")[1:-1]
        except:
            return None
        try:
            docs = []
            for row in rows:
                tdata = row.findAll("td")
                seq = tdata[0].text
                descr = tdata[1].text
                doc_name = tdata[2].text
                doc_url = tdata[2].find("a").get("href")
                doc_url = 'https://www.sec.gov' + doc_url
                doc_type = tdata[3].text
                size = tdata[4].text
                docs.append(Scraper.Document(seq, descr, doc_name, doc_url, doc_type, size))
            return docs
        except:
            return None

    @staticmethod
    def _companies_data(soup):
        try:
            companies = soup.findAll("div", {"id": "filerDiv"})
        except:
            return None

        cmp_list = []
        for company in companies:
            comp = company.find("span", {"class": "companyName"}).text.split("\n")
            cik_ = company.text.replace('\n', ' ')
            if 'CIK: ' in cik_:
                cik = ""
                metch = re.search(r'(CIK: )(\d+)', cik_)
                if metch:
                    cik = metch.group(2)
            else:
                cik = ""
            name = comp[0]
            data = company.find("p", {"class": "identInfo"}).text.\
                replace("Type:", " | Type:").\
                replace("SIC:", " | SIC:").\
                replace("Assistant Director", " | Assistant Director:").\
                replace(": ", ":")
            if data[:2] == " |": data = data[2:]
            (irs_no, state_of_incorp, fiscal_year_end, type_, act, file_no, film_no, sic) = ("",)*8
            for item in data.split(" | "):
                (lbl, val) = item.split(":")
                if lbl == "IRS No.":
                    irs_no = val
                elif lbl == "State of Incorp.":
                    state_of_incorp = val
                elif lbl == "Fiscal Year End":
                    fiscal_year_end = val
                elif lbl == "Type":
                    type_ = val
                elif lbl == "Act":
                    act = val
                elif lbl == "File No.":
                    file_no = val
                elif lbl == "Film No.":
                    film_no = val
                elif lbl == "SIC":
                    sic = val
            cmp_list.append(Scraper.Company(
                name, cik, irs_no, state_of_incorp,
                fiscal_year_end, type_, act,
                file_no, film_no, sic
            ))
        return cmp_list


def _fill(db_data):
    pass


def fill_db():
    data = read_csv(num=-1)
    for item in tqdm(data):
        cik = item[1]
        access_no = item[2]
        url = r'https://www.sec.gov/Archives/edgar/data/' \
              + cik[3:] + '/' + access_no + '-index.htm'
        try:
            db_data = Scraper.scrap(url)
            _fill(db_data)
        except:
            pass


if __name__ == '__main__':
    pass