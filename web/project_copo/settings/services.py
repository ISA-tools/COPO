# define parameters for repositories

REPOSITORIES = {
    'ENA': {
        'api': 'aspera',
        'resource_path': 'reposit/aspera/Aspera Connect.app/Contents/Resources/',
        'credentials': {
            'user_token': 'Webin-39962@webin.ebi.ac.uk',
            'password': 'toni12',  # TODO: probably in mongo?
            'remote_path': 'copo'
        }
    },
    'IRODS': {
        'api': 'irods',
        'resource_path': '/tempZone/home/rods/copo-data',
        'credentials': {
            'user_token': 'etuka',
            'host_token': 'v0546.nbi.ac.uk',
            'program': 'python',
            'password': 'RwvmPMC7',  # TODO: probably in mongo?
            'script': 'myptest.py'
        }
    },
    'ORCID': {
        'api': 'orcid',
        'client_id': '0000-0002-4011-2520',
        'client_secret': '634ce113-2768-40bf-a4a7-20e8fbf8aa10',
        'urls':{
            'ouath/token':'https://api.sandbox.orcid.org/oauth/token?',
            'base_url': 'https://sandbox.orcid.org',
            'authorise_url': 'http://orcid.org/oauth/authorize?client_id=0000-0002-4011-2520&response_type=code&scope=/authenticate&redirect_uri=http://127.0.0.1:8000/copo/',
            'redirect': 'http://127.0.0.1:8000/copo/',
        }
    }
}

SCHEMAS = {
    'ENA': {
        'path_to_json': 'apps/web_copo/schemas/ena/isa_ena_model.json'
    }
}
