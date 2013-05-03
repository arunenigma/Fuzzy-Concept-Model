relation = ['Arun', 'Hari']
people = ['Mani', 'Arun', 'Akil', 'Varun', 'Hari', 'Karni']
indices = []
for person in relation:
    indices.append(people.index(person))
print people[indices[0]: indices[1] + 1]
