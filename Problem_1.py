'''
1168 Optimal Water Distribution in a Village
https://leetcode.com/problems/optimize-water-distribution-in-a-village/description/

There are n houses in a village. We want to supply water for all the houses by building wells and laying pipes.

For each house i, we can either build a well inside it directly with cost wells[i - 1] (note the -1 due to 0-indexing), or pipe in water from another well to it. The costs to lay pipes between houses are given by the array pipes where each pipes[j] = [house1j, house2j, costj] represents the cost to connect house1j and house2j together using a pipe. Connections are bidirectional, and there could be multiple valid connections between the same two houses with different costs.

Return the minimum total cost to supply water to all houses.

Example 1:
Input: n = 3, wells = [1,2,2], pipes = [[1,2,1],[2,3,1]]
Output: 3
Explanation: The image shows the costs of connecting houses using pipes.
The best strategy is to build a well in the first house with cost 1 and connect the other houses to it with cost 2 so the total cost is 3.

Example 2:
Input: n = 2, wells = [1,1], pipes = [[1,2,1],[1,2,2]]
Output: 2
Explanation: We can supply water with cost two using one of the three options:
Option 1:
  - Build a well inside house 1 with cost 1.
  - Build a well inside house 2 with cost 1.
The total cost will be 2.
Option 2:
  - Build a well inside house 1 with cost 1.
  - Connect house 2 with house 1 with cost 1.
The total cost will be 2.
Option 3:
  - Build a well inside house 2 with cost 1.
  - Connect house 1 with house 2 with cost 1.
The total cost will be 2.
Note that we can connect houses 1 and 2 with cost 1 or with cost 2 but we will always choose the cheapest option.

Constraints:
2 <= n <= 10^4
wells.length == n
0 <= wells[i] <= 10^5
1 <= pipes.length <= 10^4
pipes[j].length == 3
1 <= house1_j, house2_j <= n
0 <= cost_j <= 10^5
house1_j != house2_j

Solution:
1. Build a minimum cost spanning tree using Kruskal's algorithm
We connect each house to a virtual node 0 using the well cost as an edge. Then we collect all those edges along with the real pipes into one list and sort by cost. Using Union-Find, we keep adding the cheapest edges that connect new components until all are connected.

The most important takeaway here is in Union Find (unionizing). It involves the use of an array to assign the group membership of nodes in disjoint sets.

https://youtu.be/MaHBeXA3jI0?t=1308 (explanation and dry run)
https://youtu.be/MaHBeXA3jI0?t=2581 (code)
https://youtu.be/wU6udHRIkcc?t=667 (dry run of unionization)

Time: O((N+M) log (N+M)), N = num houses, M = num pipes
Space: O(N+M) (edges[] is O(N+M) and uf[] is O(N))
(Thus N + M = total no. of edges in the graph)

More generally, if there are E edges and V vertices in the graph,
Time: O(E log E), Space: O(E+V)

2. Min-Heap
We connect each house to a virtual node 0 using the well cost as an edge.
Use a priority queue (min-heap) to always pick the cheapest edge connecting a new house. Keep adding edges until all nodes are visited, and sum their costs for the answer.
https://youtu.be/4ZlRH0eK-qQ?t=694
Time: O((N+M) log (N)), N = num houses, M = num pipes
Space: O(N+M) (edges[] is O(N+M) and uf[] is O(N))

'''
from typing import List
from collections import defaultdict

def minCostToSupplyWater_Kruskal(n: int, wells: List[int], pipes: List[List[int]]) -> int:
    def union_find(uf, child):
        parent = uf[child]
        if child == parent:
            return parent
        ancestor = union_find(uf, parent)
        uf[child] = ancestor
        return ancestor

    if n == 0:
        return
    uf = [i for i in range(n+1)] # well: i = 0 , pipes: i > 0
    edges = []
    for i in range(len(wells)):
        edges.append([0, i+1, wells[i]])
    edges.extend(pipes)
    edges.sort(key = lambda x: x[2]) # sorting can be done by a min-heap as well

    total_cost = 0
    for edge in edges:
        x, y, cost = edge[0], edge[1], edge[2]
        px = union_find(uf, x)
        py = union_find(uf, y)
        if px == py: # this edge will form a loop.
            continue # hence skip adding this edge
        # At this point, px != py. Hence, unionize which
        # means make two nodes have the same parent
        uf[px] = py
        #compress_path(uf)
        total_cost += cost
    return total_cost

def minCostToSupplyWater_MinHeap(n, wells, pipes):
        edges = []
        for pipe in pipes:
            edges.append(pipe)

        for i in range(1, n + 1):
            edges.append([0, i, wells[i - 1]])

        map = defaultdict(list)
        for edge in edges:
            map[edge[0]].append([edge[1], edge[2]])
            map[edge[1]].append([edge[0], edge[2]])

        import heapq
        pq = []
        heapq.heappush(pq, [0, 0])

        visited = [False] * (n + 1)
        result = 0

        while pq:
            node, cost = heapq.heappop(pq)
            if visited[node]:
                continue

            visited[node] = True
            result += cost

            for ne in map[node]: # worst case O(N)
                if not visited[ne[0]]:
                    heapq.heappush(pq, ne)

        return result

def run_minCostToSupplyWater():
    tests = [(3, [1,2,2], [[1,2,1],[2,3,1]], 3),
             (2, [1,1], [[1,2,1],[1,2,2]], 2),
    ]
    for test in tests:
        n, wells, pipes, ans = test[0], test[1], test[2], test[3]
        print(f"\nwells= {wells}")
        print(f"pipes = {pipes}")
        print(f"num houses = {n}")
        for method in ['Kruskal', 'Min-Heap']:
            if method == 'Kruskal':
                cost = minCostToSupplyWater_Kruskal(n, wells, pipes)
            elif method == 'Min-Heap':
                cost = minCostToSupplyWater_MinHeap(n, wells, pipes)
            print(f"Method {method}: min cost = {cost}")
            success = (ans == cost)
            print(f"Pass: {success}")
            if not success:
                print("Failed")
                return

run_minCostToSupplyWater()