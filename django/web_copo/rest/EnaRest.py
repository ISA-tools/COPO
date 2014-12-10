__author__ = 'fshaw'
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from web_copo.models import Collection, Resource, Profile, EnaStudy, EnaSampleAttr, EnaSample, EnaStudyAttr, Document, DocumentForm
from rest_framework.renderers import JSONRenderer
import web_copo.xml.EnaParsers as parsers
from web_copo.utils.EnaUtils import get_sample_html_from_collection_id, handle_uploaded_file
import jsonpickle
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist






class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'

        super(JSONResponse, self).__init__(content, **kwargs)



def get_ena_study_controls(request):
    #get list of controllers
    out = parsers.get_study_form_controls('web_copo/xml/schemas/ena/SRA.study.xsd.xml')
    c_id = request.GET['collection_id']
    #check to see if there are any ena studies associated with this collection

    study_id = request.GET['study_id']

    out_str = ''

    if study_id:

        #if a study ID has been provided in the ajax call, then we are dealing with an existing study, so collect it,
        #populate the html form using its values
        study = EnaStudy.objects.get(id=study_id)

        #out_str += "<input type='hidden' id='study_id' value='" + str(study.id) + "'/>"
        for obj in out:
            out_str += "<div class='form-group'>"

            out_str += "<label for='" + obj.name + "'>" + obj.tidy_name + "</label>"
            if(obj.type == 'input'):
                out_str += "<input type='text' class='form-control' id='" + str(obj.name) + "' name='" + str(obj.name) + "' value='" + str(getattr(study, obj.name.lower())) + "'/>"
            elif(obj.type == 'textarea'):
                out_str += "<textarea type='text' rows='6' class='form-control' id='" + str(obj.name) + "' name='" + str(obj.name) + \
                       "'>" + str(getattr(study, obj.name.lower())) + "</textarea>"
            else:
                out_str += "<div class='form-group'>"
                out_str += "<select class='form-control' name='" + str(obj.name) + "' id='" + str(obj.name) + "'>"
                for opt in obj.values:
                    out_str += "<option>" + str(opt) + "</option>"
                out_str += "</select>"
            out_str += "</div>"
    else:
        #else we are dealing with a study which hasn't yet been saved, so just make a blank form
        for obj in out:
            out_str += "<div class='form-group'>"
            out_str += "<label for='" + obj.name + "'>" + obj.tidy_name + "</label>"
            if(obj.type == 'input'):
                out_str += "<input type='text' class='form-control' id='" + obj.name + "' name='" + obj.name + "'/>"
            elif(obj.type == 'textarea'):
                out_str += "<textarea type='text' rows='6' class='form-control' id='" + obj.name + "' name='" + obj.name + "'/>"
            else:
                out_str += "<div class='form-group'>"
                out_str += "<select class='form-control' name='" + obj.name + "' id='" + obj.name + "'>"
                for opt in obj.values:
                    out_str += "<option>" + opt + "</option>"
                out_str += "</select>"
            out_str += "</div>"
    return HttpResponse(out_str, content_type='html')


def get_ena_study_attr(request):
    c_id = request.GET['collection_id']
    try:
        study = EnaStudy.objects.get(collection__id=c_id)
    except ObjectDoesNotExist:
        return HttpResponse('not found', content_type='text')

    str = ''
    attr_set = EnaStudyAttr.objects.filter(ena_study__id=study.id)
    if attr_set.exists():
        for attr in attr_set:
            str += '<div class="form-group col-sm-10">'
            str += '<div class="attr_vals">'
            str += '<input type="text" class="col-sm-3 attr" name="tag_1" placeholder="tag" value="' + attr.tag + '"/>'
            str += '<input type="text" class="col-sm-3 attr" name="tag_1" placeholder="tag" value="' + attr.value + '"/>'
            str += '<input type="text" class="col-sm-3 attr" name="tag_1" placeholder="tag" value="' + attr.unit + '"/>'
            str += '</div>'
            str += '</div>'
    return HttpResponse(str, content_type='html')

def get_ena_sample_controls(request):
    html = parsers.get_sample_form_controls('web_copo/xml/schemas/ena/SRA.sample.xsd.xml')
    return HttpResponse(html, content_type='html')

