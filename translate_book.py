# translate book from given pkl file

import pyautogui as pg 
import time
import pyperclip as clip
import pandas as pd
import tagui as t
import sys 
MODIFIER = ""
if sys.platform == 'darwin':
    MODIFIER = '[cmd]'
elif sys.platform == 'linux':
    MODIFIER = '[ctrl]'
else:
    raise NotImplementedError(f"platform {sys.platform} not implented!")
import cv2 as cv
import pyautogui as pg 
import numpy as np
import collections
# class Point():
#     def __init__(self, left, top, width, height):
#         self.left = int(left) 
#         self.top = int(top) 
#         self.width = int(width) 
#         self.height = int(height) 
Box = collections.namedtuple('Box', 'left top width height')
def locate(icon: str = None): 
    # used to replace the bad pyautogui 
    # return (left, top, width, height) in pyautogui style, where 0,0 is top left.

    img_rgb = cv.imread(icon)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    full = pg.screenshot()
    filename = "full.png"
    full.save(filename)
    template = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    w, h = img_gray.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    ratio = template.shape[1]/pg.size()[0]
    print(template.shape[1], pg.size()[0])
    for pt in zip(*loc[::-1]):
        (left, top, width, height )= (int(pt[0]), int(pt[1]), w, h)
        x,y,xw,xh = left/ratio, top/ratio, width/ratio, height/ratio
        # return Point(x,y,xw,xh)
        return Box(x,y,xw,xh)

def click(icon: str = None):
    try:
        box = locate(icon)
    except Exception as e:
        print(f"icon {icon} not found!")
    x,y,w,h =box.left,box.top,box.width,box.height
    pg.moveTo(x,y,duration=0.3)
    pg.click(x,y-2*h, clicks=2, interval=1)

def translate(inputs):
    t.init(visual_automation = True)
    t.url('https://translate.google.com/?sl=zh-CN&tl=en&text=%3Ctag%3E&op=translate')
    t.wait(3)
    t.keyboard('[esc]')
    t.click('<tag>')
    clip.copy(inputs)
    str = clip.paste() + '<tag>'
    # pg.hotkey('command','v')
    
    t.keyboard(f'{MODIFIER}a')
    t.keyboard(f'{MODIFIER}v')
    # 等待翻译结果
    time.sleep(2)
    # t.click('保存翻译')
    # t.click("//button[@aria-label='保存翻译']")
    for i in range(0,8):
        t.wait(0.5)
        t.keyboard('[tab]')
    # click('icon/mac_save.png')
    # pg.hotkey('command','down')
    t.keyboard(f'{MODIFIER}[down]')
    # click('icon/mac_copy.png')
    try:
        t.click('复制译文')
    except Exception as e:
        print(e)
    try:
        t.click('Copy translation')
    except Exception as e:
        print(e)
    while clip.paste() == str:
        pass 
    str = clip.paste()
    t.close()
    return str
# X, Y = 1381,-798
# # pg.moveTo(X, Y, duration=1.1) 
# pg.click(X, Y, duration = 0) # , 自动move to
# # pg.write('Chrome')
# # pg.press('enter')
# # pg.hotkey('command','a')

if __name__ == "__main__":
    df = pd.read_pickle('dataset.pkl')
    for index,row in df.iterrows():
        if (row['en'] == None):
            row_en = translate(row['cn'])
            row['en'] = row_en
            df.to_pickle('dataset.pkl')