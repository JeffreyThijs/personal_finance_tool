
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

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();
today = dd + '-' + mm + '-' + yyyy;
var change_date_id_element = document.getElementById("add_new_form_date");
change_date_id_element.value = today