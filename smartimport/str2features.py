from collections import defaultdict
import numpy as np

DEFAULT_LETTERS = 'azertyuiopqsdfghjklmwxcvbnéèçàâêîôûù1234567890,;.:!?/@- '

class OnePixelByLetter:

    def __init__(self, max_length=50, letters=DEFAULT_LETTERS):
        self.max_length = max_length
        self.letters = letters
        # bag of characters dictionnary
        self.dictionnary = {}
        for idx, char in enumerate(self.letters):
            self.dictionnary[char] = idx
        # For unknown letters
        self.dictionnary['unknown'] = len(self.letters)
        # For uppercase
        self.dictionnary['upper'] = len(self.letters) + 1

    def _to_matrix(self, text):
        # check text length
        if len(text) >= self.max_length:
            text = text[:self.max_length]

        # create bag of characters
        matrix = np.zeros((self.max_length, len(self.dictionnary)))

        for idx, char in enumerate(text):
            if char.lower() in self.dictionnary:
                matrix[idx, self.dictionnary[char.lower()]] += 1
                if char.isupper():
                    matrix[idx, self.dictionnary['upper']] += 1
            else:
                matrix[idx][self.dictionnary['unknown']] += 1

        return matrix

    def convert(self, text):
        """
        convert text into 1D features vector
        :param text: the text to be coded
        :return: a matrix representing the text
        """
        result = self._to_matrix(text)
        # return as 1D vector to match with skicit-learn implementation of ML methods
        return result.reshape(result.size)

    def nb_features(self):
        return self.max_length * len(self.dictionnary)

    def to_image(self, text):
        """ Return a pillow image instance that can be saved with `img.save(path)`
        or displayed with `img.show()`."""
        from PIL import Image

        matrix = self._to_matrix(text)
        rgb = np.zeros((matrix.shape[0], matrix.shape[1], 3), dtype=np.uint8)
        rgb[:, :, 0] = matrix*255
        rgb[:, :, 1] = matrix*255
        rgb[:, :, 2] = matrix*255
        img = Image.fromarray(rgb, 'RGB')
        return img

    def to_str(self, text):
        lines = []
        lines.append(' '.join(self.letters))

        matrix = self._to_matrix(text)
        for row in matrix:
            lines.append(' '.join(str(int(i)) for i in row))

        return '\n'.join(lines)

class OnePixelByPosition:

    def __init__(self, depth=5, letters=DEFAULT_LETTERS):
        self.depth = depth
        self.letters = letters
        self.dictionnary = {}

        for idx, char in enumerate(self.letters):
            self.dictionnary[char] = idx

        # For unknown letters
        self.dictionnary['unknown'] = len(self.letters)
        # For uppercase
        self.dictionnary['upper'] = len(self.letters) + 1

    def _to_matrix(self, text):
        # create bag by position of characters
        matrix = np.zeros((self.depth, len(self.dictionnary)))
        matrix_pos = defaultdict(lambda : 0)

        for pos, char in enumerate(text):
            lchar = char.lower()
            if lchar in self.dictionnary:
                if matrix_pos[lchar] < self.depth:
                    matrix[matrix_pos[lchar], self.dictionnary[lchar]] = 1 - ((pos + 1) / len(text))
                    if char.isupper():
                        matrix[matrix_pos[lchar], self.dictionnary['upper']] = 1
                    matrix_pos[lchar] += 1
            else:
                matrix[matrix_pos['unknown']][self.dictionnary['unknown']] = 1
        return matrix

    def convert(self, text):
        """
        convert text into 1D features vector
        :param text: the text to be coded
        :return: a matrix representing the text
        """

        # return as 1D vector to match with skicit-learn implementation of ML methods
        result = self._to_matrix(text)
        return result.reshape(result.size)

    def nb_features(self):
        return self.depth * len(self.dictionnary)

    def to_str(self, text):
        lines = []
        lines.append(' '.join("   %s" % l for l in self.letters))

        matrix = self._to_matrix(text)
        for row in matrix:
            lines.append(' '.join("%.2f" % i for i in row))

        return '\n'.join(lines)

    def to_image(self, text):
        """ Return a pillow image instance that can be saved with `img.save(path)`
        or displayed with `img.show()`."""
        from PIL import Image

        matrix = self._to_matrix(text)
        rgb = np.zeros((matrix.shape[0], matrix.shape[1], 3), dtype=np.uint8)
        rgb[:, :, 0] = matrix*255
        rgb[:, :, 1] = matrix*255
        rgb[:, :, 2] = matrix*255
        img = Image.fromarray(rgb, 'RGB')
        return img

if __name__ == '__main__':
    # Testing 
    # TODO Should be done with pytest
    algo1 = OnePixelByLetter()
    algo2 = OnePixelByPosition()

    print(algo1.convert("Bonjour monde"))
    print(algo1.to_str("Bonjour monde"))

    #img = algo1.to_image("Bonjour monde 3356")
    #img.show()

    print(algo2.convert("Bonjour monde"))
    print(algo2.to_str("Bonjour monde"))

    img = algo2.to_image("Bonjour monde 3356")
    img.show()
