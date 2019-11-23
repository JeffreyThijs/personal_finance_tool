import { get_placeholder_date_today } from './dateutils.js';

$('.accordion-toggle').click(function(){
	$('.hiddenRow').hide();
	$(this).next('tr').find('.hiddenRow').show();
});

$(document).ready(function(){
    var date_input=$('input[name="change_date_input"]'); //our date input has the name "date"
    date_input.datepicker({
        format: 'yyyy',
        autoclose: true,
        startView: 2,
        minViewMode: 2
    }).on('changeDate', function(ev){
        var change_date_id_element = document.getElementById("change_date_id");
        change_date_id_element.value = change_date_input.value;
        document.getElementById("change_date").submit(); 
    })
})

get_placeholder_date_today();