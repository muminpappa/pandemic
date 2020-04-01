from pandemic import individual

vulnerable_fraction = 0.1


def test_infection():
    ind = individual(0.5)
    ind.infect()
    assert ind.infected == 1
