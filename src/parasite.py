import random

class Parasite:
	'''
	Parasite class that handles all of hte logic of parasite objects.

	get_score : returns the fitness score of the parasite according to an organism

	reproduce : returns a list of Parasites that are the children of the current Parasites

	details : prints out the details of the current Parasite
	'''
	mutation_rate = 0.5
	death_rate = 1/1.1
	def __init__(self, k, n, genot = None):
		self.loci = k
  		self.id = n
		self.genotype = ""
		self.hostyear = 0
		self.score = -1
		genotemp = ""
		for i in range(0,k):
			genotemp += str(random.randint(0,1))
		self.genotype = genot or genotemp
	def get_score(self, organism, specie):
		'''
		Method that returns the fitness score of this parasite in reference to the
		Host organisms gene sequence that codes resistance

		Args:
		organism (Organism) : organism object that is the host of this Parasite
		specie (integer) : the specie number within the organism. Used to determine
			which gene sequence to compare this parasite's genome to.

		Returns (integer) : fitness score of the parasite
		'''
		if organism.age == self.hostyear and self.score >= 0:
			return self.score
		else:
			org_sequence = organism.gene[specie]
			assert len(genot) == self.loci, "mismatched loci size"
			score = 0
			# make this into a dot product
			for i in range(0, self.loci):
				if self.genotype[i] == org_sequence[i]:
					score +=1
			self.score = score
			return self.score
	def reproduce(self, score):
		'''
		Method that causes the parasite to produce 2^score offspring

		Args:
		score  (integer) : the fitness score of this parasite
		'''
		num_offspring = 2**score
		output = []
		for _ in range(num_offspring):
			new_genotype = ""
			for loci in self.genotype:
				if random.random() < self.mutation_rate:
					new_genotype += str((int(loci)+1)%2)
				else:
					new_genotype += loci
			child = Parasite(self.loci, self.id, new_genotype)
			output.append(child)
		return output
	def details(self):
		print self.genotype
		print "Loci: "+ str(self.loci)
		print "ID: "+ str(self.id)
	#outdated method: death now handled by World.py
	'''
	def death(self):
		if random.random() < death_rate:
			return True
		else:
			return False

'''
