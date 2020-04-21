# -*- coding: utf-8 -*-
"""
A Simple Version of Midway Island Naval Warfare with Python for Easy Learning by lixingqiu
This shooting game is made using Arcade module. This version is the core version and demonstrates explosion effects, class inheritance, and key detection.
The scrolling background is made using two pictures, which are separated by the height SCREEN_HEIGHT. If the top of the picture reaches the bottom, that is, the coordinate is 0, then it will move instantaneously to the top.
It should be noted that the coordinate system of Arcade is the same as the coordinate system in mathematics. In this game, the lower left corner is used as the origin, and the y axis is upward. In Pygame, the upper left corner is the origin, and the y-axis is positive > bottom.

"""

__author__ = "lixingqiu/sontru"
__date__ = "2019/3/13"
__url__ = "http://www.lixingqiu.com/?p=209"
__qq__ = "406273900"

import os
import random
import arcade

SPRITE_SCALING = 1.0

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "A Simple Version of Midway Island Naval Warfare with Python for Easy Learning Python"
ENEMY_COUNT = 100
MOVEMENT_SPEED  = 5

START_SCREEN = 1

class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class Explosion(arcade.Sprite):
    """ create explosion sprite""" 

    def __init__(self, texture_list,x,y):
        """texture_list load"""
        super().__init__()
        self.center_x = x
        self.center_y = y
        # 第一帧
        self.current_texture = 0      # 这是造型索引号
        self.textures = texture_list  # 这是每帧图片列表
        self.set_texture(self.current_texture)

    def update(self):

        # 更新每帧的图片，到了最后一帧后就会删除自己。
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()

class Bullet(arcade.Sprite):
    """子弹类，继承自Arcade自带的角色类，它从飞机的坐标射出"""
    def __init__(self,image,plane):
        super().__init__(image)
        self.center_x = plane.center_x
        self.center_y = plane.center_y
        self.change_y = 20        

    def update(self):
        """ update coordinates"""
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.bottom >  SCREEN_HEIGHT: self.kill()
        
class Background(arcade.Sprite):
    
    def __init__(self,image):
        super().__init__(image)    
        self.change_y = -10       

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.top <=0 : self.bottom = SCREEN_HEIGHT
        
class Enemy(arcade.Sprite):
    def __init__(self,image):
        super().__init__(image)
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT,SCREEN_HEIGHT*30)

    def update(self):
        
        if self.top<=0:self.kill()
        
