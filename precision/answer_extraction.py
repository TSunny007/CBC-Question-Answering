class AnswerExtractor:

    @staticmethod
    def get_answer(question, sentence):
        """
        :param question: spacy span
        :param sentence: spacy span
        :return: answer text
        """

        for token in question:
            if token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
                q_type = token.lemma_
                q_index = token.i

        assert q_type

        if q_type == 'where':
            return ' '.join(entity.text for entity in sentence.ents if
                            (entity.label_ == 'GPE' or
                             entity.label_ == 'LOC') and entity.text not in question.text)

        elif q_type == 'who':
            return ' '.join(entity.text for entity in sentence.ents if
                            (entity.label_ == 'PERSON' or
                             entity.label_ == 'NORP' or
                             entity.label_ == 'FAC' or
                             entity.label_ == 'ORG' or
                             entity.label_ == 'GPE') and entity.text not in question.text)

        elif q_type == 'how':
            # if there is an qdjective then we return numerical information
            if question[q_index + 1].pos_ == 'ADJ':
                return ' '.join(entity.text for entity in sentence.ents if
                                (entity.label_ == 'QUANTITY' or
                                 entity.label_ == 'TIME' or
                                 entity.label_ == 'CARDINAL' or
                                 entity.label_ == 'MONEY' or
                                 entity.label_ == 'PERCENT') and entity.text not in question.text)
            return sentence.text

        elif q_type == 'when':
            # If there is an entity in the sentence
            time = ' '.join(entity.text for entity in sentence.ents if
                            (entity.label_ == 'DATE' or
                             entity.label_ == 'TIME' or
                             entity.label_ == 'PERCENT') and entity.text not in question.text)
            if time.strip():
                return time
            # when the sentence itself has 'when' eg 'when he died'
            sentence_split = sentence.text.split()
            for index, word in enumerate(sentence_split):
                if word == 'when':
                    return sentence[index:].text

            # otherwise
            return ''

        elif q_type == 'which':
            return ' '.join(token.text for token in sentence if
                            (token.tag_ == 'NOUN' or
                             token.tag_ == 'PROPN') and token.text not in question.content)

        elif q_type == 'what':
            return sentence.text

        elif q_type == 'why':
            # when the sentence itself has 'because' eg 'because he died'
            sentence_split = sentence.text.split()
            for index, word in enumerate(sentence_split):
                if word == 'because':
                    return sentence[index:].text
                elif word == 'so that' or word == 'so' or word == 'since' or word == 'due to':
                    return sentence[index:].text
            return sentence.text

        else:
            return sentence.text
