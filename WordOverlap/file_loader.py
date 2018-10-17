from typing import List
class Story:
    headline: str
    date: str
    Id: str
    text: List[str]
    def __init__(self):
        self.text = []

class FileLoader:
    @staticmethod
    def load_story(filepath) -> Story:
        story: Story = Story()
        with open(filepath, 'r') as story_file:
            for line_number, line in enumerate(story_file):
                line = line.strip()
                if line_number is 0:
                    story.headline = line.replace('HEADLINE:', '')
                elif line_number is 1:
                    story.date = line.replace('DATE:', '')
                elif line_number is 2:
                    story.Id = line.replace('STORYID:', '')
                elif line_number > 4:
                    if not line:
                        story.text.append('')
                    else:
                        story.text[-1] += ' '+line
        story.text = [text.strip() for text in story.text]
        return story


print(FileLoader.load_story('../developset/1999-W02-5.story').__dict__)
                