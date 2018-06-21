fig = plt.figure(figsize=(12, 14))
idx = 1

a1 = 0.1
global gll, grl # global left and right lines
try:
    del(gll)
    del(grl)
except:
    pass
    
def predict(lines, y=None, a1=0.8):
    """ Combine several lines and predict by y.
    """
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    if len(lines) > 0:
        average_x1 = int(sum(map(lambda p: p[0], lines)) / len(lines))
        average_y1 = int(sum(map(lambda p: p[1], lines)) / len(lines))
        average_x2 = int(sum(map(lambda p: p[2], lines)) / len(lines))
        average_y2 = int(sum(map(lambda p: p[3], lines)) / len(lines))
        if y:
            slope = (average_x2-average_x1)/(average_y2-average_y1)
            # Decide whether to replace point 1 or point 2, based on which one closer to bottom
            if average_y1 > average_y2:
                x1 = average_x2
                y1 = average_y2
            else:
                x1 = average_x1
                y1 = average_y1
            x2 = int(slope*(y-y1) + x1)
            y2 = y
        else:
            x1 = average_x1
            y1 = average_y1
            x2 = average_x2
            y2 = average_y2
            
    return (x1, y1, x2, y2)
    
def draw_predictd_lines(img, lines, y=None, color=[200, 0, 0], thickness=10, slope_threshold=0.5, show_all=False, duo_colors=False):
    """ Draw predictd lines
    
    First, we group all left and right lines, then calculate the middle lines for each.
    Args:
        y: predict x based on this y value.
        slope_threshold: We don't want to include lines with slope lower than this.
    """
    global gll, grl # global left and right lines
    left_lines = []
    right_lines = []
    main_color = color
    if duo_colors:
        alt_color=[0, 255, 0]
    else:
        alt_color = color
    for line in lines:
        for x1,y1,x2,y2 in line:
            slope = (y2-y1)/(x2-x1)
            # Use square instead of abs for slightly faster calculation
            if slope**2 > slope_threshold**2:
                if slope < 0:
                    # left lane
                    left_lines.append((x1, y1, x2, y2))
                    if show_all:
                        cv2.line(img, (x1, y1), (x2, y2), main_color, thickness)
                else:
                    # right lane
                    right_lines.append((x1, y1, x2, y2))
                    if show_all:
                        cv2.line(img, (x1, y1), (x2, y2), alt_color, thickness)

    if not show_all:
        x1, y1, x2, y2 = predict(left_lines, y)
        try:
            x1 = int(gll[0]*(1-a1) + x1*a1)
            x2 = int(gll[2]*(1-a1) + x2*a1)
            y1 = int(gll[1]*(1-a1) + y1*a1)
            y2 = int(gll[3]*(1-a1) + y2*a1)
        except:
            pass

        gll = [x1, y1, x2, y2]
        cv2.line(img, (x1, y1), (x2, y2), main_color, thickness)

        x1, y1, x2, y2 = predict(right_lines, y)
        try:
            x1 = int(grl[0]*(1-a1) + x1*a1)
            x2 = int(grl[2]*(1-a1) + x2*a1)
            y1 = int(grl[1]*(1-a1) + y1*a1)
            y2 = int(grl[3]*(1-a1) + y2*a1)
        except:
            pass
        grl = [x1, y1, x2, y2]
        cv2.line(img, (x1, y1), (x2, y2), alt_color, thickness)
        
        

def processing_img(raw_image, get_vertices=False):
    grayImg = grayscale(raw_image)

    image = gaussian_blur(grayImg, kernel_size=3)

    image = canny(image, low_threshold=50, high_threshold=150)

    imshape = image.shape
    vertices = np.array([[(0.1*imshape[1], 1*imshape[0]),
                          (0.45*imshape[1], 0.60*imshape[0]),
                          (0.57*imshape[1], 0.60*imshape[0]),
                          (1*imshape[1], 1*imshape[0])]], dtype=np.int32)
    image = region_of_interest(image, vertices)

    hough = hough_lines(image,
                        rho=2,
                        theta=np.pi/180,
                        threshold=50,
                        min_line_len=120,
                        max_line_gap=150)

    result = weighted_img(hough, raw_image)

    if get_vertices:
        return (result, vertices)
    else:
        return result
    
for img in os.listdir("test_images/"):
    raw_image = (mpimg.imread(os.path.join("test_images",img))).astype('uint8')
    
    image, vertices = processing_img(raw_image, get_vertices=True)
    try:
        del(gll)
        del(grl)
    except:
        pass
    
    a=fig.add_subplot(4,2,idx)

    # Code to show region of interest
    x = [vertices[0,0,0], vertices[0,1,0], vertices[0,2,0], vertices[0,3,0]]
    y = [vertices[0,0,1], vertices[0,1,1], vertices[0,2,1], vertices[0,3,1]]
    plt.plot(x, y, 'b--', lw=4)
    
    plt.imshow(image)
    idx+=1