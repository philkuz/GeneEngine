organism_parameters = {
    "loci": 3,
    "num_parasites": 6,
    "species": 6,
    "juvenile_period": 13.0,
    "mutation_rate": 0.01
}
organism_parameters["death_rate"] = 1.0 / \
    (organism_parameters['juvenile_period'] + 1)
organism_parameters["fertility_rate"] = organism_parameters['death_rate'] / \
    ((1-organism_parameters['death_rate']) **
        (organism_parameters['juvenile_period']+1))
