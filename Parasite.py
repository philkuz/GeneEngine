import random

class Parasite:
	def __init__(self, k, n, genot):
		self.loci = k
  		self.iD = n
		self.score = 0
		self.genotype = ""
		genotemp = ""
		for i in range(0,k):
			genotemp += str(random.randint(0,1))
		self.genotype = genot or genotemp
	def getscore(self, genot):
		if len(genot) != self.loci:
			print "mismatched loci size"
		
		score = 0
		for i in range(0, self.loci):
			if self.genotype[i] == genot[i]:
				score +=1
		self.score = score
		print self.score