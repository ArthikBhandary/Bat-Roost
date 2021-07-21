from django.contrib import admin

from .models import Submission, SubmissionImage

from leaflet.admin import LeafletGeoAdmin
class SubmissionAdmin(LeafletGeoAdmin):
    list_display=('user','location')
admin.site.register(Submission,SubmissionAdmin)
admin.site.register(SubmissionImage)

# Register your models here.
