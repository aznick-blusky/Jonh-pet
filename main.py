)#e20000import math
import os
import random
import sys
from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics import Color, PopMatrix, PushMatrix, Rectangle, Scale, Translate
from kivy.uix.widget import Widget

# --- FORZA LA CARTELLA DI LAVORO AUTOMATICA ---
try:
  script_dir = os.path.dirname(os.path.abspath(__file__))
  os.chdir(script_dir)
except Exception:
  pass

# Imposta una dimensione iniziale della finestra simile a prima (ottimizzata per portrait)
Window.size = (720, 1280)

sprites_john_fermo = []
sprites_john_corre = []
errore_testo = ""

# --- CARICAMENTO DELLA SEQUENZA DI SPRITE CON KIVY ---
try:
  for i in range(1, 5):
    nome_file = f"John_Guard{i}.png"
    img = CoreImage(nome_file).texture
    sprites_john_fermo.append(img)
  for i in range(1, 3):
    nome_file = f"John_Run{i}.png"
    img = CoreImage(nome_file).texture
    sprites_john_corre.append(img)
except Exception as e:
  errore_testo = str(e)
  # Fallback texture di sicurezza se mancano i file
  from kivy.graphics.texture import Texture

  buf = bytes([0, 140, 255, 255] * 64 * 64)
  t = Texture.create(size=(64, 64), colorfmt="rgba")
  t.blit_buffer(buf, colorfmt="rgba", bufferfmt="ubyte")
  sprites_john_fermo = [t]
  sprites_john_corre = [t]


# --- FUNZIONI DI SUPPORTO GEOMETRICO ---
def lerp(a, b, t):
  return a + (b - a) * t


def sign(x):
  if x > 0:
    return 1
  if x < 0:
    return -1
  return 0


def point_distance(x1, y1, x2, y2):
  return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def lengthdir_x(length, direction):
  return length * math.cos(math.radians(direction))


def lengthdir_y(length, direction):
  # In Kivy l'asse Y va verso l'alto (come la trigonometria classica)
  return length * math.sin(math.radians(direction))


def point_direction(x1, y1, x2, y2):
  angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
  return angle if angle >= 0 else angle + 360


# --- CLASSE JOHN (LOGICA AGGIORNata A KIVY) ---
class John:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.target_x = x
    self.target_y = y
    self.vel = 5
    self.couldown = 120
    self.stato = "fermo"
    self.girato = 0  # 0 = normale, 1 = specchiato
    self.frames = sprites_john_fermo
    self.frame_index = 0
    self.anim_timer = 0

  def step(self, screen_w, screen_h):
    # Animazione fotogrammi
    if len(self.frames) > 1:
      self.anim_timer += 2
      if self.anim_timer >= 10:
        self.anim_timer = 0
        self.frame_index = (self.frame_index + 1) % len(self.frames)

    # Dimensioni correnti dello sprite
    texture_corrente = self.frames[self.frame_index]
    spr_w = texture_corrente.width
    spr_h = texture_corrente.height

    # Movimento autonomo
    if self.stato == "corre":
      distanza = point_distance(self.x, self.y, self.target_x, self.target_y)
      direzione = point_direction(self.x, self.y, self.target_x, self.target_y)

      passo = min(self.vel, distanza)
      self.x += lengthdir_x(passo, direzione)
      self.y += lengthdir_y(passo, direzione)

      # Gestione direzione flip
      self.girato = 1 if (self.target_x < self.x) else 0

      # Vincoli bordi schermo Kivy (0,0 in basso a sinistra)
      self.x = max(0, min(self.x, screen_w - spr_w))
      self.y = max(0, min(self.y, screen_h - spr_h))

      if distanza <= self.vel:
        self.x = self.target_x
        self.y = self.target_y
        self.frames = sprites_john_fermo
        self.frame_index = 0
        self.stato = "fermo"
        self.couldown = random.randint(60, 180)

    elif self.stato == "fermo":
      self.couldown -= 1
      if self.couldown <= 0:
        self.stato = "corre"
        self.frames = sprites_john_corre
        self.frame_index = 0
        self.target_x = random.randint(0, int(screen_w - spr_w))
        self.target_y = random.randint(0, int(screen_h - spr_h))


# --- WIDGET PRINCIPALE DEL GIOCO ---
class JohnGameWidget(Widget):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    # Posiziona John al centro dello schermo Kivy
    self.john = John(320, 640)
    # Avvia il loop di aggiornamento a 60 FPS
    Clock.schedule_interval(self.update, 1.0 / 60.0)

  def update(self, dt):
    # Aggiorna la logica passando le dimensioni correnti della finestra
    self.john.step(self.width, self.height)

    # Ridisegna lo schermo
    self.canvas.clear()
    with self.canvas:
      # Sfondo scuro (grigio scuro)
      Color(0.12, 0.12, 0.12, 1)
      Rectangle(pos=(0, 0), size=self.size)

      # Ottiene la texture corrente
      texture = self.john.frames[self.john.frame_index]
      w = texture.width
      h = texture.height

      # Gestione del Flip orizzontale in Kivy tramite Matrici di Trasformazione
      if self.john.girato == 1:
        PushMatrix()
        # Sposta l'origine al centro dell'immagine, specchia sull'asse X, e riporta indietro
        Translate(self.john.x + w / 2, self.john.y + h / 2)
        Scale(-1, 1, 1)
        Translate(-(self.john.x + w / 2), -(self.john.y + h / 2))
        Color(1, 1, 1, 1)
        Rectangle(texture=texture, pos=(self.john.x, self.y), size=(w, h))
        PopMatrix()
      else:
        Color(1, 1, 1, 1)
        Rectangle(texture=texture, pos=(self.john.x, self.y), size=(w, h))


# --- APPLICAZIONE KIVY ---
class JohnApp(App):

  def build(self):
    return JohnGameWidget()


if __name__ == "__main__":
  JohnApp().run()
