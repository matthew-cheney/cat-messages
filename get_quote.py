def get_quote():
    with open('cat_quotes.txt', 'r') as f:
        raw_text = f.read()
    quotes = [(x.split('\n')[0], x.split('\n')[1]) for x in raw_text.split('\n\n')]
    with open('quote_counter.txt', 'r') as f:
        counter = int(f.read())
    if counter > len(quotes) - 1:
        counter = 0
    with open('quote_counter.txt', 'w') as f:
        f.write(f'{counter + 1}')
    return quotes[counter]

if __name__ == '__main__':
    for i in range(82):
        print(get_quote())
