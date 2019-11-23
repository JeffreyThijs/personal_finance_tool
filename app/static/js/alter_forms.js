import { parse_object } from './object_parsing.js';

function obtain_prognosis_info(prognosis) {
    console.log(prognosis);
    var tr = parse_object(prognosis);
    var prognosis_id_field_element = document.getElementById("prognosis_id");
    var date_field_element = document.getElementById("edit_form_date");
    var comment_field_element = document.getElementById("edit_form_comment");
    var amount_field_element = document.getElementById("edit_form_amount");
    var occurance_field_element = document.getElementById("edit_form_occurance");
    var incoming_field_element = document.getElementById("incoming");
    prognosis_id_field_element.value = parseInt(tr.id, 10);
    date_field_element.value = tr.fdate;
    amount_field_element.value = tr.amount;
    comment_field_element.value = tr.comment;
    occurance_field_element.value = tr.type;
    incoming_field_element.checked = tr.incoming;
}

function remove_prognosis(prognosis_id){
    var prognosis_id_field_element = document.getElementById("remove_prognosis_id");
    prognosis_id_field_element.value = parseInt(prognosis_id, 10);
}

function obtain_transaction_info(transaction) {
    console.log(transaction);
    var tr = parse_object(transaction);
    var transaction_id_field_element = document.getElementById("transaction_id");
    var date_field_element = document.getElementById("edit_form_date");
    var comment_field_element = document.getElementById("edit_form_comment");
    var price_field_element = document.getElementById("edit_form_price");
    var category_field_element = document.getElementById("edit_form_category");
    var incoming_field_element = document.getElementById("incoming");
    transaction_id_field_element.value = parseInt(tr.id, 10);
    date_field_element.value = tr.fdate;
    price_field_element.value = tr.price;
    comment_field_element.value = tr.comment;
    category_field_element.value = tr.type;
    incoming_field_element.checked = tr.incoming;
}

function remove_transaction(transaction_id){
    var transaction_id_field_element = document.getElementById("remove_transaction_id");
    transaction_id_field_element.value = parseInt(transaction_id, 10);
}