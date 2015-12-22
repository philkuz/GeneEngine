''' Parasite class
This module handles all of the logic of Parasite objects.

'''
from utils import *
import random


class Parasite:
    '''
    Parasite class that handles all of hte logic of parasite objects.
    fitness : returns the fitness score of the parasite according to an
        organism
    reproduce : returns a list of Parasites that are the children of the
        current Parasites
    print_details : prints out the specs of the current Parasite
    '''
    mutation_rate = parasite_params['mutation_rate']
    death_rate = parasite_params['death_rate']
    def __init__(self, host, specie, dna = None):
        self.host = host
        self.loci_length = host.loci_length
        self.specie = specie
        if dna:
            self.dna = dna
        else:
            self.dna = self.new_genome()
        self.alive = True
        self.age = 0
        self.scores = {}
    def new_genome(self):
        return [random.randint(0,1) for _ in range(self.loci_length)]

    def __repr__(self):
        return "Parasite({0})".format("".join([str(a) for a in self.dna])
    @property
    def score(self):
        return self.scores(self.age)
    @score.setter
    def score(self, new_score):
        self.scores[self.age] = new_score
    def fitness(self):
        '''
        Method that returns the fitness score of this parasite in reference to
            the host organisms gene sequence that codes resistance

        Args:
        organism (Organism) : organism object that is the host of this Parasite
        specie (integer) : the specie number within the organism. Used to
            determine which gene sequence to compare this parasite's genome to.

        Returns (integer) : fitness score of the parasite
        '''
        if self.age in self.scores:
            return self.score
        else:
            host_seq = self.host.get_genome(self.specie)
            assert len(host_seq) == self.loci_length, "Mismatched loci size"
            self.score = sum([1 for i in range(self.loci_length) if self.dna[i] == host_seq[i]])/self.loci_length
            return self.score

    def mutate(self,base):
        '''
        Returns the base or the mutated base depending on the probabiltiy of
        mutation
        '''
        if random.random() < self.mutation_rate:
            return (base + 1) % 2
        else:
            return base
    def reproduce(self):
        '''
        Method that manages a single reproduction of a parasite to produce
            2^score offspring

        Args:
        score  (integer) : the fitness score of this parasite
        '''

        num_offspring = 2**self.fitness()
        children = []
        for _ in range(num_offspring):
            new_genotype = [mutate(base) for base in self.dna]
            child = Parasite(self.host, self.specie, new_genotype)
            children.append(child)
        return children
    def death_chance(self):
        m = 2 * (1 - self.death_rate)
        b = 1 / m
        return (1 - self.fitness())* m + b
    def will_die(self):
        '''
        Should only be called when parasite will be killed
        '''
        self.alive = random.random() < self.death_chance()
        return self.alive
    def print_details(self):
        print (self.dna)
        print( "Loci: " + str(self.loci_length))
