import java.util.*;

class Solution {
    // Each adjacency entry is {neighbor, edgeIndex}; avoids boxing both an Edge
    // object per relax and a boxed Long per edge (the original's HashSet<Long>
    // edge-key scheme) in favor of a plain boolean[] indexed by edge id.
    public boolean[] findAnswer(int n, int[][] edges) {
        int m = edges.length;
        List<int[]>[] graph = new List[n];
        for (int i = 0; i < n; i++) {
            graph[i] = new ArrayList<>();
        }
        for (int i = 0; i < m; i++) {
            int u = edges[i][0], v = edges[i][1];
            graph[u].add(new int[]{v, i});
            graph[v].add(new int[]{u, i});
        }

        // Dijkstra's algorithm to find the shortest path distances
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        pq.offer(new int[]{0, 0});

        while (!pq.isEmpty()) {
            int[] current = pq.poll();
            int currentDist = current[0];
            int currentNode = current[1];

            if (currentDist != dist[currentNode]) continue;

            for (int[] edge : graph[currentNode]) {
                int v = edge[0], idx = edge[1];
                int newDist = currentDist + edges[idx][2];
                if (newDist < dist[v]) {
                    dist[v] = newDist;
                    pq.offer(new int[]{newDist, v});
                }
            }
        }

        // Backtrack from n - 1, marking every edge that lies on some shortest path
        boolean[] res = new boolean[m];
        boolean[] visited = new boolean[n];
        Deque<Integer> queue = new ArrayDeque<>();
        queue.add(n - 1);
        visited[n - 1] = true;

        while (!queue.isEmpty()) {
            int currentNode = queue.poll();
            for (int[] edge : graph[currentNode]) {
                int v = edge[0], idx = edge[1];
                if (dist[currentNode] - edges[idx][2] == dist[v]) {
                    if (!visited[v]) {
                        visited[v] = true;
                        queue.add(v);
                    }
                    res[idx] = true;
                }
            }
        }

        return res;
    }
}

public class Find_Edges_in_Shortest_Paths {
public static void runTests(Solution solution) {
    // Test case 1: Simple connected graph with unique shortest path
    int n1 = 4;
    int[][] edges1 = {{0, 1, 1}, {1, 2, 1}, {2, 3, 1}, {0, 3, 4}};
    boolean[] expected_result1 = {true, true, true, false};
    assert Arrays.equals(solution.findAnswer(n1, edges1), expected_result1) : "Test case 1 failed. Expected " + Arrays.toString(expected_result1);

    // Test case 2: Multiple shortest paths
    int n2 = 3;
    int[][] edges2 = {{0, 1, 1}, {1, 2, 1}, {0, 2, 2}};
    boolean[] expected_result2 = {true, true, true};
    assert Arrays.equals(solution.findAnswer(n2, edges2), expected_result2) : "Test case 2 failed. Expected " + Arrays.toString(expected_result2);

    // Test case 3: Disconnected graph
    int n3 = 4;
    int[][] edges3 = {{0, 1, 1}, {2, 3, 1}};
    boolean[] expected_result3 = {false, false};
    assert Arrays.equals(solution.findAnswer(n3, edges3), expected_result3) : "Test case 3 failed. Expected " + Arrays.toString(expected_result3);

    // Test case 4: Graph with loop back to start
    int n4 = 6;
    int[][] edges4 = {{0, 1, 4}, {0, 2, 1}, {1, 3, 2}, {1, 4, 3}, {1, 5, 1}, {2, 3, 1}, {3, 5, 3}, {4, 5, 2}};
    boolean[] expected_result4 = {true, true, true, false, true, true, true, false};
    assert Arrays.equals(solution.findAnswer(n4, edges4), expected_result4) : "Test case 4 failed. Expected " + Arrays.toString(expected_result4);

    // Test case 5: Multiple paths, some edges irrelevant to shortest path
    int n5 = 5;
    int[][] edges5 = {{0, 1, 2}, {0, 2, 4}, {1, 3, 1}, {2, 3, 1}, {3, 4, 3}};
    boolean[] expected_result5 = {true, false, true, false, true};
    assert Arrays.equals(solution.findAnswer(n5, edges5), expected_result5) : "Test case 5 failed. Expected " + Arrays.toString(expected_result5);

    // Test case 6: Graph with a direct shortest path
    int n6 = 4;
    int[][] edges6 = {{2, 0, 1}, {0, 1, 1}, {0, 3, 4}, {3, 2, 2}};
    boolean[] expected_result6 = {true, false, false, true};
    assert Arrays.equals(solution.findAnswer(n6, edges6), expected_result6) : "Test case 6 failed. Expected " + Arrays.toString(expected_result6);
}

    public static void main(String[] args) {
        Solution solution = new Solution();
        for (int i = 0; i < 10000000; i++) {
            runTests(solution); // Ensure your test cases are implemented inside runTests
        }
    }
}
