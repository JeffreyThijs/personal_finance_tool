function parse_prognosis(prognosis) {
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

    prognosis = prognosis.slice(1, prognosis.length - 1);
    var objects = prognosis.split(",");
    var kv_pairs = objects.map(get_key_value);
    return to_object(kv_pairs);
}

function get_type(obj) {
    return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
}

function obtain_prognosis_info(prognosis) {
    console.log(prognosis);
    var tr = parse_prognosis(prognosis);
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