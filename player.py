class Player(Sprite):
	"""A class to manage the ship."""

	def __init__(self, sal_game):
		"""Initialize the ship and set its starting position."""
		super().__init__()
		self.screen = sal_game.screen
		self.settings = sal_game.settings
		self.screen_rect = sal_game.screen.get_rect()

		# Load the ship image and get its rect.
		self.player = pygame.draw.circle(self.screen, BLACK, (20,450), 5)
		self.rect = self.player.get_rect()
		# Start each new ship at the bottom center of the screen
		self.rect.midbottom = self.screen_rect.midbottom

		#Store a decimal value for the ship horizontal postion
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		# Movement flag
		self.moving = False

	def update(self):
		"""Update the ships position based on the movement flag."""
		# Upade the ships x value not the rect.
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		# Update rect object from self.x.
		self.rect.x = self.x

	def blitme(self):
		"""Draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Center the ship on the screen"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)