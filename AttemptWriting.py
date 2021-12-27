if self.DIRECTION == 'Right':
    self.image = right_robber_image

else:
    self.image = left_robber_image

heart_image.set_colorkey("white")
heart_image_rect = heart_image.get_rect()
heart_image_rect.center = x, y

self.image.set_colorkey('white')
self.type = 'Robber'

self.rect = self.image.get_rect()
self.rect.center = x, y
