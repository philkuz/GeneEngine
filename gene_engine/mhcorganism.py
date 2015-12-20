from organism import Organism
class MHCOrganism(Organism):

    def __init__(self, genotype, parasites, mhc):
        Organism.__init__(self, genotype, parasites, mhc)
        print(mhc)
    @property
    def mhc(self):
        return self.dna[0]
    @property.setter
    def mhc(self,x):
        assert len(str(x)) == 1, "mhc should only be 1 character"
        self.dna[0] = x
    def get_genome(self, index):
        return self.dna[index+1]
