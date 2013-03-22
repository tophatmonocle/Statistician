from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie import fields
from stats.models import Metric, MetricData, Instrument, Event, Reading
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from django.conf.urls.defaults import url
from tastypie.utils import trailing_slash
from tastypie.exceptions import BadRequest
from iso8601 import parse_date
from datetime import timedelta
from django.db.models import Avg, Max, Min, Sum, Variance, StdDev, Count
import simplejson


class BucketResource(ModelResource):
    max_buckets = 100
    agg_funcs = {
        "Avg": Avg,
        "Max": Max,
        "Min": Min,
        "Sum": Sum,
        "Variance": Variance,
        "StdDev": StdDev,
        "Count": Count
    }  # TODO do this dynamically

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/buckets%s$' % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('get_buckets'),
                name='api_get_buckets')
        ]

    def get_buckets(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        bundle = self.build_bundle(request=request)
        return self.create_response(request,
                                    self.build_buckets(bundle, **kwargs))

    def build_filters(self, filters=None):
        if filters is not None:
            if 'from' in filters:
                filters['timestamp__gte'] = filters['from']
            if 'to' in filters:
                filters['timestamp__lt'] = filters['to']
        return super(BucketResource, self).build_filters(filters)

    def build_buckets(self, bundle, **kwargs):
        clean_kwargs = self.remove_api_resource_names(kwargs)
        try:
            from_date = parse_date(bundle.request.GET.get('from'))
            to_date = parse_date(bundle.request.GET.get('to'))
        except:
            raise BadRequest('missing required fields: from, to')

        width = int(bundle.request.GET.get('width', 1))

        dt = (to_date - from_date).total_seconds()
        bucket_count = dt / width

        if bucket_count > self.max_buckets:
            width = dt / self.max_buckets

        if bucket_count < 0:
            raise BadRequest('to was less than from')

        buckets = []
        this_bucket = from_date

        obj_list = self.obj_get_list(bundle, **clean_kwargs).order_by('timestamp')
        readings = dict((a['name'], a) for a in simplejson.loads(bundle.request.GET.get('readings', "[]")))
        for name, a in readings.iteritems():
            a['list'] = obj_list.filter(metric__slug=a['metric'])

        while this_bucket < to_date:
            next_bucket = this_bucket + timedelta(seconds=width)
            bucket = {
                "timestamp": this_bucket.isoformat(),
            }

            for name, a in readings.iteritems():
                bucket_obj = a['list'].filter(timestamp__gte=this_bucket,
                                              timestamp__lt=next_bucket)

                aggregation_params = {a['name']: self.agg_funcs[a['method']]('value')}
                aggretate = bucket_obj.aggregate(**aggregation_params)
                bucket.update(aggretate)

            buckets.append(bucket)
            this_bucket = next_bucket

        result = {
            "total_count": obj_list.count(),
            "width": width,
            "buckets": buckets
        }

        return result


class MetricResource(ModelResource):
    def build_filters(self, filters=None):
        slug = None
        if filters is not None:
            if 'project' in filters:
                slug = filters['project']
                del filters['project']
        result = super(MetricResource, self).build_filters(filters)
        if slug:
            result["project__slug"] = slug
        return result

    class Meta:
        queryset = Metric.objects.all()
        resource_name = 'metrics'


class MetricDataResource(BucketResource):
    # metric = fields.ToOneField(MetricResource, 'metric')
    metric = fields.CharField()

    def build_filters(self, filters=None):
        slug = None
        if filters is not None:
            if 'metric' in filters:
                slug = filters['metric']
                del filters['metric']
        result = super(MetricDataResource, self).build_filters(filters)
        if slug:
            result["metric__slug"] = slug
        return result

    def dehydrate_metric(self, bundle):
        return bundle.obj.metric.slug

    def hydrate_metric(self, bundle):
        print bundle.request.POST
        bundle.obj.metric = Metric.objects.get(slug=bundle.data.get('metric'))
        return bundle

    class Meta:
        queryset = MetricData.objects.all()
        resource_name = 'metric_data'
        fields = ['value', 'timestamp']
        authorization = Authorization()
        authentication = Authentication()
        # authentication = StatsAuthentication()
        filtering = {
            'timestamp': ALL,
            # 'metric': ALL_WITH_RELATIONS
        }
        ordering = {
            'timestamp'
        }


class ReadingResource(ModelResource):
    metric_slug = fields.CharField()

    def dehydrate_metric_slug(self, bundle):
        return bundle.obj.metric.slug

    class Meta:
        queryset = Reading.objects.all()
        resource_name = "readings"
        fields = ['name', 'method', 'stroke', 'fill']


class InstrumentResource(ModelResource):
    readings = fields.ToManyField(ReadingResource, 'reading_set', full=True)

    # def build_filters(self, filters=None):
    #     slug = None
    #     if filters is not None:
    #         if 'project' in filters:
    #             slug = filters['project']
    #             del filters['project']
    #     result = super(InstrumentResource, self).build_filters(filters)
    #     if slug:
    #         result["metric__project__slug"] = slug
    #     return result

    class Meta:
        queryset = Instrument.objects.filter(id=9)
        resource_name = "instruments"
        fields = ['name', 'width', 'domain', 'units', 'offset', 'stack']


class EventResource(ModelResource):

    def build_filters(self, filters=None):
        slug = None
        if filters is not None:
            if 'project' in filters:
                slug = filters['project']
                del filters['project']
        result = super(EventResource, self).build_filters(filters)
        if slug:
            result["project__slug"] = slug
        return result

    class Meta:
        queryset = Event.objects.order_by('-timestamp')
        resource_name = "events"
