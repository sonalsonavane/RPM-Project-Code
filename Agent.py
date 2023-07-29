# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
from PIL import Image
import numpy
import cv2

import problem_b


# Install Pillow and uncomment this line to access image processing.
# from PIL import Image
# import numpy

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        # Problem Images
        self.imageA = [],
        self.imageB = [],
        self.imageC = [],
        self.imageD = [],
        self.imageE = [],
        self.imageF = [],
        self.imageG = [],
        self.imageH = [],

        # Choice Images
        self.option1 = [],
        self.option2 = [],
        self.option3 = [],
        self.option4 = [],
        self.option5 = [],
        self.option6 = [],
        self.option7 = [],
        self.option8 = []
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
        # if problem.problemType == "2x2" and "Problems B" in problem.problemSetName and "Basic Problem B-01" in problem.name:
        if problem.problemType == "2x2":
            ans = self.solve_problems_B(problem)
            print("ans is", ans)
            print(ans is not None)
            if ans and ans != 'None':
                return ans
        else:
            ans = 1
            return ans
        # if problem.problemType == "2x2":
        #     ans = self.solve_problems_B(problem)
        #     print("ans is", ans)
        #     return ans

    # elif problem.problemType == "3x3" and "Problems C" in problem.problemSetName:
    #     print("This is Problem C", problem.problemSetName)
    # elif problem.problemType == '3x3' and "Problems D" or "Problems E" in problem.problemSetName:
    #     print("This is problem set D and E", problem.problemSetName)

    def pre_process_images(self, ravens_problem, problem_type):
        # for key, value in ravens_problem.figures.items():
        # Problem Images
        self.imageA = Image.open(ravens_problem.figures['A'].visualFilename).convert('L')
        self.imageB = Image.open(ravens_problem.figures['B'].visualFilename).convert('L')
        self.imageC = Image.open(ravens_problem.figures['C'].visualFilename).convert('L')

        # Choice Images
        self.option1 = Image.open(ravens_problem.figures['1'].visualFilename).convert('L')
        self.option2 = Image.open(ravens_problem.figures['2'].visualFilename).convert('L')
        self.option3 = Image.open(ravens_problem.figures['3'].visualFilename).convert('L')
        self.option4 = Image.open(ravens_problem.figures['4'].visualFilename).convert('L')
        self.option5 = Image.open(ravens_problem.figures['5'].visualFilename).convert('L')
        self.option6 = Image.open(ravens_problem.figures['6'].visualFilename).convert('L')

        # self.option6 = Image.open(ravens_problem.figures['6'].visualFilename).convert('L')
        # option6_array = numpy.array(self.option6)
        # print(option6_array)

        if problem_type == '3x3':
            self.imageD = Image.open(ravens_problem.figures['D'].visualFilename).convert('L')
            self.imageE = Image.open(ravens_problem.figures['E'].visualFilename).convert('L')
            self.imageF = Image.open(ravens_problem.figures['F'].visualFilename).convert('L')
            self.imageG = Image.open(ravens_problem.figures['G'].visualFilename).convert('L')
            self.imageH = Image.open(ravens_problem.figures['H'].visualFilename).convert('L')

            self.option7 = Image.open(ravens_problem.figures['7'].visualFilename).convert('L')
            self.option8 = Image.open(ravens_problem.figures['8'].visualFilename).convert('L')
        pass

    def solve_problems_B(self, ravens_problem):
        self.pre_process_images(ravens_problem, "2x2")
        transformation_a_b = self.find_image_transformation_2x2(self.imageA, self.imageB)
        transformation_a_c = self.find_image_transformation_2x2(self.imageA, self.imageC)

        if transformation_a_b != -1:
            return self.map_transformation_to_options(transformation_a_b, self.imageC)
        elif transformation_a_c != -1:
            return self.map_transformation_to_options(transformation_a_c, self.imageB)

    def solve_problem_3x3(self):
        pass

    def find_image_transformation_2x2(self, image1, image2):
        if self.mse(numpy.array(image1), numpy.array(image2)) < 0.2:
            return 1
        elif self.is_rotated(image1, image2) != -1:
            return self.is_rotated(image1, image2)
        elif self.is_flipped(image1, image2) != -1:
            return self.is_flipped(image1, image2)
        else:
            return -1

        pass

    def map_transformation_to_options(self, transformation, image):

        options = [self.option1, self.option2, self.option3, self.option4, self.option5, self.option6]

        print("Transformation  is", transformation)

        if transformation == 1:
            # Equal Image
            ans = self.find_equal_image(image, options)
            return ans
        elif transformation in [90, 180, 270, -45, -90, -180, -270]:
            # rotate image
            ans = self.find_rotated_image(image, options, transformation)
            return ans
        elif transformation == 2:
            ans = self.find_flipped_image(image, options, 0)
            return ans
        elif transformation == 3:
            ans = self.find_flipped_image(image, options, 1)
            return ans
            # flip images
        else:
            return 1

    def find_equal_image(self, image, options):
        img = numpy.array(image)
        for option in options:
            option_img = numpy.array(option)
            if self.mse(img, option_img) <= 0.2:
                return options.index(option) + 1

    def find_flipped_image(self, image, options, axis):
        img = numpy.array(self.flip_image(image, axis))
        for option in options:
            option_img = numpy.array(option)
            if self.mse(img, option_img) < 10:
                return options.index(option) + 1
        # return -1
        pass

    def find_rotated_image(self, image, options, angle):
        img = numpy.array(self.rotate_image(image, angle))
        for option in options:
            option_img = numpy.array(option)
            if self.mse(img, option_img) <= 0.2:
                return options.index(option) + 1
        pass

    def is_rotated(self, image1, image2):
        angles = [90, 180, 270, -45, -90, -180, -270]
        img2 = numpy.array(image2)
        for angle in angles:
            rotated_image = numpy.array(image1.rotate(angle))
            # print("mse value", self.mse(rotated_image, img2))
            if self.mse(rotated_image, img2) <= 11:
                return angle
        return -1


    def is_flipped(self, image1, image2):
        horizontally_flipped_image1 = numpy.array(self.flip_image(image1, 1))
        vertically_flipped_image1 = numpy.array(self.flip_image(image1, 0))

        # print("vertical flipped", self.mse(vertically_flipped_image1, numpy.array(image2)))
        # print("horizontally flipped", self.mse(horizontally_flipped_image1, numpy.array(image2)))

        if self.mse(vertically_flipped_image1, numpy.array(image2)) < 75:
            return 2
        elif self.mse(horizontally_flipped_image1, numpy.array(image2)) < 75:
            return 3
        else:
            return -1

    def flip_image(self, image, direction):
        flipped_image_array = numpy.flip(numpy.array(image), axis=direction)
        return flipped_image_array

    def rotate_image(self, image, angle):
        rotated_img = image.rotate(angle)
        return rotated_img

    # /*BEGIN CODE FROM(https://pyimagesearch.com/2014/09/15/python-compare-two-images/) */
    def mse(self, image1, image2):
        err = numpy.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image2.shape[1])
        return err
        pass

    # /* Code Ends Here */
