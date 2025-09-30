boys = ['Peter', 'Alex', 'John', 'Artur', 'Richard']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

if len(boys) != len(girls):
    print("Внимание, кто-то может остаться без пары.")
else:
    sorted_boys = sorted(boys)
    sorted_girls = sorted(girls)
    pairs = zip(sorted_boys, sorted_girls)
    print("Идеальные пары: \n")
    for pair in pairs:
        print(pair)
