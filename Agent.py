# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image

import numpy


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        if problem.problemType == "2x2" and "Problems B" in problem.problemSetName:
            ans = self.solve_2x2(problem)
            if ans != -1:
                return ans
        else:
            return 1

    def solve_2x2(self, ravens_problem):
        problem = []
        choices = []

        for key, value in ravens_problem.figures.items():
            if key in ['A', 'B', 'C']:
                problem.append(value)
            elif key in ['1', '2', '3', '4', '5', '6']:
                choices.append(value)
        for i in range(2):
            diff1 = self.get_pixel_difference(self.convert_to_numpy_array(problem[0]),
                                              self.convert_to_numpy_array(problem[1]))
            diff2 = self.get_pixel_difference(self.convert_to_numpy_array(problem[1]),
                                              self.convert_to_numpy_array(problem[2]))

        if diff1 < diff2:
            target_image = self.convert_to_numpy_array(problem[0]) + self.convert_to_numpy_array(
                problem[2]) - self.convert_to_numpy_array(problem[1])
        else:
            target_image = self.convert_to_numpy_array(problem[2]) + self.convert_to_numpy_array(
                problem[1]) - self.convert_to_numpy_array(problem[0])

        min_difference = float('inf')
        best_option = None
        for choice in choices:
            option_image = Image.open(choice.visualFilename).convert("L")  # Convert to grayscale
            option_array = numpy.array(option_image)
            difference = self.get_pixel_difference(target_image, option_array)
            if difference < min_difference:
                min_difference = difference
                best_option = choice

        return int(best_option.name)

    def get_pixel_difference(self, image1, image2):
        return numpy.sum(numpy.abs(image1 - image2))

    def convert_to_numpy_array(self, value):
        img_array = []
        img = Image.open(value.visualFilename)
        if img:
            img_array = numpy.array(img)
        return img_array
