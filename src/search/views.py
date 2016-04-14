from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.shortcuts import render
from .forms import *

from .app_scripts import search_script

def index(request):
    header = "Home page"
    context = {
        'header': header,
        'text': "This is an home page. You can do here three types of search you can see above.",
    }

    if request.method == 'POST':
        search_type = request.POST['search_type']
        if search_type == "1":
            print
            print "POST request: Search for agreements."
            form = AgreementsForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data

                agr_name = data['agr_name']
                agr_type = data['agr_type']
                date_start = data['date_start']
                date_end = data['date_end']
                pr_only = bool(data['pr_only'])

                party = []
                capacity = []
                for item in sorted(request.POST):
                    if 'capacity' in item:
                        capacity.append(request.POST[item])
                    if 'party' in item:
                        party.append(request.POST[item])

                while "" in party:
                    i = party.index('')
                    del party[i]
                    del capacity[i]

                print 'Agreement name:', agr_name
                print 'Agreement type:', agr_type
                print 'Start date:    ', str(date_start)
                print 'End date:      ', str(date_end)
                print 'Only primaries:', pr_only

                for i in range(len(party)):
                    print 'Party ' + str(i) + ':    ' + party[i]
                    print 'Capacity ' + str(i) + ': ' + capacity[i]
                print

                result = search_script.search_1(agr_name, agr_type, date_start, date_end, party, capacity, pr_only)
                return render(request, 'search/agreements_results_page.html',
                              {'data': result, 'party': bool(party)})
            else:
                print "BAD Request"

        if search_type == "2":
            print
            print "POST request: Search for SEC filings."
            form = SecFilingsForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                c = data['company']
                f = data['sec_form']
                d0 = data['date_start']
                d1 = data['date_end']
                p = bool(data['pr_only'])

                print 'SEC Form:      ', f
                print 'Start date:    ', str(d0)
                print 'End date:      ', str(d1)
                print 'Only primaries:', p

                result = search_script.search_2(c, f, d0, d1, p)
                return render(request, 'search/sec_filings_result_page.html', {'data': result})
            else:
                print "BAD Request"

        if search_type == "3":
            form = FilersForm(request.POST)

            if form.is_valid():
                data = form.cleaned_data
                search_for = data['search_for']
                if search_for == '1':
                    from app_scripts.search_script import search_by_company
                    company = data['company']
                    sec_form = data['sec_form']
                    sic = data['sic']
                    agr_type = data['agr_type']
                    primary = bool(data['pr_only'])
                    companies = search_by_company(company=company, sic=sic, sec_form=sec_form, agr_type=agr_type, search_type="3", primary=primary)
                    print "We have a result: ", len(companies)
                    return render(request, 'search/agreements_results_page.html', {'data': companies})

                if search_for == '2':
                    # DO search
                    from app_scripts.search_script import search_by_company
                    company = data['company']
                    sec_form = data['sec_form']
                    sic = data['sic']
                    agr_type = data['agr_type']
                    primary = bool(data['pr_only'])
                    companies = search_by_company(company=company,
                                                  sic=sic,
                                                  sec_form=sec_form,
                                                  agr_type=agr_type,
                                                  search_type="4",
                                                  primary=primary)
                    print "We have a result: ", len(companies)

                    return render(request, 'search/sec_filings_result_page.html', {'data': companies})

                return render(request, 'search/index.html', {'header': "THANKS"})
            else:
                print "BAD Request"

    return render(request, 'search/home.html', context)


def agreements(request):
    form = AgreementsForm()
    header = "Search for agreements"
    context = {
        'header': header,
        'show_form': True,
        'show_parties': True,
        'form': form,
    }
    return render(request, 'search/index.html', context)


def sec_filings(request):
    print type(request)
    header = "Search for SEC filings"
    context = {
        'header': header,
        'form': SecFilingsForm(),
        'show_form': True,
    }
    return render(request, 'search/index.html', context)


def filers(request):
    print type(request)
    header = "Search for filers (companies)"
    context = {
        'header': header,
        'form': FilersForm(),
        'show_form': True,
    }
    return render(request, 'search/index.html', context)


def test_view(request):
    return render(request, "search/test.html", {})
