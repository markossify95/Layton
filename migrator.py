from collections import defaultdict


def generate_prefix_dict(file="prefiksi.txt"):
    prefiks_dict = defaultdict(list)
    with open(file) as f:
        for l in f:
            if len(l) > 0 and not "//" in l:
                prefiks_dict[l[:2]].append(l[3:].strip())
    return prefiks_dict
