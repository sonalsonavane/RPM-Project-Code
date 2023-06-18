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
        problem = self.load_images(problem)
        choices = self.load_images(choices)

        return 0

    def get_pixel_difference(self, image1, image2):
        return numpy.sum(numpy.abs(image1 - image2))

    def load_images(self,images):
        images = []
        for image in images:
            img = Image.open(image.visualFilename).convert("L")  # Convert to grayscale
            images.append(numpy.array(img))
        return images
