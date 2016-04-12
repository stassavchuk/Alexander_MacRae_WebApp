from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Filing(models.Model):
    access_num = models.CharField(max_length=60, default="", unique=True)    # Accession number
    fil_date = models.DateField(null=True)                      # Filing date
    fil_date_ch = models.DateField(null=True)                   # Filing date changed
    accepted = models.DateTimeField(null=True)                  # Accepted
    doc_count = models.IntegerField(default=0)                  # Document count
    sec_form = models.CharField(max_length=30, default="")      # Sec Form. Type of Document whose seq == 1
    sec_form_det = models.CharField(max_length=500, null=True)

    def __unicode__(self):
        return self.access_num


class Company(models.Model):
    name = models.CharField(max_length=300, default="")                     # Name of Company
    irs_no = models.CharField(max_length=20, default="")                    # IRS No
    state_inc = models.CharField(max_length=10, null=True)                  # State of Incorporation
    f_year_end = models.CharField(max_length=10, null=True)                 # Fiscal year end
    c_type = models.CharField(max_length=30, default="")                    # Company type
    act = models.CharField(max_length=10, null=True)
    file_no = models.CharField(max_length=40, null=True)
    film_no = models.CharField(max_length=40, null=True)
    sic = models.CharField(max_length=150, null=True)
    cik = models.CharField(max_length=30, default="")
    primary = models.BooleanField(default=False)

    # State of business
    # Ticker
    # Exchange
    filing = models.ForeignKey(Filing, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name + " " + self.cik


class Document(models.Model):
    seq = models.IntegerField(default=0)
    description = models.CharField(max_length=300, null=True)
    doc_name = models.CharField(max_length=100, default="")
    url = models.CharField(max_length=160, default="")
    doc_type = models.CharField(max_length=100, default="")
    size = models.CharField(max_length=30, default="")
    agr_name = models.CharField(max_length=500, null=True)       # Agreement name
    agr_type = models.CharField(max_length=500, null=True)       # Agreement type
    agr_date = models.DateField(null=True)                       # Agreement date

    def get_name(self):
        return ''.join(self.doc_name.split('.')[:-1])

    # Detailed description
    # Detailed type
    other_info = models.CharField(max_length=500, null=True)
    filing = models.ForeignKey(Filing, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.filing.access_num + ': ' + str(self.url)


class Party(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, default="")
    capacity = models.CharField(max_length=500, null=True)

    def __unicode__(self):
        return self.document.filing.access_num + ' (Seq: ' + str(self.document.seq) + '):  ' + self.name

