from collections import defaultdict


def generate_prefix_dict(file="data/prefiksi.txt"):
    prefiks_dict = defaultdict(list)
    with open(file) as f:
        for l in f:
            if len(l) > 0 and "//" not in l:
                prefiks_dict[l[:2]].append(l[3:].strip())
    return prefiks_dict


def split_field(value):
    field_dict = {}
    for item in value:
        if len(item.strip('\n')) > 1:
            field_dict[item[:1]] = item[1:].strip('\n')

    return field_dict
