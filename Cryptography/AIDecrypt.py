import base64
import string
import random
import sys


def ProgressBar(curr, total, size):
    # Calculate the percentage
    if total == 0:
        raise ZeroDivisionError("Total must be greater than 0")
    percent = (curr / total) * 100

    # Calculate the number of '#' to display in the progress bar
    num_blocks = int(size * (percent / 100))
    # Create the progress bar string
    progress_bar = '[' + '#' * num_blocks + '-' * (size - num_blocks) + ']'
    # Display the progress bar and percentage
    sys.stdout.write(f"\r{progress_bar}\t{round(percent, 1)}%")
    sys.stdout.flush()

class XORCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, text):
        encrypted_text = ""  #bytearray()
        for i in range(len(text)):
            #print(chr(text[i]))
            encrypted_text += chr(ord(chr(text[i])) ^ ord(self.key[i % len(self.key)]))
        return encrypted_text

    def decrypt(self, encrypted_text):
        decrypted_text = "" #bytearray
        for i in range(len(encrypted_text)):
            decrypted_text += chr(ord(encrypted_text[i]) ^ ord(self.key[i % len(self.key)]))
        return decrypted_text

class Genome:
    score = 10000
    alphabet = string.ascii_letters + string.digits + "-_"
    def __init__(self, key=None):
        if key:
            self.key = key
        else:
            self.key = ''.join(random.choices(self.alphabet, k=32))

    def mutate(self, type=None):
        

        key_length = len(self.key)
        start_index = random.randint(0, key_length - 4)  # Ensure a range of at least length 4
        end_index = start_index + 3
        if type is not None and type == 1:
            rand = ''.join(random.choices(self.alphabet, k=4))
            mutated_key = self.key[:start_index] + rand + self.key[end_index+1:]
        # Scramble the characters between start and end indexes
        elif type is not None and type == 2:
            mutated_key = self.key[:start_index] + "".join(random.sample(self.alphabet, 1)) + self.key[start_index+1:]
        else: 
            chars_to_scramble = list(self.key[start_index:end_index+1])
            random.shuffle(chars_to_scramble)
            scramble = ''.join(chars_to_scramble)
            mutated_key = self.key[:start_index] + scramble + self.key[end_index+1:]

        self.key = mutated_key

    def crossover(self, other_genome):
        key_length = len(self.key)
        # Generate a crossover mask with up to 1/4 of the key length being 1's
        mask_length = random.randint(1, key_length // 4)
        mask_indexes = random.sample(range(key_length), mask_length)
        mask = ['1' if i in mask_indexes else '0' for i in range(key_length)]
        mask = ''.join(mask)
        # Apply crossover using the mask
        child1_key = ''.join([self.key[i] if mask[i] == '0' else other_genome.key[i] for i in range(key_length)])
        child2_key = ''.join([other_genome.key[i] if mask[i] == '0' else self.key[i] for i in range(key_length)])
        return Genome(child1_key), Genome(child2_key)

    def getFitness(self, evaluator):
        #print("Getting Fitness...")
        self.score = evaluator.evaluate(self.key)
    
    
class Evaluator:
    """
    expfreq = {
        "a" : 0.085,
        "b" : 0.016,
        "c" : 0.0316,
        "d" : 0.0387,
        "e" : 0.121,
        "f" : 0.0218,
        "g" : 0.0209,
        "h" : 0.0496,
        "i" : 0.0733,
        "j" : 0.0022,
        "k" : 0.0081,
        "l" : 0.0421,
        "m" : 0.0253,
        "n" : 0.0717,
        "o" : 0.0747,
        "p" : 0.0207,
        "q" : 0.001,
        "r" : 0.0633,
        "s" : 0.0673,
        "t" : 0.0894,
        "u" : 0.0268,
        "v" : 0.0106,
        "w" : 0.0183,
        "x" : 0.0019,
        "y" : 0.0172,
        "z" : 0.0011
    }
    """
    expfreq = {
        " " : 0.1662397373587528,
        "'" : 0.001809165560335683,
        "(" : 0.0003238341968911917,
        ")" : 0.0003238341968911917,
        "," : 0.01655925232446724,
        "." : 0.007895552061022744,
        "0" : 0.0005434782608695652,
        "1" : 0.0018388150484343322,
        "2" : 0.0005955733273259743,
        "3" : 0.0003238341968911917,
        "5" : 0.0008673124577607569,
        "6" : 0.0002717391304347826,
        "7" : 0.0014628857850867312,
        "8" : 0.0003238341968911917,
        "9" : 0.0003238341968911917,
        "a" : 0.06872463302045699,
        "b" : 0.011936018394410523,
        "c" : 0.020094276447451414,
        "d" : 0.034317955848006024,
        "e" : 0.09744060606573673,
        "f" : 0.020816176328249246,
        "g" : 0.014405174409104925,
        "h" : 0.047566112415167824,
        "i" : 0.05609650662868808,
        "j" : 0.0005955733273259743,
        "k" : 0.0044522112427791555,
        "l" : 0.030343448574155288,
        "m" : 0.019206901721723707,
        "n" : 0.06493636959187285,
        "o" : 0.060570157814970424,
        "p" : 0.011264856415160701,
        "q" : 0.0005955733273259743,
        "r" : 0.04768998502554188,
        "s" : 0.04360905695904223,
        "t" : 0.06296582119196033,
        "u" : 0.01967606647763011,
        "v" : 0.010309057301557427,
        "w" : 0.017331418043045735,
        "y" : 0.013880668036837523,
        "z" : 0.0005434782608695652,
        "\"" : 0.0020263941969820573,
        "-" : 0.0002717391304347826
}
    
    common_words = ["the", "to", "for", "be", "and", "in", 
                    "that", "of", "it", "have", "as", "do", 
                    "on", "with", "not", "this", "but", "by", 
                    "from", "they", "at", "all", "so", "get"]
    
    def __init__(self, encrypted_text):
        self.enc_text = encrypted_text

    def evaluate(self, key):
        score = 0
        cipher = XORCipher(key)
        plain_text = cipher.decrypt(self.enc_text)
        #print(plain_text)
        for c in self.expfreq.keys():
            score += abs((plain_text.count(c) / len(plain_text)) - self.expfreq[c])

        for w in self.common_words:
            if w in plain_text:
                score -= 0.005

        score += sum(1 for char in plain_text if ord(char) >= 128)*0.001

        if score < 0:
            score = 0
        return score
        

def GeneticAlgorithm(encrypted_text, numGens, popsize, crossover_rate, mutation_rate, kval, out_file=None):
    currPop = []
    bestKey = None
    eval = Evaluator(encrypted_text)
    
    print("Creating Initial Population...")
        #initial Pop and sort
    for i in range(popsize):
        ProgressBar(i, popsize-1, 50)
        g = Genome() #random key
        currPop.append(g)

        #get scores for currPop
        for g in currPop:
            g.getFitness(eval)
    
        #sort the current population based on score
    currPop = sorted(currPop, key=lambda x: x.score)
    if out_file is not None:
        out_file.write(f"Gen 0  : {currPop[0].key}\t{currPop[0].score}\n")
    
    print("\nRunning Key Search...")
    for i in range(numGens):
        selectedParents = []
        nextPop = []
        ProgressBar(i, numGens-1, 50)

        #check for nones
        #for g in range(len(currPop)):
        #    if currPop[g] == None:
        #        print(f"currPop[{g}] is Null")
                #break 

            #move top 3 into selectedParents
        for j in range(2):
            selectedParents.append(currPop[j])

            #fill rest of selectedParents using tournament selection
        while len(selectedParents) < popsize:
            kGroup = random.sample(currPop, kval) 
            for k in kGroup:
                if k is None:
                    kGroup.remove(k)
            selectedParents.append(min(kGroup, key=lambda x: x.score))

        while len(nextPop) < popsize:
            parents = random.sample(selectedParents, 2)
                
            if random.random() <= crossover_rate:
                children = parents[0].crossover(parents[1])
            else:
                children = parents
                
                #apply mutation
            for j in range(len(children)):
                if random.random() <= mutation_rate:
                    if i >= numGens/2:
                        children[j].mutate(2)
                    else:
                        children[j].mutate()
                    
            nextPop.append(children[0])
            nextPop.append(children[1])

            #move next population to current
        currPop = nextPop

            #get scores for currPop
        for j in range(popsize):
            currPop[j].getFitness(eval)
            
            #sort the current population based on score
        currPop = sorted(currPop, key=lambda x: x.score)
        if out_file is not None:
            out_file.write(f"Gen {i+1:<3}: {currPop[0].key}\t{currPop[0].score}\n")
        bestKey = currPop[0].key
                    
    print(f"\nBEST KEY: {bestKey}\tSCORE: {currPop[0].score}\n")
    ciph = XORCipher(bestKey)
    text = ciph.decrypt(encrypted_text=encrypted_text)
    print(text)



goal_key = "thisismykey1234567890ABCDEFGHIJK" #32 char length
enc_cipher = XORCipher(goal_key)


with open("samples/sample002.txt", "rb") as file:
    text = file.read()
enc_text = enc_cipher.encrypt(text)

#eval = Evaluator(enc_text)
#gn = Genome(goal_key)
#gn.getFitness(eval)
#print("Successfully Encrypted Text")
print(f"GOAL: {goal_key}")
#print(f"{gn.key}\t{gn.score}")

params = [
    {"numGens" : 85, "popSize" : 500, "cross_rate" : 0.9, "mut_rate" : 0.15, "kval" : 5},
    {"numGens" : 85, "popSize" : 500, "cross_rate" : 0.85, "mut_rate" : 0.15, "kval" : 5},
    {"numGens" : 85, "popSize" : 500, "cross_rate" : 0.9, "mut_rate" : 0.3, "kval" : 5},
    {"numGens" : 85, "popSize" : 500, "cross_rate" : 0.85, "mut_rate" : 0.3, "kval" : 5},
    {"numGens" : 85, "popSize" : 500, "cross_rate" : 0.95, "mut_rate" : 0.15, "kval" : 5},
    {"numGens" : 85, "popSize" : 500, "cross_rate" : 0.95, "mut_rate" : 0.3, "kval" : 5},
]

#for p in params:
#    print(f"""TESTING: 
#        Number of Gens: {p["numGens"]}
#        Population Size: {p["popSize"]}
#        Crossover Rate: {p["cross_rate"]}
#        Mutation Rate: {p["mut_rate"]}
#        K Value: {p["kval"]}
#        """)
#    GeneticAlgorithm(enc_text, p["numGens"], p["popSize"], p["cross_rate"], p["mut_rate"], p["kval"])

file = open("results.txt", "w")

p = {"numGens" : 150, "popSize" : 500, "cross_rate" : 0.85, "mut_rate" : 0.35, "kval" : 4}
#print(enc_cipher.decrypt(enc_text))
GeneticAlgorithm(enc_text, p["numGens"], p["popSize"], p["cross_rate"], p["mut_rate"], p["kval"], file)