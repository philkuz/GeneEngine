import random
import os
from parasite import Parasite
from organism import Organism

class Petri:
    def __init__(self, population):
        self.parasite_count = 0
        self.organism_count = 0
        self.year = 0
    def matchmaker(self):
        '''
        Traverses the population of organisms and returns
        a list 1 member from each mating pair
        '''

        unmated = self.organisms[:]
        mated = []
        while len(unmated) > 0:
            candidate = unmated.pop(0)
            if not cur.can_mate():
                continue
            shuffled_orgs = random.sample(unmated,len(unmated))
            org = shuffled_orgs.pop(0)
            while True:
                if org.can_mate():
                    if candidate.will_mate(org):
                        candidate.mate = org
                        unmated.remove(org)
                        mated.append(candidate)
                        break
                else:
                    unmated.remove(org)
                org = shuffled_orgs.pop(0)
        return mated
    def incubator(self, mated):
        '''
        Takes in a list of 1 member from each mating pair and then
        reproduces based on fertility_rate
        '''
        reproducing_mates = random.sample(mated, len(mated)*self.fertility_rate)
        for mate in reproducing_mates:
            child = mate.reproduce()
            if child:
                self.organisms.append(child)
    def reaper(self):
        '''
        Handles death in the populations
        '''
        self.organisms[:] = [organism for organism in self.organisms if not organism.will_die()]
    def cycle(self):
        mates = self.matchmaker()
        self.incubator(mates)
        self.reaper()
        for organism in self.organisms:
            organism.next_cycle()
        self.year+=1


    def mating(self, threshold=0.4):
                    curScore = cur.mhcScore(tempOrganism)
                    if output is None:
                        output = tempOrganism
                    if curScore > highScore:
                        highScore = curScore
                        output = tempOrganism
                    if curScore >= mhcThreshhold:
                        break
        self.organisms = opOrgs[:]



    def writeOrganisms(self, string, newLine=False):
        if newLine:
            string = "\n"+string

        self.orgsFile.write(string+"\t")

    def writeParasites(self, string, newLine=False):
        if newLine:
            string = "\n"+string

        self.paraFile.write(string+"\t")

    def new_year(self, threshold=0.4):
        self.writeOrganisms(str(self.year), True)
        self.writeParasites(str(self.year), True)
        print self.year,
        for organism in self.organisms:
            organism.new_year()

        parasiteCount = 0
        for organism in self.organisms:
            parasiteCount += organism.parasiteCount()
        self.writeParasites(str(parasiteCount))
        # ranked parasite elimination, but with randomized selection of the
        # often repeated ranks
        zeros = []
        ones = []
        twos = []
        threes = []
        order = self.organisms[:]
        for orgCt in range(len(order)):
            organism = order[orgCt]
            for count in range(1, len(organism.parasites)+1):
                species = organism.parasites[count-1]
                for psiteCt in range(len(species)):
                    parasite = species[psiteCt]
                    score = parasite.get_fitness(organism, count)
                    if score == 0:
                        zeros.append([parasite, count, orgCt])
                    elif score == 1:
                        ones.append([parasite, count, orgCt])
                    elif score == 2:
                        twos.append([parasite, count, orgCt])
                    elif score == 3:
                        threes.append([parasite, count, orgCt])
                count += 1
        nums = [zeros, ones, twos, threes]
        deadSites = int(parasiteCount*Parasite.death_rate)
        while(deadSites > 0):
            numsIdx = 0
            while(len(nums[numsIdx]) == 0):
                numsIdx += 1
                if numsIdx > 3:
                    print "greater than threes"
            # IE zeros
            curList = nums[numsIdx]
            # returns the parasite currently working with
            curParasite = curList.pop(random.randint(len(curList)-1))
            organism = order[curParasite[2]]
            species = organism.parasites[curParasite[1]-1]
            for parasite in species:
                if parasite.genotype == curParasite[0].genotype:
                    species.remove(parasite)
                    deadSites -= 1
                    break
            else:
                print "fail"

        parasiteCount = 0
        for organism in order:
            parasiteCount += organism.parasiteCount()
        self.writeParasites(str(parasiteCount))
        order = []

        self.writeOrganisms(str(len(self.organisms)))
        # print str(len(self.organisms)),
        for organism in self.organisms:
            if len(order) == 0:
                    order.append(organism)
            else:
                for x in range(0, len(order)):
                    if order[x].fitness() > organism.fitness():
                        order.insert(x, organism)
                        break
                    elif x == len(order) - 1:
                        order.append(organism)
        order = order[int(len(order)*Organism.death_rate):]
        self.organisms = order[:]
        print str(len(self.organisms)),
        self.writeOrganisms(str(len(self.organisms)))
        self.mating(threshold)
        print (len(self.organisms), self.countMHC())
        self.writeOrganisms(str(len(self.organisms)))
        self.writeOrganisms(str(self.countMHC()))

        self.year += 1
if __name__ == "__main__":
    cx = World(250)
    for j in range(3, 7):
        threshold = j*0.1
        for k in range(0, 5):
            if j == 4 and k == 0:
                continue
            for i in range(500):
                cx.new_year(threshold)
            os.rename("organisms.txt", "orgs0"+str(j)+"_"+"0"+str(k))
            os.rename("parasites.txt", "pars0"+str(j)+"_"+"0"+str(k))
