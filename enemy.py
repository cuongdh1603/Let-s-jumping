import pygame
import random

class Enemy(pygame.sprite.Sprite):
	def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
		pygame.sprite.Sprite.__init__(self)
		#define variables
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()
		self.direction = random.choice([-1, 1])
		if self.direction == 1:
			self.flip = True
		else:
			self.flip = False

		#khởi tạo animation từ spritesheet
		animation_steps = 9
		for animation in range(animation_steps):
			image = sprite_sheet.get_image(animation, 42, 40, scale, (0, 0, 0))
			image = pygame.transform.flip(image, self.flip, False)
			image.set_colorkey((0, 0, 0))
			self.animation_list.append(image)
		
		#tạo 1 hình chữ nhật bao quanh animation
		self.image = self.animation_list[self.frame_index]
		self.rect = self.image.get_rect()

		if self.direction == 1:
			self.rect.x = 0
		else:
			self.rect.x = SCREEN_WIDTH
		self.rect.y = y
	def update(self, scroll, SCREEN_WIDTH):
		# animation
		ANIMATION_COOLDOWN = 65
		#Cập nhật animation dựa trên frame hiện tại
		self.image = self.animation_list[self.frame_index]
		#Kiểm tra xem đã hết thời gian chưa kể từ lần cập nhật trước
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#Kiểm tra xem animation đã kết thúc chưa và khởi tạo lại
		if self.frame_index >= len(self.animation_list):
			self.frame_index = 0

		#di chuyển của animation
		self.rect.x += self.direction * 2
		self.rect.y += scroll

		#Kiểm tra xem animation đã ra khỏi màn hình chưa
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()