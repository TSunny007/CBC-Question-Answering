from typing import List


class Story:
    headline = ""
    date = ""
    id = ""
    text = list()

    def __init__(self):
        self.text = []

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()


class Question:
    id = ""
    content = ""
    difficulty = ""

    # only present if an answer file is loaded
    answers = list()

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()




class FileLoader:
    @staticmethod
    def load_story(filepath) -> Story:
        """
        Loads a story given its path. The story must be in the format
        HEADLINE:
        DATE:
        STORYID:

        <Story>

        The file extension must also be 'story'
        :param filepath: filepath of the story
        :return: a story object
        """
        assert filepath.split('.')[-1] == 'story'

        story = Story()
        with open(filepath, 'r') as story_file:
            for line_number, line in enumerate(story_file):
                line = line.strip()
                if line_number is 0:
                    story.headline = line.replace('HEADLINE:', '').strip()
                elif line_number is 1:
                    story.date = line.replace('DATE:', '').strip()
                elif line_number is 2:
                    story.id = line.replace('STORYID:', '').strip()
                elif line_number > 4:
                    if not line:
                        # make a new text element
                        story.text.append('')
                    else:
                        # keep adding this line to the last element of the list.
                        story.text[-1] += ' ' + line
        story.text = [text.strip() for text in story.text]
        return story

    @staticmethod
    def load_questions(question_file) -> List[Question]:
        """
        Loads a question or an answer file. The file extensions must be '.questions' or '.answers'
        :param question_file: filepath of the question or answer file
        :return: a array of question objects, where each question will contain an 'answers' field if we were
        given an answer file.
        """
        assert (question_file.split('.')[-1] == 'questions') or (question_file.split('.')[-1] == 'answers')
        questions = []
        with open(question_file, 'r') as question_file:
            question = ""
            for line in question_file:
                if not line:
                    continue
                line = line.strip()
                line_parts = line.split()
                if line_parts:
                    if line_parts[0] == 'QuestionID:':
                        question = Question(' '.join(line_parts[1:]))
                    elif line_parts[0] == 'Question:':
                        question.content = ' '.join(line_parts[1:])
                    elif line_parts[0] == 'Answer:':
                        question.answers = ' '.join(line_parts[1:]).split('|')
                        questions.append(question)
                    elif line_parts[0] == 'Difficulty:':
                        question.difficulty = ' '.join(line_parts[1:])
                        questions.append(question)
        return questions

# Testing. If any of these lines following lines fail we're in trouble

# print(FileLoader.load_story('../developset/1999-W02-5.story').__dict__)
# print(FileLoader.load_questions('../developset/1999-W02-5.questions')[0].__dict__)
# print(FileLoader.load_questions('../developset/1999-W02-5.answers')[0].__dict__)
