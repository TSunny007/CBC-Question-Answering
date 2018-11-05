import re

import spacy

from general.file_loader import *
from spaCy.question_extraction import QuestionExtractor


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
            scores = self.get_score(text, question_features, question_content)
            if scores > max_score:
                max_score = scores
                best_clause = text
        return best_clause

    @staticmethod
    def get_score(text, features, question_content):
        score = 0
        for entity in ClauseFinder.nlp(text).ents:
            if (features[0][1] == 'where') and not (re.search(entity.text, question_content.text, re.IGNORECASE)):
                if entity.label_ == 'GPE':
                    score += 5
                elif entity.label_ == 'LOC':
                    score += 3
                break

        for feature in features:
            if feature[0] == 'NOUN':
                if re.search(feature[1], question_content.text, re.IGNORECASE) or (
                        len(feature) > 2 and re.search(feature[2], question_content.text, re.IGNORECASE)):
                    score += 1

            elif feature[0] == 'VERB':
                pass
            elif feature[0] == 'ROOT':
                pass
            elif feature[0] == 'Q_TYPE':
                pass
            else:
                print('panic with extraction tag {}'.format(feature[0]))
        return score


questions = FileLoader.load_questions('developset/1999-W02-5.questions')
story = FileLoader.load_story('developset/1999-W02-5.story')
finder = ClauseFinder(story)
print(finder.find(questions[0]))
