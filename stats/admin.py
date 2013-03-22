from django.contrib import admin
from stats.models import Metric, Instrument, Reading


class MetricAdmin(admin.ModelAdmin):
    list_display = ['name']


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Metric, MetricAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Reading)
