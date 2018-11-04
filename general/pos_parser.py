class PosParser:
    @staticmethod
    def PosParser(sentence):
        pos_set = set()    
        for i in range(len(sentence)-1):
            if sentence[i] + sentence[i+1] not in kGrams:
                pos_set.add(sentence[i] + sentence[i+1])
        return pos_set
