from django.db import models
from django import forms
from django.contrib.auth.models import User
import datetime
from time import time
from django.core.files.storage import FileSystemStorage
from chunked_upload.models import ChunkedUpload

fs = FileSystemStorage(location='/Users/fshaw/Desktop/test')


def get_upload_file_name(instance, filename):
    return 'uploaded_files/%s_%s' % (str(time()).replace('.', '_'), filename)


# profile is the top level container object representing a profile of work
class Profile(models.Model):
    title = models.CharField(max_length=500)
    abstract = models.TextField(null=True, blank=True)
    abstract_short = models.CharField(max_length=150, null=True, blank=True)
    date_created = models.DateField(default=datetime.date.today)
    date_modified = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title


#collection represents a type of data i.e. ENA, GenBank, pdf, image data, movie etc.
class Collection(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default="custom submission")
    profile = models.ForeignKey(Profile)

    def __unicode__(self):
        return self.name


#resource is a object which represents raw data as either a file path or a url
class Resource(models.Model):
    name = models.CharField(max_length=50)
    URL = models.CharField(max_length=200, null=True, blank=True)
    path = models.CharField(max_length=200, null=True, blank=True)
    md5_checksum = models.CharField(max_length=200, null=True, blank=True)
    collection = models.ForeignKey(Collection)

    def __unicode__(self):
        return self.name


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class Document(models.Model):
    docfile = models.FileField(upload_to='/Users/fshaw/Desktop/test')

    @classmethod
    def create(cls, file, location):
        doc = cls(docfile=file)
        doc.docfile.upload_to = location

        return doc


#the following ENA objects are self explanatory
class EnaStudy(models.Model):
    collection = models.ForeignKey(Collection)
    study_title = models.CharField(max_length=1000)
    study_type = models.CharField(max_length=5000)
    study_abstract = models.TextField(null=True, blank=True)
    center_name = models.CharField(max_length=100, null=True, blank=True)
    center_project_name = models.CharField(max_length=100, null=True, blank=True)
    study_description = models.CharField(max_length=5000, null=True, blank=True)

    def __unicode__(self):
        return self.study_title


class EnaStudyAttr(models.Model):
    ena_study = models.ForeignKey(EnaStudy)
    tag = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.tag


class EnaSample(models.Model):
    ena_study = models.ForeignKey(EnaStudy)
    title = models.CharField(max_length=50, null=True, blank=True)
    taxon_id = models.IntegerField()
    scientific_name = models.CharField(max_length=50, null=True, blank=True)
    common_name = models.CharField(max_length=50, null=True, blank=True)
    anonymized_name = models.CharField(max_length=50, null=True, blank=True)
    individual_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)


class EnaSampleAttr(models.Model):
    ena_sample = models.ForeignKey(EnaSample)
    tag = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, null=True, blank=True)


class EnaExperiment(models.Model):
    study = models.ForeignKey(EnaStudy, null=True)
    sample = models.ForeignKey(EnaSample, null=True)
    platform = models.CharField(max_length=50, null=True, blank=True)
    instrument = models.CharField(max_length=50, null=True, blank=True)
    lib_name = models.CharField(max_length=50, null=True, blank=True)
    lib_source = models.CharField(max_length=50, null=True, blank=True)
    lib_selection = models.CharField(max_length=50, null=True, blank=True)
    lib_strategy = models.CharField(max_length=50, null=True, blank=True)
    insert_size = models.IntegerField(default=0, null=True, blank=True)
    design_description = models.CharField(max_length=50, null=True, blank=True)
    lib_construction_protocol = models.CharField(max_length=50, null=True, blank=True)
    lib_layout = models.CharField(max_length=50, null=True, blank=True)
    file_type = models.CharField(max_length=50, null=True, blank=True)
    lib_name = models.CharField(max_length=100, null=True, blank=True)
    #panel id allows for multiple experiments to be displayed as if they were multiplexed
    #single experiments. i.e. make a new panel for each new panel id
    panel_ordering = models.IntegerField(default=0)
    panel_id = models.CharField(max_length=100, null=True, blank=True)
    data_modal_id = models.CharField(max_length=100, null=True, blank=True)


class ExpFile(models.Model):
    #class to join experiments with files
    experiment = models.ForeignKey(EnaExperiment)
    file = models.OneToOneField(ChunkedUpload)
    md5_hash = models.CharField(max_length=50, null=True, blank=True)
    
