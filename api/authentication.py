from tastypie.authentication import Authentication
from stats.models import Project


class StatsAuthentication(Authentication):
    def is_authenticated(self, request):
        method = request.method.lower()

        if method in ['put', 'post', 'patch']:
            print "project method"
            # you must have a project key to create or modify entries
            key = request.META.get("HTTP_KEY")
            try:
                request.project = Project.objects.get(key=key)
                print request.project
                return True
            except Project.DoesNotExist:
                return False

        # fall back to django
        return request.user.is_authenticated()
