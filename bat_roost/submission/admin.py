from django.contrib import admin
from django.contrib.gis.admin.options import GeoModelAdmin
from .models import Submission, SubmissionImage
from django.contrib.gis.admin import GeoModelAdmin
from leaflet.admin import LeafletGeoAdmin
class SubmissionAdmin(LeafletGeoAdmin):
    list_display=('user','location')
admin.site.register(Submission,SubmissionAdmin)
admin.site.register(SubmissionImage)

# Register your models here.
