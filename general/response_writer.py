from collections import OrderedDict


class ResponseWriter:
    @staticmethod
    def write_answer(filepath: str, results: OrderedDict):
        """
        The file extension must also be 'response'
        :param filepath: filepath of output file
        :param results: OrderedDict where keys are questionId, while values are our prediction responses
        """
        assert filepath.split('.')[-1] == 'response'

        with open(filepath, 'w') as response_file:
            for (question_id, response) in results.items():
                response_file.write(question_id)
                response_file.write(response)
