'''
277 Find the celebrity
https://leetcode.com/problems/find-the-celebrity/description/

Suppose you are at a party with n people labeled from 0 to n - 1 and among them, there may exist one celebrity. The definition of a celebrity is that all the other n - 1 people know the celebrity, but the celebrity does not know any of them.

Now you want to find out who the celebrity is or verify that there is not one. You are only allowed to ask questions like: "Hi, A. Do you know B?" to get information about whether A knows B. You need to find out the celebrity (or verify there is not one) by asking as few questions as possible (in the asymptotic sense).

You are given an integer n and a helper function bool knows(a, b) that tells you whether a knows b. Implement a function int findCelebrity(n). There will be exactly one celebrity if they are at the party.

Return the celebrity's label if there is a celebrity at the party. If there is no celebrity, return -1.

Note that the n x n 2D array graph given as input is not directly available to you, and instead only accessible through the helper function knows. graph[i][j] == 1 represents person i knows person j, wherease graph[i][j] == 0 represents person j does not know person i.

Example 1:
Input: graph = [[1,1,0],[0,1,0],[1,1,1]]
Output: 1
Explanation: There are three persons labeled with 0, 1 and 2. graph[i][j] = 1 means person i knows person j, otherwise graph[i][j] = 0 means person i does not know person j. The celebrity is the person labeled as 1 because both 0 and 2 know him but 1 does not know anybody.

Example 2:
Input: graph = [[1,0,1],[1,1,0],[0,1,1]]
Output: -1
Explanation: There is no celebrity.

Constraints:
n == graph.length == graph[i].length
2 <= n <= 100
graph[i][j] is 0 or 1.
graph[i][i] == 1

Solution:
1. Indegrees and outdegrees
indegrees of vertex  i =  no .of incoming edges
outdegrees of vertex i =  no .of outgoing edges

If i is a celebrity, then:
indegrees[i] = n-1 (-1 because we do not count self-loops, i.e. dont count celebrity knows celebrity)
outdegrees[i] = 0
difference = indegrees[i] - outdegrees[i]
           = n -1

If i is not a celebrity, then:
indegrees[i] = k, k <= n-2
difference <= n-2 (but never equal to n-1)

https://youtu.be/sPOst2hE4_M?t=2257

Time: O(N^2), Space: O(2N) = O(N)


2. Similar to solution 1, but we optimize the space by using a single indegrees[] array. We add for every incoming edge and we subtract for every outgoing edge.
Time: O(N^2), Space: O(N)

3. We assume that the celebrity candidate = person 0. Then,

we check if candidate knows person 1.
yes: update the candidate to person 1. Thus, candidate = person 1
no: no change in candidate

we check if candidate knows person 2.
yes: update the candidate to person 2. Thus, candidate = person 2
no: no change in candidate

we check if candidate knows person 3.
yes: update the candidate to person 3. Thus, candidate = person 3
no: no change in candidate

We continue like this until we have ran a check on all N persons. At the end, we have a potential candidate but not a guranteed candidate yet.

Why not guranteed? Because we have always been checking if candidate knows person i, where i is any index after the candidate's index. Let candidate be at index k=i-1. Since k is a potential candidate, all we know is that person k doesn't know person i, i+1, .. N-1. But we haven't checked two things yet:
a) if candidate doesn't know persons 0,...,i-2
b) if everyone knows the candidate

Both (a) and (b) must be satisfied for the candidate to be declared a celebrity.
for i in range(n):
    if celeb != i # discard self-loops
        if knows(i, candidate) and not knows(candidate, i):
            continue
        else:
            candidate = -1
            break

The advantage of this approach is that it takes O(N) time.

https://youtu.be/sPOst2hE4_M?t=2960

Time: O(N), Space: O(1)
'''
def mprint(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

# The knows API is already defined for you.
# return a bool, whether a knows b
# def knows(a: int, b: int) -> bool:

def knows(graph, i, j):
    return graph[i][j]

def findCelebrity_1(graph, n: int) -> int:
    ''' Time: O(N^2), Space: O(2N) '''
    if n == 0:
        return -1
    indegrees = [0]*n
    outdegrees = [0]*n
    celebrity = -1
    for i in range(n):
        for j in range(n):
            if i != j:
                if knows(graph, i,j):
                    outdegrees[i] = outdegrees[i] + 1
                    indegrees[j] = indegrees[j] + 1

    for i in range(n):
        indegrees[i] = indegrees[i] - outdegrees[i]

    for i in range(n):
        if indegrees[i] == n-1 and outdegrees[i] == 0:
            celebrity = i
    return celebrity

def findCelebrity_2(graph, n: int) -> int:
    ''' Time: O(N^2), Space: O(N) '''
    if n == 0:
        return -1
    indegrees = [0]*n
    celebrity = -1
    for i in range(n):
        for j in range(n):
            if i != j:
                if knows(graph, i,j):
                    indegrees[i] = indegrees[i] - 1
                    indegrees[j] = indegrees[j] + 1

    for i in range(n):
        if indegrees[i] == n-1:
            celebrity = i
    return celebrity

def findCelebrity_3(graph, n: int) -> int:
    ''' Time: O(N), Space: O(1) '''
    if n == 0:
        return -1
    celeb = 0
    for i in range(n):
        if i != celeb:
            if knows(graph, celeb, i):
                # celeb not supposed to know i but if he knows
                # then he cannot be a celebrity. Hence, assume the
                # that the next candidate for celebrity is i
                celeb = i

    # At this point, we have a candidate celebrity. Let posn of celeb = k
    # But we haven't checked two things yet:
    # a) if candidate doesn't know persons ahead of him 0,...,k-1
    # b) if everyone knows the candidate
    # Both (a) and (b) must be satisfied for the candidate to be declared a
    # celebrity. We use the reverse logic instead, i.e., not a or not b
    for i in range(n):
        if i != celeb:
            if not knows(graph, i, celeb) or knows (graph, celeb, i):
                return -1
    return celeb


def run_findCelebrity():
    tests = [([[1,1,0],
               [0,1,0],
               [1,1,1]], 1),
             ([[1,1,1,0,0],
               [1,1,1,0,1],
               [0,0,1,0,0],
               [0,0,1,1,1],
               [0,1,1,1,1]], 2),
             ([[1,1,1,0,0],
               [1,1,1,0,1],
               [0,0,1,0,0],
               [0,0,1,1,1],
               [0,1,0,1,1]], -1),
    ]
    for test in tests:
        graph, ans = test[0], test[1]
        print(f"\ngraph:")
        mprint(graph)
        for method in [1,2,3]:
            if method == 1:
                celebrity = findCelebrity_1(graph, len(graph))
            elif method == 2:
                celebrity = findCelebrity_2(graph, len(graph))
            elif method == 3:
                celebrity = findCelebrity_3(graph, len(graph))

            print(f"Method {method}: celebrity = {celebrity}")
            success = (ans == celebrity)
            print(f"Pass: {success}")
            if not success:
                print(f"Failed")
                return

run_findCelebrity()