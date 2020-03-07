# def unwrap_dict(input_dict, new_dict=None):
#     if not isinstance(input_dict, dict):
#         raise ValueError()
#     if new_dict is None:
#         new_dict = {}
#     for k, v in input_dict.items():
#         if isinstance(v, dict):
#             unwrap_dict(v, new_dict)
#         else:
#             new_dict[k] = v
#     return new_dict

def unwrap_dict(father):
    local_list = []
    

    for key, value in father.items():
        local_list.append(key)
        local_list.extend(unwrap_dict(value))
    return local_list