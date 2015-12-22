import random
from parasite import Parasite
from utils import *

class Organism:
    '''
    Organism class that encompasess all of the Host arguments and methods
    '''
    loci_length = organism_params['loci_length']
    num_parasites = organism_params['num_parasites']
    num_species = organism_params['num_species']
    juvenile_period = organism_params['juvenile_period']
    death_rate = organism_params['death_rate']
    fertility_rate = organism_params['fertility_rate']
    mutation_rate = organism_params['mutation_rate']
    mate_threshold = organism_params['mate_threshold']


    def __init__(self, genotype = None, parasites = None):
        '''
        Args:
        mhc (integer) : binary flag that is 0 if the Organism selects mates randomly and 1 if
        the organism selects mates based on their genomic sequence (simulated MHC)

        genotype (list) : a list of species length that contains strings each with a length of
        loci

        parasites (list) : a list of the parasites that use this organism as a host. If None, then
        new parasites are generated

        Instance Variables:

        parents (list)
        parasites (list)
        mate (Organism)
        age (integer)
        gene (list)
        '''
        self.parents = []
        self.parasites = parasites
        self._mate = None
        self.age = 0
        self.alive = True
        self.dna = genotype
        self.fitscores = {}
        if self.dna is None:
            self.new_adult()

        # Generate new parasites or use the existing ones.
        if self.parasites is None:
            self.parasites = [[Parasite(self.loci_length, i)] for i in range(self.num_species)]

    def new_adult(self, genotype = None):
        '''
        Initializes "self" to an adult Organism

        Args:
        mhc (integer) : the binary flag of whether this organism selects mates
        randomly (0) or whether selecting by MHC sequence (1)

        genotype (list) : a list of species length that contains strings each with a length of
        loci
        '''
        self.age = self.juvenile_period + 1
        if genotype:
            self.dna = genotype
        else:
            self.dna = [random.randint(0,1) for _ in range(self.loci_length*self.num_species)]

    def mutate(self, value):
        if random.random() < self.mutation_rate:
            return (value + 1) % 2
        else:
            return value
    def asexual_inherit(self):
        assert len(self.parents) == 1, "Asexual reproduction is arbitrary with {0} parents".format(len(self.parents))
        self.dna = []
        for x in self.parents[0].dna:
            x = self.mutate(base)
            self.dna.append(x)
    def sexual_inherit(self):
        assert len(self.parents) == 2, "Can't perform sexual reproduction if there aren't two parents"
        seq0 = self.parents[0].dna
        seq1 = self.parents[1].dna
        assert len(seq0) == len(seq1), "Parent genome lengths are mismatched"
        self.dna = []
        for i in range(len(seq0)):
            base = seq0[i] if random.randint(0,1) else seq1[i]
            base = self.mutate(base)
            self.dna.append(base)
    def inherit_parasites(self):
        self.parasites = []
        if len(self.parents) == 1:
            for i, specie in enumerate(self.parents[0].parasites):
                #potential problems if self.parasites has a specie with 0 individuals
                if len(specie) > 0:
                    self.parasites.append([specie[random.randint(len(specie)-1)]])
                else:
                    self.parasites.append([Parasite(self.loci, i)])
        elif len(self.parents) == 2:
            pars0 = self.parents[0].parasites
            pars1 = self.parents[1].parasites
            pos = 0
            for specie0, specie1 in zip(pars0,pars1):
                specie = random.sample(specie0, random.randint(0,len(specie0)//2))
                specie += random.sample(specie1, random.randint(0,len(specie1)//2))
                if not specie:
                    self.parasites.append(specie)
                else:
                    self.parasites.append([Parasite(self.loci, pos)])

                pos += 1


    def inherit(self):

        # if len(parents) == 1:
        self.dna = []
        if len(self.parents) == 1:
            asexual_inherit()
        elif len(self.parents) == 2:
            sexual_inherit()
        inherit_parasites()
    def will_birth(self):
        # sd = prob_std(self.fertility_rate)
        # return random.random() <random.gauss(self.fertility_rate,sd)
        return random.random() < self.fertility_rate
    def reproduce(self, parent2 = None):
        '''
        Produces offspring based on gene sequence, an optional additional parent's
        gene sequence, and any mutation that may happen along the way

        Args:
        parent2 (Organism) : An optional Organism argument that marks the other
        parent. If this is left out, reproduction is considered asexual.
        '''
        if self.try_children():
            parents = [self]
            if parent2:
                parents.append(parent2)
            elif self.mate:
                parents.append(self.mate)
            child = self.__class__()
            child.parents = parents
            return child
        else:
            return False
    def __repr__(self):
        '''
        The string representation of this organism
        '''
        return self.parasite_genotypes()
    def parasite_genotypes(self):
        '''
        Returns the genotype info of each parasite organized by specie

        Returns (list) of lists that contain the parasite info in each
        '''
        return [[str(parasite) for parasite in specie]
            for specie in self.parasites]
    def print_details(self):
        '''
        Prints the string representation of this
        '''
        output = []
        for x in range(len(self.parasites)):
            cur_line = str(x)+ "."
            # for each parasite in the species array
            for y in self.parasites[x]:
                print(y.genotype)
            print("")
        for i in range(len(self.parents)):
            print( "Parent"+str(i)+": "+str(self.parents[i].gene))
        print("Genotype: "+ str(self.dna))
    #Score system to determine partner diversity
    def diversity_score(self, partner):
        score = 0
        for i in range(self.num_species):
            host_seq = self.get_genome(i)
            partner_seq = partner.get_genome(i)
            score += sum([1 for x in range(self.loci_length) if host_seq[x] != partner_seq[x]])
        return score
    def fitness(self):
        '''
        Calculates percent fitness based on parasite fitness
        '''
        if self.age in self.fitscores:
            return self.fitscores[self.age]
        else:
            score = 0
            for specie in self.parasites:
                score += sum([parasite.fitness() for parasite in specie])
            score = 1 - score / self.parasite_count()
            self.fitscores[self.age] = score
            return score
    @property
    def mate(self):
        if self._mate:
            return self._mate
        else:
            return False
    @mate.setter
    def mate(self, partner):
        self._mate = partner
        partner._mate = self
    def can_mate(self):
        return self.age > self.juvenile_period and self.mate
    def will_mate(self, candidate):
        # return candidate.fitness() > self.mate_threshold
        return True # default organism doesn't care
    def parasite_count(self):
        lens  = [len(specie) for specie in self.parasites]
        return sum(lens)
    def kill_parasite(self, parasite, species = None):
        if not species:
            for specie in self.parasites:
                if parasite in specie:
                    specie.remove(parasite)
                    break
        else:
            self.parasites[species].remove(parasite)
    def get_genome(self, index):
        first = index*self.loci_length
        return genome[first:first+self.loci_length]
    def parasite_increment(self):
        for i,specie in enumerate(self.parasites):
            host_genome = get_genome(i)
            for parasite in specie:
                children = parasite.reproduce(host_genome)
                specie.extend(children)
    def try_children(self):
        if random.random() < self.fertility_rate and self.can_mate:
            self.reproduce()
    def death_chance(self):
        m = 2 * (1 - self.death_rate)
        b = 1 / m
        return (1 - self.fitness())* m + b
    def will_die(self):
        '''
        Should only be called when the organism is removed from the population
        AKA true death
        '''
        self.alive = random.random() < self.death_chance()
        return self.alive
    def immunesystem(self):
        '''
        Handles parasite death
        '''
        for specie in self.parasites:
            specie[:] = [parasite for parasite in specie if not parasite.will_die()]

    def next_cycle(self):
        self.immunesystem()
        self.parasite_increment()
        # self.try_children()
        self.age += 1
        # #parasite reproduction handling
        # for specie in range(0,len(self.parasites)):
        #     survivingSpecie = []
        #     genomeLoc = specie + 1
        #     for individual in self.parasites[specie]:
        #         curChildren = individual.reproduce(individual.get_fitness(self, genomeLoc))
        #         for child in curChildren:
        #             survivingSpecie.append(child)
        #         survivingSpecie.append(individual)
        #     self.parasites[specie] = survivingSpecie
        # #child handling
        # if random.random() < self.fertility_rate and self.age > self.juvenile_period and self._mate is not None:
        #     self.reproduce(self._mate)
"""def reproduce(self, parent2 = None):
    parents = [self]
    child_genotype = []
    genotype1 = self.dna
    parasites = []
    #check for 2 parents
    if parent2 is not None:
        #sexual reproduction where recombination as well as mutation occur
        parents.append(parent2)
        genotype2 = parent2.dna
        for i in range(len(genotype1)):
            sequence1 = genotype1[i]
            sequence2 = genotype2[i]
            op = ""
            for j in range(len(sequence1)):
                par = random.randint(0,1)
                locus = int(sequence2[j] if par else sequence1[j])
                if random.random() < self.mutation_rate:
                    locus = (locus + 1) % 2
                op += str(locus)
            child_genotype.append(op)
        for i, specie in enumerate(self.parasites):
            #potential problems if self.parasites has a specie with 0 individuals
            if len(specie) > 0:
                parasites.append([specie[random.randint(len(specie)-1)]])
            else:
                parasites.append([Parasite(self.loci, i)])
    else:
        #asexual reproduction where only mutation is a factor
        for i in range(0,len(genotype1)):
            cur = genotype1[i]
            op=""
            for j in cur:
                locus = int(j)
                if random.random() < self.mutation_rate:
                    locus=(j+1)%2
                op+=str(locus)
            child_genotype.append(op)
        #parasite handling done within the initializer
        parasites = None
    child = Organism(None, child_genotype, parasites)
    child.parents = parents
    child.loci_length = self.loci_length
    child.num_species = self.num_species
    child.age = 0
    return child"""
