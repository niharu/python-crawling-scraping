d = {'a':1, 'b':2}
try:
    print(d['x'])
except KeyError:
    print('x is not found')

with open('index.html') as f:
    print(f.read())