import argparse
from tqdm import tqdm
import graphviz as gv


class DeBruijnException(BaseException):
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

        self.edge_sequence += following_edge.edge_sequence[-1]
        self.v2 = following_edge.v2
        self.coverage = round(self.coverage + following_edge.coverage) / 2
        return self

    def __str__(self):
        return str(self.edge_sequence)


edge_sequences = set()


class Vertex:
    show_sequences = False

    def __init__(self, seq):
        self.seq = seq
        self.input = set()
        self.output = set()

    def add_edge(self, other):
        if not isinstance(other, Vertex):
            raise DeBruijnException("'other' must be Vertex instance!")

        self.output.add(Edge(self, other))
        other.input.add(Edge(self, other))
        edge_sequences.add(Edge(self, other).edge_sequence)

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
        if not isinstance(seq1, Vertex) or not isinstance(seq2,  Vertex):
            raise DeBruijnException("seq1 and seq2 must be Vertex instances!")

        if seq1.seq in self.g and seq2.seq in self.g:
            edge_sequence = seq1.seq + seq2.seq[-1]
            for v in self.g.values():
                for edge in v.output:
                    if edge.edge_sequence == edge_sequence:
                        edge.inc_coverage()
        else:
            if seq1.seq not in self.g and seq2.seq not in self.g:
                seq1.add_edge(seq2)
                self.g[seq1.seq] = seq1
                self.g[seq2.seq] = seq2
            elif seq1.seq in self.g and seq2.seq not in self.g:
                self.g[seq1.seq].add_edge(seq2)
                self.g[seq2.seq] = seq2
            elif seq1.seq not in self.g and seq2.seq in self.g:
                self.g[seq1.seq] = seq1
                self.g[seq1.seq].add_edge(self.g[seq2.seq])

    def add_seq(self, seq):
        for i in range(len(seq) - self.k):
            first_seq = Vertex(seq[i: i+self.k])
            second_seq = Vertex(seq[i+1: i+self.k+1])
            self.add_edge(first_seq, second_seq)

    def compress(self):
        to_delete = []  # List of redundant vertices
        for kmer, vertex in self.g.items():
            if vertex.compress():
                to_delete.append(kmer)

        for kmer in to_delete:
            mid_vertex = self.g[kmer]
            previous_edge = next(iter(mid_vertex.input))
            next_edge = next(iter(mid_vertex.output))

            previous_kmer = previous_edge.v1.seq
            next_kmer = next_edge.v2.seq

            self.g[previous_kmer].output = {previous_edge.merge(next_edge)}
            self.g[next_kmer].input = {previous_edge.merge(next_edge)}
            del self.g[kmer]
    # Delete redundant vertex

    def save_dot(self, outp):
        digraph = gv.Digraph(format='svg')
        for kmer in self.g:
            digraph.node(kmer)

        for vertex in self.g.values():
            for edge in vertex.output:
                digraph.edge(vertex.seq, edge.v2.seq, label="{}".format(
                             edge.coverage))

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
