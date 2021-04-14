


window.onload = function() {

    // Menu Toggle Script
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });


}





//-------------------------------------------------------
// Apexcharts
//-------------------------------------------------------

var charts = []

function getChartBaseOptions(chartId) {

    var chartBaseOptions = {
        title: {
            text: 'Graph',
        },
        chart: {
            id: chartId,
            type: 'line',
            height: 350,
            group: 'charts',
        },
        noData: {
            text: 'Loading...'
        },
        series: [],
        xaxis: {
            type: 'datatime'
        },
        yaxis: {
            labels: {
                minWidth: 40
            }
        },
    }

    return chartBaseOptions

}


function addChart(id, dataUrl) {

    var chart = new Chart(id, dataUrl, document.querySelector('#chart' + id), getChartBaseOptions(id));
    charts.push(chart);

    return chart;
}


function getChart(id) {

    for (const chart of charts) {
        if (chart.id == id) {
            return chart;
        }
    }

}

function updateAllCharts() {
    for (const chart of charts) {
        chart.updateData();
    }
}

class Chart extends ApexCharts {

    constructor(id, dataUrl, element, options) {
        super(element, options);
        this.id = id;
        this.dataUrl = dataUrl;
        super.render()
        this.updateData()
    }
    
    updateData() {
        var id = this.id
        $.getJSON(this.dataUrl, function(response) {
            ApexCharts.exec(id, 'updateSeries', response)
        });
    }
}