with open("knjige.txt", "r") as f:
    for line in f:
        linija = line.split(chr(30))
        print("LAJNA", linija)
        for el in linija:
            print(str(   el[6:]).split(chr(31))   )

        break
