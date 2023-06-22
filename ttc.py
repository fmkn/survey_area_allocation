import networkx as nx
import random
import matplotlib.pyplot as plt

def ttc_algorithm(preference_dict: dict):
    result_cycles_list = []

    while preference_dict != {}:

        # create directed graph
        g = nx.DiGraph()

        # add nodes
        nodes_list = []
        for key in preference_dict:
            nodes_list.append(key)

        nodes_list.sort()

        for elem in nodes_list:
            g.add_node(elem)

        for key in preference_dict:
            g.add_edge(key, preference_dict[key][0])

        # search for cycles
        cycles = nx.simple_cycles(g)
        cycles_list = list(cycles)

        # Graph drawing part starts here
        color_map_dict_pre = {key: "deepskyblue" for key in preference_dict.keys()}

        for cycle in cycles_list:
            for edge_name in cycle:
                color_map_dict_pre[edge_name] = "yellow"

        color_map = list(color_map_dict_pre.values())
        nx.draw_networkx(g, node_color=color_map)
        plt.show()
        # Graph drawing part ends here

        # add cycles to result
        result_cycles_list.append(cycles_list)

        # start removing edges from preference dict
        for cycle in cycles_list:
            for edge_name in cycle:
                preference_dict.pop(edge_name, None)
                for key in preference_dict:
                    if edge_name in preference_dict[key]:
                        preference_dict[key].remove(edge_name)
        # end removing edges from preference dict
    return result_cycles_list

if __name__ == "__main__":
    with open('preferences.txt', 'r') as f:
        lines = f.readlines()

    preferences = {}
    for line in lines:
        key, value = line.strip().split(':')
        preferences[int(key)] = [int(x) for x in value.strip('[]').split(',')]

    print(preferences)
    print(ttc_algorithm(preference_dict=preferences))
