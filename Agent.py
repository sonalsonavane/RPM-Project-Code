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
            if ans:
                return ans
        return 4

    def solve_2x2(self, ravens_problem):
        problem = []
        choices = []
        ans = 0

        for key, value in ravens_problem.figures.items():
            if key in ['A', 'B', 'C']:
                problem.append(value)
            elif key in ['1', '2', '3', '4', '5', '6']:
                choices.append(value)

        # A,B, C are same
        if self.A_to_B_to_C_Same(problem[0], problem[1], problem[2]):
            ans = self.find_similar_image(problem[0], choices)
        # A and C are same
        elif self.A_to_C_Same(problem[0], problem[2]):
            ans = self.find_similar_image(problem[1], choices)
            # A and B are same
        elif self.A_to_B_Same(problem[0], problem[1]):
            ans = self.find_similar_image(problem[2], choices)

        if ans:
            return int(ans.name)

    def find_similar_image(self, problem_image, choice_images):
        problem_image_array = self.convert_to_numpy_array(problem_image)
        for choice_image in choice_images:
            if numpy.array_equal(problem_image_array, self.convert_to_numpy_array(choice_image)):
                return choice_image

    def convert_to_numpy_array(self, value):
        img_array = []
        img = Image.open(value.visualFilename)
        if img:
            img_array = numpy.array(img)
        return img_array

    def A_to_B_to_C_Same(self, imageA, imageB, imageC):
        imgA = self.convert_to_numpy_array(imageA)
        imgB = self.convert_to_numpy_array(imageB)
        imgC = self.convert_to_numpy_array(imageC)
        if numpy.array_equal(imgA, imgB) and numpy.array_equal(imgB, imgC):
            return True
        return False

    def A_to_B_Same(self, imageA, imageB):
        return numpy.array_equal(self.convert_to_numpy_array(imageA), self.convert_to_numpy_array(imageB))

    def A_to_C_Same(self, imageA, imageC):
        return numpy.array_equal(self.convert_to_numpy_array(imageA), self.convert_to_numpy_array(imageC))
