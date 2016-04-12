from django import forms
from django.forms.formsets import formset_factory

YEAR_CHOICES = tuple([str(x) for x in range(2014, 2017, 1)])
CHOICES = [('1', 'Create an agreement result page'),
           ('2', 'Create a SEC Filing result page')]

like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

_text = 'Search for primary companies only'
choices = [('yes', _text)]

class AgreementsForm(forms.Form):
    agr_name = forms.CharField(label='Agreement name',
                               max_length=200,
                               required=False, widget=forms.TextInput(attrs={'placeholder': ''}))
    agr_type = forms.CharField(label='Agreement type', max_length=200, required=False)
    date_start = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES), label='Start date')
    date_end = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES), label='End date')

    search_type = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    pr_only = forms.MultipleChoiceField(required=False,
                                         widget=forms.CheckboxSelectMultiple,
                                         choices=choices,
                                         initial=choices[0])


class SecFilingsForm(forms.Form):
    sec_form = forms.CharField(label='Sec Form', max_length=200, required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'e.g 6-K'}))
    date_start = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES), label='Start date')
    date_end = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES), label='End date')

    pr_only = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=choices, initial=choices[0])

    search_type = forms.IntegerField(widget=forms.HiddenInput(), initial=2)


class FilersForm(forms.Form):
    company = forms.CharField(label='Company',
                              max_length=200,
                              required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'e.g. American Airlines'}))
    sic = forms.CharField(label='SIC',
                          max_length=200,
                          required=False,
                          widget=forms.TextInput(attrs={'placeholder': 'e.g. Real Estate'}))

    sec_form = forms.CharField(label='Sec Form',
                               max_length=200,
                               required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'e.g. 6-K'}))
    agr_type = forms.CharField(label='Agreement Type', max_length=200, required=False)

    search_for = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), initial=2)

    pr_only = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=choices, initial=choices[0])

    search_type = forms.IntegerField(widget=forms.HiddenInput(), initial=3)
