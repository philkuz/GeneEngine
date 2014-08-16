import random
from Parasite import Parasite
class Organism:
	death = 1.0/14.0
	juvenile = 13;
	fecund = death/((1-death)**(juvenile+1))
	iD = 0
	def __init__(self, sexual, n, k):
		self.sex = sexual
		self.alive = True
		self.age = 0
		self.parspec = n;
		self.loci = k;
		self.child = False
		self.gene=[]
		if sexual:
			self.gene.append("1")
		else:
			self.gene.append("0")
		for x in range(0, n):
			op = ""
			for y in range(0, k):
				op+=str(random.randint(0,1))
			self.gene.append(op)
		print self.gene
		random.randint(0,1)
		self.ID = Organism.iD
		Organism.iD += 1
	def advance(self):
		chance = random.random()
		if self.age > Organism.juvenile:
			chance = random.random()
			if chance < Organism.fecund:
				self.reproduce()
		self.age+=1

	def reproduce(self):
		self.child = True
		#print str(self.ID)+". Birth";
class Simulation:
	#n | parspecs = parasite species, k | loci = loci per species
	def __init__(self, n, k):
		self.parspecs = n;
		self.loci = k;

