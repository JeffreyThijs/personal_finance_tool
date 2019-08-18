
$(document).ready(function(){
    var date_input=$('input[name="change_date_input"]'); //our date input has the name "date"
    // var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
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
