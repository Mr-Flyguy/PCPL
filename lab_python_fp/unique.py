from gen_random import gen_random
class Unique(object):
    def __init__(self, items, **kwargs):
        self.ignore_case = kwargs.get('ignore_case', False)
        self.items = iter(items)
        self.seen = set()

    def __next__(self):
        while True:
            item = next(self.items)
            
            if self.ignore_case and type(item) == str:
                key = item.lower()
            else:
                key = item
            
            if key not in self.seen:
                self.seen.add(key)
                return item

    def __iter__(self):
        return self

def main():
    data = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    print(*Unique(data, ignore_case=True))
    data = gen_random(10, 1, 3)
    print(*Unique(data, ignore_case=True))
    data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    print(*Unique(data, ignore_case=True))
    print(*Unique(data))
    
if __name__ == '__main__':
    main()