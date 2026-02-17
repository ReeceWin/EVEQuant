from sde import get_all_jumps

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