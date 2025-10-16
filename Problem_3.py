'''
Travelling is Fun
https://github.com/Zhouzhiling/leetcode/blob/master/Mathworks%20OA%202019%20Traveling%20is%20Fun.md

Julia is planning a vacation and has a list of cities she wants to visit. She doesn't have a map of the area, but she does have some data that will help here determine whether there is a road connection all the cities she wants to visit. The data comes in the form of two arrays. Each of the first array's elements is an origin city. Each of the second array's is a destination. There is also an integer value threshold. She can tell that any two cities are connected if the values at origin and destination share a common divisor greater than the threshold. Citites are indexed starting at 0.

Each of the pairs, originCities[0] and destinationCities[0] for example, represents a route she wants to take. For each pair, determine whether there is a route between cities. The route does not have to be direct. See the explanation to Sample Case 1 relating to originCity equals 2 or 4 for examples.

For instance, consider an array originCities = [1,2,3] and destinationCities = [4,5,6]. The threshold value is 2. There are 6 total cities. To draw the map, first determine the divisors of all cities:
Origin Cities 	Divisors 	Destination Cities 	Divisors
1 	                1 	        4 	            1,2,4
2 	                1,2 	    5 	            1,5
3 	                1,3 	    6 	            1,2,3,6

The threshold is 2, so we can eliminate cities 1 and 2. Their deivisors are not greater than the threshold. This leaves city 3 to check in the origins list. It has a divisor in common with city 6, and is greater than the threshold so there is a road between them. This is the only pair connected cities. Now that we have created a map, we can check her routes.

She wants to go from originCity[0] = 1 to desitinationCity[0] = 4 but there is no road. There is no road for her second route either, form city 2 to 5. There is only a road that matches her third route at index 2, from city 3 to 6. A true/fals array of her results would be paths = [0,0,1].

Function description
Complete the function findConnection() below. The function must return a true/false array where each paths[i] contains 1 if the route between originCities[i] and destinationCities[i] exists, or 0 if it does not.

findConnection() has the following parameter(s): n: integer, the number of cities g: integer, the threshold value originCities[originCities[0], ... originCities[q-1]]: an array of integers desitinationCities[desitnationCities[0], ... desitinationCities[q-1]]: an array of integers

Constraints
2 <= n <= 2 *10^5
0 <= g <= n
1 <= q <= min(n*(n-1)/2, 10^5)
1 <= originCities[i], destinationCities[i] <= n, where 0 <= i < q
originCities[i] != destinationCities[i], where 0 <= i < q

Example 1:
Input: n = 6
       threshold = 0
       origin = [1,4,3,6]
       destination = [3,6,2,5]
Output: [1, 1, 1, 1]

Example 2:
Input: n = 6
       threshold = 1
       origin = [1,2,4,6]
       destination = [3,3,3,4]
Output:  [0, 1, 1, 1]

Solution:
1. BFS
We connect all node pairs whose GCD is greater than the threshold.
Then for each query, we do a BFS from origin to destination. If we can reach it, we set 1; if not, we leave it as 0.
https://youtu.be/MaHBeXA3jI0?t=3796
Time: O(V^2 · logV + q·(V + E)) where V - vertices, E - Edges and q - number of queries. V^2 for building the graph, log V for finding GCD, V+E for BFS
Space: O(V^2 + V) (adjacency list. Worst case V^2 if graph is dense. V for queue)

2. DFS
We connect all node pairs whose GCD is greater than the threshold.
Then for each query, we do a DFS from origin to destination. If we can reach it, we set 1; if not, we leave it as 0.  If it does, we mark the result as 1, otherwise it's 0.
Time: O(V^2 · logV + q·(V + E)), Space: O(V^2 + V) (space V^2 for adj list + V recursion depth)

3. Disjoint Union
We group all nodes using union-find where GCD is above threshold.
Either check every pair or multiples (commented version). For each query, we check if origin and destination are in the same group.
Time: O(V^2 · logV + q) where V - vertices, E - Edges and q - number of queries. V^2 for building the graph, log V for finding GCD.
Space: O(V) (V for parent[] array)

'''
from collections import defaultdict, deque

