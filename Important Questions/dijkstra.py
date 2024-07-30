import heapq #Priority Queue

def dijkstra(graph, start):
    queue, distances = [(0, start)], {start: 0}
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances

graph = {
    'A': {'B': 1, 'C': 2},
    'B': {'A': 9, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 100},
    'D': {'B': 5, 'C': 1}
}

start_node = 'A'
print(dijkstra(graph, start_node))
