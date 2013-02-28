/*global Backbone, window, _, $*/
(function () {
    "use strict";
    this.collections.Requests = Backbone.Collection.extend({
        model: this.models.Request,
        urlRoot: "/api/v1/requests/",
        update: function (data) {
            this.fetch({
                data: data,
            });
        }
    });

    this.collections.Buckets = Backbone.Collection.extend({
        model: this.models.BucketReport,
        update: function (data) {
            this.each(function (bucket) {
                bucket.set(data);
                bucket.fetch();
            });
        }
    });

    this.collections.ExceptionLogs = Backbone.Collection.extend({
        urlRoot: '/api/v1/exceptions',
        model: this.models.ExceptionLog
    });

    this.collections.Metrics = Backbone.Collection.extend({
        urlRoot: '/api/v1/metrics/',
        model: this.models.Metric
    });

    this.collections.Instruments = Backbone.Collection.extend({
        urlRoot: '/api/v1/instruments/',
        model: this.models.Instrument
    });
}.call(window.Stats));