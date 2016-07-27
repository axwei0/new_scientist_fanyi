#-*- coding:utf-8 -*-
import pygame
#/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc为树莓派的汉字字体库路径，请自行替换
def tToP(text):
        pygame.init()
        file = open(text, 'r')
        font = pygame.font.Font("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 20)
        done = 0
        lines = []
        line = ''
        i = 0
        tempWord = ''
        while not done:
                aLine = file.readline()
                aLine = aLine.replace('\r\n', '')
                if (aLine != ''):
                        for charactor in aLine.decode('utf-8'):
                                # 微博图片大小设定为440,根据这个大小来进行换行
                                if font.size(line + tempWord)[0] > 440:
                                        lines.append(line)
                                        line = ''
                                        # 把余出的英文单词留到下一行
                                        tempWord = tempWord + charactor
                                else:
                                        tempWord = tempWord + charactor
                                        # 对英文单词的换行进行判断
                                        if charactor == ' ':
                                                line = line + tempWord
                                                tempWord = ''
                                # 设定为419是因为字符大小为20;汉字之间没有空格,换行必须增加判断
                                if font.size(tempWord)[0] > 419 and font.size(tempWord)[0] <= 440:
                                        lines.append(tempWord)
                                        tempWord = ''
                        lines.append(line + tempWord)
                        line = ''
                        tempWord = ''
                else:
                        done = 1
        line_height = font.size(line)[1]
        img_height = line_height * (len(lines) + 1)
        rtext = pygame.Surface((440, img_height))
        rtext.fill([255, 255, 255])
        for line in lines:
                rtext1 = font.render(line, True, (0, 0, 0), (255, 255, 255))
                rtext.blit(rtext1, (0, i * line_height))
                i = i + 1
        pygame.image.save(rtext, text + ".jpg")

        file.close()




















