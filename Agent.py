import math
from PIL import Image
import numpy


class Agent:

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

    def Solve(self, problem):
        if problem.problemType == "2x2":
            print(problem.name)
            ans = self.solve_problems_B(problem)
            print("ans is", ans)
            if ans is not None:
                return ans
            else:
                return 1
        # elif problem.problemType == "3x3" and "Problems C" in problem.problemSetName:
        elif problem.problemType == "3x3":
            ans = self.solve_problem_3x3(problem)
            if ans is not None:
                return ans
            else:
                return 1
        # elif problem.problemType == "3x3" and "Problems D" in problem.problemSetName:
        #     ans = self.solve_problem_3x3(problem)
        #     if ans is not None:
        #         return ans
        #     else:
        #         return 5
        # elif problem.problemType == "3x3" and "Problems E" in problem.problemSetName:
        #     ans = self.solve_problem_3x3(problem)
        #     if ans is not None:
        #         return ans
        #     else:
        #         return 4
        else:
            ans = 1
            return ans

    # elif problem.problemType == "3x3" and "Problems C" in problem.problemSetName:
    #     print("This is Problem C", problem.problemSetName)
    # elif problem.problemType == '3x3' and "Problems D" or "Problems E" in problem.problemSetName:
    #     print("This is problem set D and E", problem.problemSetName)

    def pre_process_images(self, ravens_problem, problem_type):
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

    def solve_problem_3x3(self, ravens_problem):
        self.pre_process_images(ravens_problem, "3x3")
        ans = 1
        # if "Problems D" in ravens_problem.problemSetName:
        #     ans = 4
        # if "Problems E" in ravens_problem.problemSetName:
        #     ans = 7
        # if "Problems C" in ravens_problem.problemSetName:
        #     ans = 2

        options = [self.option1, self.option2, self.option3, self.option4, self.option5, self.option6]

        # ans = self.is_similar_row_images(self.imageA, self.imageB, self.imageC)
        # print("Is True", self.is_similar_row_images(self.imageA, self.imageB, self.imageC))

        if self.is_similar_row_images(self.imageA, self.imageB, self.imageC):
            ans = self.find_horizontal_similar_image(self.mse(numpy.array(self.imageG), numpy.array(self.imageH)),
                                                     self.imageH, options)
        if self.calculate_dark_pixel_ratio(self.imageA, self.imageE) == 0:
            diagonal_ans = self.find_diagonal_similar_images(options)
            if diagonal_ans is None:
                ans = diagonal_ans

        mse1 = math.ceil(self.mse(numpy.array(self.imageB), numpy.array(self.imageD)) / 100)
        mse2 = math.ceil(self.mse(numpy.array(self.imageH), numpy.array(self.imageF)) / 100)
        if self.compare_two_mse(mse1, mse2) <= 5:
            ans = self.find_diagonal_corner_similar_images(options)

        # self.calculate_dark_pixel_ratio(self.imageA, self.imageB)

        # print("diagonal", ans)
        # print(ravens_problem.name)
        return ans
        pass

    def is_similar_row_images(self, image1, image2, image3):
        if self.mse(numpy.array(image1), numpy.array(image2)) == self.mse(numpy.array(image2), numpy.array(image3)):
            return True

    def find_image_D_2x2(self, options):
        difference1 = self.calculate_dark_pixel_ratio(self.imageA, self.imageB)
        difference2 = self.calculate_dark_pixel_ratio(self.imageA, self.imageC)

        for option in options:
            difference3 = self.calculate_dark_pixel_ratio(self.imageC, option)
            difference4 = self.calculate_dark_pixel_ratio(self.imageB, option)
            print(difference1, difference3, difference2, difference4)
            if difference1 == difference3 or difference2 == difference4:
                return options.index(option) + 1
        pass

    def find_horizontal_similar_image(self, mse, image2, options):
        for option in options:
            if mse == self.mse(numpy.array(image2), numpy.array(option)):
                return options.index(option) + 1
        pass

    def find_diagonal_similar_images(self, options):
        mse1 = math.ceil(self.mse(numpy.array(self.imageA), numpy.array(self.imageE)) / 100)
        for option in options:
            mse2 = math.ceil(self.mse(numpy.array(self.imageA), numpy.array(option)) / 100)
            # print(mse1, mse2)
            if abs(mse2 - mse1) < 25:
                return options.index(option) + 1

    def find_diagonal_corner_similar_images(self, options):
        mse1 = math.ceil(self.mse(numpy.array(self.imageA), numpy.array(self.imageG)) / 100)
        for option in options:
            mse2 = math.ceil(self.mse(numpy.array(self.imageC), numpy.array(option)) / 100)
            if mse1 != mse2 and abs(mse1 - mse2 < 10):
                return options.index(option) + 1

    def find_image_transformation_2x2(self, image1, image2):
        if self.mse(numpy.array(image1), numpy.array(image2)) < 0.2:
            return 1
        elif self.is_flipped(image1, image2) != -1:
            return self.is_flipped(image1, image2)
        elif self.is_rotated(image1, image2) != -1:
            return self.is_rotated(image1, image2)
        else:
            return -1

        # return -1

    def map_transformation_to_options(self, transformation, image):

        options = [self.option1, self.option2, self.option3, self.option4, self.option5, self.option6]

        # print("Transformation  is", transformation)

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
            ans = self.find_image_D_2x2(options)
            return ans

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
            if self.mse(img, option_img) <= 11:
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
            rotated_image = numpy.array(self.rotate_image(image1, angle))
            if self.mse(rotated_image, img2) < 50:
                return angle

        # return -1

    def is_flipped(self, image1, image2):
        horizontally_flipped_image1 = numpy.array(self.flip_image(image1, 1))
        vertically_flipped_image1 = numpy.array(self.flip_image(image1, 0))
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

    # /*BEGIN CODE FROM(https://www.geeksforgeeks.org/calculate-the-euclidean-distance-using-numpy/) */
    def calculate_euclidean_distance(self, point1, point2):
        return numpy.sqrt(numpy.sum((point1 - point2) ** 2))

    # /* Code Ends Here */

    # /*BEGIN CODE FROM(https://stackoverflow.com/questions/60664003/how-do-i-get-the-count-dark-pixel-of-an-image-with-numpy) */
    def calculate_dark_pixel_ratio(self, image1, image2):
        total_pixels_image1 = numpy.array(image1)
        total_pixels_image2 = numpy.array(image2)
        dark_pixels1 = numpy.count_nonzero(total_pixels_image1 == 0)
        dark_pixels2 = numpy.count_nonzero(total_pixels_image2 == 0)
        total = abs(dark_pixels1 - dark_pixels2)
        return total

    # /* Code Ends Here */

    def compare_two_mse(self, mse1, mse2):
        return abs(mse2 - mse1) < 25
        pass
