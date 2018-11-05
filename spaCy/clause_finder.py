import spacy

from general.file_loader import *
from spaCy.question_extraction import QuestionExtractor


class ClauseFinder:
    nlp = spacy.load('en_core_web_sm')

    def __init__(self, passage):
        self.passage = passage

    def find(self, question):
        question_features = QuestionExtractor.extract_question_features(ClauseFinder.nlp(question.content))
        print(question_features)
        max_score, best_clause = 0, None
        for text in self.passage.text:
            scores = self.get_score(text, question_features)
            if scores > max_score:
                best_clause = text
        return best_clause

    @staticmethod
    def get_score(text, features):
        score = 0
        for feature in features:
            if feature[0] == 'NOUN':
                pass
            elif feature[0] == 'VERB':
                pass
            elif feature[0] == 'ROOT':
                pass
            else:
                print('panic with extraction tag {}'.format(feature[0]))
        return 0


questions = FileLoader.load_questions('developset/1999-W02-5.questions')
story = FileLoader.load_story('developset/1999-W02-5.story')
finder = ClauseFinder(story)
print(finder.find(questions[1]))
