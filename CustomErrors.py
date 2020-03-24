class EmailNotFoundError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'EmailNotFoundError, {self.message}'
        else:
            return 'EmailNotFoundError has been raised.'
