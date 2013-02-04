/*global window, $, Backbone, _, document*/
(function () {
    'use strict';
    $(document).ready(function () {
        var app, from, to, response_time_view, response_time_bucket, exception_bucket, request_count_view, exception_view, buckets, graph_time_picker, queries, table, table_view, slow_time_picker, trending_exceptions;
        app = window.Statistician;

        from = new Date();
        to = new Date();
        from.setDate(to.getDate() - 1);
        response_time_bucket = new app.models.BucketReport({
            from: from,
            to: to,
            width: 60 * 30, // half hour intervals
            aggregates: [{
                func: 'Avg',
                attr: 'time',
                name: 'time'
            }],
            resource: 'requests'
        });
        response_time_view = new app.views.Bucket({
            el: $('#app_target'),
            model: response_time_bucket,
            field: 'time',
            transform: {
                y: function (y) { return y * 1000; }
            },
            name: 'Response time (ms)',
            width: 420,
            height: 100
        });
        response_time_view.render();

        request_count_view = new app.views.Bucket({
            el: $('#app_target2'),
            model: response_time_bucket,
            field: 'total',
            name: 'Response rate',
            width: 420,
            height: 100
        });
        request_count_view.render();

        exception_bucket = new app.models.BucketReport({
            from: from,
            to: to,
            width: 60 * 30, // half hour intervals
            filters: {
                status: 500
            },
            resource: 'requests'
        });

        exception_view = new app.views.Bucket({
            el: $('#app_target3'),
            model: exception_bucket,
            field: 'total',
            name: 'Exceptions',
            width: 420,
            height: 100
        });
        exception_view.render();

        buckets = new app.collections.Buckets([
            response_time_bucket,
            exception_bucket
        ]);

        graph_time_picker = new app.views.PeriodPicker({
            model: buckets,
            selected: '1d'
        });
        graph_time_picker.render();
        $('#graphs .annotation').append(graph_time_picker.el);

        queries = new app.collections.Requests();
        queries.fetch({
            data: {
                from: from.toISOString(),
                to: to.toISOString(),
                order_by: '-time',
                limit: 10
            },
            success: function () {
                table_view.render();
            }
        });

        slow_time_picker = new app.views.PeriodPicker({
            model: queries,
            selected: '1d'
        });
        slow_time_picker.render();
        $('#requests .annotation').append(slow_time_picker.el);

        table = new Backbone.Table({
            items: queries,
            columns: [
                {
                    title: 'URL',
                    render: function (request) {
                        return '<a href="' + request.get_detail_url() + '"><span class="no-overflow">' + request.get('url') + '</span></a>';
                    }
                },
                {
                    title: 'Time',
                    render: function (request) {
                        return Math.round(request.get('time') * 1000) + ' ms';
                    }
                }
            ]
        });
        table_view = new Backbone.TableView({
            model: table,
            render_foot: false
        });
        $('#requests').append(table_view.el);
        table_view.render();

        response_time_bucket.fetch();
        exception_bucket.fetch();

        trending_exceptions = new app.collections.ExceptionLogs();
        trending_exceptions.fetch({
            data: {
                from: from.toISOString(),
                to: to.toISOString(),
                order_by: '-last_seen'
            },
            success: function () {
                this.each(function (exception) {
                    var view;
                    view = new app.views.ExceptionSummary({model: exception});
                    $('#trending_exceptions').append(view.el);
                    view.render();
                });
            }.bind(trending_exceptions)
        });
    });
}.call());
