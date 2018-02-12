import migrator
import util


def parse_tags():
    short_dict = util.generate_prefix_dict()

    for k, v in short_dict.items():
        short_dict[k] = ", ".join(short_dict[k])  # PRETVARAMO VALUES IZ LIST U STR

    new_dict = dict(short_dict)
    migrator.insert_keys(new_dict)


def parse_books():
    with open("data/knjige.txt", "r") as f:
        all_records = list()
        short_dict = util.generate_prefix_dict()

        for line in f:
            fields = line.split(chr(30))
            record = {}
            for el in fields:
                tag = el[:3]
                field_type = set()
                value = (el[6:]).split(chr(31))
                polja = util.split_field(value)

                for k, v in short_dict.items():
                    for t in v:
                        if tag in t:
                            field_type.add(k)

                if field_type is None:
                    continue

                if len(polja) > 0:
                    record[tag] = polja

            all_records.append(record)

        migrator.insert_books(all_records)
        # json.dumps(record, ensure_ascii=False))


def parse_prefixes():
    prefixes = {}
    with open("data/PrefixNames_sr.properties", "rb") as f:
        for l in f:
            k_v = l.decode("unicode_escape").split('=')  # kljuc vrednost parovi tipa AU: Autor
            prefixes[k_v[0]] = k_v[1].rstrip('\n')

    migrator.insert_prefixes(prefixes)

#ove funkcije se pozivaju redom samo prilikom migracije