import cv2 as cv
import numpy as np
import math
import serial

point = [] 
global mask
point_detec: int 
point_tron: int
point_vuong: int
point_tam_giac: int
index_point: int = 0
height:int 
width: int
def draw_red_circle(event, x, y, flags, param):
    global point_tron, point_detec, point_vuong, point_tam_giac, index_point
    
    if event == cv.EVENT_LBUTTONDBLCLK:
        center = (x, y)
        radius = 1
        color = (0,0,255)
        thickness = 1
        cv.circle(img, center, radius, color, thickness)
        if index_point == 0:
            point_detec = y
        elif index_point == 1:
            point_tron = y
        elif index_point == 2:
            point_vuong = y
        elif index_point == 3:
            point_tam_giac = y
        cv.line(img, (0, y), (width - 1, y), (255,0, 0), 3) 

    
    elif event == cv.EVENT_RBUTTONDBLCLK:
        index_point = (index_point + 1) % 4
        print(index_point)

class item:
    id: int
    shape: int
    approx: any
    center: list
    
    count_tam_giac = 0
    count_vuong = 0
    count_tron = 0
    
    count_ignore = 5
    is_update = 0
    
    is_detected = 0
    def __init__(seft, id, approx, shape):
        seft.shape = 0
        seft.detect_object_many_times(shape)
        seft.id = id
        seft.approx = approx
        seft.x, seft.y, seft.w, seft.h = cv.boundingRect(approx)
        seft.center = [seft.x + int(seft.w/2), seft.y + int(seft.h/2)]
    
    def show(seft):
        output = "id: " + str(seft.id)
        output += ", shape: " + str(seft.shape)
        output += ", center: (" + str(seft.center[0]) + ":" + str(seft.center[1]) + ")"
        output += ", ignore: " + str(seft.count_ignore)
        # output += ", is_update: " + str(seft.is_update)
        print(output)
    def detect_object_many_times(seft, shape):
        if seft.is_detected == 1:
            return
        
        if shape == 3:#TAM_GIAC
            seft.count_tam_giac += 1
            seft.count_vuong = 0
            seft.coung_tron = 0
            
            if seft.count_tam_giac >= 3:
                if seft.shape == 0:#UNKNOW
                    seft.shape = 3 #TAM GIAC
                elif ((seft.shape == 4) | (seft.shape == 5)):
                    seft.shape = 0 #UNKNOW
                    seft.count_vuong = 0
                    seft.count_tam_giac = 0
                    seft.coung_tron = 0
                    # seft.is_detected = 1
                    
        elif shape == 4:#VUONG
            seft.count_vuong += 1
            seft.count_tam_giac = 0
            seft.coung_tron = 0
            
            if seft.count_vuong >= 3:
                if seft.shape == 0: #UNKNOW
                    seft.shape = 4 #VUONG
                elif ((seft.shape == 3) | (seft.shape == 5)):
                    seft.shape = 0 #UNKNOW
                    seft.count_vuong = 0
                    seft.count_tam_giac = 0
                    seft.coung_tron = 0
                    # seft.is_detected = 1
        elif shape == 5:#TRON
            seft.count_tron += 1
            seft.count_vuong = 0
            seft.coung_tam_giac = 0
            
            if seft.count_tron >= 3:
                if seft.shape == 0: #UNKNOW
                    seft.shape = 5 #TRON
                elif ((seft.shape == 3) | (seft.shape == 4)):
                    seft.shape = 0 #UNKNOW
                    seft.count_vuong = 0
                    seft.count_tam_giac = 0
                    seft.coung_tron = 0
                    # seft.is_detected = 1
        
items: list[item] = []
id = 0       
    
#làm tiếp đoạn nhận diện 1 một nhiều lần rồi mới kết luận



#--------------------------------------------------
    
def to_hop(arr, n) -> list:
    stack = []
    result = [] 
    for i in range(len(arr) - n + 1):
        first = arr[i]
        stack.append(first)
        
        for j in range(i + 1, len(arr) - n + 2):
            second = arr[j]
            stack.append(second)
            
            for k in range(j + 1, len(arr)):
                third = arr[k]
                stack.append(third)
                result.append((first, second, third))
                stack.pop()
            stack.pop()
        stack.pop() 
    return result

def convert_approx_to_list(approx) -> list:
    arr = []
    for i in approx:
        x = i[0][0]
        y = i[0][1]
        arr.append((x, y))
    return arr

def distance(point1:tuple, point2:tuple) -> float:
    x_square = (point1[0] - point2[0])
    x_square *= x_square
    
    y_square = (point1[1] - point2[1])
    y_square *= y_square
    
    result = math.sqrt(x_square + y_square)
    return result


def expression_of_line(point1: tuple, point2: tuple) -> tuple:
    #ax + by + c = 0
    u_vector = (point2[0] - point1[0], point2[1] - point1[1])
    n_vector = (-u_vector[1], u_vector[0])
    a = n_vector[0]
    b = n_vector[1]
    #ax + by + c = 0
    # -> c = -ax - by
    c = -a*point1[0] - b*point1[1]
    return (a, b, c)
