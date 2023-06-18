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

from RavensFigure import RavensFigure


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
            if problem.name == "Basic Problem B-03":
                ans = self.solve_2x2(problem)
                if ans:
                    return ans

        return 1

    def solve_2x2(self, ravens_problem):
        problem = []
        choices = []
        ans = 0

        for key, value in ravens_problem.figures.items():
            if key in ['A', 'B', 'C']:
                problem.append(value)
            elif key in ['1', '2', '3', '4', '5', '6']:
                choices.append(value)

        print(self.A_to_B_to_C_Same(problem[0], problem[1], problem[2]))

        # Rotate A to B 90 degree clockwise B = Rotated A 90 clockwise
        if self.is_rotated_clockwise(problem[0], problem[1], -90):
            ans = self.find_similar_image(self.rotate_image(problem[2], -90), choices)
        elif self.is_rotated_clockwise(problem[0], problem[1], -180):
            ans = self.find_similar_image(self.rotate_image(problem[2], -180), choices)
        elif self.is_rotated_clockwise(problem[0], problem[1], -270):
            ans = self.find_similar_image(self.rotate_image(problem[2], -270), choices)

        # Rotate A to B 90 degree anti-clockwise
        elif self.is_rotated_anti_clockwise(problem[0], problem[1], 90):
            ans = self.find_similar_image(self.rotate_image(problem[2], 90), choices)
        elif self.is_rotated_anti_clockwise(problem[0], problem[1], 180):
            ans = self.find_similar_image(self.rotate_image(problem[2], 180), choices)
        elif self.is_rotated_anti_clockwise(problem[0], problem[1], 270):
            ans = self.find_similar_image(self.rotate_image(problem[2], 270), choices)

        # Rotate A to C 90 degree clockwise
        elif self.is_rotated_clockwise(problem[0], problem[2], -90):
            ans = self.find_similar_image(self.rotate_image(problem[1], -90), choices)
        elif self.is_rotated_clockwise(problem[0], problem[2], -180):
            ans = self.find_similar_image(self.rotate_image(problem[1], -180), choices)
        elif self.is_rotated_clockwise(problem[0], problem[2], -270):
            ans = self.find_similar_image(self.rotate_image(problem[1], -270), choices)

        # Rotate A to C 90 degree anti-clockwise
        elif self.is_rotated_anti_clockwise(problem[0], problem[2], 90):
            ans = self.find_similar_image(self.rotate_image(problem[1], 90), choices)
        elif self.is_rotated_anti_clockwise(problem[0], problem[2], 180):
            ans = self.find_similar_image(self.rotate_image(problem[1], 180), choices)
        elif self.is_rotated_anti_clockwise(problem[0], problem[2], 270):
            ans = self.find_similar_image(self.rotate_image(problem[1], 270), choices)

        # B = Flipped A FLIP_LEFT_RIGHT, ans = Flipped C Horizontal
        elif self.is_flipped(problem[0], problem[1], Image.FLIP_LEFT_RIGHT):
            ans = self.find_similar_image(self.rotate_image(problem[2], Image.FLIP_LEFT_RIGHT), choices)

        # B = Flipped A FLIP_TOP_BOTTOM Vertical
        elif self.is_flipped(problem[0], problem[1], Image.FLIP_TOP_BOTTOM):
            ans = self.find_similar_image(self.rotate_image(problem[2], Image.FLIP_TOP_BOTTOM), choices)

        # A,B, C are same
        if self.A_to_B_to_C_Same(problem[0], problem[1], problem[2]):
            ans = self.find_similar_image(problem[0], choices)
        # A and C are same
        if self.A_to_C_Same(problem[0], problem[2]):
            ans = self.find_similar_image(problem[1], choices)
        # A and B are same
        if self.A_to_B_Same(problem[0], problem[1]):
            ans = self.find_similar_image(problem[2], choices)

        if ans:
            return int(ans.name)

    def find_similar_image(self, problem_image, choice_images):
        if type(problem_image) is RavensFigure:
            problem_image_array = self.convert_to_numpy_array(problem_image)
        else:
            problem_image_array = numpy.array(problem_image)

        for choice_image in choice_images:
            if self.compare_images(problem_image_array, self.convert_to_numpy_array(choice_image)) < 0.5:
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
        # imgC = self.convert_to_numpy_array(imageC)
        if self.compare_images(imgA, imgB) < 0.4:
            return True
        return False

    def A_to_B_Same(self, imageA, imageB):
        return self.compare_images(self.convert_to_numpy_array(imageA), self.convert_to_numpy_array(imageB)) < 0.4

    def A_to_C_Same(self, imageA, imageC):
        return self.compare_images(self.convert_to_numpy_array(imageA), self.convert_to_numpy_array(imageC)) < 0.4

    def is_rotated_clockwise(self, imageA, imageB, angle):
        is_rotated_clockwise = self.compare_images(self.convert_to_numpy_array(imageB),
                                                   numpy.array(self.rotate_image(imageA, angle))) < 0.5
        return is_rotated_clockwise

    def is_rotated_anti_clockwise(self, imageA, imageB, angle):
        return self.compare_images(self.convert_to_numpy_array(imageB),
                                   numpy.array(self.rotate_image(imageA, angle))) < 0.5

    def rotate_image(self, problem_image, angle):
        img = Image.open(problem_image.visualFilename)
        rotated_image = img.rotate(angle)
        return rotated_image

    def flip_image(self, problem_image, direction):
        img = Image.open(problem_image.visualFilename)
        flipped_image = img.transpose(direction)
        return flipped_image

    def is_flipped(self, image1, image2, direction):
        # is_flipped = numpy.array_equal(self.convert_to_numpy_array(image2),
        #                                numpy.array(self.flip_image(image1, direction)))
        is_flipped = self.compare_images(self.convert_to_numpy_array(image2),
                                         numpy.array(self.flip_image(image1, direction))) < 0.5
        return is_flipped

    def compare_images(self, image1, image2):
        mse = numpy.mean((image1 - image2) ** 2)
        return mse
