'''
Created on November 15, 2020
@author: Niall Dagg
'''


import pandas as pd
from math import inf

class Router():
    def __init__(self, start, graph):

        self.start = start
        self.graph = graph

    #def get_path(self, router_name):
      # Performs Dijkstra's algorithm to return distance and add the path between the router and the 
      # router specified by router_name
      # Should output - Start node and End node, Path taken, the cost

    def get_path(self, end):

        #creates a global variable of result for use in our print
        global dijk_result
        #start is the start of our graph
        start = self.start

        #dictionary to find the shortest, updates with where path was
        prev_node = {}

        #dictionary of a node and its shortest distance
        shortest_distance = {}

        #this is our graph, creates a copy for local function use
        unvistedNodes = dict.copy(self.graph.connection)

        #our full graph to be used 
        full_graph = self.graph.connection

        #imported infinity to be used as the unknown of the distance between nodes
        infinity = inf

        #the list we will use to record the path taken between shortest distance
        taken_path = []

        #this for loop starts the algorithm by making the distance to the start 0
        #and the distance from every other node infinite
        for node in unvistedNodes:
            shortest_distance[node] = infinity
        shortest_distance[start] = 0

        #this is our full loop to check each node to find the shortest distance
        #overwriting the shortest distance when required
        while unvistedNodes:
            #set the minNode to None for starting
            minNode = None
            #a for loop to check if the distance between each node is smaller than our current minNode
            for node in unvistedNodes:
                if minNode is None:
                    minNode = node
                elif shortest_distance[node] < shortest_distance[minNode]:
                    minNode = node
            
            #this for loop is to go through each distance of each connecting node to check and reitrerate the shortest distance
            for child, cost in full_graph[minNode].items():
                if cost + shortest_distance[minNode] < shortest_distance[child]:
                    shortest_distance[child] = cost + shortest_distance[minNode]
                    prev_node[child] = minNode
            unvistedNodes.pop(minNode)
    
        #this is a loop to add our distance and our path to our path list
        currentNode = end
        while currentNode != start:
            try:
                taken_path.insert(0,currentNode)
                currentNode = prev_node[currentNode]
            except KeyError:
                print('Path not reachable')
                break
        
        end_cost = ""

        taken_path.insert(0,start)

        if shortest_distance[end] != infinity:
            #creates our return result for printing in our print function
            end_cost = str(shortest_distance[end])
            taken_path = "->".join(taken_path)
        dijk_result = [start, end, end_cost, taken_path]
        return [start, end, end_cost, taken_path]

    #a function to print our result, so we can use our get_path function 
    #within other functions without our print statement

    def print_dijkstra(self):

        print("Start: {}\nEnd: {}\nPath: {}\nCost: {}".format(dijk_result[0], dijk_result[1], dijk_result[2], dijk_result[3]))


    #our function to print our routing table

    def print_routing_table(self):

        #a list to add a geth path return statement for each node in our graph
        #list is cl-short for connectionslist
        #makes our panda dataframe easier to read
        start = self.start
        cl = []
        for k in self.graph.connection:
            cl.append(self.get_path(k))

        #pop off our start which is just a distance of 0 and is unneccessary

        #start == a
        if cl[0][1] == start:
            cl.pop(0)
        #start == b
        if cl[1][1] == start:
            cl.pop(1)
        #start == c
        if cl[2][1] == start:
            cl.pop(2)
        #start == d
        if cl[3][1] == start:
            cl.pop(3)
        #start == e
        if cl[4][1] == start:
            cl.pop(4)

        

        #create a panda dataframe using our data that we have created within our connections list
        data = {"from": [start, start, start , start, start], "to":[ cl[0][1], cl[1][1], cl[2][1], cl[3][1], cl[4][1]],\
        "cost": [cl[0][2], cl[1][2], cl[2][2], cl[3][2], cl[4][2]], "path": [cl[0][3], cl[1][3], cl[2][3], cl[3][3], cl[4][3]]}
        print(pd.DataFrame.from_dict(data))
    
    #our function to remove a router from our graph
    def remove_router(self, router_name):

        #start is always, our start node specified in our Router class
        start = self.start

        #create a copy of our global dictionary for local use within this func
        graph_dict = dict.copy(self.graph.connection)
        #as we use a nested dicitonary, deleting is as easy as this
        del graph_dict[router_name]


        #a loop to remove any instance of our router_name from our nested dictionary
        for key, route in graph_dict.items():
            if router_name in route.keys():
                del graph_dict[key][router_name]


        #then it is set up as before but with one less in the list
        dl = []
        for k in graph_dict:
            #we append each list of [start, end, cost, path] from every node to our
            #dl which is shorthand for delete list
            dl.append(self.get_path(k))
        #we then pop off our starting node as distance is 0
        dl.pop(0)
        
        data = {"from": [start, start, start , start], "to":[ dl[0][1], dl[1][1], dl[2][1], dl[3][1]],\
        "cost": [dl[0][2], dl[1][2], dl[2][2], dl[3][2]], "path": [dl[0][3], dl[1][3], dl[2][3], dl[3][3]]}
        print(pd.DataFrame.from_dict(data))



         

