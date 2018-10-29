import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import math

class JaccardDistance:
    @staticmethod
    def twoCharGram(sentence):
        kGrams = set()
        # 2-Char gram
        for i in range(len(sentence)-1):
            if sentence[i] + sentence[i+1] not in kGrams:
                kGrams.add(sentence[i] + sentence[i+1])
        return kGrams

    @staticmethod
    def threeCharGram(sentence):
        kGrams = set()
        # 3-Char gram
        for i in range(len(sentence)-2):
            if sentence[i] + sentence[i+1] + sentence[i+2] not in kGrams:
                kGrams.add(sentence[i] + sentence[i+1] + sentence[i+2])
        return kGrams

    @staticmethod
    def twoWordGram(sentence):
        kGrams = set()
        #2-word gram
        for i in range(len(sentence)-1):
            if sentence[i] + ' ' + sentence[i+1] not in kGrams:
                kGrams.add(sentence[i] + ' ' + sentence[i+1])
        return kGrams

    @staticmethod
    def jaccard(question, story):
        """
        Calculate the similarity percentage bewtween two the question
        and story dataset 
        """
        similarity_perc = (100. * len(question.intersection(story)) / len(question.union(story)))
        return similarity_perc



