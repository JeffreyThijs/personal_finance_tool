import { get_placeholder_date_today } from './dateutils.js';

$(document).ready(function(){
    var date_input=$('input[name="change_date_input"]'); //our date input has the name "date"
    date_input.datepicker({
        format: 'mm-yyyy',
        autoclose: true,
        startView: 1,
        minViewMode: 1
    }).on('changeDate', function(ev){
        var change_date_id_element = document.getElementById("change_date_id");
        change_date_id_element.value = change_date_input.value;
        document.getElementById("change_date").submit(); 
    })
})

get_placeholder_date_today();