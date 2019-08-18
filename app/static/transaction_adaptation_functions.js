function parse_transaction(transaction) {
    function to_object(kv_pairs) {
        var obj = {};
        for (var i = 0; i < kv_pairs.length; i++) {
            obj[kv_pairs[i][0]] = kv_pairs[i][1];
        }
        return obj;
    }

    function get_key_value(value, index, array) {
        var kv = value.split(":")
        return [kv[0].trim(), kv.slice(1).join(":").trim()];
    }

    transaction = transaction.slice(1, transaction.length - 1);
    var objects = transaction.split(",");
    var kv_pairs = objects.map(get_key_value);
    return to_object(kv_pairs);
}


function obtain_transaction_info(transaction) {
    console.log(transaction);
    var tr = parse_transaction(transaction);
    var transaction_id_field_element = document.getElementById("transaction_id");
    var date_field_element = document.getElementById("edit_form_date");
    var comment_field_element = document.getElementById("edit_form_comment");
    var price_field_element = document.getElementById("edit_form_price");
    var category_field_element = document.getElementById("edit_form_category");
    var incoming_field_element = document.getElementById("incoming");
    transaction_id_field_element.value = parseInt(tr.id, 10);
    date_field_element.value = tr.date;
    price_field_element.value = tr.price;
    comment_field_element.value = tr.comment;
    incoming_field_element.checked = (tr.incoming == "True");
    category_field_element.value = tr.type;
    console.log(transaction_id_field_element.value);
}

function remove_transaction(transaction_id){
    var transaction_id_field_element = document.getElementById("remove_transaction_id");
    transaction_id_field_element.value = parseInt(transaction_id, 10);
}