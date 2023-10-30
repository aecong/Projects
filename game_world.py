objects = [[] for _ in range(4)]


def add_object(o, depth=0):   # 게임 월드에 객체 추가
    objects[depth].append(o)

# def add_objects(ol, depth = 0): # 게임 월드에 객체'들'을 추가
#     objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in objects:
        if o in layer:  # 객체가 layer 에 들어 있으면
            layer.remove(o)
            return
    raise ValueError('존재하지 않는 객체는 지울 수 없음') # 코드 강제 발생


def clear():
    for layer in objects:
        layer.clear()