def assign_point_to_line(line:tuple, point: tuple) -> int:
    a = line[0]
    b = line[1]
    c = line[2]
    x0 = point[0]
    y0 = point[1]
    result = a*x0 + b*y0 + c
    return result

def distance_from_point_to_line(point: tuple, expression_line: tuple) -> float:
    a = expression_line[0]
    b = expression_line[1]
    c = expression_line[2]
    
    tu = a*point[0] + b*point[1] + c
    if tu < 0:
        tu = -tu
    mau_square = a*a + b*b
    mau = math.sqrt(mau_square)
    
    return tu/mau


        
        
#check point1 is middle of point2 and point3
def check_is_middle(point1: tuple, point2: tuple, point3: tuple):
    
    x_min = point2[0]
    if x_min > point3[0]:
        x_min = point3[0]
    x_max = point2[0] + point3[0] - x_min
    
    y_min = point2[1]
    if y_min > point3[1]:
        y_min = point3[1]
    y_max = point2[1] + point3[1] - y_min
    
    print(f"x_min: {x_min}, x_max: {x_max}")
    print(f"y_min: {y_min}, y_max: {y_max}")
    print(f"x_point1: {point1[0]}, y_point1: {point1[1]}")
    
    if ((point1[0] < x_max) & (point1[0] > x_min)):
        print(f"According x: {point1} is middle of {point2} and {point3}")
        return
    
    if ((point1[1] < y_max) & (point1[1] > y_min)):
        print(f"According y {point1} is middle of {point2} and {point3}")
        return 
    
def distance_from_middle_point_to_line(point1:tuple, point2:tuple, point3:tuple) -> float:
    line = expression_of_line(point1, point3)
    distance = distance_from_point_to_line(point2, line)
    return distance

is_removed: int = 0
def filter_for_remove_vectecx(arr: list) -> int:
    global is_removed
    # print(f"Array input in function filter_for_remove_vectecx is: {arr}")
    
    number_of_vertecx = len(arr)
    
    for i in range(number_of_vertecx):
        
        before = i - 1
        after = (i + 1) % len(arr)
        distance = distance_from_middle_point_to_line(arr[before], arr[i], arr[after])
        
        distance_bound = 15
        if distance < distance_bound:
            # print(f"Distance from {arr[i]} to line {arr[before]} -> {arr[after]} is: {distance}")
            # print(f"Remove {arr[i]} because distace small less than {distance_bound}")
            arr.remove(arr[i])
            is_removed = 1
            return filter_for_remove_vectecx(arr)
    
    return number_of_vertecx
        