def save_ena_study_callback(request):
    return_type = True;
    values = jsonpickle.decode(request.GET['values'])
    values.pop('', None)
    attributes = jsonpickle.decode(request.GET['attributes'])
    collection_id = request.GET['collection_id']
    study_id = request.GET['study_id']

    #check to see if study_id had been provided, if not we are saving a new study, if so that we should update an
    #existing study
    if study_id:
        e = EnaStudy.objects.get(pk=study_id)
        e.study_title=values['STUDY_TITLE']
        e.study_type=values['STUDY_TYPE']
        e.study_abstract=values['STUDY_ABSTRACT']
        e.center_name=values['CENTER_NAME']
        e.study_description=values['STUDY_DESCRIPTION']
        e.center_project_name=values['CENTER_PROJECT_NAME']
        e.save()

        #now clear existing attributes and add the updated set
        for a in e.enastudyattr_set.all():
            a.delete()
        for att_group in attributes:
                a = EnaStudyAttr(
                    ena_study=e,
                    tag=att_group[0],
                    value=att_group[1],
                    unit=att_group[2]
                )
                a.save()
    else:
        try:
            #make the study object
            e = make_and_save_ena_study(collection_id, **values)
            #now make attribute objects
            for att_group in attributes:
                a = EnaStudyAttr(
                    ena_study=e,
                    tag=att_group[0],
                    value=att_group[1],
                    unit=att_group[2]
                )
                a.save()
        except(TypeError):
            return_type = False

    return_structure = {'return_value':return_type}
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')


def make_and_save_ena_study(c_id, CENTER_NAME, STUDY_DESCRIPTION, STUDY_TYPE, CENTER_PROJECT_NAME, STUDY_ABSTRACT, STUDY_TITLE):
    e = EnaStudy()
    e.collection_id=c_id
    e.study_title=STUDY_TITLE
    e.study_type=STUDY_TYPE
    e.study_abstract=STUDY_ABSTRACT
    e.center_name=CENTER_NAME
    e.study_description=STUDY_DESCRIPTION
    e.center_project_id=CENTER_PROJECT_NAME
    e.save()
    return e


def save_ena_sample_callback(request):
    #get sample form list, attribute list, and the collection id
    collection_id = jsonpickle.decode(request.GET['collection_id'])
    study_id = request.GET['study_id']
    sample_id = request.GET['sample_id']
    #get details of user enetered sample
    sample = jsonpickle.decode(request.GET['sample_details'])
    #if a sample_id has been supplied then we dealing with an existing sample so should collect it from the db
    #and edit it. If not then create a new sample
    if sample_id:
        enasample = EnaSample.objects.get(pk=sample_id)
        enasample.title=sample['TITLE']
        enasample.taxon_id=sample['TAXON_ID']
        enasample.common_name=sample['COMMON_NAME']
        enasample.anonymized_name=sample['ANONYMIZED_NAME']
        enasample.individual_name=sample['INDIVIDUAL_NAME']
        enasample.scientific_name=sample['SCIENTIFIC_NAME']
        enasample.description=sample['DESCRIPTION']
        enasample.save()

        #now clear attributes and readd the new set
        attr = jsonpickle.decode(request.GET['sample_attr'])

        attrset = enasample.enasampleattr_set.all()
        for a in attrset:
            a.delete()
        for a in attr:
            at = EnaSampleAttr(tag=a[0], value=a[1], unit=a[2])
            at.ena_sample = enasample
            at.save()
        out = get_sample_html_from_collection_id(collection_id)

    else:

        attr = jsonpickle.decode(request.GET['sample_attr'])

        #get study
        collection_id = int(collection_id)
        study = EnaStudy.objects.get(pk=study_id)

        #now make sample
        enasample = EnaSample()
        enasample.title=sample['TITLE']
        enasample.taxon_id=sample['TAXON_ID']
        enasample.common_name=sample['COMMON_NAME']
        enasample.anonymized_name=sample['ANONYMIZED_NAME']
        enasample.individual_name=sample['INDIVIDUAL_NAME']
        enasample.scientific_name=sample['SCIENTIFIC_NAME']
        enasample.description=sample['DESCRIPTION']
        enasample.ena_study=study
        enasample.save()

        for a in attr:
            at = EnaSampleAttr(tag=a[0], value=a[1], unit=a[2])
            at.ena_sample = enasample
            at.save()
        out = get_sample_html_from_collection_id(collection_id)

    return HttpResponse(out, content_type='html')

def populate_samples_form(request):
    collection_id = request.GET['collection_id']
    out = get_sample_html_from_collection_id(collection_id)
    return HttpResponse(out, content_type='html')

def get_sample_html(request):
    sample_id = request.GET['sample_id']
    s = EnaSample.objects.get(id=sample_id)
    sa = EnaSampleAttr.objects.filter(ena_sample__id=s.id)
    out = {}
    out['sample_id'] = str(s.id)
    out['title'] = s.title
    out['taxon_id'] = s.taxon_id
    out['scientific_name'] = s.scientific_name
    out['common_name'] = s.common_name
    out['anonymized_name'] = s.anonymized_name
    out['individual_name'] = s.individual_name
    out['description'] = s.description
    out['attributes'] = serializers.serialize("json", sa)
    data = serializers.serialize("json", sa)
    j = jsonpickle.encode(out)
    return HttpResponse(j, content_type='json')

