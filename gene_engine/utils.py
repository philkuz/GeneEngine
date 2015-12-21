organism_params = {
    "loci": 3,
    "num_parasites": 6,
    "species": 6,
    "juvenile_period": 13.0,
    "mutation_rate": 0.01
}
organism_params["death_rate"] = 1.0 / \
    (organism_params['juvenile_period'] + 1)
organism_params["fertility_rate"] = organism_params['death_rate'] / \
    ((1-organism_params['death_rate']) **
        (organism_params['juvenile_period']+1))
parasite_params = {
    "mutation_rate": 0.5,
    "death_rate": 1/1.1
}
def prob_std(p):
    return (p*(1-p))**.5
