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
import cv2


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
        if problem.problemType == "3x3" and "Problems C" in problem.problemSetName:
            ans = self.solve_3x3(problem)
            if ans != -1:
                return ans
        else:
            return 1

    def solve_3x3(self, ravens_problem):

        # Problem Images
        imageA = self.convert_to_numpy_array(ravens_problem.figures['A'])
        imageB = self.convert_to_numpy_array(ravens_problem.figures['B'])
        imageC = self.convert_to_numpy_array(ravens_problem.figures['C'])
        imageD = self.convert_to_numpy_array(ravens_problem.figures['D'])
        imageE = self.convert_to_numpy_array(ravens_problem.figures['E'])
        imageF = self.convert_to_numpy_array(ravens_problem.figures['F'])
        imageG = self.convert_to_numpy_array(ravens_problem.figures['G'])
        imageH = self.convert_to_numpy_array(ravens_problem.figures['H'])

        # option Images
        option1 = self.convert_to_numpy_array(ravens_problem.figures['1'])
        option2 = self.convert_to_numpy_array(ravens_problem.figures['2'])
        option3 = self.convert_to_numpy_array(ravens_problem.figures['3'])
        option4 = self.convert_to_numpy_array(ravens_problem.figures['4'])
        option5 = self.convert_to_numpy_array(ravens_problem.figures['5'])
        option6 = self.convert_to_numpy_array(ravens_problem.figures['6'])
        option7 = self.convert_to_numpy_array(ravens_problem.figures['7'])
        option8 = self.convert_to_numpy_array(ravens_problem.figures['8'])

        for key, value in


        return 1
        pass

    def convert_to_numpy_array(self, value):
        img_array = []
        img = Image.open(value.visualFilename)
        if img:
            img_array = numpy.array(img)
        return img_array
