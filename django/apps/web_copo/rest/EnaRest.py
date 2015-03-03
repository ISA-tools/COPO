__author__ = 'fshaw'
import os
import hashlib
import gzip
import uuid

from django.http import HttpResponse
from django.core.context_processors import csrf
from rest_framework.renderers import JSONRenderer
import jsonpickle
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from chunked_upload.models import ChunkedUpload
from django.core.files.base import ContentFile

from apps.web_copo.models import Collection, EnaStudy, EnaSample, EnaStudyAttr, EnaSampleAttr, EnaExperiment, ExpFile
import apps.web_copo.xml_tools.EnaParsers as parsers
import apps.web_copo.utils.EnaUtils as u
import project_copo.settings.settings as settings


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'

        super(JSONResponse, self).__init__(content, **kwargs)


def get_ena_study_controls(request):
    # get list of controllers
    out = parsers.get_study_form_controls('apps/web_copo/xml_tools/schemas/ena/SRA.study.xsd.xml')
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
            if (obj.type == 'input'):
                out_str += "<input type='text' class='form-control' id='" + str(obj.name) + "' name='" + str(
                    obj.name) + "' value='" + str(getattr(study, obj.name.lower())) + "'/>"
            elif (obj.type == 'textarea'):
                out_str += "<textarea type='text' rows='6' class='form-control' id='" + str(
                    obj.name) + "' name='" + str(obj.name) + \
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
            if (obj.type == 'input'):
                out_str += "<input type='text' class='form-control' id='" + obj.name + "' name='" + obj.name + "'/>"
            elif (obj.type == 'textarea'):
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
    html = parsers.get_sample_form_controls('apps/web_copo/xml_tools/schemas/ena/SRA.sample.xsd.xml')
    return HttpResponse(html, content_type='html')


def save_ena_study_callback(request):
    return_type = True;
    values = jsonpickle.decode(request.GET['values'])
    values.pop('', None)
    attributes = jsonpickle.decode(request.GET['attributes'])
    collection_id = request.GET['collection_id']
    study_id = request.GET['study_id']

    # check to see if study_id had been provided, if not we are saving a new study, if so that we should update an
    #existing study
    if study_id:
        e = EnaStudy.objects.get(pk=study_id)
        e.study_title = values['STUDY_TITLE']
        e.study_type = values['STUDY_TYPE']
        e.study_abstract = values['STUDY_ABSTRACT']
        e.center_name = values['CENTER_NAME']
        e.study_description = values['STUDY_DESCRIPTION']
        e.center_project_name = values['CENTER_PROJECT_NAME']
        e.save()
        study_id = e.id
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

    return_structure = {'return_value': return_type, 'study_id': e.id}
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')


def make_and_save_ena_study(c_id, CENTER_NAME, STUDY_DESCRIPTION, STUDY_TYPE, CENTER_PROJECT_NAME, STUDY_ABSTRACT,
                            STUDY_TITLE):
    e = EnaStudy()
    e.collection_id = c_id
    e.study_title = STUDY_TITLE
    e.study_type = STUDY_TYPE
    e.study_abstract = STUDY_ABSTRACT
    e.center_name = CENTER_NAME
    e.study_description = STUDY_DESCRIPTION
    e.center_project_id = CENTER_PROJECT_NAME
    e.save()
    return e


