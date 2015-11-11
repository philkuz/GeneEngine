import random
from parasite import Parasite
class Organism:
	'''
	Organism class that encompasess all of the Host arguments and methods
	'''
	loci = 3
	num_parasites = 6
	species = 6
	juvenile_period = 13.0
	death_rate = 1.0/ (juvenile_period+1)
	fertility_rate = death_rate / ((1-death_rate)**(juvenile_period+1))
	mutation_rate = 0.01
	def __init__(self, mhc = None, genotype = None, parasites = None):
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
		self.parasites = []
		self.mate = None
		self.age = 0
		if mhc is None:
			mhc = random.randint(0,1)
		if genotype is None:
			self.new(mhc)
		else:
			self.gene = genotype
		# Generate new parasites or use the existing ones.
		if parasites is None:
			for specie in range(self.species):
				self.parasites.append([Parasite(self.loci, specie)])
		else:
			self.parasites = parasites

	def new(self, mhc, genotype = None):
		'''
		Initializes "self" to an adult Organism

		Args:
		mhc (integer) : the binary flag of whether this organism selects mates
		randomly (0) or whether selecting by MHC sequence (1)

		genotype (list) : a list of species length that contains strings each with a length of
		loci
		'''
		self.loaded = True
		self.age = self.juvenile_period + 1
		if genotype is None:
			self.gene = [str(mhc)]

			for i in range(0,self.species):
				cur = ""
				for j in range(0,self.loci):
					cur += str(random.randint(0,1))
				self.gene.append(cur)
		else:
			self.gene = genotype
	def is_mhc(self):
		'''
		Abstraction that returns whether this Organism selects for MHC sequence or not
		'''
		if self.gene[0] == str(1):
			return True
		else:
			return False
	def reproduce(self, parent2 = None):
		'''
		Produces offspring based on gene sequence, an optional additional parent's
		gene sequence, and any mutation that may happen along the way

		Args:
		parent2 (Organism) : An optional Organism argument that marks the other
		parent. If this is left out, reproduction is considered asexual.
		'''
		parents = [self]
		loaded = True
		genotype = []
		genotype1 = self.gene
		parasites = []
		#check for 2 parents
		if parent2 is not None:
			#sexual reproduction where recombination as well as mutation occur
			parents.append(parent2)
			genotype2 = parent2.gene
			for i in range(len(genotype1)):
				sequence1 = genotype1[i]
				sequence2 = genotype2[i]
				op = ""
				for j in range(len(sequence1)):
					par = random.randint(0,1)
					locus = ""
					if par == 0:
						locus=sequence1[j]
					else:
						locus=sequence2[j]
					if random.random() < self.mutation_rate:
						locus=str((int(locus)+1)%2)
					op+=locus
				genotype.append(op)
			prCt = 0
			for specie in self.parasites:
				#potential problems if self.parasites has a specie with 0 individuals
				if len(specie) > 0:
					parasites.append([specie[random.randint(0,len(specie)-1)]])
				else:
					parasites.append([Parasite(self.loci, prCt)])
				prCt += 1
		else:
			#asexual reproduction where only mutation is a factor
			for i in range(0,len(genotype1)):
				cur = genotype1[i]
				op=""
				for j in cur:
					locus = j
					if random.random() < self.mutation_rate:
						locus=str((int(j)+1)%2)
					op+=locus
				child_genotype.append(op)
			#parasite handling done within the initializer
			parasites = None
		child = Organism(None, child_genotype, parasites)
		child.loaded = True
		child.parents = parents
		child.loci = self.loci
		child.species = self.species
		child.age = 0
		return child
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
		output = []
		for specie in self.parasites:
			specie_genotypes = []
			for individual in current_specie):
				specie_genotypes.append(str(individual))
			output.append(specie)
		return output
	def details(self):
		'''
		Prints the string representation of ht
		'''
		output = []
		for x in range(len(self.parasites)):
			cur_line = str(x)+ "."
			# for each parasite in the species array
			for y in self.parasites[x]:
				print(y.genotype),
			print ""
		for i in range(len(self.parents)):
			print "Parent"+str(i)+": "+str(self.parents[i].gene)
		print "Genotype: "+ str(self.gene)
	#Score system to determine diversity
	def mhcScore(self, organism):
		score = 0
		for i in range(1, len(self.gene)):
			selfGene = self.gene[i]
			orgGene = organism.gene[i]
			for x in range(0,self.loci):
				if selfGene[x] != orgGene[x]:
					score += 1
		return score
	#parasite scores
	def parasiteScore(self):

		score = 0
		for specie in range(0,len(self.parasites)):
			for individual in self.parasites[specie]:
				score += individual.get_score(self, specie+1)
		return self.parasiteCount()*self.loci - score
	def getMate(self):
		return self.mate
	def setMate(self, organism):
		self.mate = organism
	def canMate(self):
		if self.age <= self.juvenile_period:
			return False
		else:
			return True
	def parasiteCount(self):
		count = 0
		for specie in range(0, len(self.parasites)):
			count += len(self.parasites[specie])
		return count
	def removeParasite(self, parasite, species):
		self.parasites[species].remove(parasite)
	def newYear(self):
		#parasite reproduction handling
		for specie in range(0,len(self.parasites)):
			survivingSpecie = []
			genomeLoc = specie + 1
			for individual in self.parasites[specie]:
				curChildren = individual.reproduce(individual.get_score(self, genomeLoc))
				for child in curChildren:
					survivingSpecie.append(child)
				survivingSpecie.append(individual)
			self.parasites[specie] = survivingSpecie
		#child handling
		if random.random() < self.fertility_rate and self.age > self.juvenile_period and self.mate is not None:
			self.reproduce(self.mate)
		self.age += 1
