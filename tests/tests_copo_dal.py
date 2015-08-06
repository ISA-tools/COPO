from django.test import TestCase


class DataAccessLayerTests(TestCase):
    def profile_put(self):
        from dal import Profile
        Profile().PUT("")
