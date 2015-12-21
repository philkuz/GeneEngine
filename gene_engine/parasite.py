''' Parasite class
This module handles all of the logic of Parasite objects.

'''
import random


class Parasite:
    '''
    Parasite class that handles all of hte logic of parasite objects.
    get_fitness : returns the fitness score of the parasite according to an
        organism
    reproduce : returns a list of Parasites that are the children of the
        current Parasites
    print_details : prints out the specs of the current Parasite
    '''
    mutation_rate = 0.5
    death_rate = 1/1.1

    def __init__(self, k, n, genot=None):
        self.loci_length = k
        self.id = n
        self.dna = ""
        self.hostyear = 0
        self.score = -1
        genotemp = ""
        for i in range(k):
            genotemp += str(random.randint(0,1))
        self.dna = genot or genotemp

    def __repr__(self):
        return "Parasite({0})".format(self.dna)

    def get_fitness(self, organism, specie):
        '''
        Method that returns the fitness score of this parasite in reference to
            the host organisms gene sequence that codes resistance

        Args:
        organism (Organism) : organism object that is the host of this Parasite
        specie (integer) : the specie number within the organism. Used to
            determine which gene sequence to compare this parasite's genome to.

        Returns (integer) : fitness score of the parasite
        '''
        if organism.age == self.hostyear and self.score >= 0:
            return self.score
        else:
            org_sequence = organism.get_genome(specie)
            assert len(org_sequence) == self.loci_length, "Mismatched loci size"
            self.score = sum([1 for i in range(self.loci_length) if self.dna[i] == org_sequence[i]])
            return self.score

    def reproduce(self, score):
        '''
        Method that manages a single reproduction of a parasite to produce
            2^score offspring

        Args:
        score  (integer) : the fitness score of this parasite
        '''
        num_offspring = 2**score
        output = []
        for _ in range(num_offspring):
            new_genotype = ""
            for sequence in self.dna:
                if random.random() < self.mutation_rate:
                    new_genotype += str((int(sequence)+1) % 2)
                else:
                    new_genotype += sequence
            child = Parasite(self.loci_length, self.id, new_genotype)
            output.append(child)
        return output

    def print_details(self):
        print (self.dna)
        print( "Loci: " + str(self.loci_length))
        print ("ID: " + str(self.id))
