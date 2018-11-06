from collections import deque


class AnswerExtractor:
    @staticmethod
    def extract_clause_features(clause_content): 
        # format:
        # entity, ent.label_
        keywords = []
        for ent in clause_content.ents:
            keywords.insert(0, (ent.text, ent.label_))
        return keywords