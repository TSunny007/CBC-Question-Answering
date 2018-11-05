import spacy

from general.file_loader import *

nlp = spacy.load('en_core_web_sm')
questions = FileLoader.load_questions('developset/1999-W02-5.questions')
story = FileLoader.load_story('developset/1999-W02-5.story')


def get_compound_nouns(en_doc, token, token_text):
    ptoken = token

    # print(token.text, token.dep_)
    while token.i > 0 and en_doc[token.i - 1].dep_ == "compound":
        token_text = en_doc[token.i - 1].text + " " + token_text
        token = en_doc[token.i - 1]

    token = ptoken

    while token.i < len(en_doc) - 1 and en_doc[token.i + 1].dep_ == "compound":
        token_text = token_text + " " + en_doc[token.i + 1].text
        token = en_doc[token.i + 1]

    return token_text


def get_adj_phrase(token, token_text):
    for child in token.children:
        if child.dep_ == "amod" or child.dep_ == "acomp" or child.dep_ == "ccomp":  # not for how many
            if child.text != "much" and child.text != "many":
                token_text = child.lemma_ + " " + token_text
    return token_text


def get_root_phrase(token, keywords):
    for child in token.children:
        if child.dep_ == "acomp" or child.dep_ == "xcomp" or child.dep_ == "ccomp":
            keywords.append(child.lemma_)
    return keywords


def get_noun_chunk(sent, en_doc, keywords):
    root = ""
    for token in sent:
        if token.tag_ == "NN" or token.tag_ == "NNP" or token.tag_ == "NNPS" or token.tag_ == "NNS":
            if token.dep_ != "compound":
                print("notcompund: ", token.text)
                token_text = get_compound_nouns(en_doc, token, token.text)
                token_text = get_adj_phrase(token, token_text)
                keywords.append(token_text)

        if token.dep_ == "nummod" or token.tag_ == "CD":
            token_text = token.text
            if token.i > 0:
                if en_doc[token.i - 1].tag_ == "JJ":
                    token_text = en_doc[token.i - 1].text + " " + token.text
            if token.i < len(en_doc) - 1:
                if en_doc[token.i + 1].tag_ == "JJ":
                    token_text = token.text + " " + en_doc[token.i + 1].text
            keywords.append(token_text)

        if token.dep_ == "ROOT":
            root = token.lemma_
            keywords = get_root_phrase(token, keywords)
            if token.text != token.lemma_:
                keywords.append(token.text)

    return root, keywords

def get_pos_chunk(sent, en_doc, pos_dict):
    for token in sent:
        pos_dict[token.text] = token.pos_

    return pos_dict

def get_entity_chunk(sent, en_doc, entity_dict):
    for token in sent:
        entity_dict[token.text] = token.pos_

    return entity_dict

def extractFeatures(en_doc):
    keywords = []

    for sent in en_doc.sents:
        root, keywords = get_noun_chunk(sent, en_doc, keywords)
        keywords.append(root)

    return keywords

def extractPOS(en_doc):
    pos_dict = {}

    for sent in en_doc.sents:
        pos_dict = get_pos_chunk(sent, en_doc, pos_dict)
    
    return pos_dict

def extractNameEntities(en_doc):
    entity_dict = {}

    for sent in en_doc.sents:
        entity_dict = get_entity_chunk(sent, en_doc, entity_dict)
    
    return pos_dict

def run(question):
    question = question
    en_doc = nlp(u'' + question)

    keywords = extractFeatures(en_doc)
    pos = extractPOS(en_doc)

    print(question)

    print(keywords)

    print(pos)


for question in questions:
    # q = nlp(question.content)
    # print(question.content, list(q.ents) + list(q.noun_chunks))
    run(question.content)
    # print()
