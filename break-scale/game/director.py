import arcade
import os
from game import constants 
from game.foodApple import Apple
from game.player import Player
import random
import math
from game.donut import Donut
from game.carrot import Carrot
from game.pizza import Pizza


class Director(arcade.Window):
    def __init__(self):
        """Set up the game . Call this function to restart the game """
        # call the parent class and set up the window 
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

        # Each sprite should go into a list set to none 
        self.player_list = None
        self.apple_list = None
        self.wall_list = None
        self.donut_list = None
        self.pizza_list = None
        self.carrot_list = None
        self.timer = 0.0
        self.timer_output = "00:00:00"

        # separate variable that holds the player sprite
        self.player_sprite = None
        self.score = 150

        # set background color or set the tileMap
        #arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """set up the game here. call this function to restart the game """
        # setup the cameras
        
        # sprite list create the object instance for individual 
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash= True)
        self.donut_list = arcade.SpriteList()
        self.pizza_list = arcade.SpriteList()
        self.carrot_list = arcade.SpriteList()
        self.timer = 0.0

        # keep track of score
        self.score = 150 #set to zero here and in initialize 
        
        # set up player sprite
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        #create the apple
        for a in range(10):
            #create the apple instane
            # apple image from ???
            apple = Apple("break-scale/game/resources/images/food/apple_sprite.png", constants.FOOD_SCALING)
            # position the apple
            apple.center_x = random.randrange(constants.SCREEN_WIDTH)
            apple.center_y = random.randrange(constants.SCREEN_HEIGHT)
            #apple.speed = random.randrange(30,40)
            self.apple_list.append(apple)

        for d in range(20):
            donut = Donut("break-scale/game/resources/images/food/donut_sprite.png",constants.FOOD_SCALING)
            donut.center_x = random.randrange(constants.SCREEN_WIDTH)
            donut.center_y = random.randrange(constants.SCREEN_HEIGHT)
            self.donut_list.append(donut)

        for c in range(20):
            carrot = Carrot("break-scale/game/resources/images/food/carrot_sprite.png",constants.FOOD_SCALING)
            carrot.center_x = random.randrange(constants.SCREEN_WIDTH)
            carrot.center_y = random.randrange(constants.SCREEN_HEIGHT)
            self.carrot_list.append(carrot)
        
        for p in range(20):
            pizza = Pizza("break-scale/game/resources/images/food/pizza_sprite.png",constants.FOOD_SCALING)
            pizza.center_x = random.randrange(constants.SCREEN_WIDTH)
            pizza.center_y = random.randrange(constants.SCREEN_HEIGHT)
            self.pizza_list.append(pizza)
        

        # create the ground 
        # this shows using a loop to place multiple sprites horizontally 

        # create the trees on the ground
        # this shows using a coordinate list to place sprites. 
        # create the physics engine 

        # --- set up the wall instance
        # create horizontal rows of boxes
            # top edges
            # bottom edges
        # create vertical columns of boxes
            # left
            # right
            # create a box in the middle 

        # create the food instance
            # create it need width and height
            # position the food need center x and center y
            # add the food to the list

        # explosion 
        
        #don't show the mouse pointer # snowflake ex
        self.set_mouse_visible(False)

        # set up the background
        #arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # create the physics engine by setting it to arcades physcis engine
        # and adding the player sprite and the scene sprite list to walls
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        


    def on_draw(self):
        """render the screen"""
        # clear the screen to the background color
        arcade.start_render()
        self.apple_list.draw()
        self.player_list.draw()
        self.donut_list.draw()
        self.pizza_list.draw()
        self.carrot_list.draw()

        # put text on screen 
        output = f"Weight: {self.score}"
        arcade.draw_text(output, 650, 560, arcade.color.WHITE, 16)

        # set up timer output the time text
        arcade.draw_text(self.timer_output, 10, 560, arcade.color.WHITE, 16)

        # put instructions on screen 
        # instructions = "Move left or right arrows to get eat food"
        # arcade.draw_text(instructions, 10,90, arcade.color.WHITE,12)

        # activate the game camera

        # draw our score on the screen, scrolling it with the viewport
        # player explodes

    def on_key_press(self, key, modifiers):
        """ called whenever a key on the keyboard is pressed
        for a list of keys, see:https://api.arcade.academy/en/latest/arcade.key.html """
        #self.player_sprite.update(key)
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = - constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        """ called whenever the user lets off a previously pressed key basically stops the player from moving"""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        """movement and game logic"""
        # position the camera
        
        self.player_list.update()
        
        # Generate a list of all sprites that collided with the player.
        self.apple_list.update()
        self.donut_list.update()
        self.pizza_list.update()
        self.carrot_list.update()

        # timer 
        # set up timer
        self.timer += delta_time
        # calculate minutes
        minutes = int(self.timer) // 60
        # calculate seconds
        seconds = int(self.timer) % 60
        # calculate 100s of a second
        seconds_100 = int((self.timer - seconds) * 100)
        # figure out our output
        self.timer_output = f"Time: {minutes:02d}:{seconds:02d}:{seconds_100:02d}"

        #loop through each food  see if we hit  change it, and add to score if any and remove it 
        apple_hit = arcade.check_for_collision_with_list(self.player_sprite, self.apple_list)
        for apple in apple_hit:
            apple.remove_from_sprite_lists()
            self.score += 1
        
        donut_hit = arcade.check_for_collision_with_list(self.player_sprite, self.donut_list)
        for donut in donut_hit:
            donut.reset_pos()
            self.score += 40

        pizza_hit = arcade.check_for_collision_with_list(self.player_sprite, self.pizza_list)
        for pizza in pizza_hit:
            pizza.reset_pos()
            self.score += 40

        carrot_hit = arcade.check_for_collision_with_list(self.player_sprite, self.carrot_list)
        for carrot in carrot_hit:
            carrot.reset_pos()
            self.score += 5

        self.physics_engine.update()
        

        