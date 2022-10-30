def check(arr_to_check, end):
    is_final = True
    for i in arr_to_check:
        if i[0][-1] == str(end):
            continue
        else:
            is_final = False
            break
    return is_final


Q = 10
evaporation = 0.666

epochs = int(input("Введите количество пробегов: "))

start = 0
end = 0
nodes = {}
with open("input1.txt") as file:
    for line in file:
        arr = [int(i) for i in line.split()]
        if len(arr) < 3:
            start = int(arr[0])
            end = int(arr[1])
        else:
            # path from: [to, length]
            if arr[0] in nodes:
                nodes[arr[0]].append([arr[1], arr[2]])
            else:
                nodes[arr[0]] = [[arr[1], arr[2]]]

nodes = {key: nodes[key] for key in sorted(nodes.keys())}


# Finding all possible paths in graph

all_paths = []

for i in nodes[start]:
    length0 = i[1]
    path0 = str(start) + str(i[0])
    paths = [[path0, length0]]
    while not check(paths, end):
        newpaths = []
        for j in paths:
            path = j[0]
            length = j[1]
            last_node = int(j[0][-1])
            if last_node ==  end:
                newpaths.append([path, length])
            else:
                for k in nodes[last_node]:
                    path += str(k[0])
                    newpaths.append([path, length + k[1]])
                    path = path[:-1]
            paths = newpaths
    all_paths.append(paths)

paths_lengths = {}

# ant_way : ant_pheromone
ants = {}
for i in all_paths:
    for j in i:
        ants[j[0]] = Q / j[1]
        paths_lengths[j[0]] = j[1]
# road: pheromone_on_the_road
roads = {}
for i in nodes:
    for j in nodes[i]:
        roads[str(i) + str(j[0])] = 1.0

for _ in range(epochs):
    # Evaporation at first
    for road in roads:
        roads[road] *= evaporation
    # Then all ants start walking
    for ant_way in ants:
        for i in range(len(ant_way)-1):
            roads[ant_way[i] + ant_way[i+1]] += ants[ant_way]

roads = {k: v for k, v in sorted(roads.items(), key=lambda item: item[1], reverse=True)}
# print(roads)

for i in range(len(nodes[start])):
    way = ''
    for road in roads:
        if road[0] == str(start):
            way += road
            break
    roads.pop(way)
    while way[-1] != str(end):
        for road in roads:
            if road[0] == way[-1]:
                way += road[1]
                continue
    print(f"Лучший путь с началом '{way[:2]}' : {way}, длина пути: {paths_lengths[way]}")