class Graph():

    def __init__(self):

        #I have used a nested dictionary format to contain our data as it makes printing and deleting much easier
        self.connection = {}

        #Our function to add a router to our nested dictionary
        #Takes in a router, a connecting router and a distance cost between them
    def add_edge(self, router_one, router_two, cost):
        if router_one not in self.connection:
            self.connection[router_one] = {}
        self.connection[router_one][router_two] = cost

    def opening(self):
        print("\nWelcome to Niall's graph and routing table calculator!")
        print("Add routers to our graph with 'graph.add_router('start','end', cost).")
        print("Once you have added all your routers to your graph, initialise with 'router = Router('a', graph).")
        print("I have created a sample graph and an example of the various functions you can do!\n")
        print("My graph is a directed graph, so it can only go one way.")

    def dijk_para(self):
            print("This is an example of our get_path function, which uses dijkstra's algorithm to find the shortest path.")
            print("In this case, I called the function to find the distance from the start to the f node.\n")
    
    def routing_para(self):
        print("\n")
        print("This is an example of our routing table, with the cost and path of the start node to all other nodes.\n")

    def delete_para(self):
        print("\n")
        print("I have also created a remove router function, which deletes the node in the argument and then recalculates")
        print("The distance between the start to every available node.\n")

    def multi_para(self):
        print("\n")
        print("We can also create routing tables for every other node, but as it is one directional, we must make sure")
        print("every node has a connection.\n")


def main():   
    graph = Graph()
    graph.opening()
    graph.add_edge("a", "b", 7)
    graph.add_edge("b", "a", 4)
    graph.add_edge("a", "c", 9)
    graph.add_edge("a", "f", 14)
    graph.add_edge("b", "c", 10)
    graph.add_edge("b", "d", 15)
    graph.add_edge("c", "a", 5)
    graph.add_edge("c", "b", 7)
    graph.add_edge("c", "d", 5)
    graph.add_edge("c", "f", 2)
    graph.add_edge("d", "e", 6)
    graph.add_edge("e", "f", 0)
    graph.add_edge("f", "e", 11)
    router = Router("a", graph)
    router2 = Router("b", graph)
    

    print("\nhaha router goes b" + "r"*10)
    
    graph.dijk_para()
    router.get_path("f")
    router.print_dijkstra()
    
    graph.routing_para()
    router.print_routing_table()
    
    graph.multi_para()
    router2.print_routing_table()

    graph.delete_para()
    router.remove_router("c")

if __name__ == "__main__":
    main()



Router.get_path.__doc__="This is a function that performs dijkstras algorithm to find the optimal path\
                        between a start node and an end argument node, it returns a list containing\
                        [start, end, cost, path_taken]."

Router.print_dijkstra.__doc__="A helper function to print out the result of our gt_path func\
                                in the output specified. It allows us to use the get_path in\
                                different functions without printing out the result."

Router.print_routing_table.__doc__="A function that prints a table of the distance and path\
                                    between our start and every other node in the graph.\
                                    It uses the panda dataframe module to create an easy\
                                    to read table as requested."

Router.remove_router.__doc__="A function that allows us to remove a router from our graph.\
                            This in turn recalculates all the distances again and prints\
                                in the same easy to read table format."