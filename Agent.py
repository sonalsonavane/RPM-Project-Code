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

        if self.is_A_B_C_Same(problem[0], problem[1], problem[2]):
            val = self.find_solution(problem[0], choices)
            return int(val.name)
        elif self.is_A_C_Same(problem[0], problem[2]):
            val = self.find_solution(problem[1], choices)
            return int(val.name)
        elif self.is_A_B_Same(problem[0], problem[1]):
            val = self.find_solution(problem[2], choices)
            return int(val.name)
        else:
            return 4

    def is_A_B_C_Same(self, imageA, imageB, imageC):
        is_A_to_B = self.compare_images(self.convert_to_numpy_array(imageA), self.convert_to_numpy_array(imageB)) < 0.5
        is_B_to_C = self.compare_images(self.convert_to_numpy_array(imageB), self.convert_to_numpy_array(imageC)) < 0.5
        is_A_to_C = self.compare_images(self.convert_to_numpy_array(imageA), self.convert_to_numpy_array(imageC)) < 0.5
        is_A_B_C_Same = is_A_to_B and is_B_to_C and is_A_to_C
        return is_A_B_C_Same

    def is_A_C_Same(self, imageA, imageC):
        is_A_to_C = self.compare_images(self.convert_to_numpy_array(imageA), self.convert_to_numpy_array(imageC)) < 0.2
        return is_A_to_C

    def is_A_B_Same(self, imageA, imageB):
        is_A_to_B = self.compare_images(self.convert_to_numpy_array(imageA), self.convert_to_numpy_array(imageB)) < 0.2
        return is_A_to_B

    def find_solution(self, image, choices):
        for choice_image in choices:
            if self.compare_images(self.convert_to_numpy_array(image), self.convert_to_numpy_array(choice_image)) < 0.2:
                return choice_image

    def convert_to_numpy_array(self, value):
        img_array = []
        img = Image.open(value.visualFilename)
        if img:
            img_array = numpy.array(img)
        return img_array

    def compare_images(self, image1, image2):
        mse = numpy.mean((image1 - image2) ** 2)
        return mse