def save_ena_sample_callback(request):
    # get sample form list, attribute list, and the collection id
    collection_id = jsonpickle.decode(request.GET['collection_id'])
    study_id = request.GET['study_id']
    sample_id = request.GET['sample_id']
    #get details of user enetered sample
    sample = jsonpickle.decode(request.GET['sample_details'])
    #if a sample_id has been supplied then we dealing with an existing sample so should collect it from the db
    #and edit it. If not then create a new sample
    if sample_id:
        enasample = EnaSample.objects.get(pk=sample_id)
        enasample.title = sample['TITLE']
        enasample.taxon_id = sample['TAXON_ID']
        enasample.common_name = sample['COMMON_NAME']
        enasample.anonymized_name = sample['ANONYMIZED_NAME']
        enasample.individual_name = sample['INDIVIDUAL_NAME']
        enasample.scientific_name = sample['SCIENTIFIC_NAME']
        enasample.description = sample['DESCRIPTION']
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
        out = u.get_sample_html_from_collection_id(collection_id)

    else:

        attr = jsonpickle.decode(request.GET['sample_attr'])

        #get study
        collection_id = int(collection_id)
        study = EnaStudy.objects.get(pk=study_id)

        #now make sample
        enasample = EnaSample()
        enasample.title = sample['TITLE']
        enasample.taxon_id = sample['TAXON_ID']
        enasample.common_name = sample['COMMON_NAME']
        enasample.anonymized_name = sample['ANONYMIZED_NAME']
        enasample.individual_name = sample['INDIVIDUAL_NAME']
        enasample.scientific_name = sample['SCIENTIFIC_NAME']
        enasample.description = sample['DESCRIPTION']
        enasample.ena_study = study
        enasample.save()

        for a in attr:
            at = EnaSampleAttr(tag=a[0], value=a[1], unit=a[2])
            at.ena_sample = enasample
            at.save()
        out = u.get_sample_html_from_collection_id(collection_id)

    return HttpResponse(out, content_type='html')


def populate_samples_form(request):
    collection_id = request.GET['collection_id']
    out = u.get_sample_html_from_collection_id(collection_id)
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
    # specify path for experiment xsd schema
    xsd_path = 'apps/web_copo/xml_tools/schemas/ena/SRA.experiment.xsd.xml'
    out = {}
    out['strategy_dd'] = parsers.get_library_dropdown(xsd_path, 'LIBRARY_STRATEGY')
    out['selection_dd'] = parsers.get_library_dropdown(xsd_path, 'LIBRARY_SELECTION')
    out['source_dd'] = parsers.get_library_dropdown(xsd_path, 'LIBRARY_SOURCE')
    out = jsonpickle.encode(out)
    return HttpResponse(out, content_type='json')


