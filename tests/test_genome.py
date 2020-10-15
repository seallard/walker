from neat.link_gene import LinkGene


def test_insert_link_at_end(genome, tracker):
    new_link = LinkGene(from_node=None, to_node=None)
    new_link.id = 10
    genome.insert_link(new_link)

    assert genome.links[1] == new_link, "link inserted at end"
    assert genome.links[0].id < new_link.id, "link id is greater than previous id"


def test_insert_link_in_middle(genome, tracker):
    last_link = LinkGene(from_node=None, to_node=None)
    last_link.id = 10
    genome.insert_link(last_link)

    link = LinkGene(from_node=None, to_node=None)
    link.id = 5
    genome.insert_link(link)

    assert genome.links[1] == link, "link inserted in middle"
    assert genome.links[1].id > genome.links[0].id, "id greater than previous id"
    assert genome.links[1].id < genome.links[2].id, "id smaller than next id"
