from .sde import get_all_jumps
from collections import deque

def build_graph():
    jumps = get_all_jumps()
    graph = {}
    for jump in jumps:
        source = jump[0]
        destination = jump[1]
        
        # If we haven't seen this source system before, start a new list
        if source not in graph:
            graph[source] = []
            
        # Add the neighbor to the list
        graph[source].append(destination)
        
    return graph

JUMP_GRAPH = build_graph() # Use capitals for global variables

def get_neighbours(system_id: int) -> list[int]:
    return JUMP_GRAPH.get(system_id, [])

def find_route(start_system, end_system):
    # Create a queue using deque as it is more optimised for first in first out algorithms like BFS
    queue = deque([[start_system]])
    # Initialize visited with the starting system
    visited = {start_system}
    while queue:
        # Initialize path by popping the first item out (start_system)
        path = queue.popleft()
        print(path)
        # Current system is the last item in the path (the current route we are examining)
        current_system = path[-1]
        # if the current system is our destination we return the path
        if current_system == end_system:
            print("Current system is end system")
            return path
        # Initialize neighbours using the get_neighbours function passing current system
        # This pulls all the neighbouring systems to the current system
        neighbours = get_neighbours(current_system)
        # Then iterate over the neighbours in the returned list from the function
        for neighbour in neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

def get_systems_in_range(start_system, max_jumps):
    queue = deque([[start_system]])
    visited = {start_system}
    while queue:
        path = queue.popleft()
        print(path)

        current_system = path[-1]

        if (len(path) - 1) < max_jumps:
            neighbours = get_neighbours(current_system)
            for neighbour in neighbours:
                if neighbour not in visited:
                    visited.add(neighbour)
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

    return list(visited)

def main():
    route = find_route(30000142, 30002187)
    bubble = set()
    for system in route:
        systems = get_systems_in_range(system, 2)
        bubble.update(systems)
        print("Bubble: ", bubble)

main()
        