def get_instrument_models(request):
    # return instrument model list depending on input type
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

    #this method is called for writing smaller files (<= 260MB) to disk, larger files use the
    #upload method in ChunkedUpload class

    from django.utils import timezone
    # need to make a chunked upload record to store deails of the file
    if request.method == 'POST':

        c = {}
        f = request.FILES['file']

        fname = f.__str__()
        attrs = {'user': request.user, 'filename': fname, 'completed_on': timezone.now(), 'offset': f.size}
        chunked_upload = ChunkedUpload(**attrs)
        # file starts empty
        chunked_upload.file.save(name='', content=ContentFile(''), save=True)


        path = chunked_upload.file
        destination = open(os.path.join(settings.MEDIA_ROOT, path.file.name), 'w+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        c.update(csrf(request))

        # create output structure to pass back to jquery-upload
        files = {}
        files['files'] = {}
        files['files']['name'] = f._name

        files['files']['size'] = path.size / (1000 * 1000.0)
        files['files']['id'] = chunked_upload.id
        files['files']['url'] = ''
        files['files']['thumbnailUrl'] = ''
        files['files']['deleteUrl'] = ''
        files['files']['deleteType'] = 'DELETE'

        str = jsonpickle.encode(files)
    return HttpResponse(str, content_type='json')


def hash_upload(request):
    #utiltiy method to create an md5 hash of a given file path
    # open uploaded file
    file_id = request.GET['file_id']
    print 'hash started ' + file_id
    file_upload = ChunkedUpload.objects.get(pk=file_id)
    file_name = os.path.join(settings.MEDIA_ROOT, file_upload.file.name)

    #now hash opened file
    md5 = hashlib.md5()
    with open(file_name, 'r') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    output_dict = {'output_hash': md5.hexdigest(), 'file_id': file_id}
    out = jsonpickle.encode(output_dict)
    print 'hash complete ' + file_id
    return HttpResponse(out, content_type='json')


def inspect_file(request):
    #utillity method to examine a file and return meta-data to the frontend
    output_dict = {'file_type': 'unknown', 'gzip': False}
    # get reference to file
    file_id = request.GET['file_id']
    chunked_upload = ChunkedUpload.objects.get(id=int(file_id))
    file_name = os.path.join(settings.MEDIA_ROOT, chunked_upload.file.name)

    if (u.is_fastq_file(file_name)):
        output_dict['file_type'] = 'fastq'
        #if we have a fastq file, check that it is gzipped
        if (u.is_gzipped(file_name)):
            output_dict['gzip'] = True
    elif (u.is_sam_file(file_name)):
        output_dict['file_type'] = 'sam'
    elif (u.is_bam_file(file_name)):
        output_dict['file_type'] = 'bam'

    out = jsonpickle.encode(output_dict)
    return HttpResponse(out, content_type='json')


def zip_file(request):
    # need to get a reference to the file to zip
    f_id = request.GET['file_id']
    print "zip started " + f_id
    file_obj = ChunkedUpload.objects.get(pk=f_id)

    #get the name of the file to zip and change its suffix to .gz
    input_file_name = os.path.join(settings.MEDIA_ROOT, file_obj.file.name)
    output_file_name = os.path.splitext(file_obj.filename)[0] + '.gz'
    try:
        #open the file as gzip acrchive...set compression level
        temp_name = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4()) + '.tmp')
        myzip = gzip.open(temp_name, 'wb', compresslevel=1)
        src = open(input_file_name, 'rb')

        #write input file to gzip archive in n byte chunks
        n = 100000000
        for chunk in iter(lambda: src.read(n), ''):
            myzip.write(chunk)
    finally:

        myzip.close()
        src.close()

    print 'zip complete ' + f_id
    #now need to delete the old file and update the file record with the new file
    file_obj.filename = output_file_name
    file_obj.save()

    os.remove(input_file_name)
    os.rename(temp_name, input_file_name)
    stats = os.stat(input_file_name)
    new_file_size = stats.st_size / 1000 / 1000


    out = {'zipped': True, 'file_name':output_file_name, 'file_size':new_file_size}
    out = jsonpickle.encode(out)
    return HttpResponse(out, content_type='text/plain')

def save_experiment(request):
    #method to save ENA experiment object(s). One experiment object is created for each panel on the
    #front-end (although as far as the users are concerned, multiple panels can belong to the same experiment

    #certain attributes are shared between the different experiments generated by the front end
    common = jsonpickle.decode(request.POST.get('common'))
    #others are particular to the individual object
    per_panel = jsonpickle.decode(request.POST.get('per_panel'))

    if(per_panel['experiment_id'] == ''):
        #if we are dealing with a new experiment (i.e. no id has been supplied)
        #then create a new object
        exp = EnaExperiment()
    else:
        #else retrieve the existing object
        exp = EnaExperiment.objects.get(id=int(per_panel['experiment_id']))

    exp.platform = common['platform']
    exp.instrument = common['model']
    exp.lib_source = common['lib_source']
    exp.lib_selection = common['lib_selection']
    exp.lib_strategy = common['lib_strategy']
    exp.panel_ordering = int(per_panel['panel_ordering'])
    exp.panel_id = per_panel['panel_id']
    exp.data_modal_id = per_panel['data_modal_id']
    exp.copo_exp_name = common['copo_exp_name']
    try:
        exp.insert_size = int(common['insert_size'])
    except:
        exp.insert_size = 0
    study_id = common['study']
    exp.study = EnaStudy.objects.get(id = int(study_id))
    sample_id = per_panel['sample_id']
    exp.sample = EnaSample.objects.get(id = int(sample_id))

    exp.lib_name = per_panel['lib_name']
    exp.file_type = per_panel['file_type']
    exp.save()
    #here we need to loop through per_fil.files creating new ExpFile objects for each file id

    for k in range(0, len(per_panel['files'])):
        #for each file in the list supplied, create a new
        #ExpFile object to join the experiment object and the chunked upload entry
        f = ExpFile()

        #get chunkedUpload object
        f.file = ChunkedUpload.objects.get(id=int(per_panel['files'][k]))
        #assign experiment
        f.experiment = exp
        f.md5_hash = per_panel['hashes'][k]
        f.save()
        out = {'experiment_id': exp.id}
        out = jsonpickle.encode(out)
    return HttpResponse(out, content_type='text/plain')

