import migrator
import json

short_dict = migrator.generate_prefix_dict()
print(short_dict)

with open("knjige.txt", "r") as f:
    for line in f:
        fields = line.split(chr(30))
        record = {}
        for el in fields:
            tag = el[:3]
            field_type = set()
            value = (el[6:]).split(chr(31))
            polja = migrator.split_field(value)

            for k, v in short_dict.items():
                for t in v:
                    if tag in t:
                        field_type.add(k)

            if field_type is None:
                continue

            if len(polja) > 0:
                record[tag] = polja

        print(json.dumps(record, ensure_ascii=False))
        break
