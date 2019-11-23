// updates add new form date in add new form
export function get_placeholder_date_today(){
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = dd + '-' + mm + '-' + yyyy;
    var change_date_id_element = document.getElementById("add_new_form_date");
    change_date_id_element.value = today
}