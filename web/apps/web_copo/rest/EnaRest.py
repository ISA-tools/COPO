import uuid

__author__ = 'fshaw'
import gzip
import os

import hashlib
from django.http import HttpResponse
from django.core.context_processors import csrf
from rest_framework.renderers import JSONRenderer
import jsonpickle
from django.core.files.base import ContentFile
from bson.json_util import dumps

from chunked_upload.models import ChunkedUpload
import web.apps.web_copo.xml_tools.EnaParsers as parsers
import web.apps.web_copo.utils.EnaUtils as u
# from web.apps.web_copo.repos.irods import *
from settings_dev import MEDIA_ROOT
from dal.ena_da import EnaCollection
from dal.copo_base_da import Collection_Head
from dal.mongo_util import cursor_to_list


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'

        super(JSONResponse, self).__init__(content, **kwargs)




'''
def get_ena_study_attr(request):
    c_id = request.GET['collection_id']
    try:
        study = EnaStudy.objects.get(collection__id=1)
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
'''

def get_ena_sample_controls(request):
    html = parsers.get_sample_form_controls('apps/web_copo/xml_tools/schemas/ena/SRA.sample.xsd.xml')
    return HttpResponse(html, content_type='html')


def save_ena_study(request):
    return_type = True;
    values = jsonpickle.decode(request.GET['values'])
    values.pop('', None)
    attributes = jsonpickle.decode(request.GET['attributes'])
    collection_id = request.GET['collection_id']
    ena_study_id = request.GET['study_id']
    out = ''
    if(ena_study_id == ''):
        ena_study_id = EnaCollection().add_study(values, attributes)
        Collection_Head().add_collection_details(collection_id, ena_study_id)
        request.session['collection_details'] = str(ena_study_id)
        return_structure = {'return_value': return_type, 'study_id': str(ena_study_id)}
        out = jsonpickle.encode(return_structure)
    else:
        EnaCollection().update_study(ena_study_id, values, attributes)
        request.session['study_id'] = str(ena_study_id)
        return_structure = {'return_value': return_type, 'study_id': str(ena_study_id)}
        out = jsonpickle.encode(return_structure)

    return HttpResponse(out, content_type='json')



def save_ena_sample_callback(request):
    # get sample form list, attribute list, and the collection id
    #collection_id = request.GET['collection_id']
    details_id = request.GET['study_id']
    sample_id = request.GET['sample_id']
    #get details of user enetered sample
    sample = jsonpickle.decode(request.GET['sample_details'])
    attr = jsonpickle.decode(request.GET['sample_attr'])

    if sample_id == '':
        EnaCollection().add_sample_to_study(sample, attr, details_id)
    else:
        EnaCollection().update_sample_in_study(sample, attr, details_id, sample_id)

    #now clear attributes and readd the new set
    out = u.get_sample_html_from_details_id(details_id)

    return HttpResponse(out, content_type='html')


def populate_samples_form(request):
    collection_id = request.GET['collection_id']
    collection_id = 1
    out = u.get_sample_html_from_collection_id(collection_id)
    return HttpResponse(out, content_type='html')


def get_sample_html(request):
    sample_id = request.GET['sample_id']
    #s = EnaSample.objects.get(id=sample_id)
    #sa = EnaSampleAttr.objects.filter(ena_sample__id=s.id)
    s = EnaCollection().get_sample(sample_id)
    out = {}
    out['sample_id'] = str(s["_id"])
    out['Source_Name'] = s["Source_Name"]
    out['Taxon_ID'] = s["Taxon_ID"]
    out['Scientific_Name'] = s["Scientific_Name"]
    out['Common_Name'] = s["Common_Name"]
    out['Anonymized_Name'] = s["Anonymized_Name"]
    out['Individual_Name'] = s["Individual_Name"]
    out['Description'] = s["Description"]
    out['Characteristics'] = s["Characteristics"]

    return HttpResponse(jsonpickle.encode(out), content_type='json')


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
    samples = EnaCollection().get_samples_in_study(study_id)
    samples = cursor_to_list(samples)
    data = dumps(samples)

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
        destination = open(os.path.join(MEDIA_ROOT, path.file.name), 'wb+')
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

        # status = register_to_irods()
        # print(status)

        str = jsonpickle.encode(files)
    return HttpResponse(str, content_type='json')


