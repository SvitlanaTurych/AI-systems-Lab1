"""
Ітеративний алгоритм пошуку у глибину (DFS) зі стеком, реалізований
без залежності від GUI, щоб його можна було покроково викликати
з таймера інтерфейсу (або використовувати окремо, наприклад у тестах).
"""


class DFSSearch:
    """Тримає весь стан покрокового DFS: стек, відвідані вершини,
    батьківські покажчики та лічильник розкритих вершин."""

    def __init__(self, graph, start, goal, order="asc"):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.order = order  # "asc" або "desc"

        self.stack = [start]
        self.visited = set()
        self.parent = {start: None}
        self.expanded_count = 0
        self.current_node = None
        self.path = []

        self.found = False
        self.finished = False

    def step(self):
        """Виконує один крок алгоритму.

        Повертає один із рядків:
        - "expanded"  - розкрито чергову (нецільову) вершину;
        - "found"     - розкрито цільову вершину, шлях побудовано;
        - "not_found" - стек порожній, шлях не існує.
        """
        if self.finished:
            return "not_found" if not self.found else "found"

        node = None
        while self.stack:
            candidate = self.stack.pop()
            if candidate not in self.visited:
                node = candidate
                break

        if node is None:
            self.finished = True
            self.found = False
            return "not_found"

        self.current_node = node
        self.visited.add(node)
        self.expanded_count += 1

        if node == self.goal:
            self.path = self._reconstruct_path(node)
            self.finished = True
            self.found = True
            return "found"

        neighbors = sorted(self.graph.neighbors(node), reverse=(self.order == "desc"))
        to_push = [nb for nb in neighbors if nb not in self.visited]
        # пушимо у зворотному порядку, щоб зі стеку першою вийшла
        # вершина, яка йде першою у обраному порядку обходу (LIFO)
        for nb in reversed(to_push):
            self.stack.append(nb)
            if nb not in self.parent:
                self.parent[nb] = node

        return "expanded"

    def _reconstruct_path(self, goal):
        path = [goal]
        while self.parent.get(path[-1]) is not None:
            path.append(self.parent[path[-1]])
        path.reverse()
        return path