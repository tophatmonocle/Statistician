/*global Backbone, _, Rickshaw, window, $*/
/*nomen=false*/
(function () {
    'use strict';
    this.views.Instrument = Backbone.View.extend({
        className: "widget span6",
        initialize: function () {
            this.listenTo(this.model, 'change:buckets', this.set_data, this);
            this.template = _.template($('#instrument_template').html());
        },
        map_data: function () {
            var buckets = this.model.get('buckets');
            return _.map(buckets, function (bucket) {
                var x, y;
                x = new Date(bucket.timestamp).getTime();
                y = bucket[this.options.field] || 0;
                return {
                    x: x,
                    y: y
                };
            }.bind(this));
        },
        set_data: function () {
            var data = this.map_data();
            if (data.length == 0) { return; }
            this.$('.loading').hide();
            this.$('.graph').show();
            this.has_data = true;

            var vis = d3.select(this.el);

            var yMin = _.min(data, function (datum) { return datum.y }).y,
                yMax = _.max(data, function (datum) { return datum.y }).y,
                xMin = _.min(data, function (datum) { return datum.x }).x,
                xMax = _.max(data, function (datum) { return datum.x }).x;

            var buffer = (yMax - yMin) * 0.1
            yMin = Math.max(0, yMin - buffer);
            yMax += buffer;

            this.x.domain([xMin, xMax]);
            this.y.domain([yMin, yMax]);
            this.x2.domain(this.x.domain());
            this.y2.domain(this.y.domain());

            vis.selectAll('path.plot')
                .data([data])
                .attr("clip-path", "url(#clip)")
                .attr("d", this.area);

            vis.selectAll('path.miniplot')
                .data([data])
                .attr("clip-path", "url(#clip)")
                .attr("d", this.area2);

            this.yAxis.scale(this.y);
            this.focus.select('.y.axis')
                .call(this.yAxis);

            this.xAxis.scale(this.x);
            this.focus.select('.x.axis')
                .call(this.xAxis);

            this.xAxis2.scale(this.x2);
            this.context.select('.x.axis')
                .call(this.xAxis2);

            this.brush.x(this.x2);
            this.zoomView();
        },
        render: function () {
            this.$el.append(this.template(this.model));

            this.x = d3.time.scale(),
            this.x2 = d3.time.scale(),
            this.y = d3.scale.linear(),
            this.y2 = d3.scale.linear();

            this.xAxis = d3.svg.axis(),
            this.xAxis2 = d3.svg.axis(),
            this.yAxis = d3.svg.axis();

            this.brush = d3.svg.brush()
                .on("brush", this.zoomView.bind(this))
                .on('brushend', this.refineData.bind(this));

            this.area = d3.svg.area()
                .interpolate("monotone")
                .x(function(d) {
                    return this.x(d.x);
                }.bind(this))
                .y0(0)
                .y1(function(d) {
                    return this.y(d.y);
                }.bind(this));

            this.area2 = d3.svg.area()
                .interpolate("monotone")
                .x(function(d) {
                    return this.x2(d.x);
                }.bind(this))
                .y1(function(d) {
                    return this.y2(d.y);
                }.bind(this));

            this.svg = d3.select(this.$('.graph')[0]).append("svg")

            this.svg.append("defs").append("clipPath")
                .attr("id", "clip")
              .append("rect");

            this.focus = this.svg.append("g");

            this.context = this.svg.append("g")

            this.focus.append("path")
                .attr("clip-path", "url(#clip)")
                .attr('class', 'plot');

            this.focus.append("g")
                .attr("class", "x axis")
            this.focus.append("g")
                .attr("class", "y axis")
                .call(this.yAxis);
            this.context.append("path")
                .attr('class', 'miniplot');
            this.context.append("g")
                .attr("class", "x axis")
            this.context.append("g")
                .attr("class", "x brush")

            $(window).on('resize', this.resizeChart.bind(this));
            this.resizeChart();
        },
        resizeChart: function () {
            var svg = this.$('svg');
            svg.hide();

            var margin = {top: 10, right: 10, bottom: 80, left: 60},
                margin2 = {top: 210, right: 10, bottom: 20, left: 60},
                width = this.$el.width() - margin.left - margin.right,
                height = 270 - margin.top - margin.bottom,
                height2 = 270 - margin2.top - margin2.bottom;

            this.x.range([0, width]);
            this.x2.range([0, width]);
            this.y.range([height, 0]);
            this.y2.range([height2, 0]);

            this.xAxis.scale(this.x).orient("bottom"),
            this.xAxis2.scale(this.x2).orient("bottom"),
            this.yAxis.scale(this.y).orient("left");

            var svgW = width + margin.left + margin.right,
                svgH = height + margin.top + margin.bottom;

            this.svg
                .attr("width", svgW)
                .attr("height", svgH)
              .select("#clip rect")
                .attr("width", width)
                .attr("height", height);

            this.brush.x(this.x2)
            this.svg.select('.brush')
                .call(this.brush)
                .selectAll("rect")
                .attr("y", -6)
                .attr("height", height2 + 7);

            this.area
                .y0(height);

            this.area2
                .y0(height2);

            this.focus
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
              .select('g')
                .attr("transform", "translate(0," + height + ")")
                .call(this.xAxis);

            if (this.has_data) {
                this.focus.select("path").attr("d", this.area);
                this.focus.select(".x.axis").call(this.xAxis);
                this.context.select("path").attr("d", this.area2);
                this.context.select(".x.axis").call(this.xAxis2);
            }

            this.context
                .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")")
              .select('g')
                .attr("transform", "translate(0," + height2 + ")")
                .call(this.xAxis2);

            svg.show();
        },
        zoomView: function () {
          this.x.domain(this.brush.empty() ? this.x2.domain() : this.brush.extent());
          this.focus.select("path").attr("d", this.area);
          this.focus.select(".x.axis").call(this.xAxis);
        },
        refineData: function() {
            var extent = this.brush.extent(), from, to;
            if (!this.brush.empty()) {
                from = extent[0];
                to = extent[1];
                this.model.getData({
                    from: from,
                    to: to
                })
            }
        }
    });

    this.views.Event = Backbone.View.extend({
        className: 'timeslot',
        icon: function () {
            switch (this.model.get('type')) {
            default:
                return "fa-icon-calendar"
            }
        },
        render: function () {
            this.$el.append(_.template($('#event_template').html(), this.model));
            var icon = this.icon(this);
            this.$('.icon').append('<i class="' + this.icon() + '"></i>');
            if (this.options.alt) {
                this.$el.addClass('alt');
            }
        }
    });
}.call(window.Stats));
