import pygame

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image
		self.sheet.set_colorkey((0, 0, 0))
	
	def get_image(self, frame, offset, w_h, scale, colorkey = (0, 0, 0)):
		image = pygame.Surface(w_h).convert_alpha()
		image.blit(self.sheet, (0, 0), (0 + offset[0], (frame * w_h[1]) + offset[1], w_h[0], w_h[1]))
		image = pygame.transform.scale(image, (w_h[0] * scale, w_h[1] * scale))
		image.set_colorkey(colorkey)
		return image