def gcd(a, b):
    if a == 0:
        return b
    return gcd(b%a, a)

def build_graph(n, threshold):
        adj_list = defaultdict(set)
        for i in range(1, n+1):
            for j in range(1, n+1):
                if i == j:
                    continue
                g = gcd(i,j)
                if g > threshold:
                    adj_list[i].add(j)
                    adj_list[j].add(i)
        return adj_list

def findConnection_BFS(n, threshold, origin, destination):
    graph = build_graph(n, threshold)
    paths = [0]*len(origin)
    for i in range(len(origin)):
        source = origin[i]
        target = destination[i]
        q = deque()
        q.append(source)
        visited = [False]*(n+1)
        visited[source] = True
        while q:
            curr = q.popleft()
            if curr == target:
                paths[i] = 1
                break
            for nbr in graph[curr]:
                if not visited[nbr]:
                    q.append(nbr)
                    visited[nbr]=True
    return paths

def findConnection_DFS(n, threshold, origin, destination):
    def dfs(source, target, graph, visited):
        # base
        if source == target:
            return True

        # logic
        for nbr in graph[source]:
            if not visited[nbr]:
                visited[nbr] = True
                reached = dfs(nbr, target, graph, visited)
                if reached:
                    return True
        return False

    graph = build_graph(n, threshold)
    paths = [0]*len(origin)
    for i in range(len(origin)):
        source = origin[i]
        target = destination[i]
        visited = [False]*(n+1)
        visited[source] = True
        reached = dfs(source, target, graph, visited)
        if reached: paths[i] = 1
    return paths

def findConnection_Union(n, threshold, origin, destination):
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px = find(x)
        py = find(y)
        if px != py:
            parent[px] = py


    global parent
    parent = [i for i in range(n + 1)]

    # build graph using GCD
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                continue
            if gcd(i, j) > threshold:
                union(i, j)

    result = []
    for x, y in zip(origin, destination):
        result.append(1 if find(x) == find(y) else 0)
    return result

def run_findConnection():
    tests = [(6,0,[1,4,3,6],[3,6,2,5],[1,1,1,1]),
             (6,1,[1,2,4,6],[3,3,3,4],[0,1,1,1]),
    ]
    for test in tests:
        n, threshold, origin, destination, ans = test[0], test[1], test[2], test[3], test[4]
        print(f"\nno. of cities = {n}")
        print(f"threshold = {threshold}")
        print(f"origin cities = {origin}")
        print(f"destination cities = {destination}")
        for method in ['BFS', 'DFS', 'Disjoint-Union']:
            if method == 'BFS':
                paths = findConnection_BFS(n, threshold, origin, destination)
            elif method == 'DFS':
                paths = findConnection_DFS(n, threshold, origin, destination)
            elif method == 'Disjoint-Union':
                paths = findConnection_Union(n, threshold, origin, destination)
            print(f"Method {method}: paths = {paths}")
            success = (ans == paths)
            print(f"Pass: {success}")
            if not success:
                print(f"Failed")
                return

run_findConnection()

# n=6
# threshold = 0
# origin = [1,4,3,6]
# destination = [3,6,2,5]
# paths = findConnection_BFS(n, threshold, origin, destination)
# print(paths)
# paths = findConnection_DFS(n, threshold, origin, destination)
# print(paths)
# paths = findConnection_Union(n, threshold, origin, destination)
# print(paths)

# n=6
# threshold = 1
# origin = [1,2,4,6]
# destination = [3,3,3,4]
# paths = findConnection_BFS(n, threshold, origin, destination)
# print(paths)
# paths = findConnection_DFS(n, threshold, origin, destination)
# print(paths)
# paths = findConnection_Union(n, threshold, origin, destination)
# print(paths)
