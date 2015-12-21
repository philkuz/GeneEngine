from organism import Organism
class MhcOrganism(Organism):
    def __init__(self, genotype, parasites, mhc):
        Organism.__init__(self, genotype, parasites)
    @property
    def mhc(self):
        return self.dna[0]
    @mhc.setter
    def mhc(self,x):
        assert len(str(x)) == 1, "mhc should only be 1 character"
        self.dna[0] = x
    def is_mhc(self):
        '''
        Returns whether this organism chooses mates based on mhc or not
        '''
        return self.mhc == 1
    def get_genome(self, index):
        start = self.loci_length*index + 1
        return self.dna[start:start+self.loci_length]
