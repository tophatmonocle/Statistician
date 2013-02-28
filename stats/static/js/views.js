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
            console.log(this.$el.width());
            this.$el.append(this.template(this.model));
            var margin = {top: 10, right: 10, bottom: 80, left: 60},
                margin2 = {top: 210, right: 10, bottom: 20, left: 60},
                width = this.$el.width() - margin.left - margin.right,
                height = 270 - margin.top - margin.bottom,
                height2 = 270 - margin2.top - margin2.bottom;

            this.x = d3.time.scale().range([0, width]),
            this.x2 = d3.time.scale().range([0, width]),
            this.y = d3.scale.linear().range([height, 0]),
            this.y2 = d3.scale.linear().range([height2, 0]);

            this.xAxis = d3.svg.axis().scale(this.x).orient("bottom"),
            this.xAxis2 = d3.svg.axis().scale(this.x2).orient("bottom"),
            this.yAxis = d3.svg.axis().scale(this.y).orient("left");

            this.brush = d3.svg.brush()
                .x(this.x2)
                .on("brush", this.zoomView.bind(this))
                .on('brushend', this.refineData.bind(this));

            this.area = d3.svg.area()
                .interpolate("monotone")
                .x(function(d) {
                    return this.x(d.x);
                }.bind(this))
                .y0(height)
                .y1(function(d) {
                    return this.y(d.y);
                }.bind(this));

            this.area2 = d3.svg.area()
                .interpolate("monotone")
                .x(function(d) {
                    return this.x2(d.x);
                }.bind(this))
                .y0(height2)
                .y1(function(d) {
                    return this.y2(d.y);
                }.bind(this));

            var svgW = width + margin.left + margin.right,
                svgH = width + margin.top + margin.bottom;

            this.aspect = svgW / svgH;

            this.svg = d3.select(this.$('.graph')[0]).append("svg")
                .attr("width", svgW)
                .attr("height", svgH)
                .attr('viewBox', '0 0 '+svgW+' '+svgH)
                .attr('preserveAspectRatio', 'xMidyMid')

            this.svg.append("defs").append("clipPath")
                .attr("id", "clip")
              .append("rect")
                .attr("width", width)
                .attr("height", height);

            this.focus = this.svg.append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            this.context = this.svg.append("g")
                .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

            this.focus.append("path")
                .attr("clip-path", "url(#clip)")
                .attr('class', 'plot');

            this.focus.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(this.xAxis);
            this.focus.append("g")
                .attr("class", "y axis")
                .call(this.yAxis);
            this.context.append("path")
                .attr('class', 'miniplot');
            this.context.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height2 + ")")
                .call(this.xAxis2);
            this.context.append("g")
                .attr("class", "x brush")
                .call(this.brush)
                .selectAll("rect")
                .attr("y", -6)
                .attr("height", height2 + 7);

            $(window).on('resize', this.resizeChart.bind(this));
        },
        resizeChart: function () {
            var svg = this.$('svg');
            svg.hide();
            svg.attr('width', this.$el.width());
            svg.attr('height', this.$el.width() / this.aspect);
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
}.call(window.Stats));
