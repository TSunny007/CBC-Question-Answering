from collections import deque


class QuestionExtractor:
        
    @staticmethod
    def get_compound_nouns(en_doc, token):

        i = token.i

        compounded_part = deque()
        compounded_part.append(token.text)

        # build the word before the token's word
        while i > 0 and en_doc[i - 1].dep_ == 'compound':
            compounded_part.appendleft(en_doc[i - 1].text)
            i -= 1

        i = token.i
        # build the compound word after the token's word
        while i < len(en_doc) - 1 and en_doc[i + 1].dep_ == 'compound':
            compounded_part.append(en_doc[i + 1].text)
            i += 1

        return ' '.join(compounded_part)

    @staticmethod
    def get_adj_phrase(token, current_text):
        adj_phrase = deque()
        adj_phrase.append(current_text)

        for child in token.children:
            if child.dep_ == 'amod' or child.dep_ == 'acomp' or child.dep_ == 'ccomp':
                if child.text != 'much' and child.text != 'many':
                    adj_phrase.appendleft(child.lemma_)
        return ' '.join(adj_phrase)

    @staticmethod
    def get_root_phrase(token):
        keywords = []
        for child in token.children:
            if child.tag_ == 'acomp' or child.dep_ == 'xcomp' or child.dep_ == 'ccomp':
                if child.lemma_ != 'be' and child.lemma_ != 'do':
                    keywords.append(('VERB', child.lemma_))
        return keywords

    @staticmethod
    def extract_question_features(en_doc):
        # format:
        # 1) 'NOUN', noun, (optional) noncompound_version
        # 2) 'ROOT', root.lemma
        # 3) 'VERB', child_verbs.lemma
        keywords = []
        for token in en_doc:
            # check for noun type
            if token.tag_ == 'NN' or token.tag_ == 'NNP' or token.tag_ == 'NNPS' or token.tag_ == 'NNS':
                # add compounded and concise version as well: 'south queens junior high school -> school'.
                if token.dep_ != 'compound':

                    token_text = QuestionExtractor.get_compound_nouns(en_doc, token)
                    token_text = QuestionExtractor.get_adj_phrase(token, token_text)

                    if token_text != token.text:
                        keywords.append(('NOUN', token.lemma_, token_text))
                    else:
                        keywords.append(('NOUN', token.text))

            if token.dep_ == 'ROOT' and token.pos:
                if token.lemma_ != 'be' and token.lemma_ != 'do':
                    keywords.append(('ROOT', token.lemma_))
                keywords += (QuestionExtractor.get_root_phrase(token))

            if token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
                keywords.insert(0, ('Q_TYPE', token.lemma_, token.text + ' ' + en_doc[token.i + 1].text))
        return keywords


# import spacy
# from general.file_loader import *
# import os
#
# nlp = spacy.load('en_core_web_sm')
#
#
# def run(question):
#     en_doc = nlp(u'' + question)
#
#     keywords = QuestionExtractor.extract_question_features(en_doc)
#     # pos = extract_pos(en_doc)
#
#     print(question)
#
#     print(keywords)
#
#     # print(pos)
#
#
# for file in [file for file in os.listdir('developset/') if '.questions' in file]:
#     for question in FileLoader.load_questions('developset/'+file):
#         # q = nlp(question.content)
#         # print(question.content, list(q.ents) + list(q.noun_chunks))
#         run(question.content)
#         print()


# def get_pos_chunk(sent, pos_dict):
#     for token in sent:
#         pos_dict[token.text] = token.pos_
#     return pos_dict
#
#
# def extract_pos(en_doc):
#     pos_dict = {}
#
#     for sent in en_doc.sents:
#         pos_dict = get_pos_chunk(sent, pos_dict)
#
#     return pos_dict
