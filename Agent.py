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

        check = self.is_A_to_C_rotated(problem[0], problem[1])


        # # If A == C
        # if self.is_A_to_C_same(problem[0], problem[2]):
        #     ans = self.choice_equal_to_B(problem[1], choices)

        ans = self.choice_equal_to_B(problem[1], choices)
        if ans:
            return int(ans.name)
        else:
            return 4
        pass

    def choice_equal_to_B(self, problem_image, choice_images):
        problem_image_array = self.convert_to_numpy_array(problem_image)
        for choice_image in choice_images:
            if numpy.array_equal(problem_image_array, self.convert_to_numpy_array(choice_image)):
                return choice_image
        return False

    def convert_to_numpy_array(self, value):
        img_array = []
        img = Image.open(value.visualFilename)
        if img:
            img_array = numpy.array(img)
        return img_array

    def is_A_to_C_same(self, imageA, imageC):
        isSame = numpy.array_equal(self.convert_to_numpy_array(imageA), self.convert_to_numpy_array(imageC))
        return isSame

    def is_A_to_C_rotated(self, imageA, imageC):
        img = Image.open(imageC.visualFilename)
        rotatedC = img.rotate(90)

        isSame = numpy.array_equal(self.convert_to_numpy_array(imageA), numpy.array(rotatedC))

        return isSame

    def is_A_to_C_flipped(self, imageA, imageC):
        flippedC = numpy.flip(self.convert_to_numpy_array(imageC), axis=1)
        isFlipped = numpy.array_equal(self.convert_to_numpy_array(imageA), numpy.array(flippedC))
        return isFlipped
