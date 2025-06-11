def reader(path):
    words = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            for symbol in [',', ';', '(', ')']:
                line = line.replace(symbol, f' {symbol} ')
            for word in line.split():
                words.append(word)
    return words
    
words = reader('code.txt')
for word in words:
    print(word)
