/*global Backbone, window, _, $*/
(function () {
    "use strict";
    this.models.Request = Backbone.Model.extend({
        urlRoot: "/api/v1/requests/",
        get_detail_url: function () {
            return "/requests/" + this.get('id');
        }
    });

    this.models.RequestCollection = Backbone.Collection.extend({
        model: this.models.Request,
        urlRoot: "/api/v1/requests/"
    });

    this.models.BucketReport = Backbone.Model.extend({
        defaults: {
            filters: {},
            aggregates: [],
            annotations: [],
            data: null
        },
        fetch: function (cb, context) {
            var url, data;
            url = '/api/v1/' + this.get('resource') + '/buckets/';
            data = {
                from: this.get('from').toISOString(),
                to: this.get('to').toISOString(),
                width: this.get('width'),
                aggregates: JSON.stringify(this.get('aggregates')),
                annotations: JSON.stringify(this.get('annotations'))
            };
            _.extend(data, this.get('filters'));

            return $.ajax({
                url: url,
                dataType: 'json',
            type: 'GET',
                data: data,
                context: this,
                success: function (data, statux, xhr) {
                    this.set({data: data});
                    if (_.isFunction(cb)) {
                        cb.call(context);
                    }
                }
            });
        }
    });

    this.models.BucketCollection = Backbone.Collection.extend({
        model: this.models.BucketReport
    });

    this.models.ExceptionLog = Backbone.Model.extend({
        urlRoot: '/api/v1/exceptions/'
    });

    this.models.ExceptionLogCollection = Backbone.Collection.extend({
        urlRoot: '/api/v1/exceptions',
        model: this.models.ExceptionLog
    });

    this.models.Metric = Backbone.Model.extend({
        urlRoot: '/api/v1/metrics/',
    });
}.call(window.Statistician));