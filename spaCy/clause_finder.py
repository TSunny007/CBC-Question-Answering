import re

import spacy

from general.file_loader import *
from spaCy.question_extraction import QuestionExtractor
from spaCy.answer_extraction import AnswerExtractor

class ClauseFinder:
    nlp = spacy.load('en_core_web_sm')

    def __init__(self, passage):
        self.passage = passage

    def find(self, question):
        # features will look like this
        # [('Q_TYPE', 'when', 'When are'), ('ROOT', 'be'), ('NOUN', 'summer', 'next summer'), ('NOUN', 'Olympics')]
        # Q_TYPE will always be first here
        question_content = ClauseFinder.nlp(question.content)
        question_features = QuestionExtractor.extract_question_features(question_content)
        print(question_features)
        max_score, best_clause = 0, None
        for text in self.passage.text:
            scores = self.get_score(ClauseFinder.nlp(text), question_features, question_content)
            if scores > max_score:
                max_score = scores
                best_clause = text
        return best_clause

    @staticmethod
    def get_score(passage: spacy.tokens.doc.Doc, features: List[str], question_content: spacy.tokens.doc.Doc):
        score = 0
        for entity in passage.ents:
            if (features[0][1] == 'where') and not (re.search(entity.text, question_content.text, re.IGNORECASE)):
                if entity.label_ == 'GPE' or entity.label_ == 'LOC':
                    score += 5
                break

            if (features[0][1] == 'who') and not (re.search(entity.text, question_content.text, re.IGNORECASE)):
                if entity.label_ == 'PERSON' or entity.label_ == 'NORP':
                    score += 5
                elif entity.label_ == 'ORG' or entity.label_ == 'GPE':
                    score += 2
                break

            if (features[0][1] == 'how') and not (re.search(entity.text, question_content.text, re.IGNORECASE)):
                if entity.label_ == 'PERSON' or entity.label_ == 'NORP':
                    score += 5
                elif entity.label_ == 'ORG' or entity.label_ == 'GPE':
                    score += 2
                break

        for feature in features:
            if feature[0] == 'NOUN':
                if re.search(feature[1], passage.text, re.IGNORECASE) or (
                        len(feature) > 2 and re.search(feature[2], passage.text, re.IGNORECASE)):
                    score += 1

            elif feature[0] == 'VERB':
                for token in passage:
                    if token.pos_ == 'VERB' and token.lemma_ == feature[1]:
                        score += 1

            elif feature[0] == 'ROOT':
                for token in passage:
                    if token.pos_ == 'VERB' and token.lemma_ == feature[1]:
                        score += 5
            elif feature[0] == 'Q_TYPE':
                pass
            else:
                print('panic with extraction tag {}'.format(feature[0]))
        return score

    def extractAnswer(self, clause):
        answers = []

        question_content = ClauseFinder.nlp(question.content)
        question_features = QuestionExtractor.extract_question_features(question_content)

        clause_content = ClauseFinder.nlp(clause)
        clause_features = AnswerExtractor.extract_clause_features(clause_content)
        print(clause_features)

        print("Q ft =", question_features[0][1])
        for clause_ft in clause_features:
            # print (quest_ft, clause_ft)
            print("C ft =", clause_ft[1])
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
    