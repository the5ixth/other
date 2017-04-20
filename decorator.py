import functools

def uppercase(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        old = func(*args, **kwargs)
        new = old.upper()
        return new
    return wrapper

class bs():
    def __init__(self, string="hello"):
        self.string = string
    @uppercase(
    def hello(self):
        '''Return a string as uppercase'''
        return self.string 
b = bs()
