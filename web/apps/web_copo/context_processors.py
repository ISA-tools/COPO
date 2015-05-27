__author__ = 'felix.shaw@tgac.ac.uk - 27/05/15'
from apps.web_copo.mongo.copo_base_da import Profile_Status_Info as psi

def get_status(request):

    # call method to obtain number of profiles which have outstanding issues
    num_issues = psi().get_profiles_status()
    if num_issues == 0:
        return {'issues': ''}
    else:
        return {'issues': num_issues}