from random import randint
from math import floor
import pygame as pg
import math


ACTION_NONE = {'forward': False, 'backward': False,
               'left': False, 'right': False, 'attack': False}


class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [4, 2, 1, 1]
        self.action = ACTION_NONE.copy()
        self.playerID = helper.get_self_id()
        self.walls = self.helper.get_wall_position()

    def reset(self):
        self.action = ACTION_NONE.copy()

    def avoidbullet(self):
        bullet = self.helper.get_bullet_info()
        # print(bullet)
        # print('==========')
        for i in bullet:
            myPos = self.helper.get_self_position()
            speed = i.get('speed')
            angle = myPos.angle_to(speed)
            angle = (angle*180)/math.pi  # rad轉deg
            if angle > 0:  # 轉成最小同位角
                angle = angle % 360
            else:
                if abs(angle) % 360 == 0:
                    angle = angle + 360 * abs(angle) // 360
                else:
                    angle = angle + 360 * ((abs(angle) // 360) + 1)

            print(angle)

    def avoid_RE_field(self):
        rePos = self.helper.get_nearest_RE_position()
        selfpos = self.helper.get_self_position()
        selfdir = self.helper.get_self_direction()
        x1, y1 = rePos[0], rePos[1]
        x2, y2 = selfpos[0], selfpos[1]
        print(x1, y1, x2, y2, selfdir[0], selfdir[1], sep=' ')
        self.action['left'] = True
        if x1 > x2:
            if y1 > y2:  # re在me右下
                if (selfdir[0] < 0.85 and selfdir[0] > 0.65) and (selfdir[1] < 0.85 and selfdir[1] > 0.65):
                    self.action['attack'] = True
                else:
                    self.action['left'] = True
            else:  # re在me右上
                if (selfdir[0] < 0.85 and selfdir[0] > 0.65) and (selfdir[1] > -0.85 and selfdir[1] < -0.65):
                    self.action['attack'] = True
                else:
                    self.action['left'] = True
        else:
            if y1 > y2:  # re在me左下
                if (selfdir[0] > -0.85 and selfdir[0] > -0.65) and (selfdir[1] < 0.85 and selfdir[1] > 0.65):
                    self.action['attack'] = True
                else:
                    self.action['left'] = True
            else:  # re在me左上
                if (selfdir[0] > -0.85 and selfdir[0] < -0.65) and (selfdir[1] > -0.85 and selfdir[1] < -0.65):
                    self.action['attack'] = True
                else:
                    self.action['left'] = True

    def buff(self):  # 找buff
        buffpos = self.helper.get_nearest_item_info()['position']
        selfpos = self.helper.get_self_position()
        selfdir = self.helper.get_self_direction()
        x1, y1 = buffpos[0], buffpos[1]
        x2, y2 = selfpos[0], selfpos[1]
        if x1 - x2 > 0.5:  # buff在右
            if (selfdir[0] <= 1 and selfdir[0] > 0.95) and (selfdir[1] > -0.05 and selfdir[1] < 0.05):
                self.action['forward'] = True
            else:
                self.action['left'] = True
        elif x2 - x1 > 0.5:  # buff在左
            if (selfdir[0] >= -1 and selfdir[0] < -0.95) and (selfdir[1] > -0.05 and selfdir[1] < 0.05):
                self.action['forward'] = True
            else:
                self.action['left'] = True
        else:
            if y1 - y2 > 0.5:  # buff在下
                if (selfdir[0] > -0.05 and selfdir[0] < 0.05) and (selfdir[1] <= 1 and selfdir[1] > 0.95):
                    self.action['forward'] = True
                else:
                    self.action['left'] = True
            elif y2 - y1 > 0.5:  # buff在上
                if (selfdir[0] > -0.05 and selfdir[0] < 0.05) and (selfdir[1] >= -1 and selfdir[1] < -0.95):
                    self.action['forward'] = True
                else:
                    self.action['left'] = True
        # if ((selfpos-buffpos).normalize() - self.helper.get_self_direction()).magnitude() < 0.1:
        #     self.action['forward'] = True
        # else:
        #     self.action['left'] = True

    def buff_decide(self):  # 判斷與目標間是否有障礙
        self_position = self.helper.get_self_position()
        nearest_item = self.helper.get_nearest_item_info().get("position")
        x1, y1 = self_position[0], self_position[1]
        x2, y2 = nearest_item[0], nearest_item[1]
        if floor(x1) == floor(x2):
            # y下去比
            y1, y2 = floor(y1) + 0.5, floor(y2) + 0.5
            x1, x2 = floor(x1) + 0.5, floor(x2) + 0.5
            if y1 >= y2:
                for i in range(int(y1-y2)+2):
                    if pg.Vector2([x1, y2]) in self.walls:
                        #print('obstacle detected 1')
                        return False
                    y2 += 1
                #print('non-detected 1')
                return True

            else:
                for i in range(int(y2-y1)+2):
                    if pg.Vector2([x1, y1]) in self.walls:
                        #print('obstacle detected 2')
                        return False
                    y1 += 1
                #print('non-detected 2')
                return True

        elif floor(y1) == floor(y2):
            # x下去比
            y1, y2 = floor(y1) + 0.5, floor(y2) + 0.5
            x1, x2 = floor(x1) + 0.5, floor(x2) + 0.5
            if x1 >= x2:
                for i in range(int(x1-x2)+2):
                    if pg.Vector2([x2, y1]) in self.walls:
                        #print('obstacle detected 3')
                        return False
                    x2 += 1
                #print('non-detected 3')
                return True

            else:
                for i in range(int(x2-x1)+2):
                    if pg.Vector2([x1, y1]) in self.walls:
                        #print('obstacle detected 4')
                        return False
                    x1 += 1
                #print('non-detected 4')
                return True
        else:
            y1, y2 = floor(y1) + 0.5, floor(y2) + 0.5
            x1, x2 = floor(x1) + 0.5, floor(x2) + 0.5
            if x1 < x2:
                if y1 < y2:
                    for i in range(int(x2-x1+y2-y1)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 5')
                            return False
                        x1 += 1
                        y1 += 1
                    #print('non-detected 5')
                    return True
                else:
                    for i in range(int(x2-x1+y1-y2)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 6')
                            return False
                        x1 += 1
                        y1 -= 1
                    #print('non-detected 6')
                    return True
            else:
                if y1 > y2:
                    for i in range(int(x1-x2+y1-y2)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 5')
                            return False
                        x1 -= 1
                        y1 -= 1
                    #print('non-detected 5')
                    return True
                else:
                    for i in range(int(x1-x2+y2-y1)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 6')
                            return False
                        x1 -= 1
                        y1 += 1
                    #print('non-detected 6')
                    return True

    def attack_decide(self):  # 判斷與目標間是否有障礙
        self_position = self.helper.get_self_position()
        nearest_player = self.helper.get_nearest_player_position()
        x1, y1 = self_position[0], self_position[1]
        x2, y2 = nearest_player[0], nearest_player[1]
        if floor(x1) == floor(x2):
            # y下去比
            y1, y2 = floor(y1) + 0.5, floor(y2) + 0.5
            x1, x2 = floor(x1) + 0.5, floor(x2) + 0.5
            if y1 >= y2:
                for i in range(int(y1-y2)+2):
                    if pg.Vector2([x1, y2]) in self.walls:
                        #print('obstacle detected 1')
                        return False
                    y2 += 1
                #print('non-detected 1')
                return True

            else:
                for i in range(int(y2-y1)+2):
                    if pg.Vector2([x1, y1]) in self.walls:
                        #print('obstacle detected 2')
                        return False
                    y1 += 1
                #print('non-detected 2')
                return True

        elif floor(y1) == floor(y2):
            # x下去比
            y1, y2 = floor(y1) + 0.5, floor(y2) + 0.5
            x1, x2 = floor(x1) + 0.5, floor(x2) + 0.5
            if x1 >= x2:
                for i in range(int(x1-x2)+2):
                    if pg.Vector2([x2, y1]) in self.walls:
                        #print('obstacle detected 3')
                        return False
                    x2 += 1
                #print('non-detected 3')
                return True

            else:
                for i in range(int(x2-x1)+2):
                    if pg.Vector2([x1, y1]) in self.walls:
                        #print('obstacle detected 4')
                        return False
                    x1 += 1
                #print('non-detected 4')
                return True
        else:
            y1, y2 = floor(y1) + 0.5, floor(y2) + 0.5
            x1, x2 = floor(x1) + 0.5, floor(x2) + 0.5
            if x1 < x2:
                if y1 < y2:
                    for i in range(int(x2-x1+y2-y1)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 5')
                            return False
                        x1 += 1
                        y1 += 1
                    #print('non-detected 5')
                    return True
                else:
                    for i in range(int(x2-x1+y1-y2)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 6')
                            return False
                        x1 += 1
                        y1 -= 1
                    #print('non-detected 6')
                    return True
            else:
                if y1 > y2:
                    for i in range(int(x1-x2+y1-y2)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 5')
                            return False
                        x1 -= 1
                        y1 -= 1
                    #print('non-detected 5')
                    return True
                else:
                    for i in range(int(x1-x2+y2-y1)):
                        if pg.Vector2([x1, y1]) in self.walls:
                            #print('obstacle detected 6')
                            return False
                        x1 -= 1
                        y1 += 1
                    #print('non-detected 6')
                    return True

    def attack(self):  # 向plqyer所在方位攻擊
        playerpos = self.helper.get_nearest_player_position()
        selfpos = self.helper.get_self_position()
        selfdir = self.helper.get_self_direction()
        x1, y1 = playerpos[0], playerpos[1]
        x2, y2 = selfpos[0], selfpos[1]
        self.action['left'] = True
        if x1 > x2:
            if y1 > y2:  # player在me右下
                if (selfdir[0] < 0.85 and selfdir[0] > 0.65) and (selfdir[1] < 0.85 and selfdir[1] > 0.65):
                    self.action['attack'] = True
                else:
                    self.action['left'] = True
            else:  # player在me右上
                if (selfdir[0] < 0.85 and selfdir[0] > 0.65) and (selfdir[1] > -0.85 and selfdir[1] < -0.65):
                    self.action['attack'] = True
                else:
                    self.action['left'] = True
        else:
            if y1 > y2:  # player在me左下
                if (selfdir[0] > -0.85 and selfdir[0] < -0.65) and (selfdir[1] < 0.85 and selfdir[1] > 0.65):
                    self.action['attack'] = True
                else:
                    self.action['left'] = True
            else:  # player在me左上
                if (selfdir[0] > -0.85 and selfdir[0] < -0.65) and (selfdir[1] > -0.85 and selfdir[1] < -0.65):
                    self.action['attack'] = True
                else:
                    self.action['left'] = True

    def away_RE_field(self):  # 判斷是否接近re
        self_position = self.helper.get_self_position()
        nearest_RE = self.helper.get_nearest_RE_position()
        distance2RE = ((self_position[0]-nearest_RE[0])
                       ** 2 + (self_position[1]-nearest_RE[1])**2)**0.5
        return False if distance2RE <= 1.5 else True

    def decide(self):
        self.reset()
        if self.away_RE_field():
            if self.attack_decide() and self.helper.get_self_next_attack() == 0:
                print('attack_mode', self.helper.get_self_next_attack())
                self.attack()
            elif self.helper.get_self_gun_type() in [1, 3]:
                print('crazy_mode')
                self.action['attack'] = True
            elif self.buff_decide():
                print('buff_mode')
                self.buff()
            else:
                print('wander_mode')
                self.action['forward'] = True
                self.action['left'] = True
        else:
            print('avoid_mode')
            self.avoid_RE_field()

        return self.action
