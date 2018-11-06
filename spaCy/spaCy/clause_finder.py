import re

import spacy

from general.file_loader import *
from spaCy.question_extraction import QuestionExtractor
from spaCy.answer_extraction import AnswerExtractor

class ClauseFinder:
    nlp = spacy.load('en_core_web_sm')

    @staticmethod
    def extractAnswer(self, clause):
        answers = []
        
        question_content = ClauseFinder.nlp(question.content)
        question_features = QuestionExtractor.extract_question_features(question_content)

        clause_content = ClauseFinder.nlp(clause)
        clause_features = AnswerExtractor.extract_clause_features(clause_content)
        print(clause_features)

        # print("Q ft =", question_features[0][1])
        for clause_ft in clause_features:
            # print (quest_ft, clause_ft)
            # print("C ft =", clause_ft[1])
            if (question_features[0][1] == 'where'):
                if clause_ft[1] == 'GPE' or clause_ft[1] == 'LOC':
                    answers.append(clause_ft[0])
                    break

            if (question_features[0][1] == 'who'):
                if clause_ft[1] == 'PERSON' or clause_ft[1] == 'NORP':
                    answers.append(clause_ft[0])
                # elif clause_ft[1] == 'ORG' or clause_ft[1] == 'GPE':
                #     answers.append(clause_ft[0])
                    break

            if (question_features[0][1] == 'how'):
                if (question_features[0][2] == 'how much'):
                    if clause_ft[1] == 'MONEY' or clause_ft[1] == 'TIME' or clause_ft[1] == 'PERCENT':
                        answers.append(clause_ft[0])
                        break

                if clause_ft[1] == 'QUANTITY':
                    answers.append(clause_ft[0])
                    break

            if (question_features[0][1] == 'what'):
                if clause_ft[1] == 'ORG' or clause_ft[1] == 'LOC':
                    answers.append(clause_ft[0])
                    break
        return answers

questions = FileLoader.load_questions('developset/1999-W02-5.questions')
story = FileLoader.load_story('developset/1999-W02-5.story')
finder = ClauseFinder(story)
for question in questions:
    clause = finder.find(question)
    print(clause)
    print(finder.extractAnswer(clause))
    