// Plot function
function plotter(data, limits, loc) {
    //Width and height
    var w = 500;
    var h = 100;

    //Create SVG element
    var svg = d3.select(loc)
        .append("svg")
        .attr("width", w)
        .attr("height", h);

    //Create Xscale
    var xScale = d3.time.scale()
        .domain(limits)
        .range([0, w]);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom")
        .ticks(8);

    //Create Bars
    svg.selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("fill", "#337ab7")
        .attr("x", function (d, i) {
            return xScale(d);
        })
        .attr("y", 0)
        .attr("width", 5)
        .attr("height", 100 - 20);

    // Apply Axis
    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + (h - 20) + ")")
        .call(xAxis);
}

// Display a choice
function display_option(choice) {
    // Validate page
    if (choice < 0) choice = 0;
    if (choice > numChoices()) choice = numChoices();

    // Change restaurant type
    document.getElementById("rtype").innerHTML = dat[choice].type;

    // Be Grammar
    function vowelTest(s) {return (/^[aeiou]$/i).test(s);}
    if (vowelTest(dat[choice].type[0])) {
        document.getElementById("pretype").innerHTML = "an"
    } else {
        document.getElementById("pretype").innerHTML = "a"
    }

    // Plot Checkins
    function get_checks(data) {
        // Get this choice's data
        var cdat = $.grep(data, function(element, index){
          return element.type == dat[choice].type;})

        // Convert to date object
        var rdate = cdat.map(function(x) {return new Date(x.time * 1000)})

        return rdate
    };

    // Plot


    // Chang elements for solo or together results
    try {
        document.getElementById("check1").innerHTML = dat[choice].tsince_x;
        document.getElementById("check2").innerHTML = dat[choice].tsince_y;

        var udat = get_checks(uchecks);
        var fdat = get_checks(fchecks);

        plotter(udat, [d3.min(udat.concat(fdat)), Date.now()], "#uchart");
        plotter(fdat, [d3.min(udat.concat(fdat)), Date.now()], "#fchart");

    } catch(err) {
        // Change User Elements
        document.getElementById("check1").innerHTML = dat[choice].tsince;

        var udat = get_checks(uchecks);
        plotter(udat, [d3.min(udat), Date.now()], "#uchart");
    }
}

function prevChoice() {
    if (current_choice > 0) {
        current_choice--;
        d3.selectAll("svg").remove();
        display_option(current_choice);
    } else {
        $('#prebutt').toggleClass('btn-inact');
    }
}

function nextChoice() {
    if (current_choice < numChoices()) {
        current_choice++;
        d3.selectAll("svg").remove();
        display_option(current_choice);
    }
}

function numChoices() {
    return Math.ceil(dat.length-1);
}
