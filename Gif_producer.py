# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 22:48:53 2020

@author: Scrachel
"""

from PIL import Image,ImageDraw,ImageFont

def png_producer():
    '''测试生成png
    '''
    font_size=32
    fnt = ImageFont.truetype(r'C:\\Windows\\Fonts\\msyh.ttc', font_size)
    im = Image.new("RGBA", (640,640), (255,255,255))  #(255,255,255) > white
    draw = ImageDraw.Draw(im)
    draw.text((im.size[0]/2-font_size,(im.size[1]-font_size)/2), u'小静', 
              fill=(55,132,48), font=fnt) 
    im.show()
    
    new_img='C:\\Users\\Scrachel\\Pictures\\New.png'
    im.save(new_img, 'png')  
    
def color_fill_producer(frame_count, font_size, basic_img, word_i, word_all,
                        original_color, list_color, horizontal=1, direction=1):
    '''逐帧渲染 -> 方块式演变
    frame_count -> 帧数
    horizontal -> 水平演变（默认=1） =0 垂直
    direction=1 -> 顺序演进 =0 逆序
    basic_img -> original img
    '''
    fnt = ImageFont.truetype(r'C:\\Windows\\Fonts\\msyh.ttc', font_size)
    
#    color_0 = (255,255,255)
#    color_1 = (-128*frame_count//32*horizontal+128*frame_count//32*direction+151,
#               128*frame_count//32*horizontal-128*frame_count//32*direction+151,
#               128*frame_count//32*horizontal+128*frame_count//32*direction+51)
    color_0 = original_color
    color_1 = (64*frame_count//32*horizontal+64*frame_count//32*(1+direction),
               64*frame_count//32*(horizontal-1)+64*frame_count//32*direction,
               64*frame_count//32*(1+horizontal)-64*frame_count//32*direction)
    color_1 = color_add(color_1, original_color)
    
    #每个小颜色片的平移大小
    translation_size=[32,32]
    
    if not direction:
        sgn = 1
    else:
        sgn = 0
    
    #先整体上色
    if not basic_img:
        im_0 = Image.new("RGBA", (320,320), color_0)  #(255,255,255) white
    else:
        im_0 = basic_img.copy()  #copy image to different address
    draw = ImageDraw.Draw(im_0)

    if horizontal:
        im = Image.new("RGBA", (frame_count+1,32), color_1)
        for x_range in range(im_0.size[0]/translation_size[0]):
            for y_range in range(im_0.size[1]/translation_size[1]):
                im_0.paste(im, (translation_size[0]*x_range
                                +(32-frame_count)*sgn, 
                                translation_size[1]*y_range))
    else:
        im = Image.new("RGBA", (32,frame_count+1), color_1)
        for y_range in range(im_0.size[1]/translation_size[1]):
            for x_range in range(im_0.size[0]/translation_size[0]):
                im_0.paste(im, (translation_size[0]*x_range, 
                                translation_size[1]*y_range
                                +(32-frame_count)*sgn))
    
    #字体上色
    if not word_all:
        word_all=u'小静真好'
        
    word_list = [word_all[i:i + 1] for i in range(0, len(word_all), 1)]

    for i in range(word_i+1):
        #计算出现字的位置
        word_addr = ((320-4*font_size)/2+i*font_size, (320-font_size)/2)
        draw.text(word_addr, word_list[i], fill=list_color[i], font=fnt) 
#        draw.text(word_addr, word_list[i], fill='white', font=fnt) 
    
    return im_0, color_1

def gif_producer():
    frames = []
    frame_size = (320,320)
    color_0 = (255,255,255)
    list_color = [color_0]
    frame_0 = Image.new("RGBA", frame_size, color_0)
    
    word_all=u'小静真好'
    font_size=32
    for i in range(4):
        hori_index = i % 2
        direct_index = i // 2
    
        for frame_count in range(32):
            #frame_0 = Image.new("RGBA", (320,320), (255,255,255))
            new_frame, new_color = color_fill_producer(frame_count, 
                                            font_size=font_size, 
                                            word_all=word_all,
                                            word_i=i, horizontal=hori_index, 
                                            direction=direct_index, 
                                            basic_img=frame_0, 
                                            original_color=color_0,
                                            list_color=list_color)
            frames.append(new_frame)
#            print(frame_count)
        frame_0=new_frame.copy()
        list_color.append(new_color)
        color_0 = new_color
    
    frames[0].save('C:\\Users\\Scrachel\\Pictures\\xiaojing_3.gif', 
          format='GIF', append_images=frames[1:], save_all=True, 
          duration=50, loop=1)
    
def color_add(color_1, color_2):
    if len(color_1) == len(color_2):
        color_0 = ()
        for i in range(len(color_1)):
            color_0 = color_0 + ((color_1[i] + color_2[i])%256,)
        return color_0
    else:
        print('Error! Length of color tumple unequal.')
     
    
if  __name__=="__main__":
    gif_producer()