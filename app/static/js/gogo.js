
function get_machine_list() {
	mylist = [];
	for (i = 1; i <= 25; ++i) {
		if (document.getElementById("check_machine_" + i).checked) {
			mylist.push(i);
		}
	}
	return mylist;
}

function select(flag) {
	for (i = 1; i <= 25; ++i) {
		document.getElementById("check_machine_" + i).checked = flag;
	}
}

function set_start_time(value) {
	if (typeof value == 'undefined') {
		return;
	}
	$('#date_timepicker_start').val(value);
}

function set_end_time(value) {
	if (typeof value == 'undefined') {
		return;
	}
	$('#date_timepicker_end').val(value);
}

function get_min_datetime(chartData, m) {
	var data_size = chartData[m].length;
	var min_time = chartData[m][0]['datetime'];
	for (i = 1; i < data_size; ++i) {
		if (chartData[m][i]['datetime'] < min_time) {
			min_time = chartData[m][i]['datetime'];
		}
	}
	return min_time
}

function get_max_datetime(chartData, m) {
	var data_size = chartData[m].length;
	var max_time = chartData[m][0]['datetime'];
	for (i = 1; i < data_size; ++i) {
		if (chartData[m][i]['datetime'] > max_time) {
			max_time = chartData[m][i]['datetime'];
		}
	}
	return max_time
}

// this method is called when chart is first inited as we listen for "rendered" event
function zoomChart(chart, chartData) {
    // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
    chart.zoomToIndexes(chartData.length - 30000, chartData.length - 1);
}

// generate some random data, quite different range
function generateChartData(data_from_python) {
    
    var chartData = [];

    for (i in data_from_python) {
        datetimeStr = data_from_python[i].datetime;
        dateTime = datetimeStr.split(" ")
        var date = dateTime[0].split("-");
        var yy = date[0];
        var mm = date[1]-1;
        var dd = date[2];

        var time = dateTime[1].split(":");
        var hh = time[0];
        var m = time[1];
        var ss = parseInt(time[2]);

        var newDate = new Date(yy, mm, dd, hh, m, ss);
        var amp = parseInt(data_from_python[i].value, 10)
        chartData.push({
            date: newDate,
            value: amp
        });
    }
    return chartData;
}

function update_amchart(data_from_python) {
	var chartData = generateChartData(data_from_python);
	//var chartData = (data_from_python);
	var chart = AmCharts.makeChart("my_amchart", {
		"type": "serial",
		"theme": "light",
		"marginRight": 80,
		"autoMarginOffset": 20,
		"marginTop": 7,
		"dataProvider": chartData,
		"valueAxes": [{
			"axisAlpha": 0.2,
			"dashLength": 1,
			"position": "left"
		}],
		"mouseWheelZoomEnabled": true,
		"graphs": [{
			"id": "g1",
			"balloonText": "[[value]]",
			"bullet": "round",
			"bulletBorderAlpha": 1,
			"bulletColor": "#FFFFFF",
			"hideBulletsCount": 50,
			"title": "red line",
			"valueField": "value",
			"useLineColorForBulletBorder": true,
			"balloon":{
				"drop":true
			},
            "fillAlphas": 0.2
		}],
		"chartScrollbar": {
			"autoGridCount": true,
			"graph": "g1",
			"scrollbarHeight": 40
		},
		"chartCursor": {
		   "limitToGraph":"g1",
           "categoryBalloonDateFormat": "YYYY/MM/DD HH:NN:SS"
		},
		"categoryField": "date",
		"categoryAxis": {
            "minPeriod" : "ss",
			"parseDates": true,
			"axisColor": "#DADADA",
			"dashLength": 1,
			"minorGridEnabled": true
		},
		"export": {
			"enabled": true
		}
	});

	chart.addListener("rendered", zoomChart);
	zoomChart(chart, chartData);


}

$(function(){
	var min_datetime, max_datetime;
	jQuery.datetimepicker.setLocale('zh-TW');
	$('#date_timepicker_start').datetimepicker({format: 'Y-m-d H:i:s'});
	$('#date_timepicker_end').datetimepicker({format: 'Y-m-d H:i:s'});
	$('#start_button').click(function() {
		set_start_time(min_datetime);
	});
	$('#end_button').click(function() {
		set_end_time(max_datetime);
	});
	$('#press_go').click(function() {
		//var machine_list = get_machine_list();	
	    	
		$.ajax({
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				"datetime_start" : $('#date_timepicker_start').val(),
				"datetime_end" : $('#date_timepicker_end').val()
				}),
				dataType: 'json',
				url: '/draw_chart',
				success: function(chartData) {
					var data_size = chartData['m1'].length;
					min_datetime = get_min_datetime(chartData, 'm1');
					max_datetime = get_max_datetime(chartData, 'm1');
					
					$("#result").html("共有" +  data_size + "筆資料，起始時間：" + min_datetime + "，結束時間：" + max_datetime);
					/*
					$("#algorithmChart").empty();
					machines = []
					labels = []
					machine_list.forEach(function(m_id) {
						machines.push("M" + m_id);
						labels.push("M" + m_id);
					});
					var morrisChart = Morris.Line({
						element: 'algorithmChart',
						data: chartData['data'],
						xkey: 'datetime',
						parseTime: true,
						ykeys: machines,
						labels: labels,
						lineWidth: 1,
						smooth: true,
						goals: [120],
						goalStrokeWidth: 5
					});
                    */
                    update_amchart(chartData['m1']);
				},
				error: function(error) {
					console.log('error');
					console.log(eval(error));
				}
		});
	});
	
});