class MyGame(arcade.Window):
    """ 应用程序主要类. """

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        self.gamestate = 1
        # 角色列表定义
        self.all_sprites_list = None
        self.enemy_list = None

        # 定义玩家的相关变量 
        self.score = 0
        self.player_sprite = None

        self.enemy_explosion_images = []

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"
        # Load the explosions from a sprite sheet
        self.enemy_explosion_images = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

    def start_new_game(self):
        """ 设置与初始化游戏 """
        
        self.shoot_sound = arcade.sound.load_sound("images/midway/Shot.wav")        
        self.background_music = arcade.sound.load_sound("images/midway/background.wav")
        arcade.sound.play_sound(self.background_music)        
        
        # 实例化所有角色列表      
        self.enemy_list = arcade.SpriteList()            # 敌人列表        
        self.bullet_list = arcade.SpriteList()           # 玩家子弹列表
        self.all_sprites_list = arcade.SpriteList()      # 所有角色列表
        self.enemy_explosion_list = arcade.SpriteList()  # 所有敌人的爆炸角色列表
        
        # Set the player-operated aircraft
        self.score = 0
        self.player_sprite = arcade.AnimatedTimeSprite("images/midway/Plane 1.png",0.8)
        self.player_sprite.textures.append(arcade.load_texture("images/midway/Plane 2.png"))
        self.player_sprite.textures.append(arcade.load_texture("images/midway/Plane 3.png"))
        self.player_sprite.scale = 1.0
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_sprite.health  = 10                  # No of Lives
        self.player_sprite.update()
        self.player_sprite.update_animation()
        self.all_sprites_list.append(self.player_sprite)

        # 敌人角色生成
        for i in range(ENEMY_COUNT):
            enemy = Enemy("images/midway/Fighters.png")
            self.enemy_list.append(enemy)
            self.all_sprites_list.append(enemy)
            
        sea_image = "images/midway/sea.png"
        # Setting a Fixed Background To cover up rolling background cracks
        self.background = arcade.Sprite(sea_image)
        self.background.center_x = SCREEN_WIDTH // 2
        self.background.bottom = 0
        
        # Set the scrolling background, the two first drawn characters move down, move to a certain coordinate and go to the top
        self.background1 = Background(sea_image)
        self.background1.center_x = SCREEN_WIDTH // 2
        self.background1.bottom = 0
        self.all_sprites_list.append(self.background1)
        
        self.background2 = Background(sea_image)
        self.background2.center_x = SCREEN_WIDTH // 2
        self.background2.bottom = SCREEN_HEIGHT  
        self.all_sprites_list.append(self.background2)

        # 1943logo (new)
        self.logo_1943 = arcade.Sprite("images/midway/1943Logo3.png")
        self.logo_1943.center_x  = SCREEN_WIDTH // 2
        self.logo_1943.center_y  = SCREEN_HEIGHT // 2
        self.interval = 60
        self.interval_counter = 0

        # Start screen
        self.demo_background = arcade.Sprite("images/midway/Logo2.png")
        self.demo_background.left = 50
        self.demo_background.top = SCREEN_HEIGHT

        
    def on_key_press(self, key, modifiers):
        """ Mouse button events """
        if self.player_sprite.health <=0 :return
        if key == arcade.key.SPACE:
            self.gamestate = 0
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.J:
            arcade.sound.play_sound(self.shoot_sound)
            self.bullet = Bullet("images/midway/Shot 1.png",self.player_sprite)
            self.bullet_list.append(self.bullet)
            self.all_sprites_list.append(self.bullet)            

    def on_key_release(self, key, modifiers):
        """ Mouse release event """
        if self.player_sprite.health <=0 :return
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def update(self, delta_time):
        """ Game update logic """

        if self.gamestate != START_SCREEN:
            # Update coordinates, etc.
            #  print(self.background2.bottom - self.background1.top)
            distance = self.background2.bottom - self.background1.top
            if  distance < 0 and distance > -40:   # Fissure remedy - Make up for the cracks
             
                self.background2.bottom = self.background1.top
            
            self.enemy_list.move(0, -5)
            self.all_sprites_list.update() 
            self.player_sprite.update_animation()         

            if self.player_sprite.health > 0:
                # Collision detection between players and all enemy aircraft.
                hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_list)
                # Traverse the list of enemy aircraft encountered
                for enemy in hit_list:
                    enemy.kill()
                    self.player_sprite.health -= 1
                    if self.player_sprite.health < 0 :
                        e = Explosion(self.enemy_explosion_images)
                        e.center_x = self.player_sprite.center_x
                        e.center_y = self.player_sprite.center_y
                        e.update()
                        self.player_sprite.kill()
                    
                    e = Explosion(self.enemy_explosion_images,enemy.center_x,enemy.center_y)
                    e.center_x = enemy.center_x
                    e.center_y = enemy.center_y
                    e.update()
                    self.enemy_explosion_list.append(e)
                    self.all_sprites_list.append(e)
            
            # Did each enemy hit the bullet
            for enemy in self.enemy_list:   
                hit_list = arcade.check_for_collision_with_list(enemy,self.bullet_list)
                if len(hit_list) > 0:
                    enemy.kill()
                    [b.kill() for b in hit_list]   # Delete every bullet encountered
                    self.score += len(hit_list)                
                    e = Explosion(self.enemy_explosion_images,enemy.center_x,enemy.center_y)
                    e.center_x = enemy.center_x
                    e.center_y = enemy.center_y
                    e.update()
                    self.enemy_explosion_list.append(e)
                    self.all_sprites_list.append(e)
                
    def on_draw(self):
        """ Render screen """

        arcade.start_render()
        if self.gamestate == START_SCREEN:
            self.demo_background.draw()
            self.player_sprite.center_x = 650
            self.player_sprite.center_y = 100
            self.player_sprite.draw()
            return 
        else:
            # Start rendering, this command must be before all redraw commands
            self.background.draw()    # Unmovable background to make up for the problem of rolling background cracks
            self.background1.draw()   # Paint scroll background
            self.background2.draw()   # Paint scroll background
            # Draw all the characters
            self.enemy_list.draw()
            if self.player_sprite.health > 0:            
               self.player_sprite.draw()
            self.bullet_list.draw()
            self.enemy_explosion_list.draw()
        
            # 画得分情况
            score = "Kills: " + str(self.score) + ", Lives: " + str(self.player_sprite.health)
            arcade.draw_text(score, 10, 20, arcade.color.WHITE, 14 )

            if self.player_sprite.health < 1:  # 血量小于1显示游戏结束
               self.interval_counter +=1
               if self.interval_counter < self.interval // 2: self.logo_1943.draw()
               if self.interval_counter % self.interval == 0: self.interval_counter = 0

            if self.player_sprite.left < 0:
                self.player_sprite.left = 0
            elif self.player_sprite.right > SCREEN_WIDTH - 1:
                self.player_sprite.right = SCREEN_WIDTH - 1

            if self.player_sprite.bottom < 0:
                self.player_sprite.bottom = 0
            elif self.player_sprite.top > SCREEN_HEIGHT - 1:
                self.player_sprite.top = SCREEN_HEIGHT - 1


def main():

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.start_new_game()
    arcade.run()


if __name__ == "__main__":
    main()
