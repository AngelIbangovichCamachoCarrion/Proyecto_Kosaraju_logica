import random
import time
import networkx as nx
import matplotlib.pyplot as plt

class SocialNetWorkGraph:
    def __init__(self,users):
        self.V = users
        self.adj =[[] for _ in range(users)]
        
        
    def add_following(self, u, v):
        self.adj[u].append(v)
        
    def dfs(self, v, visitante, stack):
        visitante[v] = True
        
        for vecino in self.adj[v]:
            if not visitante[vecino]:
                self.dfs(vecino, visitante, stack)
        stack.append(v)
        
    def  transpose(self):
        Gt = SocialNetWorkGraph(self.V)
        for v in range(self.V):
            for vecino in self.adj[v]:
                Gt.add_following(vecino, v)
        return Gt
    
    def dfs_scc(self, v, visitante, componente):
        visitante[v] = True
        componente.append(v)
        for vecino in self.adj[v]:
            if not visitante[vecino]:
                self.dfs_scc(vecino, visitante, componente)
    
    
    def kosaraju(self):
        stack = []
        visitante = [False] * self.V
        
        for i in range(self.V):
            if not visitante[i]:
                self.dfs(i, visitante, stack)
        
        transpose_graph = self.transpose()
        visitante = [False] * self.V
        sccs = []
        
        while stack:
            v = stack.pop()
            if not visitante[v]:
                componente = []
                transpose_graph.dfs_scc(v , visitante, componente)
                sccs.append(componente)
        return sccs
    
    def tarjan_dfs(self, u, ids, low, on_stack, stack, sccs, index):
        ids[u] = low[u] = index[0]
        index[0] += 1
        stack.append(u)
        on_stack[u] = True
        
        
        for v in self.adj[u]:
            if ids[v] == -1:
                self.tarjan_dfs(v, ids, low, on_stack, stack, sccs, index)    
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], ids[v])
                
        if ids[u] == low[u]:
            scc = []
            while True:
                v = stack.pop()
                on_stack[v] = False
                scc.append(v)
                if v == u:
                    break
            sccs.append(scc)
    
    def tarjan(self):
        ids = [-1] * self.V
        low = [-1] * self.V
        on_stack = [False] * self.V
        stack = []
        sccs = []
        index = [0]
        
        for i in range(self.V):
            if ids[i] == -1:
                self.tarjan_dfs(i, ids, low, on_stack, stack, sccs, index)
        
        return sccs
    
    def visualizar(self, sccs):
        G = nx.DiGraph()
        color_map = {}
        
        for i , componente in enumerate(sccs):
            for nodo in componente:
                color_map[nodo] = i
                for vecino in self.adj[nodo]:
                    G.add_edge(nodo, vecino)
        
        posicion = nx.spring_layout(G)
        colores = [color_map.get(nodo, 0) for nodo in G.nodes()]
        nx.draw(G, posicion, with_labels=True, node_color=colores, cmap=plt.cm.rainbow, node_size=500)
        plt.show()
    
    def generate_random_network(self, edges_percentage=0.3):
        
        total_possible_edges = self.V * (self.V - 1) 
        num_edges = int(total_possible_edges * edges_percentage)

        for _ in range(num_edges):
            u, v = random.sample(range(self.V), 2)  
            self.add_following(u, v)
        
def test_twiter_social(num_users=10,follow_prob=0.3):
    g= SocialNetWorkGraph(num_users)
    g.generate_random_network(follow_prob)
        

    start = time.time()
    sccs_kosaraju = g.kosaraju()
    end = time.time()
    print("Grupos de Usuarios: ", sccs_kosaraju,"Tiempo: ", end - start)
    g.visualizar(sccs_kosaraju)
    
    
    start = time.time()
    sccs_tarjan = g.tarjan()
    end = time.time()
    print("Grupos de Usuarios: ", sccs_tarjan,"Tiempo: ", end - start)
    g.visualizar(sccs_tarjan)
        
test_twiter_social() 