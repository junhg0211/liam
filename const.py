from json import load

with open('./res/const.json', 'r') as _file:
    const = load(_file)

strings = const['strings']
