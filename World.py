import random
import sys
from Parasite import Parasite
from Organism import Organism
class World:
	parasiteCount = 0
	organismCount = 0
	distrib = []
	for i in range(0,Organism.defLoci*Organism.defPars+1):
		distrib.append(0) 
	def __init__(self, size, mhcAsrt = None):
		self.organisms = []
		self.mhc = mhcAsrt or False
		for i in range(0, size):
			self.organisms.append(Organism())
	#depreciated reproduction models
	'''
	def urmate_MHC(self):
		tempOrgs = list(self.organisms)
		opOrgs = []
		while(len(tempOrgs) > 0):
			cur = tempOrgs[0]
			highScore = 0
			output = None
			for i in range(1, len(tempOrgs)):
				curScore = cur.mhcScore(tempOrgs[i])
				if curScore > highScore:
					highScore = curScore
					output = tempOrgs[i]
			if output is None:
				output = tempOrgs[len(tempOrgs)-1]
			World.distrib[highScore]+=1
			cur.setMate(output)
			output.setMate(cur)
			opOrgs.append(cur)
			opOrgs.append(output)
			tempOrgs.remove(cur)
			tempOrgs.remove(output)
		self.organisms = list(opOrgs)
	def mate_MHC(self):
		tempOrgs = list(self.organisms)
		opOrgs = []
		threshold = 6
		while(len(tempOrgs) > 0):
			cur = tempOrgs[0]
			highScore = 0
			output = None
			for i in range(1, len(tempOrgs)):
				curScore = cur.mhcScore(tempOrgs[i])
				if curScore > highScore:
					highScore = curScore
					output = tempOrgs[i]
				if curScore >= threshold:
					break
			if output is None:
				output = tempOrgs[len(tempOrgs)-1]
			World.distrib[highScore]+=1
			cur.setMate(output)
			output.setMate(cur)
			opOrgs.append(cur)
			opOrgs.append(output)
			tempOrgs.remove(cur)
			tempOrgs.remove(output)
	'''
	def mating(self):
		tempOrgs = random.shuffle(self.organisms)
		opOrgs = []
		mhcThreshhold = int(.7 * tempOrgs[0].loci*tempOrgs[0].species)
		while(len(tempOrgs) > 0):
			cur = tempOrgs[0]
			output = None
			if cur.isMHC():
				highScore = 0
				for i in range(1, len(tempOrgs)):
					curScore = cur.mhcScore(tempOrgs[i])
					if curScore > highScore:
						highScore = curScore
						output = tempOrgs[i]
					if curScore >= mhcThreshold:
						break
				else:
					output = tempOrgs[len(tempOrgs)-1]
			else:
				output = tempOrgs[random.randint(0,len(tempOrgs)-1)]
			cur.setMate(output)
			output.setMate(cur)
			opOrgs.append(cur)
			opOrgs.append(output)
			tempOrgs.remove(cur)
			tempOrgs.remove(output)
		self.organisms = list(tempOrgs)
	'''
	def checkMates(self):
		for x in self.organisms:
			print x.details()
			print x.mhcScore(x.mate)
			print x.mate.details()
	def newYear(self):
		order = []
		for organism in self.organisms:
			organism.newYear()
			if len(order) == 0:
				order.append(organism)
			else:
				for x in range(0, len(order)):
					if order[x].parasiteScore() > organism.parasiteScore():
						order.insert(x, organism)
						break;
					elif x == len(order) - 1:
						order.append(organism)
		order = order[int(len(order)*Organism.deathRate):]

		parasiteCount = 0
		for organism in order:
			parasiteCount += organism.parasiteCount()
		print parasiteCount,; print ", ",
		#random parasite elimination: ignored because it selects out the ideal forms of genes too quickly
		'''
		for i in range(0,int(parasiteCount*Parasite.deathRate)):
			organismsLeft = range(0,len(order))
			index = random.randint(0,len(organismsLeft)-1)
			organism = order[organismsLeft[index]]
			organismsLeft.pop(index)
			tempIndex = random.randint(0,organism.species-1)
			count = 0 
			speciesLeft = range(0,organism.species)
			while len(organism.parasites[tempIndex]) == 0:
				if len(speciesLeft) == 0:
					index = random.randint(0,len(organismsLeft)-1)
					organism = order[organismsLeft[index]]
					organismsLeft.pop(index)
					speciesLeft = range(0, organism.species)
					continue
				tempIndex = speciesLeft[random.randint(0,len(speciesLeft)-1)]
				speciesLeft.remove(tempIndex)
				
			specie = organism.parasites[tempIndex]
			specie.remove(specie[random.randint(0,len(specie)-1)])
		parasiteCount = 0
		for organism in order:
			parasiteCount += organism.parasiteCount()
		print parasiteCount
		'''
		zeros = []
		ones = []
		twos = [] 
		threes = []
		for orgCt in range(0,len(order)):
			organism = order[orgCt]
			for count in range (1,len(organism.parasites)+1):
				species = organism.parasites[count-1]
				for psiteCt in range(0,len(species)):
					parasite = species[psiteCt]
					score = parasite.getscore(organism, count)
					if score == 0:
						zeros.append([parasite, count, orgCt])
					elif score == 1:
						ones.append([parasite, count, orgCt])
					elif score == 2:
						twos.append([parasite, count, orgCt])
					elif score == 3:
						threes.append([parasite, count, orgCt])
				count+=1
		nums = [zeros, ones, twos, threes]
		deadSites = int(parasiteCount*Parasite.deathRate)
		while(deadSites > 0):
			numsIdx = 0
			while(len(nums[numsIdx])==0):
				numsIdx+=1
				if numsIdx > 3:
					print "greater than threes"
			#IE zeros
			curList = nums[numsIdx]
			#returns the parasite currently working with
			curParasite = curList.pop(random.randint(0,len(curList)-1))
			organism = order[curParasite[2]]
			species = organism.parasites[curParasite[1]-1]
			for parasite in species:
				if parasite.genotype == curParasite[0].genotype:
					species.remove(parasite)
					deadSites-=1
					break;
			else:
				print "fail"
			
		parasiteCount = 0
		for organism in order:
			parasiteCount += organism.parasiteCount()
		print parasiteCount
cx = World(250)
for i in range(0,30):
	cx.newYear()
