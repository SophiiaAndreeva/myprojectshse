words = ['test', 'testing', 'book', 'booking']

for word in words:
    lenght = len(word)
    mid = lenght // 2
    if lenght % 2 == 0:
        result = word[mid-1:mid+1]
    else:
        result = word[mid]
