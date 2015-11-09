import random
import sys
import os
from parasite import Parasite
from organism import Organism

class World:
	""" The "environment" of the simulation. Contains all controls
	for managing mating, parasite generation etc.
	"""
	parasiteCount = 0
	organismCount = 0
	distrib = []
	for i in range(0, Organism.defLoci*Organism.defPars+1):
		distrib.append(0)
	def __init__(self, size, mhcAsrt = False):
		self.organisms = []
		self.mhc = mhcAsrt
		for i in range(0, size/2):
			self.organisms.append(Organism(0))
			self.organisms.append(Organism(1))
		self.orgsFile = open('organisms.txt', 'w')
		self.writeOrganisms("Year\tInit\tAfterDeath\tAfterBirth\tMHC\t")
		self.paraFile = open('parasites.txt', 'w')
		self.writeParasites("Year\tReproduce\tAlive")
		self.year = 0
	def mating(self, threshold = 0.4):
		tempOrgs = list(self.organisms)
		opOrgs = []
		mhcThreshhold = int(threshold * tempOrgs[0].loci*tempOrgs[0].species)
		while(len(tempOrgs) > 0):
			cur = tempOrgs[0]
			#eliminates juveniles from the breeding pool
			if not cur.canMate():
				opOrgs.append(cur)
				tempOrgs.remove(cur)
				continue
			output = None
			if cur.isMHC():
				highScore = 0
				#cycles through remaining organisms
				offset = 0
				for i in range(1, len(tempOrgs)):
					tempOrganism = tempOrgs[i-offset]
					#eliminates juveniles from the breeding pool
					if not tempOrganism.canMate():
						opOrgs.append(tempOrganism)
						tempOrgs.remove(tempOrganism)
						offset+=1
						continue
					#compares score to current high score and saves the highest organism; ends loop if it passes threshold.
					curScore = cur.mhcScore(tempOrganism)
					if output is None:
						output = tempOrganism
					if curScore > highScore:
						highScore = curScore
						output = tempOrganism
					if curScore >= mhcThreshhold:
						break
			else:
				#output is either novel or cur. If it is cur, then output.canMate() should be true, and would be handled later
				if len(tempOrgs) > 1:
					output = tempOrgs[random.randint(1, len(tempOrgs)-1)]
					while not output.canMate():
						opOrgs.append(output)
						tempOrgs.remove(output)
						if len(tempOrgs) > 0:
							output = None
							break
						else:
							output = tempOrgs[random.randint(1, len(tempOrgs)-1)]
			opOrgs.append(cur)
			tempOrgs.remove(cur)
			if output is not cur and output is not None:
				cur.setMate(output)
				output.setMate(cur)
				opOrgs.append(output)
				tempOrgs.remove(output)
		self.organisms = opOrgs[:]
		for i in range(0, int(len(opOrgs)*Organism.fertilityRate)):
			if len(opOrgs) == 0:
				break
			curOrganism = opOrgs[random.randint(0, len(opOrgs)-1)]
			quit = False
			while curOrganism.mate is None and len(opOrgs) > 0:
				opOrgs.remove(curOrganism)
				if len(opOrgs) == 0:
					quit = True
					break
				curOrganism = opOrgs[random.randint(0, len(opOrgs)-1)]
			if quit:
				break
			child = curOrganism.reproduce(curOrganism.mate)
			opOrgs.remove(curOrganism)
			self.organisms.append(child)
	def checkMates(self):
		for x in self.organisms:
			print x.details()
			print x.mhcScore(x.mate)
			print x.mate.details()
	def writeOrganisms(self, string, newLine = False):
		if newLine:
			string = "\n"+string

		self.orgsFile.write(string+"\t")
	def writeParasites(self, string, newLine = False):
		if newLine:
			string = "\n"+string

		self.paraFile.write(string+"\t")
	def countMHC(self):
		count = 0
		for organism in self.organisms:
			if organism.isMHC():
				count+=1
		return count
	def newYear(self, threshold = 0.4):
		self.writeOrganisms(str(self.year), True)
		self.writeParasites(str(self.year), True)
		print self.year,
		for organism in self.organisms:
			organism.newYear()

		parasiteCount = 0
		for organism in self.organisms:
			parasiteCount += organism.parasiteCount()
		self.writeParasites(str(parasiteCount))
		#print str(parasiteCount),
		#ranked parasite elimination, but with randomized selection of the often repeated ranks
		zeros = []
		ones = []
		twos = []
		threes = []
		order = self.organisms[:]
		for orgCt in range(0,len(order)):
			organism = order[orgCt]
			for count in range (1,len(organism.parasites)+1):
				species = organism.parasites[count-1]
				for psiteCt in range(0,len(species)):
					parasite = species[psiteCt]
					score = parasite.get_score(organism, count)
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
		deadSites = int(parasiteCount*Parasite.death_rate)
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
		#print str(parasiteCount),
		self.writeParasites(str(parasiteCount))
		order = []

		self.writeOrganisms(str(len(self.organisms)))
		#print str(len(self.organisms)),
		for organism in self.organisms:
			if len(order) == 0:
					order.append(organism)
			else:
				for x in range(0, len(order)):
					if order[x].parasiteScore() > organism.parasiteScore():
						order.insert(x, organism)
						break;
					elif x == len(order) - 1:
						order.append(organism)
		order = order[int(len(order)*Organism.death_rate):]
		self.organisms = order[:]
		print str(len(self.organisms)),
		self.writeOrganisms(str(len(self.organisms)))
		self.mating(threshold)
		print str(len(self.organisms)),; print str(self.countMHC())
		self.writeOrganisms(str(len(self.organisms)))
		self.writeOrganisms(str(self.countMHC()))

		self.year += 1

cx = World(250)
for j in range(3,7):
	threshold = j*0.1
	for k in range(0,5):
		if j == 4 and k == 0:
			continue
		for i in range(0,500):
			cx.newYear(threshold)
		os.rename("organisms.txt", "orgs0"+str(j)+"_"+"0"+str(k))
		os.rename("parasites.txt", "pars0"+str(j)+"_"+"0"+str(k))
