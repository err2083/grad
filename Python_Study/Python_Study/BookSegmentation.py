import cv2
import numpy as np
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getDistance(self, point):
        if type(point) is not Point:
            raise Exception('is not Point Class')
        length = math.sqrt((self.x - point.x)*(self.x - point.x) \
            + (self.y - point.y)*(self.y - point.y))
        return length

class BookSpineDetector:
    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(path, cv2.IMREAD_COLOR)
        if self.img is None:
            raise Exception("이미지 열기 실패")

        self.img_width = int(self.img.shape[1])
        self.img_height = int(self.img.shape[0])

    def __get_line_segment(self,img):
        img_width = int(img.shape[1])
        img_height = int(img.shape[0])
        #양방향 필터 적용 : 경계선을 좀더 강하게 하기 위함
        img_filter = cv2.bilateralFilter(img, -1, 3, 3)

        #관심영역 설정, 세로길이는 책꽂이의 1/3 지점부터 1/4크기만
        img_ROI = img_filter[int(img_height/3):int(img_height/3 + img_height/4),0:int(img_width)]
        img_ROI_height = img_ROI.shape[0]

        #Line Segement Detector
        img_gray = cv2.cvtColor(img_ROI, cv2.COLOR_BGR2GRAY)
        lsd = cv2.createLineSegmentDetector(cv2.LSD_REFINE_NONE)

        #Detect lines in the image
        #lsd.detect(img_gray)[0] Position 0 of the returned tuple are the detected lines
        return lsd.detect(img_gray)[0], img_ROI_height

    def __remove_small_line(self, lsd, height):
        lines = list()
        for point in lsd:
            pt1 = Point(point[0][0], point[0][1])
            pt2 = Point(point[0][2], point[0][3])

            if pt1.getDistance(pt2) < height :
                continue
            pt1.y += self.img_height / 3
            pt2.y += self.img_height / 3
            temp = np.array([])
            if pt1.x == pt2.x:
                lines.append([pt1.x, 0, pt2.x, self.img_height])
            else:
                slope = ((pt2.y)-pt1.y)/(pt2.x-pt1.x)
                intercept = pt1.y - slope*pt1.x
                data = [(-intercept/slope), 0,  ((self.img_height - intercept)/slope), self.img_height]
                if data[0] <0 :
                    data[0] = 0
            lines.append(data)
        lines = np.array(lines, dtype=np.int32)
        lines = lines[np.lexsort(np.transpose(lines)[::-1])]
        return lines
    
    def __remove_small_area(self, lines, area):
        new_lines = list()
        new_lines.append([0,0,0,self.img_height])
        new_lines.append(lines[0])

        prev_pt1 = Point(lines[0][0], lines[0][1])
        prev_pt2 = Point(lines[0][2], lines[0][3])
        for point in lines:
            pt1 = Point(point[0], point[1])
            pt2 = Point(point[2], point[3])

            if abs(prev_pt1.x - pt1.x) < area or \
                abs(prev_pt2.x - pt2.x) < area :
                continue
            new_lines.append(point)
            prev_pt1=pt1
            prev_pt2=pt2
    
        new_lines.append([self.img_width,0,self.img_width,self.img_height])
        lines = new_lines

        lines = np.array(lines)
        lines = lines.reshape(-1,1,4)
        return lines
    
    def __filter_lines(self, lsd):
        lines = self.__remove_small_line(lsd, self.ROI_height/2)
        lines = self.__remove_small_area(lines, 15)
        return lines
    
    def __getBookCandidate(self, points):
        book_candidate = list()
        prev_pt1 = Point(points[0][0][0], points[0][0][1])
        prev_pt2 = Point(points[0][0][2], points[0][0][3])
        for point in points:
            pt1 = Point(point[0][0], point[0][1])
            pt2 = Point(point[0][2], point[0][3])
            contour = np.array([(prev_pt1.x, prev_pt1.y), (pt1.x, pt1.y), (pt2.x, pt2.y), (prev_pt2.x, prev_pt2.y)])
            area = cv2.contourArea(contour)
            if area == 0:
                continue
            black = np.zeros(self.img.shape , dtype=np.uint8)
            mask = np.zeros(self.img.shape , dtype=np.uint8)
            cv2.drawContours(mask, [contour], 0, (255, 255, 255), cv2.FILLED, 8)
            black = cv2.bitwise_and(mask, self.img)
            book_candidate.append((black, contour))
            prev_pt1=pt1
            prev_pt2=pt2
        return book_candidate

    #MASK 적용된 책등이미지, 해당 책등 좌표값반환
    def get_book_spine(self):
        lsd, height = self.__get_line_segment(self.img)
        self.ROI_height = height
        points = self.__filter_lines(lsd)
        return self.__getBookCandidate(points)
