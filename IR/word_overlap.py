from collections import OrderedDict

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from general.file_loader import *
from general.response_writer import ResponseWriter


class WordOverlap:
    nlp = spacy.load('en_core_web_sm')

    @staticmethod
    def find_overlap(story: Story, question: Question):
        sentences = [sentence for paragraph in story.text for sentence in WordOverlap.nlp(paragraph).sents]

        stories = [[token.lemma_ for token in sentence
                    if not token.is_stop and not token.is_punct and token.lemma_ != '-PRON-' and token.lemma_.strip()]
                   for sentence in sentences]
        doc = WordOverlap.nlp(question.content)
        bagged = [token.lemma_ for token in doc if
                  not token.is_stop and not token.is_punct and token.lemma_ != '-PRON-' and token.lemma_.strip()
                  and not (token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB")]

        documents = stories + [bagged]

        modified_doc = [' '.join(i) for i in
                        documents]

        vectorizer = TfidfVectorizer(min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True)
        tf_idf = vectorizer.fit_transform(modified_doc)

        cosine_similarities = linear_kernel(tf_idf[-1], tf_idf).flatten()
        related_docs_indices = cosine_similarities.argsort()[-4:-1][::-1]
        print('Question: ', question.content)
        print('Answer: ', sentences[related_docs_indices[0]].text, '\n')
        return [sentences[related_docs_indices[i]].text for i in range(len(related_docs_indices))]


results = OrderedDict()
story = FileLoader.load_story('developset/2000-W06-4.story')
for question in FileLoader.load_questions('developset/2000-W06-4.questions'):
    results[question.id] = WordOverlap.find_overlap(story, question)[0]
    # break
ResponseWriter.write_answer('2000-W06-4.response', results)
