import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import math

class JaccardDistance:
    @staticmethod
    def twoCharGram(dataset):
        with open(dataset, 'r') as data:
            textFile = data.read().replace('\n', ' ')
            kGrams = set()
            # 2-Char gram
            for i in range(len(textFile)-1):
                if textFile[i] + textFile[i+1] not in kGrams:
                    kGrams.add(textFile[i] + textFile[i+1])
        return kGrams

    @staticmethod
    def threeCharGram(dataset):
        with open(dataset, 'r') as data:
            textFile = data.read().replace('\n', ' ')
            kGrams = set()
            # 3-Char gram
            for i in range(len(textFile)-2):
                if textFile[i] + textFile[i+1] + textFile[i+2] not in kGrams:
                    kGrams.add(textFile[i] + textFile[i+1] + textFile[i+2])
        return kGrams

    @staticmethod
    def twoWordGram(dataset):
        with open(dataset, 'r') as data:
            tokens = str.split(data.read().replace('\n', ' '))
            kGrams = set()
            #2-word gram
            for i in range(len(tokens)-1):
                if tokens[i] + ' ' + tokens[i+1] not in kGrams:
                    kGrams.add(tokens[i] + ' ' + tokens[i+1])
        return kGrams

    @staticmethod
    def jaccard(question, dataset):
        similarity_perc = (100. * len(question.intersection(dataset)) / len(question.union(dataset)))
        return similarity_perc



