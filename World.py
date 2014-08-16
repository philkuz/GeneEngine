import random
from Parasite import Parasite
class Organism:
	defLoci = 3
	defPars = 3
	defSex = 1
	def __init__(self, par1 = None, par2 = None):
		self.parents = []
		self.mutation = 0.01
		#check if it has any parents, otherwise considered novel)
		if par1 is not None:
			self.parents.append(par1)
			self.loaded = True
			self.loci = par1.loci
			self.parspecs = par1.parspecs
			self.gene = [par1.gene[0]]
			par1G = par1.gene
			#check for 2 parents
			if par2 is not None:
				if par1.gene[0] is not "1" or par2.gene[0]:
					print "Error in parentage, one parent is asexual, not sexual"
				self.parents.append(par2)
				par2G = par2.gene
				for i in range(1,len(par1G)):
					cur1 = par1G[i]
					cur2 = par2G[i]
					op = ""
					for j in range(0,par1.loci):
						par = random.randint(0,1)
						car = ""
						if par == 0:
							car=cur1[j]
						elif par == 1:
							car=cur2[j]
						if random.random() < self.mutation:
							car=str((int(car)+1)%2)
						op+=car
					self.gene.append(op)
			else:
				if par1.gene[0] is not "0":
					print "Error in parentage, parent 1 is sexual, not asexual"
				for i in range(1,len(par1G)):
					cur = par1G[i]
					op=""
					for j in cur:
						car = j 
						if random.random() < self.mutation:
							car=str((int(j)+1)%2)
						op+=car
					self.gene.append(op)
		else:
			self.new(Organism.defPars, Organism.defLoci, Organism.defSex)
	def new(self, n, k, sex):
		self.loaded = True
		self.loci = k
		self.parspecs = n
		self.gene = [str(sex)]
		for i in range(0,n):
			cur = ""
			for j in range(0,k):
				cur += str(random.randint(0,1))
			self.gene.append(cur)
	def details(self):
		#print "Loci: "+ str(self.loci)
		#print "Parasite Species: "+str(self.parspecs)
		print "Genotype: "+ str(self.gene)
		for i in range(0,len(self.parents)):
			print "Parent"+str(i)+": "+str(self.parents[i].gene)

cx = Organism()
cw = Organism()
cy = Organism(cx)
cz = Organism(cx,cy)
cv = Organism(cw,cx)
print "Org1"
cx.details()
print "Org2"
cy.details()
print "Org3"
cz.details()
print "CW"
cw.details()
print "CV"
cv.details()