#getContours according area
def getContours(img, img_contour):
    global items
    global id
    
    contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    print("##############################")
    
    
    for cnt in contours:
        area = cv.contourArea(cnt)
        if ((area > 1500) & (area < 50000)):
            print("------------------")
            print(area)
            cv.drawContours(img_contour, cnt, -1, (255, 0, 0), 2)
            
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            
            x, y, w, h = cv.boundingRect(approx)
            cv.rectangle(img_contour, (x, y), (x+w, y+h), (0,0,255), 2)
            
            center = [x+int(w/2), y+int(h/2)]
            cv.circle(img_contour, center, 1, (0,0,255), 2)
 
            
            # for i in approx:
            #     x = i[0][0]
            #     y = i[0][1]
            #     toa_do = (x, y)
            #     toa_do_str = "(" + str(x) + ":" + str(y) +")"
            #     cv.putText(img_contour, toa_do_str, toa_do, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            
            shape: int = 0
            
            print(f"Number of original vertexc is {len(approx)}")
            
            if len(approx) >= 8:  shape = 5
            else: 
                arr = convert_approx_to_list(approx)
                # print(f"List of points: {arr}")
                shape = filter_for_remove_vectecx(arr)
            print(f"Number of new vertexc is {shape}")
            #detemine center most near
            denta: int = 9999
            index_of_min_denta: int = 99
            
            for i in range(len(items)):
                object = items[i]
                tem =  object.center[1] - center[1] 
                if tem < 0: 
                    continue
                
                if denta > tem:
                    denta = tem
                    index_of_min_denta = i
            
            #not file object saticfile is empty
            if index_of_min_denta == 99:
                #add item into list
                # print(f"Add new object with center {center} to list items")
                new_object = item(id, approx, shape)
                new_object.is_update = 1
                id += 1
                items.append(new_object)
                # print(f"Put text in {(x,y)} with id: {new_object.id}")
                cv.putText(img_contour, str(new_object.shape) + ", id:" + str(new_object.id), 
                           center, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            else:
                #exist object in items most near with it object
                #check for shape of two objects is equal
                
                #update approx and center
                # print(f"Update object with center {center} to object with center {items[index_of_min_denta].center} to list items")
                items[index_of_min_denta].detect_object_many_times(shape)
                items[index_of_min_denta].approx = approx
                items[index_of_min_denta].center = center
                items[index_of_min_denta].is_update = 1
                object = items[index_of_min_denta]
                # print(f"Put text in {(x,y)} with id: {object.id}")
                cv.putText(img_contour, str(object.shape) + ", id:" + str(object.id), 
                           center, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            
            print("------------------")
            
    items_remove = []
    for i in range(len(items)):
        object = items[i]
        if object.is_update == 0:
            items[i].count_ignore -= 1
            if items[i].count_ignore <= 0:
                items_remove.append(object)
        else:
            items[i].count_ignore = 5
            items[i].is_update = 0
            
    for i in items_remove:
        items.remove(i)
        
    for i in items:
        i.show()    
            
    print("##############################")
    
def nothing(x):
    pass


def checkThrough():
    for i in range(len(items)):
        if items[i].is_detected == 1:
            if items[i].shape == 3:
                if ((items[i].center[1] <= point_tam_giac + 15) & (items[i].center[1] >= point_tam_giac - 15)):
                    print("Day tam giac")
                    
                    items[i].show()    
            elif items[i].shape == 4:
                if ((items[i].center[1] <= point_vuong + 15) & (items[i].center[1] >= point_vuong - 15)):
                    print("Day vuong")
                    # data_serial.write("21\r".encode())
                    items[i].show()    
            elif items[i].shape == 5:
                if ((items[i].center[1] <= point_tron + 15) & (items[i].center[1] >= point_tron - 15)):
                    print("Day tron")
                    # data_serial.write("11\r".encode())
                    items[i].show()    
        else:#item hasn't detected
            if ((items[i].center[1] <= point_detec + 15) & (items[i].center[1] >= point_detec - 15)):
                items[i].is_detected = 1
                print("Detected item: ")
                items[i].show()    
        
            
if __name__ == "__main__":
    # data_serial = serial.Serial("COM4", 9600)


    cv.namedWindow("adjust_bar")
    cv.createTrackbar('L-H','adjust_bar', 28, 100, nothing)
    cv.createTrackbar('L-S','adjust_bar', 29, 255, nothing)
    cv.createTrackbar('L-V','adjust_bar', 0, 255, nothing)
    cv.createTrackbar('U-H','adjust_bar', 100, 100, nothing)
    cv.createTrackbar('U-S','adjust_bar', 255, 255, nothing)
    cv.createTrackbar('U-V','adjust_bar', 255, 255, nothing)
    # ---------------------------------
    
    cap = cv.VideoCapture("./video/video1.mp4")
    _, img = cap.read()
    height, width, _ = img.shape
    
    lower_green: any
    upper_green: any
    while True:
        key1 = cv.waitKey(1)
        if key1 == ord('q'):
            break
        elif key1 == ord('n'):
            _, img = cap.read()
        img_original = img.copy()
        cv.imshow("IMAGE ORIGINAL",  img_original)
        cv.setMouseCallback('IMAGE ORIGINAL', draw_red_circle)
        # ----------------------------------
        
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        l_h = cv.getTrackbarPos('L-H', 'adjust_bar')
        l_s = cv.getTrackbarPos('L-S', 'adjust_bar')
        l_v = cv.getTrackbarPos('L-V', 'adjust_bar')
        u_h = cv.getTrackbarPos('U-H', 'adjust_bar')
        u_s = cv.getTrackbarPos('U-S', 'adjust_bar')
        u_v = cv.getTrackbarPos('U-V', 'adjust_bar')

        lower_green = np.array([l_h, l_s, l_v])
        upper_green = np.array([u_h, u_s, u_v])
            
        detec = cv.inRange(hsv, lower_green, upper_green)
        kernel = np.ones((5,5), np.uint8)
        detec = cv.erode(detec, kernel)
        
        # -------------------------------
        
        cv.imshow("DETECT",  detec)
        
    cv.destroyAllWindows()
    
    cap = cv.VideoCapture("./video/video1.mp4")
    
    while True:
        
        _, img = cap.read()
        
        # ----------------------------------
        
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            
        detec = cv.inRange(hsv, lower_green, upper_green)
        kernel = np.ones((5,5), np.uint8)
        detec = cv.erode(detec, kernel)
        
        # -------------------------------
        img_contour = img.copy()
        
        
        cv.imshow("Anh Detec", detec)
        
        getContours(detec, img_contour)
        checkThrough()
        
        cv.line(img_contour, (0, point_detec), (width - 1, point_detec), (255,0, 0), 3) 
        cv.line(img_contour, (0, point_tron), (width - 1, point_tron), (255,0, 0), 3) 
        cv.line(img_contour, (0, point_vuong), (width - 1, point_vuong), (255,0, 0), 3) 
        cv.line(img_contour, (0, point_tam_giac), (width - 1, point_tam_giac), (255,0, 0), 3) 
        
        cv.imshow("Anh Contour", img_contour)
        key = cv.waitKey(0)
        if key == ord('q'):
            continue
        
    
        