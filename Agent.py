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
from PIL import Image, ImageMath
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
        if problem.problemType == "3x3" and "Basic Problem C-01" in problem.name:
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
        # option1 = self.convert_to_numpy_array(ravens_problem.figures['1'])
        # option2 = self.convert_to_numpy_array(ravens_problem.figures['2'])
        # option3 = self.convert_to_numpy_array(ravens_problem.figures['3'])
        # option4 = self.convert_to_numpy_array(ravens_problem.figures['4'])
        # option5 = self.convert_to_numpy_array(ravens_problem.figures['5'])
        # option6 = self.convert_to_numpy_array(ravens_problem.figures['6'])
        # option7 = self.convert_to_numpy_array(ravens_problem.figures['7'])
        # option8 = self.convert_to_numpy_array(ravens_problem.figures['8'])

        choices = []
        problems = []

        for key, value in ravens_problem.figures.items():
            if key in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                problems.append(value)
            if key in ['1', '2', '3', '4', '5', '6']:
                choices.append(value)

        for i in range(0, 8):
            print("Test")

        return 1

    def convert_to_numpy_array(self, value):
        img_array = []
        img = Image.open(value.visualFilename)
        if img:
            img_array = numpy.array(img)
        return img_array

    def dark_pixel_ratio(self, A, B):
        # the difference in percentage of the number of dark-colored pixels with
        # respect
        # to the total number of pixels in the contiguous pixel sets of two
        # matrix
        # cells.
        A = numpy.array(A, dtype='float64')
        B = numpy.array(B, dtype='float64')
        dark_pixel_A_ratio = numpy.count_nonzero(A == 0) / float(A.size)
        # print np.unique(A,return_counts=True)
        dark_pixel_B_ratio = numpy.count_nonzero(B == 0) / float(B.size)
        return dark_pixel_A_ratio - dark_pixel_B_ratio

    def intersection_pixel_ratio(self, A, B):
        # A = A.convert(mode='1')
        # B = B.convert(mode='1')
        AorB = ImageMath.eval("a|b", a=A, b=B)
        AorB = AorB.convert('L')
        # AorB.save("./Problems/Basic Problems B/Basic Problem B-05/AorB.png")
        A = numpy.array(A, dtype='float64')
        B = numpy.array(B, dtype='float64')
        AorB = numpy.array(AorB, dtype='float64')
        return float(numpy.count_nonzero(AorB == 0)) / (numpy.count_nonzero(A == 0) +
                                                        numpy.count_nonzero(B == 0))

    def open_image(self, image, problem, mode='1'):
        fig = problem.figures[image]
        fig = Image.open(fig.visualFilename)
        fig = fig.convert(mode)
        return fig

    def get_dark_pixel_ratio(self):
        dpr_AB = self.dark_pixel_ratio(figA, figB)
        dpr_BC = self.dark_pixel_ratio(figB, figC)
        # r1 = (dpr_AB + dpr_BC)/2.0
        dpr_DE = self.dark_pixel_ratio(figD, figE)
        dpr_EF = self.dark_pixel_ratio(figE, figF)
        # r2 = (dpr_DE + dpr_EF)/2.0
        dpr_GH = self.dark_pixel_ratio(figG, figH)
        dpr_Hi = self.dark_pixel_ratio(figH, options[i])
        # r3 = (dpr_GH + dpr_Hi)/2.0
        dpr_AD = self.dark_pixel_ratio(figA, figD)
        dpr_DG = self.dark_pixel_ratio(figD, figG)
        # c1 = (dpr_AD + dpr_DG)/2.0
        dpr_BE = self.dark_pixel_ratio(figB, figE)
        dpr_EH = self.dark_pixel_ratio(figE, figH)
        # c2 = (dpr_BE + dpr_EH)/2.0
        dpr_CF = self.dark_pixel_ratio(figC, figF)
        dpr_Fi = self.dark_pixel_ratio(figF, options[i])
        # c3 = (dpr_CF + dpr_Fi)/2.0
        if i == 1:
            knn_hor = numpy.array([numpy.sqrt(
                (dpr_AB - dpr_DE) ** 2 + (dpr_AB-dpr_GH) ** 2 + (dpr_DE - dpr_GH) ** 2 + (dpr_BC - dpr_EF) ** 2 + (
                            dpr_BC - dpr_Hi) ** 2 +
                (dpr_EF - dpr_Hi) ** 2)])
            knn_ver = numpy.array([numpy.sqrt(
                (dpr_AD - dpr_BE) ** 2 + (dpr_AD-dpr_CF) ** 2 + (dpr_BE - dpr_CF) ** 2 + (dpr_DG - dpr_EH) ** 2 + (
                            dpr_DG - dpr_Fi) ** 2 +
                (dpr_EH - dpr_Fi) ** 2)])
        else:
            knn_hor = numpy.vstack([knn_hor, [numpy.sqrt((dpr_AB - dpr_DE) ** 2 +
                                                   (dpr_AB - dpr_GH) ** 2 + (dpr_DE - dpr_GH) ** 2 + (
                                                               dpr_BC - dpr_EF) ** 2 + (dpr_BC-dpr_Hi) ** 2 + (
                                                               dpr_EF - dpr_Hi) ** 2)]])
            knn_ver = numpy.vstack([knn_ver, [numpy.sqrt((dpr_AD - dpr_BE) ** 2 +
                                                   (dpr_AD - dpr_CF) ** 2 + (dpr_BE - dpr_CF) ** 2 + (
                                                               dpr_DG - dpr_EH) ** 2 + (dpr_DG-dpr_Fi) ** 2 + (
                                                               dpr_EH - dpr_Fi) ** 2)]])

        knn = knn_hor + knn_ver
        knn_norm = (knn - numpy.min(knn)) / (numpy.max(knn) - numpy.min(knn))
        knn_norm = 1 - knn_norm

        if 1.0 - knn_norm[knn_norm.flatten().argsort()[-2:][0]] < 0.15:
            return -1
        else:
            return numpy.argmin(knn) + 1


