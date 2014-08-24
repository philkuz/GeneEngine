import random

class Parasite:
	mutationRate = 0.01
	deathRate = 1/1.1
	def __init__(self, k, n, genot = None):
		self.loci = k
  		self.iD = n
		self.score = 0
		self.genotype = ""
		self.hostyear = 0
		self.score = -1
		genotemp = ""
		for i in range(0,k):
			genotemp += str(random.randint(0,1))
		self.genotype = genot or genotemp
	def getscore(self, orgs, specie):
		if orgs.age == self.hostyear and self.score >= 0:
			return self.score
		else:
			genot = orgs.gene[specie]
			if len(genot) != self.loci:
				print "mismatched loci size"
			
			score = 0
			for i in range(0, self.loci):
				if self.genotype[i] == genot[i]:
					score +=1
			self.score = score
			return self.score
	def reproduce(self, score):
		#system produces 2^score offspring
		offspring = 2**score
		output = []
		for child in range(0,offspring):
			newGenotype = ""
			for loci in self.genotype:
				if random.random() < Parasite.mutationRate:
					newGenotype += str((int(loci)+1)%2)
				else:
					newGenotype += loci
			child = Parasite(self.loci, self.iD, newGenotype)
			output.append(child)
		return output
	def details(self):
		print self.genotype
		print "Loci: "+ str(self.loci)
		print "ID: "+ str(self.iD)
	def death(self):
		if random.random() < deathRate:
			return True
		else:
			return False

