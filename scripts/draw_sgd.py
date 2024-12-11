import argparse
import json
import os

import networkx as nx

from sgd.full import sgd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', default='.')
    parser.add_argument('input', nargs='+')
    args = parser.parse_args()

    os.makedirs(args.dest, exist_ok=True)
    for filepath in args.input:
        basename = os.path.basename(filepath)
        graph = nx.node_link_graph(json.load(open(filepath)))
        pos = sgd(graph)
        json.dump(pos,
                  open(os.path.join(args.dest, basename), 'w'),
                  ensure_ascii=False)


if __name__ == '__main__':
    main()