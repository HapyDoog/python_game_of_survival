import pygame
import sys
import random
import time

pygame.init()

#määritellään pelilauta
RUUTU = 20
LEVEYS = 20
KORKEUS = 15

#luodaan näyttö
NÄYTÖN_KOKO = (LEVEYS*RUUTU, KORKEUS*RUUTU)
NÄYTTÖ= pygame.display.set_mode(NÄYTÖN_KOKO)
pygame.display.set_caption("MATOPELI")

#määritellään värit
taustaväri=pygame.Color(0,0,255)
madonväri= pygame.Color(0,255,0)
ruoanväri= pygame.Color(255,0,0)

#piirretään ruutuja
def piirrä_ruutu(sijainti, väri):
  (x,y)= sijainti
  #lasketaan sijainti kordinaatit
  ruutu= pygame.Rect(x * RUUTU+1, y *RUUTU+1, RUUTU -2, RUUTU -2)
  pygame.draw.rect(NÄYTTÖ, väri, ruutu)

#määritellään mato
mato= [(0,0), (1,0),(2,0),(3,0)]

#arvotaan ruuan sijainti
def arvo_ruoka():
  ruoka_x = random.randint(0, LEVEYS -1)
  ruoka_y= random.randint(0, KORKEUS -1)
  #osuuko matoon
  if (ruoka_x, ruoka_y) in mato:
    #jos madossa niin uudelleen arvotaan
    return arvo_ruoka()

  else:
    #jos ruoka ei ole madossa
    return (ruoka_x, ruoka_y)

#arvotaan ruoka
ruoka = arvo_ruoka()
#laitetaan sunta oikeaan
suunta="OIKEA"
#laitetaan kello ruudunpäivitys
kello=pygame.time.Clock()

#peliluuppi
peli_jatkuu= True
while peli_jatkuu:
  kello.tick(3)
  #tapahtumia
  for tapahtuma in pygame.event.get():
    if (tapahtuma.type==pygame.QUIT):
      pygame.quit
      sys.exit()
    if (tapahtuma.type == pygame.KEYDOWN):
      #onko alas
      if (tapahtuma.key == pygame.K_DOWN):
        suunta="ALAS"
      if (tapahtuma.key == pygame.K_UP):
        suunta="YLÖS"
      if (tapahtuma.key == pygame.K_LEFT):
        suunta="VASEN"
      if (tapahtuma.key == pygame.K_RIGHT):
        suunta="OIKEA"
  
    #taustaväri  
  NÄYTTÖ.fill(taustaväri)
    #piirretään ruoka
  piirrä_ruutu(ruoka,ruoanväri)
  #piiretään mato   
  for pala in mato:
    piirrä_ruutu(pala, madonväri)

  #näytön päivitys
  pygame.display.update()
  
  #madon liikutus
  #eka otetaam madon pään koordinaatit
  (pää_x, pää_y)= mato [-1]
  if (suunta == "OIKEA"):
    #lisätään matoon pään oikealla puolella sijainti
    mato.append((pää_x+1, pää_y))
    "meneekö mato yli"
  if pää_x+1 >= LEVEYS:
      print ("pää osuu oikealle")
      peli_jatkuu= False

  if (suunta == "ALAS"):
      #lisätään pään alapuolelle 1 
      mato.append((pää_x, pää_y+1))
      #meneekö yli alhaalta
      if pää_y+1 >= KORKEUS:
        print ("osuu alas")
        peli_jatkuu= False

  if (suunta == "VASEN"):
    mato.append((pää_x-1, pää_y))
    if (pää_x -1 <0):
      print ("osuu vasemmalle")
      peli_jatkuu= False

  if (suunta == "YLÖS"):
    mato.append((pää_x, pää_y -1))
    if (pää_y -1 <0):
      print ("osuu ylös")
      peli_jatkuu= False

  #saako mato ruuan
  if (mato[-1] == ruoka):
    #arvotaan uusi ruoka
    ruoka=arvo_ruoka()

  else:
    #jos ei osu niin poistetaan madon häntä
    mato.pop(0)
    #osuuko mato itseensä
    if mato[-1] in mato[0:-1]:
      print ("mato osuu itseensä")
      peli_jatkuu = False

#peli loppuu
print ("madon pituus: ", len(mato))

#efekti
for x in range (LEVEYS):
  for y in range (KORKEUS):
    r = 10 * (x**2 + y**2)
    g = 10 *x+y
    b = 10 * y
    r = r%256
    g = g%256
    b = b%256
  
    väri = pygame.Color(r,g,b) 
    piirrä_ruutu((x,y), väri)

leveys = LEVEYS * RUUTU
korkeus = KORKEUS * RUUTU
lopputekstiväri = pygame.Color(200,  1, 159)
iso_fontti = pygame.font.SysFont("FreeSans",50)
pistefontti= pygame.font.SysFont("FreeSans", 15)
game_over_teksti=iso_fontti.render("GAME OVER", True, lopputekstiväri)

#näytön keskipiste
keskikohta= (leveys //2, korkeus//2)
#otetaan game over tekstin ympäröivä ruutu ja laitetaan se keskelle näyttöä
game_over_ruutu=game_over_teksti.get_rect(center=keskikohta)
#piiretään teksti
NÄYTTÖ.blit(game_over_teksti, game_over_ruutu)
#renderöidään pisteet, muutetaan pisteet kokonaisluvusta eli INT muutujasta, merkkijonoksi
piste_teksti = pistefontti.render("MATO: "+str(len(mato)), True, lopputekstiväri)
#
piste_leveys= piste_teksti.get_rect().width
#lasketaan pistetekstin sijainti
pisteelle_sijainti = ((leveys-piste_leveys) //2, game_over_ruutu.bottom)
pygame.display.update()
time.sleep(10)

#lopputekstiväri
pygame.quit()
sys.exit()