def populate_data_dropdowns(request):
    #specify path for experiment xsd schema
    xsd_path = 'web_copo/xml/schemas/ena/SRA.experiment.xsd.xml'
    out = {}
    out['strategy_dd'] = parsers.get_library_dropdown(xsd_path, 'LIBRARY_STRATEGY')
    out['selection_dd'] = parsers.get_library_dropdown(xsd_path, 'LIBRARY_SELECTION')
    out['source_dd'] = parsers.get_library_dropdown(xsd_path, 'LIBRARY_SOURCE')
    out = jsonpickle.encode(out)
    return HttpResponse(out, content_type='json')





def get_instrument_models(request):
    #return instrument model list depending on input type
    type = request.GET['dd_value']
    out = ''
    if type == 'LS454':
        out += '<option value="454_GS">454 GS</option>'
        out += '<option value="454_GS_20454_GS_FLX">454 GS 20454 GS FLX</option>'
        out += '<option value="454_GS_FLX+">454 GS FLX+</option>'
        out += '<option value="454_GS_FLX_Titanium">454 GS FLX Titanium</option>'
        out += '<option value="454_GS_Junior">454 GS Junior</option>'
        out += '<option value="unspecified">Unspecified</option>'

    elif type == 'ILLUMINA':
        out += '<option value="ILLUMINA_GENOME_ANALYSER">Illumina Genome Analyzer</option>'
        out += '<option value="ILLUMINA_GENOME_ANALYSER_II">Illumina Genome Analyzer II</option>'
        out += '<option value="ILLUMINA_GENOME_ANALYSER_IIx">Illumina Genome Analyzer IIx</option>'
        out += '<option value="ILLUMINA_HISEQ_2500">Illumina HiSeq 2500</option>'
        out += '<option value="ILLUMINA_HISEQ_2000">Illumina HiSeq 2000</option>'
        out += '<option value="ILLUMINA_HISEQ_1500">Illumina HiSeq 1500</option>'
        out += '<option value="ILLUMINA_HISEQ_1500">Illumina HiSeq 1000</option>'
        out += '<option value="ILLUMINA_MISEQ">Illumina MiSeq</option>'
        out += '<option value="ILLUMINA_HISCANSQ">Illumina HiScanSQ</option>'
        out += '<option value="ILLUMINA_HISEQ_X_TEN">HiSeq X Ten</option>'
        out += '<option value="ILLUMINA_NEXTSEQ_500">NextSeq 500</option>'
        out += '<option value="UNSPECIFIED">Unspecified</option>'

    elif type == 'COMPLETE_GENOMICS':
        out += '<option value="COMPLETE_GENOMICS">Complete Genomics</option>'
        out += '<option value="UNSPECIFIED">Unspecified</option>'

    elif type == 'PACBIO_SMRT':
        out += '<option value="PACBIO_RS">PacBio RS</option>'
        out += '<option value="PACBIO_RS_II">PacBio RS II</option>'
        out += '<option value="UNSPECIFIED">Unspecified</option>'

    elif type == 'ION_TORRENT':
        out += '<option value="ION_TORRENT_PGM">Ion Torrent PGM</option>'
        out += '<option value="ION_TORRENT_PROTON">Ion Torrent Proton</option>'
        out += '<option value="UNSPECIFIED">Unspecified</option>'

    elif type == 'OXFORD_NANOPORE':
        out += '<option value="MINION">MinION</option>'
        out += '<option value="GRIDION">GridION</option>'
        out += '<option value="UNSPECIFIED">Unspecified</option>'

    else:
        out += '<option value="AB_3730XL_GENETIC_ANALYZER">AB 3730xL Genetic Analyzer</option>'
        out += '<option value="AB_3730_GENETIC_ANALYZER">AB 3730 Genetic Analyzer</option>'
        out += '<option value="AB_3500XL_GENETIC_ANALYZER">AB 3500xL Genetic Analyzer</option>'
        out += '<option value="AB_3500_GENETIC_ANALYZER">AB 3500 Genetic Analyzer</option>'
        out += '<option value="AB_3130XL_GENETIC_ANALYZER">AB 3130xL Genetic Analyzer</option>'
        out += '<option value="AB_3130_GENETIC_ANALYZER">AB 3130 Genetic Analyzer</option>'
        out += '<option value="AB_310_GENETIC_ANALYZER">AB 310 Genetic Analyzer</option>'

    return HttpResponse(out, content_type='html')


def get_experimental_samples(request):

    study_id = request.GET['study_id']
    samples = EnaSample.objects.filter(ena_study__id=study_id)
    data = serializers.serialize("json", samples)
    return HttpResponse(data, content_type="json")

def receive_data_file(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        f = request.FILES['ff_file']
        handle_uploaded_file(f)

    # Redirect to the document list after POST
    return HttpResponse('abcd', content_type='json')