import pm4py as pm
import networkx as nx


def petri_graph(net: pm.PetriNet, initial, final):
    DG = nx.DiGraph()

    for place in net.places:
        DG.add_node(place.name, node_type='place', label=place.name, is_initial=place in initial, is_final=place in final)

    for transition in net.transitions:
        tau = transition.label is None
        if tau:
            label = f'tau_{transition.name}'
        else:
            label = transition.label
        DG.add_node(transition.name, node_type='transition', label=label, is_silent=tau)

    for arc in net.arcs:
        DG.add_edge(arc.source.name, arc.target.name, weight=arc.weight)

    return DG


event_logs = pm.read_xes('Sepsis Cases - Event Log.xes.gz')
petri_net, initial_states, final_states = pm.discover_petri_net_inductive(event_logs)
pm.save_vis_petri_net(petri_net, initial_states, final_states, 'petri_net.png')

# Преобразуем сеть Петри в граф
graph = petri_graph(petri_net, initial_states, final_states)
# Матрица смежности
adj_mat = nx.adjacency_matrix(graph)

print(f'Places: {petri_net.places}')
print(f'Arcs: {petri_net.arcs}')
print(f'Transitions: {petri_net.transitions}')