def hash_upload(request):
    #utiltiy method to create an md5 hash of a given file path
    # open uploaded file
    file_id = request.GET['file_id']
    print('hash started ' + file_id)
    file_upload = ChunkedUpload.objects.get(pk=file_id)
    file_name = os.path.join(MEDIA_ROOT, file_upload.file.name)

    #now hash opened file
    md5 = hashlib.md5()
    with open(file_name, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    output_dict = {'output_hash': md5.hexdigest(), 'file_id': file_id}
    out = jsonpickle.encode(output_dict)
    print('hash complete ' + file_id)
    return HttpResponse(out, content_type='json')


def inspect_file(request):
    #utillity method to examine a file and return meta-data to the frontend
    output_dict = {'file_type': 'unknown', 'gzip': False}
    # get reference to file
    file_id = request.GET['file_id']
    chunked_upload = ChunkedUpload.objects.get(id=int(file_id))
    file_name = os.path.join(MEDIA_ROOT, chunked_upload.file.name)

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
    print("zip started " + f_id)
    file_obj = ChunkedUpload.objects.get(pk=f_id)

    #get the name of the file to zip and change its suffix to .gz
    input_file_name = os.path.join(MEDIA_ROOT, file_obj.file.name)
    output_file_name = os.path.splitext(file_obj.filename)[0] + '.gz'
    try:
        #open the file as gzip acrchive...set compression level
        temp_name = os.path.join(MEDIA_ROOT, str(uuid.uuid4()) + '.tmp')
        myzip = gzip.open(temp_name, 'wb', compresslevel=1)
        src = open(input_file_name, 'r')

        #write input file to gzip archive in n byte chunks
        n = 100000000
        for chunk in iter(lambda: src.read(n), ''):
            myzip.write(bytes(chunk, 'UTF-8'))
    finally:

        myzip.close()
        src.close()

    print('zip complete ' + f_id)
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
        experiment_id = EnaCollection().add_experiment_to_study(per_panel, common, request.session["study_id"])
    else:
        #else retrieve the existing object
        experiment_id = EnaCollection().update_experiment_in_study(per_panel, common, request.session["study_id"])

    #here we need to loop through per_file.files adding object to exp files list
    for k in range(0, len(per_panel['files'])):
        c = ChunkedUpload.objects.get(id=int(per_panel['files'][k]))
        if len(per_panel['hashes'])>k:
            hash = per_panel['hashes'][k]
        else:
            hash = ''
        EnaCollection().add_file_to_study(request.session['study_id'], experiment_id, c.id, hash)
    out = {'experiment_id': experiment_id}

    return HttpResponse(jsonpickle.encode(experiment_id), content_type='text/plain')


def get_experiment_table_data(request):
    experiment_ids = EnaCollection().get_distict_experiment_ids_in_study_(request.GET.get('study_id'))

    elements = []
    for id in experiment_ids:

        #for unique each experimental modal id, get corresponding experiments
        for me in EnaCollection().get_experiments_by_modal_id(id):
            out = {}
            out['group_size'] = 'unknown'
            if not me['experiments'][0]['copo_exp_name']:
                out['group_name'] = "default"
            else:
                out['group_name'] = me['experiments'][0]['copo_exp_name']
            out['platform'] = me['experiments'][0]['Sample_Name']
            out['last_modified'] = str(me['experiments'][0]['last_updated'])
            out['data_modal_id'] = id
            elements.append(out)



    el = jsonpickle.encode(elements)

    return HttpResponse(el, content_type='text/plain')


def populate_exp_modal(request):
    #this method gets the current files associated with an ENA experiment or group of ENA experiments
    #and populates a table in the upload modal dialogue along with delete functionality
    data_modal_id = request.GET.get('data_modal_id')
    #get experiments
    exps = EnaCollection().get_experiments_by_modal_id(data_modal_id)

    output_files = []

    for exp in exps:
        #for each experiment get a list of the associated files
        files = EnaCollection().get_files_by_experiment_id(exp["experiments"][0]["_id"])
        for file in files:
            #get chunked upload object
            ch = ChunkedUpload.objects.get(id=file['files']["chunked_upload_id"])
            #now populate output object
            f = {}
            f['id']=str(ch.id)
            f['name']=ch.filename
            f['size']=u.filesize_toString(ch.offset)
            f['md5']=file['files']["hash"]
            f['data_modal_id']=data_modal_id
            f['panel_id']=exp["experiments"][0]["panel_id"]
            f['experiment_id']=str(exp["experiments"][0]["_id"])
            output_files.append(f)

    return HttpResponse(jsonpickle.encode(output_files), content_type='text/plain')

def delete_file(request):
    #method deletes the given file, and database objects for a given file_id
    file_id = request.POST.get('file_id')
    #get chunked upload object
    #c_id = EnaCollection().get_chunked_upload_id_from_file_id(file_id)
    ch = ChunkedUpload.objects.get(id=int(file_id))

    #get full path
    filepath = os.path.join(MEDIA_ROOT, ch.file.name)
    #delete file
    os.remove(filepath)
    #now delete database entries for the file
    EnaCollection().remove_file_from_experiment(file_id)
    ch.delete()
    return HttpResponse(request.POST.get('file_id'), content_type='text/plain')
