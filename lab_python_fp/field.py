def field(data:list[dict], *args):
    assert len(args) > 0
    
    if len(args) == 1:
        return [item[args[0]] for item in data if item[args[0]]]
    
    else:
        return [{arg: item[arg] for arg in args if item[arg]} for item in data]
        
        
if __name__ == '__main__':
    goods = [
    {'title': 'Ковер', 'price': 2000, 'color': 'green'},
    {'title': 'Диван для отдыха', 'price': 5300, 'color': 'black'}
    ]
    print(*field(goods, 'title'), sep=', ')
    print(*field(goods, 'title', 'price'), sep=', ')