def get_experiment_table_data(request):
    #this method populates a table of current experiment objects for the given ENA study object.
    #this table is displayed in the Experiment Panel of an ENA Profile
    from datetime import datetime
    import pytz
    out = 'abc'

    #get all experiment objects for this study
    e = EnaExperiment.objects.filter(study_id=request.GET.get('study_id'))
    #now get a list of the unique data_modal_ids...this is what we should be returning a list of
    udm = e.values('data_modal_id').distinct()
    elements = []
    for modal in udm:
        #for each modal id, get corresponding experiments
        me = EnaExperiment.objects.filter(data_modal_id=modal['data_modal_id'])
        #do calculation to get the size of the related files and the date the group was last modified
        #get ids of experiment objects
        ids = set(exp.id for exp in me)
        #get related ExpFile objects
        file_set = ExpFile.objects.filter(experiment__in=ids)
        #get ids of related ExpFile objects
        ids = set(f.file_id for f in file_set)
        #get related chunked_upload objects
        chs = ChunkedUpload.objects.filter(id__in=ids)
        total = 0
        last_modified = datetime.min
        utc = pytz.UTC
        last_modified = utc.localize(last_modified)
        #calculate the size of the file group and when in was last modified
        if chs.exists():
            for upload in chs:
                total = total + upload.offset
                print(total)
                if upload.completed_on > last_modified:
                    last_modified = upload.completed_on
            #create output object
            out = {}
            group_type = me[0].platform
            fmt = '%d-%m-%Y %H:%M:%S'
            out['group_size'] = u.filesize_toString(total)
            out['group_name'] = me[0].copo_exp_name
            out['last_modified'] = last_modified.strftime(fmt)
            out['platform'] = group_type
            out['data_modal_id'] = modal['data_modal_id']
            elements.append(out)



    el = jsonpickle.encode(elements)

    return HttpResponse(el, content_type='text/plain')


def populate_exp_modal(request):
    #this method gets the current files associated with an ENA experiment or group of ENA experiments
    #and populates a table in the upload modal dialogue along with delete functionality
    data_modal_id = request.GET.get('data_modal_id')
    #get experiments
    exps = EnaExperiment.objects.filter(data_modal_id=data_modal_id)

    output_files = []

    for exp in exps:
        #for each experiment get a list of the associated files
        files = ExpFile.objects.filter(experiment__id=exp.id)
        for file in files:
            #get chunked upload object
            ch = file.file
            #now populate output object
            f = {}
            f['id']=ch.id
            f['name']=ch.filename
            f['size']=u.filesize_toString(ch.offset)
            f['md5']=file.md5_hash
            f['data_modal_id']=exp.data_modal_id
            f['panel_id']=exp.panel_id
            output_files.append(f)

    return HttpResponse(jsonpickle.encode(output_files), content_type='text/plain')

def delete_file(request):
    #method deletes the given file, and database objects for a given file_id
    file_id = request.POST.get('file_id')
    #get chunked upload object
    ch = ChunkedUpload.objects.get(id=int(file_id))
    ef = ch.expfile
    #get full path
    filepath = os.path.join(settings.MEDIA_ROOT, ch.file.name)
    #delete file
    os.remove(filepath)
    #now delete database entries for the file
    ef.delete()
    ch.delete()
    return HttpResponse(request.POST.get('file_id'), content_type='text/plain')


def submit_collection_handler(request):
    import apps.web_copo.utils.RepoSubmissionUtils as r
    #method to choose correct repo handler for the collection type
    collection_id = request.POST.get('collection_id')
    c = Collection.objects.get(id=collection_id)
    if c.type == 'ENA Submission':
        r.submit_ena(c)

    return HttpResponse('exiting', content_type='text/plain')
