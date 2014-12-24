/*
var width = 960,
    height = 480;

var path = d3.geo.path();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("/static/us.json", function(error, us) {
  svg.append("path")
      .datum(topojson.feature(us, us.objects.land))
      .attr("d", path)
      .attr("class", "land-boundary");

  svg.append("path")
      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
      .attr("d", path)
      .attr("class", "state-boundary");
});
*/

var width = 1280,
    height = 720;

var projection = d3.geo.albersUsa()
    .scale(1000)
    .translate([width / 2, height / 2]);

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("/static/us.json", function(error, us) {
  svg.append("path")
      .datum(topojson.feature(us, us.objects.land))
      .attr("class", "land-boundary")
      .attr("d", path);

  svg.append("path")
      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
      .attr("class", "state-boundary")
      .attr("d", path);
});
/*
d3.select(self.frameElement).style("height", height + "px");*/