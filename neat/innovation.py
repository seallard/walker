

class Innovation:
    __slots__ = ['gene', 'node_in', 'node_out', 'gene_type']

    def __init__(self, gene, node_in, node_out):
        """Initialises Innovation.

        Each innovation is uniquely specified by two nodes. Links are specified
        by the nodes they connect. Nodes themselves are specified by the two
        nodes they occur between.

        Args:
            gene:
                A link_gene.LinkGene or node_gene.NodeGene instance.
            node_in:
                Innovation number of preceeding node. Set to -1 if the node is an
                input or output.
            node_out:
                Innovation number of subsequent node. Set to -1 if the node is an
                input or output.
        """
        self.gene = gene
        self.node_in = node_in
        self.node_out = node_out
        self.gene_type = type(gene)


    def get_key(self):
        """Return key representation of innovation.

        Precondition:
            The in and out nodes have been assigned a valid innovation number.
        """
        assert self.node_in.innovation_number is not None
        assert self.node_out.innovation_number is not None
        return (self.node_in.innovation_number, self.node_out.innovation_number, self.gene_type)
