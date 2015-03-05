from django.contrib import admin

from apps.web_copo.models import Collection, Resource, Profile, EnaStudy, EnaStudyAttr, EnaSample, EnaSampleAttr


# Register your models here.

admin.site.register(Collection)
admin.site.register(Resource)
admin.site.register(Profile)
admin.site.register(EnaStudy)
admin.site.register(EnaStudyAttr)
admin.site.register(EnaSample)
admin.site.register(EnaSampleAttr)
