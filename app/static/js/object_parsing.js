export function parse_object(x) {
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

    x = x.slice(1, prognosis.length - 1);
    var objects = x.split(",");
    var kv_pairs = objects.map(get_key_value);
    return to_object(kv_pairs);
}

export function get_type(obj) {
    return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
}