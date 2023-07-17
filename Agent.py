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
from PIL import Image, ImageMath, ImageChops
import numpy
import cv2
from numpy import float64


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
        # if problem.problemType == "3x3" and "Basic Problem C-01" in problem.name:
        #     ans = self.solve_3x3(problem)
        #     if ans != -1:
        #         return ans
        if problem.problemType == "3x3" and "Basic Problem D" in problem.name:
            ans = self.solve_D_basic(problem)
            if ans is not None and ans > -1:
                return ans
            else:
                return 1
        elif problem.problemType == "3x3" and "Basic Problem E" in problem.name:
            ans = self.solve_D_basic(problem)
            if ans is not None and ans > -1:
                return ans
            else:
                return 4
        else:
            return 1

    def get_ravens_image(self, key, value):
        img = Image.open(value.figures[key].visualFilename)
        img = img.convert('1')
        if img:
            return img

    def convert_to_numpy_array(self, value):
        img_array = []
        img = Image.open(value.visualFilename)
        if img:
            img_array = numpy.array(img)
        return img_array

    def solve_D_basic(self, ravens_problem):
        diagonal_comp = self.get_diagonal_comparison(ravens_problem)

        if diagonal_comp == -1:
            knn_3x3 = self.knn_3x3(ravens_problem)
            if knn_3x3 != -1:
                return knn_3x3
            else:
                dpr = self.dpr_knn_3_by_3(ravens_problem)
                if dpr == -1:
                    logical_OR = self.get_logical_or_comparison(ravens_problem)
                    if logical_OR == -1:
                        logical_XOR = self.get_logical_xor_comparison(ravens_problem)
                        if logical_XOR == -1:
                            logical_and = self.get_logical_and_comparison(ravens_problem)
                            if logical_and != -1:
                                return logical_and
                            else:
                                return logical_XOR
                    else:
                        return logical_OR
                else:
                    return dpr
        else:
            return diagonal_comp
        pass

    def knn_3x3(self, problem):
        imageA = self.get_ravens_image('A', problem)
        imageB = self.get_ravens_image('B', problem)
        imageC = self.get_ravens_image('C', problem)
        imageD = self.get_ravens_image('D', problem)
        imageE = self.get_ravens_image('E', problem)
        imageF = self.get_ravens_image('F', problem)
        imageG = self.get_ravens_image('G', problem)
        imageH = self.get_ravens_image('H', problem)

        Option1 = self.get_ravens_image('1', problem)
        Option2 = self.get_ravens_image('2', problem)
        Option3 = self.get_ravens_image('3', problem)
        Option4 = self.get_ravens_image('4', problem)
        Option5 = self.get_ravens_image('5', problem)
        Option6 = self.get_ravens_image('6', problem)
        Option7 = self.get_ravens_image('7', problem)
        Option8 = self.get_ravens_image('8', problem)

        options = {
            1: Option1,
            2: Option2,
            3: Option3,
            4: Option4,
            5: Option5,
            6: Option6,
            7: Option7,
            8: Option8
        }

        # knn_dpr_hor = 0
        # knn_dpr_ver = 0
        # knn_ipr_hor = 0
        # knn_ipr_ver = 0
        for i in range(1, 9):
            dpr_AB = self.get_dark_pixel_ratio(imageA, imageB)
            dpr_BC = self.get_dark_pixel_ratio(imageB, imageC)

            dpr_DE = self.get_dark_pixel_ratio(imageD, imageE)
            dpr_EF = self.get_dark_pixel_ratio(imageE, imageF)

            dpr_GH = self.get_dark_pixel_ratio(imageG, imageH)
            dpr_Hi = self.get_dark_pixel_ratio(imageH, options[i])

            dpr_AD = self.get_dark_pixel_ratio(imageA, imageD)
            dpr_DG = self.get_dark_pixel_ratio(imageD, imageG)

            dpr_BE = self.get_dark_pixel_ratio(imageB, imageE)
            dpr_EH = self.get_dark_pixel_ratio(imageE, imageH)

            dpr_CF = self.get_dark_pixel_ratio(imageC, imageF)
            dpr_Fi = self.get_dark_pixel_ratio(imageF, options[i])

            ipr_AB = self.get_intersection_pixel_ratio(imageA, imageB)
            ipr_BC = self.get_intersection_pixel_ratio(imageB, imageC)

            ipr_DE = self.get_intersection_pixel_ratio(imageD, imageE)
            ipr_EF = self.get_intersection_pixel_ratio(imageE, imageF)

            ipr_GH = self.get_intersection_pixel_ratio(imageG, imageH)
            ipr_Hi = self.get_intersection_pixel_ratio(imageH, options[i])

            ipr_AD = self.get_intersection_pixel_ratio(imageA, imageD)
            ipr_DG = self.get_intersection_pixel_ratio(imageD, imageG)

            ipr_BE = self.get_intersection_pixel_ratio(imageB, imageE)
            ipr_EH = self.get_intersection_pixel_ratio(imageE, imageH)

            ipr_CF = self.get_intersection_pixel_ratio(imageC, imageF)
            ipr_Fi = self.get_intersection_pixel_ratio(imageF, options[i])

            if i == 1:
                knn_dpr_hor = numpy.array([numpy.sqrt(
                    (dpr_AB - dpr_DE) ** 2 + (dpr_AB - dpr_GH) ** 2 + (dpr_DE - dpr_GH) ** 2 + (
                            dpr_BC - dpr_EF) ** 2 + (dpr_BC - dpr_Hi) ** 2 + (dpr_EF - dpr_Hi) ** 2)])
                knn_dpr_ver = numpy.array([numpy.sqrt(
                    (dpr_AD - dpr_BE) ** 2 + (dpr_AD - dpr_CF) ** 2 + (dpr_BE - dpr_CF) ** 2 + (
                            dpr_DG - dpr_EH) ** 2 + (dpr_DG - dpr_Fi) ** 2 + (dpr_EH - dpr_Fi) ** 2)])
                knn_ipr_hor = numpy.array([numpy.sqrt(
                    (ipr_AB - ipr_DE) ** 2 + (ipr_AB - ipr_GH) ** 2 + (ipr_DE - ipr_GH) ** 2 + (
                            ipr_BC - ipr_EF) ** 2 + (ipr_BC - ipr_Hi) ** 2 + (ipr_EF - ipr_Hi) ** 2)])
                knn_ipr_ver = numpy.array([numpy.sqrt(
                    (ipr_AD - ipr_BE) ** 2 + (ipr_AD - ipr_CF) ** 2 + (ipr_BE - ipr_CF) ** 2 + (
                            ipr_DG - ipr_EH) ** 2 + (ipr_DG - ipr_Fi) ** 2 + (ipr_EH - ipr_Fi) ** 2)])
            else:
                knn_dpr_hor = numpy.vstack([knn_dpr_hor, [numpy.sqrt(
                    (dpr_AB - dpr_DE) ** 2 + (dpr_AB - dpr_GH) ** 2 + (dpr_DE - dpr_GH) ** 2 + (
                            dpr_BC - dpr_EF) ** 2 + (dpr_BC - dpr_Hi) ** 2 + (dpr_EF - dpr_Hi) ** 2)]])
                knn_dpr_ver = numpy.vstack([
                    knn_dpr_ver,
                    [numpy.sqrt(
                        (dpr_AD - dpr_BE) ** 2 +
                        (dpr_AD - dpr_CF) ** 2 +
                        (dpr_BE - dpr_CF) ** 2 +
                        (dpr_DG - dpr_EH) ** 2 +
                        (dpr_DG - dpr_Fi) ** 2 +
                        (dpr_EH - dpr_Fi) ** 2
                    )]
                ])

                knn_ipr_hor = numpy.vstack([
                    knn_ipr_hor,
                    [numpy.sqrt(
                        (ipr_AB - ipr_DE) ** 2 +
                        (ipr_AB - ipr_GH) ** 2 +
                        (ipr_DE - ipr_GH) ** 2 +
                        (ipr_BC - ipr_EF) ** 2 +
                        (ipr_BC - ipr_Hi) ** 2 +
                        (ipr_EF - ipr_Hi) ** 2
                    )]
                ])

                knn_ipr_ver = numpy.vstack([
                    knn_ipr_ver,
                    [numpy.sqrt(
                        (ipr_AD - ipr_BE) ** 2 +
                        (ipr_AD - ipr_CF) ** 2 +
                        (ipr_BE - ipr_CF) ** 2 +
                        (ipr_DG - ipr_EH) ** 2 +
                        (ipr_DG - ipr_Fi) ** 2 +
                        (ipr_EH - ipr_Fi) ** 2
                    )]
                ])

        knn = knn_dpr_hor + knn_dpr_ver + knn_ipr_hor + knn_ipr_ver
        knn_norm = (knn - numpy.min(knn)) / (numpy.max(knn) - numpy.min(knn))
        knn_norm = 1 - knn_norm

        if 1.0 - knn_norm[knn_norm.flatten().argsort()[-2:][0]] < 0.4:  # 10% percent
            return -1
        else:
            return numpy.argmin(knn) + 1
        pass

    def solve_E_basic(self):
        pass

    def get_dark_pixel_ratio(self, imgX, imgY):
        X = numpy.array(imgX)
        Y = numpy.array(imgY)
        dp_ratio_X = numpy.count_nonzero(X == 0) / float(X.size)
        dp_ratio_Y = numpy.count_nonzero(Y) / float(Y.size)
        return dp_ratio_X - dp_ratio_Y

    def get_intersection_pixel_ratio(self, X, Y):
        XorY = ImageMath.eval("x|y", x=X, y=Y)
        XorY = XorY.convert('L')
        X = numpy.array(X, dtype=float64)
        Y = numpy.array(Y, dtype=float64)
        XorY = numpy.array(XorY)
        return float(numpy.count_nonzero(XorY == 0)) / (numpy.count_nonzero(X == 0) +
                                                        numpy.count_nonzero(Y == 0))

    def get_diagonal_comparison(self, problem):
        imageA = self.get_ravens_image('A', problem)
        imageE = self.get_ravens_image('E', problem)

        Option1 = self.get_ravens_image('1', problem)
        Option2 = self.get_ravens_image('2', problem)
        Option3 = self.get_ravens_image('3', problem)
        Option4 = self.get_ravens_image('4', problem)
        Option5 = self.get_ravens_image('5', problem)
        Option6 = self.get_ravens_image('6', problem)
        Option7 = self.get_ravens_image('7', problem)
        Option8 = self.get_ravens_image('8', problem)

        options = {
            1: Option1,
            2: Option2,
            3: Option3,
            4: Option4,
            5: Option5,
            6: Option6,
            7: Option7,
            8: Option8
        }

        A_E_SS = self.get_similarity_score(imageA, imageE)
        if A_E_SS >= 97:
            similarity_array = []
            for i in range(1, 9):
                similarity_array.append(self.get_similarity_score(imageA, options[i]))
                return similarity_array.index(max(similarity_array)) + 1

        return -1

    def get_logical_xor_comparison(self, problem):

        imageA = self.get_inverted_image('A', problem)
        imageB = self.get_inverted_image('B', problem)
        imageC = self.get_inverted_image('C', problem)
        imageD = self.get_inverted_image('D', problem)
        imageE = self.get_inverted_image('E', problem)
        imageF = self.get_inverted_image('F', problem)
        imageG = self.get_inverted_image('G', problem)
        imageH = self.get_inverted_image('H', problem)

        Option1 = self.get_inverted_image('1', problem)
        Option2 = self.get_inverted_image('2', problem)
        Option3 = self.get_inverted_image('3', problem)
        Option4 = self.get_inverted_image('4', problem)
        Option5 = self.get_inverted_image('5', problem)
        Option6 = self.get_inverted_image('6', problem)
        Option7 = self.get_inverted_image('7', problem)
        Option8 = self.get_inverted_image('8', problem)

        options = {
            1: Option1,
            2: Option2,
            3: Option3,
            4: Option4,
            5: Option5,
            6: Option6,
            7: Option7,
            8: Option8
        }

        A_XOR_B = imageA._new(imageA.im.chop_xor(imageB.im))
        D_XOR_E = imageD._new(imageD.im.chop_xor(imageE.im))
        G_XOR_H = imageG._new(imageG.im.chop_xor(imageH.im))

        A_OR_B_C_similarity = self.get_similarity_score(A_XOR_B, imageC)
        D_OR_E_F_similarity = self.get_similarity_score(D_XOR_E, imageF)
        if A_OR_B_C_similarity >= 90.0 and D_OR_E_F_similarity >= 90.0:
            similarities = []
            for i in range(1, 9):
                similarities.append(self.get_similarity_score(G_XOR_H, options[i]))
            return similarities.index(max(similarities)) + 1
        else:
            return -1

    def get_logical_or_comparison(self, problem):

        imageA = self.get_inverted_image('A', problem)
        imageB = self.get_inverted_image('B', problem)
        imageC = self.get_inverted_image('C', problem)
        imageD = self.get_inverted_image('D', problem)
        imageE = self.get_inverted_image('E', problem)
        imageF = self.get_inverted_image('F', problem)
        imageG = self.get_inverted_image('G', problem)
        imageH = self.get_inverted_image('H', problem)

        Option1 = self.get_inverted_image('1', problem)
        Option2 = self.get_inverted_image('2', problem)
        Option3 = self.get_inverted_image('3', problem)
        Option4 = self.get_inverted_image('4', problem)
        Option5 = self.get_inverted_image('5', problem)
        Option6 = self.get_inverted_image('6', problem)
        Option7 = self.get_inverted_image('7', problem)
        Option8 = self.get_inverted_image('8', problem)

        options = {
            1: Option1,
            2: Option2,
            3: Option3,
            4: Option4,
            5: Option5,
            6: Option6,
            7: Option7,
            8: Option8
        }

        A_OR_B = imageA._new(imageA.im.chop_or(imageB.im))
        D_OR_E = imageD._new(imageD.im.chop_or(imageE.im))
        G_OR_H = imageG._new(imageG.im.chop_or(imageH.im))

        A_OR_B_C_similarity = self.get_similarity_score(A_OR_B, imageC)
        D_OR_E_F_similarity = self.get_similarity_score(D_OR_E, imageF)
        if A_OR_B_C_similarity >= 96.0 and D_OR_E_F_similarity >= 96.0:
            similarities = []
            for i in range(1, 9):
                similarities.append(self.get_similarity_score(G_OR_H, options[i]))
            return similarities.index(max(similarities)) + 1
        else:
            return -1

    def insert_image(self):
        pass

    def get_logical_and_comparison(self, problem):

        imageA = self.get_inverted_image('A', problem)
        imageB = self.get_inverted_image('B', problem)
        imageC = self.get_inverted_image('C', problem)
        imageD = self.get_inverted_image('D', problem)
        imageE = self.get_inverted_image('E', problem)
        imageF = self.get_inverted_image('F', problem)
        imageG = self.get_inverted_image('G', problem)
        imageH = self.get_inverted_image('H', problem)

        Option1 = self.get_inverted_image('1', problem)
        Option2 = self.get_inverted_image('2', problem)
        Option3 = self.get_inverted_image('3', problem)
        Option4 = self.get_inverted_image('4', problem)
        Option5 = self.get_inverted_image('5', problem)
        Option6 = self.get_inverted_image('6', problem)
        Option7 = self.get_inverted_image('7', problem)
        Option8 = self.get_inverted_image('8', problem)

        options = {
            1: Option1,
            2: Option2,
            3: Option3,
            4: Option4,
            5: Option5,
            6: Option6,
            7: Option7,
            8: Option8
        }

        A_AND_B = ImageChops.logical_and(imageA, imageB)
        A_AND_B_AND_C = ImageChops.logical_and(A_AND_B, imageC)
        # D_AND_E = ImageChops.logical_and(imageD, imageE)
        G_AND_H = ImageChops.logical_and(imageG, imageH)

        similarities = []
        for i in range(1, 9):
            G_AND_H_AND_i = ImageChops.logical_and(G_AND_H, options[i])
            similarities.append(self.get_similarity_score(A_AND_B_AND_C, G_AND_H_AND_i))

        max1=0
        max2=0
        if similarities:
            max1 = max(similarities)
            print(max1, "max1")

            max2 = 0
            for i in similarities:
                if i != max1:
                    max2 = max(i, max2)
            print(max2, "max2")
        if max1 - max2 <= 2:
            return similarities.index(max(similarities)) + 1
        else:
            return -1



    def get_inverted_image(self, key, value):
        img = Image.open(value.figures[key].visualFilename)
        img = img.convert('1')
        img = ImageChops.invert(img)
        return img

    def get_similarity_score(self, imageX, imageY):
        imageX = imageX.convert('1')
        imageY = imageY.convert('1')
        pixels = ImageChops.difference(imageX, imageY).getdata()
        total_pixel_count = len(pixels)
        white_pixel_count = 0

        for pixel in pixels:
            if pixel != 0:
                white_pixel_count = white_pixel_count + 1

        score = 100 - 100 * (white_pixel_count / float(total_pixel_count))
        return score

    # get Sum of squared errors
    def get_SSE(self, X, Y):
        X = X * (1.0 / X.max())
        Y = X * (1.0 / Y.max())

        X = numpy.array(X, dtype=float64)
        Y = numpy.array(Y, dtype=float64)

        sse = numpy.sum((X - Y) ** 2)
        sse = sse / float(X.shape[0] * Y.shape[1])
        return sse

    def dpr_knn_3_by_3(self, problem):
        figA = self.get_ravens_image('A', problem)
        figB = self.get_ravens_image('B', problem)
        figC = self.get_ravens_image('C', problem)
        figD = self.get_ravens_image('D', problem)
        figE = self.get_ravens_image('E', problem)
        figF = self.get_ravens_image('F', problem)
        figG = self.get_ravens_image('G', problem)
        figH = self.get_ravens_image('H', problem)

        Option1 = self.get_ravens_image('1', problem)
        Option2 = self.get_ravens_image('2', problem)
        Option3 = self.get_ravens_image('3', problem)
        Option4 = self.get_ravens_image('4', problem)
        Option5 = self.get_ravens_image('5', problem)
        Option6 = self.get_ravens_image('6', problem)
        Option7 = self.get_ravens_image('7', problem)
        Option8 = self.get_ravens_image('8', problem)
        options = {
            1: Option1,
            2: Option2,
            3: Option3,
            4: Option4,
            5: Option5,
            6: Option6,
            7: Option7,
            8: Option8
        }

        # knn_dpr_hor = 0
        # knn_dpr_ver = 0
        # knn_ipr_hor = 0
        # knn_ipr_ver = 0

        for i in range(1, 9):
            dpr_AB = self.get_dark_pixel_ratio(figA, figB)
            dpr_BC = self.get_dark_pixel_ratio(figB, figC)
            # r1 = (dpr_AB + dpr_BC) / 2.0
            dpr_DE = self.get_dark_pixel_ratio(figD, figE)
            dpr_EF = self.get_dark_pixel_ratio(figE, figF)
            # r2 = (dpr_DE + dpr_EF) / 2.0
            dpr_GH = self.get_dark_pixel_ratio(figG, figH)
            dpr_Hi = self.get_dark_pixel_ratio(figH, options[i])
            # r3 = (dpr_GH + dpr_Hi) / 2.0
            dpr_AD = self.get_dark_pixel_ratio(figA, figD)
            dpr_DG = self.get_dark_pixel_ratio(figD, figG)
            # c1 = (dpr_AD + dpr_DG) / 2.0
            dpr_BE = self.get_dark_pixel_ratio(figB, figE)
            dpr_EH = self.get_dark_pixel_ratio(figE, figH)
            # c2 = (dpr_BE + dpr_EH) / 2.0
            dpr_CF = self.get_dark_pixel_ratio(figC, figF)
            dpr_Fi = self.get_dark_pixel_ratio(figF, options[i])
            # c3 = (dpr_CF + dpr_Fi) / 2.0

            if i == 1:
                # option_values = np.array([r1,r2,r3,c1,c2,c3])
                # square root of sum of squares
                # knn = np.array([np.sqrt((r1-r3)**2 + (r2-r3)**2 + (c1-c3)**2 + (c2-c3)**2)])
                knn_hor = numpy.array(
                    [numpy.sqrt((dpr_AB - dpr_DE) ** 2 + (dpr_AB - dpr_GH) ** 2 + (dpr_DE - dpr_GH) ** 2 + (
                            dpr_BC - dpr_EF) ** 2 + (dpr_BC - dpr_Hi) ** 2 + (dpr_EF - dpr_Hi) ** 2)])
                knn_ver = numpy.array(
                    [numpy.sqrt((dpr_AD - dpr_BE) ** 2 + (dpr_AD - dpr_CF) ** 2 + (dpr_BE - dpr_CF) ** 2 + (
                            dpr_DG - dpr_EH) ** 2 + (dpr_DG - dpr_Fi) ** 2 + (dpr_EH - dpr_Fi) ** 2)])
            else:
                # option_values = np.vstack([option_values, [r1,r2,r3,c1,c2,c3]])
                knn_hor = numpy.vstack([knn_hor, [numpy.sqrt(
                    (dpr_AB - dpr_DE) ** 2 + (dpr_AB - dpr_GH) ** 2 + (dpr_DE - dpr_GH) ** 2 + (
                            dpr_BC - dpr_EF) ** 2 + (dpr_BC - dpr_Hi) ** 2 + (dpr_EF - dpr_Hi) ** 2)]])
                knn_ver = numpy.vstack([knn_ver, [numpy.sqrt(
                    (dpr_AD - dpr_BE) ** 2 + (dpr_AD - dpr_CF) ** 2 + (dpr_BE - dpr_CF) ** 2 + (
                            dpr_DG - dpr_EH) ** 2 + (dpr_DG - dpr_Fi) ** 2 + (dpr_EH - dpr_Fi) ** 2)]])

        # Normalize data
        knn = knn_hor + knn_ver
        knn_norm = (knn - numpy.min(knn)) / (numpy.max(knn) - numpy.min(knn))
        knn_norm = 1 - knn_norm
        if 1.0 - knn_norm[knn_norm.flatten().argsort()[-2:][0]] < 0.15:  # 1.8% percent
            return -1
        else:
            return numpy.argmin(knn) + 1
