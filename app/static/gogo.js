
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


$(function(){
	$('#date_timepicker_start').datetimepicker();
	$('#date_timepicker_end').datetimepicker();
    $('#press_go').click(function() {
		console.log(get_machine_list());
		$.getJSON('/put_data', {
			"datetime_start" : $('#date_timepicker_start').val(),
			"datetime_end" : $('#date_timepicker_end').val(),
			"mlist" : [1]
		}, function(data) {
			console.log('data: ' + data);
		});
	});
});
