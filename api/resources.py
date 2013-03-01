from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie import fields
from stats.models import Request, ExceptionLog, Traceback, Project, Metric,\
    MetricData, Instrument, Event
from django.core.exceptions import ObjectDoesNotExist
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

        obj_list = self.obj_get_list(bundle, **clean_kwargs).order_by('timestamp')

        buckets = []
        this_bucket = from_date

        annotations = simplejson.loads(bundle.request.GET.get('annotations', "[]"))
        aggregations = simplejson.loads(bundle.request.GET.get('aggregations', "[]"))

        # annotations come first
        annotation_params = dict((a['name'], self.agg_funcs[a['func']](a['attr'])) for a in annotations)
        obj_list = obj_list.annotate(**annotation_params)

        while this_bucket < to_date:
            next_bucket = this_bucket + timedelta(seconds=width)
            bucket_obj = obj_list.filter(timestamp__gte=this_bucket,
                                         timestamp__lt=next_bucket)

            count = bucket_obj.count()
            if count > 0:
                bucket = {
                    "timestamp": this_bucket.isoformat(),
                    "count": bucket_obj.count()
                }

                aggregation_params = dict((a['name'], self.agg_funcs[a['func']](a['attr'])) for a in aggregations)
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


class TracebackResource(ModelResource):
    trace = fields.CharField('trace')

    class Meta:
        queryset = Traceback.objects.all()
        resource_name = 'tracebacks'
        allowed_methods = ['get', 'post', 'patch', 'put']
        authorization = Authorization()
        authentication = Authentication()


class ExceptionResource(ModelResource):
    exception_type = fields.CharField('exception_type')
    exception_value = fields.CharField('exception_value')
    last_seen = fields.DateTimeField('last_seen', null=True, readonly=True)
    count = fields.IntegerField('count', default=0, readonly=True)

    # def dehydrate_last_seen(self, bundle):
        # return bundle.obj.request_set.order_by('-timestamp')[0].timestamp

    class Meta:
        queryset = ExceptionLog.objects.all().annotate(
            last_seen=Max('request__timestamp'), count=Count('request'))
        resource_name = 'exceptions'
        allowed_methods = ['get', 'post', 'patch', 'put']
        authorization = Authorization()
        authentication = Authentication()
        ordering = [
            'last_seen',
            'count'
        ]


class RequestResource(BucketResource):
    timestamp = fields.DateTimeField('timestamp')
    username = fields.CharField('username')
    method = fields.CharField('method')
    url = fields.CharField('url')
    status = fields.IntegerField('status')
    time = fields.FloatField('time')
    exception = fields.ToOneField(ExceptionResource,
                                  'exception_log',
                                  null=True)
    traceback = fields.ToOneField(TracebackResource,
                                  'traceback',
                                  null=True)
    hostname = fields.CharField('hostname')

    def full_hydrate(self, bundle):
        bundle.obj.project = self.get_project(bundle)
        return super(RequestResource, self).full_hydrate(bundle)

    def save_related(self, bundle):
        # almost entirely identical to super method
        project = self.get_project(bundle)
        for field_name, field_object in self.fields.items():
            if not getattr(field_object, 'is_related', False):
                continue

            if getattr(field_object, 'is_m2m', False):
                continue

            if not field_object.attribute:
                continue

            if field_object.blank:
                continue

            # Get the object.
            try:
                related_obj = getattr(bundle.obj, field_object.attribute)
            except ObjectDoesNotExist:
                related_obj = None

            # Because sometimes it's ``None`` & that's OK.
            if related_obj:
                related_obj.project = project
                related_obj.save()
                setattr(bundle.obj, field_object.attribute, related_obj)

    def get_project(self, bundle):
        # key = bundle.request.META.get("HTTP_KEY")
        try:
            project = Project.objects.get(id=1)  # TODO fix this to use key
            return project
        except Project.DoesNotExist:
            return None

    class Meta:
        queryset = Request.objects.order_by('-timestamp')
        resource_name = 'requests'
        allowed_methods = ['get', 'post', 'patch', 'put']
        filtering = {
            'timestamp': ALL,
            'username': ALL,
            'method': ALL,
            'url': ALL,
            'status': ALL,
            'time': ALL
        }
        ordering = [
            'time',
        ]
        authorization = Authorization()
        authentication = Authentication()


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


class InstrumentResource(ModelResource):
    metric = fields.CharField('metric__slug')
    annotations = fields.ListField('annotations')
    aggregations = fields.ListField('aggregations')

    def dehydrate_annotations(self, bundle):
        return simplejson.loads(bundle.obj.annotations)

    def dehydrate_aggregations(self, bundle):
        return simplejson.loads(bundle.obj.aggregations)

    def build_filters(self, filters=None):
        slug = None
        if filters is not None:
            if 'project' in filters:
                slug = filters['project']
                del filters['project']
        result = super(InstrumentResource, self).build_filters(filters)
        if slug:
            result["metric__project__slug"] = slug
        return result

    class Meta:
        queryset = Instrument.objects.all()
        resource_name = "instruments"
        fields = ['name']


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
