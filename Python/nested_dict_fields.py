"""A small util to read, set, and pop nested fields in a dictionary."""


def loop_into_dict_path(target, path_list, create_path=False):
    if not path_list:
        return target

    current = target
    for i in range(len(path_list) - 1):
        if path_list[i] not in current:
            if create_path:
                current[path_list[i]] = {}
            else:
                raise KeyError

        current = current[path_list[i]]

    return current


def pop_nested_dict_field(target, path):
    """Receive a target dict and the full path (including the field it self)
    and remove the field from dictionary. The path should be a dot-separated
    string. e.g. 'field1.field2'
    """
    path_list = path.split('.')
    return loop_into_dict_path(target, path_list).pop(path_list[-1], None)


def read_nested_dict_field(target, path):
    path_list = path.split('.')
    return loop_into_dict_path(target, path_list).get(path_list[-1])


def set_nested_dict_field(target, path, value, create_path=False):
    path_list = path.split('.')
    loop_into_dict_path(target, path_list, create_path)[path_list[-1]] = value
