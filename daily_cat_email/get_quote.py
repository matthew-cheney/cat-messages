from daily_cat_email.settings import PATH_TO_QUOTES, PATH_TO_QUOTES_COUNTER


def get_quote():
    with open(PATH_TO_QUOTES, 'r') as f:
        raw_text = f.read()
    quotes = [(x.split('\n')[0], x.split('\n')[1]) for x in raw_text.split('\n\n')]
    with open(PATH_TO_QUOTES_COUNTER, 'r') as f:
        counter = int(f.read())
    if counter > len(quotes) - 1:
        counter = 0
    with open(PATH_TO_QUOTES_COUNTER, 'w') as f:
        f.write(f'{counter + 1}')
    return quotes[counter]

if __name__ == '__main__':
    for i in range(82):
        print(get_quote())
