import argparse
import json

import performance_graph_multiple
import performance_graph_single

parser = argparse.ArgumentParser()
parser.add_argument("json")
args = parser.parse_args()
print(args.json)

with open(args.json, 'r') as graph_spec:
    graph_dict = json.load(graph_spec)

# print([type(x) for x in graph_dict['experiments']])

if graph_dict['graph_type'] == 'single':
    data = performance_graph_single.performance_graph(**graph_dict['experiment'])
    performance_graph_single.simple_plot(data, **graph_dict['graph_style'])

elif graph_dict['graph_type'] == 'multiple':
    frames = [performance_graph_multiple.performance_graph_confidence_interval(**x) for x in graph_dict['experiments']]
    performance_graph_multiple.simple_plot(frames)
