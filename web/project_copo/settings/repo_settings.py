
# define parameters for repositories


REPO_LIB_PATHS = {
    "ASPERA": "reposit/aspera/Aspera Connect.app/Contents/Resources/",
    "IRODS": "/tempZone/home/rods/copo-data",
}


REPOSITORIES = {
    'ENA': {
        'api': 'aspera',
        'resource_path': 'reposit/aspera/Aspera Connect.app/Contents/Resources/'
    },
    'IRODS': {
        'api': 'irods',
        'resource_path': '/tempZone/home/rods/copo-data',
        'credentials': {
            'user_token': 'etuka',
            'host_token': 'v0546.nbi.ac.uk',
            'program': 'python',
            'password': 'RwvmPMC7',  # TODO: probably mongo?
            'script': 'myptest.py'
        }
    }
}
