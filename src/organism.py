import random
from parasite import Parasite
class Organism:
	defLoci = 3
	defPars = 6
	defSex = 1
	juvPeriod = 13.0
	deathRate = 1.0/ (juvPeriod+1)
	fertilityRate = deathRate / ((1-deathRate)**(juvPeriod+1))
	mutationRate = 0.01
	def __init__(self, mhc = None, genotype = None, parasites = None):
		self.parents = []
		self.parasites = []
		self.mate = None
		self.age = 0
		if mhc is None:
			mhc = random.randint(0,1)
		if genotype is None:
			self.new(mhc,Organism.defPars, Organism.defLoci)
		else:
			self.gene = genotype
		if parasites is None:
			for prCt in range(0,Organism.defPars):
				self.parasites.append([Parasite(Organism.defLoci, prCt)])
		else:
			self.parasites = parasites

	def new(self, mhc, n, k, genotype = None):
		self.loaded = True
		self.loci = k
		self.species = n
		self.age = 14
		if genotype is None:
			self.gene = [str(mhc)]

			for i in range(0,n):
				cur = ""
				for j in range(0,k):
					cur += str(random.randint(0,1))
				self.gene.append(cur)
		else:
			self.gene = genotype
	def isMHC(self):
		if self.gene[0] == str(1):
			return True
		else:
			return False
	def reproduce(self, par2 = None):
		parents = [self]
		loaded = True
		genotype = []
		par1G = self.gene
		parasites = []
		#check for 2 parents
		if par2 is not None:
			#sexual reproduction where recombination as well as mutation occur
			parents.append(par2)
			par2G = par2.gene
			for i in range(0,len(par1G)):
				cur1 = par1G[i]
				cur2 = par2G[i]
				op = ""
				for j in range(0,len(cur1)):
					par = random.randint(0,1)
					locus = ""
					if par == 0:
						locus=cur1[j]
					elif par == 1:
						locus=cur2[j]
					if random.random() < Organism.mutationRate:
						locus=str((int(locus)+1)%2)
					op+=locus
				genotype.append(op)
			prCt = 0
			for specie in self.parasites:
				#potential problems if self.parasites has a specie with 0 individuals
				if len(specie) > 0:
					parasites.append([specie[random.randint(0,len(specie)-1)]])
				else:
					parasites.append([Parasite(Organism.defLoci, prCt)])
				prCt += 1
		else:
			#asexual reproduction where only mutation is a factor
			for i in range(0,len(par1G)):
				cur = par1G[i]
				op=""
				for j in cur:
					locus = j
					if random.random() < Organism.mutationRate:
						locus=str((int(j)+1)%2)
					op+=locus
				genotype.append(op)
			#parasite handling done within the initializer
			parasites = None
		child = Organism(None,genotype, parasites)
		child.loaded = True
		child.parents = parents
		child.loci = self.loci
		child.species = self.species
		child.age = 0
		return child
	def details(self):
		#print "Loci: "+ str(self.loci)
		#print "Parasite Species: "+str(self.species)
		for x in range(0,len(self.parasites)):
			print str(x)+ "."
			for y in self.parasites[x]:
				print(y.genotype),
			print ""
		for i in range(0,len(self.parents)):
			print "Parent"+str(i)+": "+str(self.parents[i].gene)
		print "Genotype: "+ str(self.gene)
	#Score system to determine diversity
	def mhcScore(self, organism):
		score = 0
		for i in range(1, len(self.gene)):
			selfGene = self.gene[i]
			orgGene = organism.gene[i]
			for x in range(0,Organism.defLoci):
				if selfGene[x] != orgGene[x]:
					score += 1
		return score
	#parasite scores
	def parasiteScore(self):

		score = 0
		for specie in range(0,len(self.parasites)):
			for individual in self.parasites[specie]:
				score += individual.getscore(self, specie+1)
		return self.parasiteCount()*self.loci-score
	def getMate(self):
		return self.mate
	def setMate(self, organism):
		self.mate = organism
	def canMate(self):
		if self.age < 14:
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
				curChildren = individual.reproduce(individual.getscore(self, genomeLoc))
				for child in curChildren:
					survivingSpecie.append(child)
				survivingSpecie.append(individual)
			self.parasites[specie] = survivingSpecie
		#child handling
		if random.random() < Organism.fertilityRate and self.age > Organism.juvPeriod and self.mate is not None:
			self.reproduce(self.mate)
		self.age += 1
