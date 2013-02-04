/*global window, $, Backbone, _, document*/
(function () {
    'use strict';
    $(document).ready(function () {
        var app, view, from, to, bucket, response_time_view;
        app = window.Statistician;

        from = new Date();
        to = new Date();
        from.setHours(to.getHours() - 1);
        bucket = new app.models.BucketReport({
            from: from,
            to: to,
            width: 60, // half hour intervals
            aggregates: [{
                func: 'Avg',
                attr: 'time',
                name: 'time'
            }],
            resource: 'requests'
        });

        view = new app.views.GraphFilter({model: bucket});
        $('#form_target').append(view.el);
        view.render();

        response_time_view = new app.views.Bucket({
            el: $('#results'),
            model: bucket,
            field: 'time',
            transform: {
                y: function (y) { return y * 1000; }
            },
            name: 'Response time (ms)',
            width: 900,
            height: 300
        });
        response_time_view.render();

        bucket.fetch()
        setInterval(function () {
            from = new Date();
            to = new Date();
            from.setHours(to.getHours() - 1);
            bucket.set({
                from: from,
                to: to
            });
            bucket.fetch();
        }, 2000)
    });
}.call());
