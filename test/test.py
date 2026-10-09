
tree = {
    'Start': ['A', 'B', 'C'],
    'A': ['Start', 'D', 'E'],
    'B': ['Start', 'F', 'G'],
    'C': ['Start', 'H'],
    'D': ['A', 'I'],
    'E': ['A', 'F', 'J'],        # Boucle avec F
    'F': ['B', 'E', 'K'],        # Boucle avec E
    'G': ['B', 'H', 'L'],        # Boucle avec H
    'H': ['C', 'G'],
    'I': ['D', 'M'],             
    'J': ['E', 'K', 'N'],        # Intersection
    'K': ['F', 'J', 'O'],
    'L': ['G', 'P'],
    'M': ['I', 'N'],             
    'N': ['J', 'M', 'Pacman'],   # Chemin 1 vers la cible
    'O': ['K', 'Pacman'],        # Chemin 2 vers la cible
    'P': ['L', 'Q'],
    'Q': ['P'],                  # Cul-de-sac
    'Pacman': ['N', 'O']
}
target = "Pacman"

start = "Start"
visited = [start]
queue = [start]
history = {}
while queue:
    node = queue.pop(0)
    if node == target:
        break
    for neighbour in tree[node]:
        if neighbour not in visited:
            visited.append(neighbour)
            history[neighbour] = node
            queue.append(neighbour)

path = []
current = target

while current in history:
    path.append(current)
    current = history[current]

path.append(current)

path.reverse()

print(path)