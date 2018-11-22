# Layer 0: Background Objects
# Layer 1: Foreground Objects

objects = [[],[],[],[],[]]


def add_object(o, layer):
    global objects
    if len(objects) == 0:
        objects = [[],[],[],[],[]]
    print(len(objects))
    objects[layer].append(o)


def add_objects(l, layer):
    for o in l:
        add_object(o, layer)

def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del(o)
            break


def clear():
    for o in all_objects():
        del o
    objects.clear()


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

