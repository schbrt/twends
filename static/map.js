var socket = io.connect('/data');

var events = []; //event cache

var width = 1280,
    height = 720;

var projection = d3.geo.albers()
    .scale(1400)
    .translate([width / 2, height / 2]); //center map within svg element

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);


socket.on('event', function(msg) {
    var data = msg;
    events.push(data)

    group = svg.selectAll("circle").data(events);

    coords = data.coords.coordinates
    pol = data.polarity

    group.enter()
    .append("circle")
    .attr("cx", function (d) { console.log(projection(d)); return projection(d)[0]; })
    .attr("cy", function (d) { return projection(d)[1]; })
    .attr("r", "5px")
    .attr("fill", "red")

    /*
    svg.selectAll("circle")
    .data([coords]).enter()
    .append("circle")
    .attr("cx", function (d) { console.log(projection(d)); return projection(d)[0]; })
    .attr("cy", function (d) { return projection(d)[1]; })
    .attr("r", "5px")
    .attr("fill", "red")
    */

});


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
