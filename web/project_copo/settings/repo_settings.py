
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
    }
}