from collections import OrderedDict

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from general.file_loader import *
from general.response_writer import ResponseWriter
from precision.answer_extraction import AnswerExtractor


class QA:
    nlp = spacy.load('en_core_web_sm')

    @staticmethod
    def get_story_setences(story: Story):
        # gets the sentences in the passage
        sentences = [sentence for paragraph in story.text for sentence in QA.nlp(paragraph).sents]

        # gets a list of list of normalized words, where the first list contains every sentence as an embedded list.
        sentences_bagged = [[token.lemma_ for token in sentence
                             if
                             not token.is_stop and not token.is_punct and token.lemma_ != '-PRON-' and token.lemma_.strip()]
                            for sentence in sentences]

        # returns a list of spacy span (for NER), a bagged list of strings
        return sentences, sentences_bagged

    @staticmethod
    def extract_question(question: Question):
        q = QA.nlp(question.content)

        # gets a list of normalized words in the sentence.
        q_bagged = [token.lemma_ for token in q if
                    not token.is_stop and not token.is_punct and token.lemma_ != '-PRON-' and token.lemma_.strip()
                    and not (token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB")]

        return q, q_bagged

    @staticmethod
    def overlap(stories: List[List[str]], bagged: List[str]):
        documents = stories + [bagged]

        modified_doc = [' '.join(i) for i in
                        documents]

        vectorizer = TfidfVectorizer(min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True)
        tf_idf = vectorizer.fit_transform(modified_doc)

        cosine_similarities = linear_kernel(tf_idf[-1], tf_idf).flatten()
        related_docs_indices = cosine_similarities.argsort()[-4:-1][::-1]  # get top three similar documents's indices

        # print(cosine_similarities)
        return related_docs_indices[0]


directory_file = 'developset/input.txt'
input_dir = None
results = OrderedDict()
with open(directory_file, 'r') as directory:
    for line in directory:
        if not input_dir:
            input_dir = line.strip()
        else:
            file = input_dir + line.strip()

            story = FileLoader.load_story(file + '.story')
            sentences, bagged_sentences = QA.get_story_setences(story)
            for question in FileLoader.load_questions(file + '.questions'):
                q, q_bagged = QA.extract_question(question)
                best_index = QA.overlap(bagged_sentences, q_bagged)

                results[question.id] = AnswerExtractor.get_answer(q, sentences[best_index])  # best_sentence
                print('Question: ', question.content)
                print('Answer: ', results[question.id], '\n')

ResponseWriter.write_answer('developset/output.response', results)
