import argparse
from tqdm import tqdm
import graphviz as gv


class DeBruijnException(Exception):
    pass


class Edge:
    show_sequences = False

    def __init__(self, v1, v2):
        if not isinstance(v1, Vertex) or not isinstance(v2,  Vertex):
            raise DeBruijnException("v1 and v2 must be Vertex instances!")

        self.v1 = v1
        self.v2 = v2
        self.coverage = 1
        self.edge_sequence = self.v1.seq + self.v2.seq[-1]

    def inc_coverage(self):
        self.coverage += 1

    def __len__(self):
        return len(self.edge_sequence) - Graph.k

    def merge(self, following_edge):
        if not isinstance(following_edge, Edge):
            raise DeBruijnException("following_edge must be Edge instance!")

        self.edge_sequence += following_edge.edge_sequence[Graph.k:]
        self.v2 = following_edge.v2
        self.coverage = (self.coverage * len(self) +
                         following_edge.coverage * len(following_edge)) / \
                        (len(self) + len(following_edge))
        return self

    def __str__(self):
        return str(self.edge_sequence)


class Vertex:
    show_sequences = False

    def __init__(self, seq):
        self.seq = seq
        self.input = {}
        self.output = {}

    def add_edge(self, other):
        if not isinstance(other, Vertex):
            raise DeBruijnException("'other' must be Vertex instance!")

        edge = Edge(self, other)
        if edge.edge_sequence not in self.output:
            self.output[edge.edge_sequence] = edge
            other.input[edge.edge_sequence] = edge
        else:
            self.output[edge.edge_sequence].inc_coverage()

    def __str__(self):
        return str(self.seq)

    def compress(self):
        if len(self.output) == 1 and len(self.input) == 1:
            return True
        return False


class Graph:
    k = None

    def __init__(self):
        self.g = {}

    def add_edge(self, seq1, seq2):
        self.g[seq1].add_edge(self.g[seq2])

    def check_vertex_existence(self, v1, v2):
        if v1 not in self.g:
            self.g[v1] = Vertex(v1)
        if v2 not in self.g:
            self.g[v2] = Vertex(v2)

    def add_seq(self, seq):
        for i in range(len(seq) - self.k):
            self.check_vertex_existence(seq[i: i+self.k], seq[i+1: i+self.k+1])
            self.add_edge(seq[i: i+self.k], seq[i+1: i+self.k+1])

    def compress(self):
        to_delete = []  # List of redundant vertices
        for kmer, vertex in self.g.items():
            if vertex.compress():
                to_delete.append(kmer)

        for kmer in to_delete:
            mid_vertex = self.g[kmer]
            previous_edge = next(iter(mid_vertex.input.values()))
            next_edge = next(iter(mid_vertex.output.values()))

            previous_kmer = previous_edge.v1.seq
            next_kmer = next_edge.v2.seq

            merged_edge = previous_edge.merge(next_edge)
            print(merged_edge)
            self.g[previous_kmer].output[merged_edge.edge_sequence] = merged_edge
            self.g[next_kmer].input[merged_edge.edge_sequence] = merged_edge

            del self.g[kmer]
            del self.g[previous_kmer].output[previous_edge.edge_sequence]
            del self.g[next_kmer].input[next_edge.edge_sequence]
    # Delete redundant vertex

    def check_vertex_show_sequences(self):
        digraph = gv.Digraph(format='svg')

        if Vertex.show_sequences:
            for kmer in self.g:
                digraph.node(kmer)
        else:
            for kmer in self.g:
                digraph.node(kmer, label="")

        return digraph

    def check_edge_show_sequences(self):
        digraph = self.check_vertex_show_sequences()

        if Edge.show_sequences:
            for vertex in self.g.values():
                for edge in vertex.output:
                    digraph.edge(vertex.seq, vertex.output[edge].v2.seq,
                                 label="{}".format(edge))
        else:
            for vertex in self.g.values():
                for edge in vertex.output.values():
                    print(edge)
                    digraph.edge(vertex.seq, edge.v2.seq,
                                 label="C: {} L: {}".format(
                                     edge.coverage,
                                     len(edge)))

        return digraph

    def save_dot(self, outp):
        digraph = self.check_edge_show_sequences()
        return digraph.render(outp)


complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}


def reverse_complement(seq):
    return ''.join(complement[nt] for nt in seq[::-1])


def read_fastq(f):
    for line in f:
        name = line.strip()
        seq = next(f).strip()
        next(f)
        next(f)
        yield name, seq


def read_fasta(f):
    name = None
    seq = None
    for line in f:
        if line.startswith('>'):
            if name:
                yield name, seq
            name = line.lstrip('>').strip()
            seq = ''
        else:
            seq += line.strip()
    yield name, seq


def read(f):
    if f.name.endswith('a'):
        return read_fasta(f)
    else:
        return read_fastq(f)


def main():
    parser = argparse.ArgumentParser(description='De Bruijn graph')
    parser.add_argument('-i', '--input', help='Input fastq', metavar='File',
                        type=argparse.FileType(), required=True)
    parser.add_argument('-k', help='k-mer size (default: 55)', metavar='Int',
                        type=int, default=55)
    parser.add_argument('-o', '--output', help='Name of output dot',
                        type=str, required=True)
    parser.add_argument('-c', '--compress', help='Shrink graph',
                        action='store_true')
    parser.add_argument('--vertex', help='Show vertex sequences',
                        action='store_true')
    parser.add_argument('--edge', help='Show edge sequences',
                        action='store_true')
    args = parser.parse_args()

    Graph.k = args.k
    Vertex.show_sequences = args.vertex
    Edge.show_sequences = args.edge

    graph = Graph()
    for name, seq in tqdm(read(args.input)):
        graph.add_seq(seq)
        graph.add_seq(reverse_complement(seq))

    if args.compress:
        graph.compress()

    graph.save_dot(args.output)


if __name__ == '__main__':
    main()
