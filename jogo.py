import pygame
import os
import random

Tela_largura = 500
tela_altura = 800

Imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join("imagens", "pipe.png")))
Imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join("imagens", "base.png")))
Imagem_ambiente = pygame.transform.scale2x(pygame.image.load(os.path.join("imagens", "bg.png")))
Imagens_passaro = [pygame.transform.scale2x(pygame.image.load(os.path.join("imagens", "bird1.png"))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join("imagens", "bird2.png"))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join("imagens", "bird3.png")))
                  
]
pygame.font.init()
Fonte = pygame.font.SysFont("arial", 50)

class passaro:
    IMGS = Imagens_passaro
    rotacao_maxima = 25
    velocidade_rotacao = 20
    tempo_animacao = 5

    def __init__(self, x, y):
        self.x =x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura  = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura =self.y

    def mover(self):
        self.tempo += 1 
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

    #resringir o deslocamento
        if deslocamento > 16:
            deslocamento=16
        elif deslocamento <0:
            deslocamento -= 2 #intensidade no pulo

        self.y =deslocamento

        #o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_maxima:
                self.angulo = self.rotacao_maxima
            else:
                if self.angulo > -90:
                    self.angulo -=self.velocidade_rotacao

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem< self.tempo_animacao:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem< self.tempo_animacao*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem< self.tempo_animacao*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem< self.tempo_animacao*4:
            self.imagem = self.IMGS[1]        
        elif self.contagem_imagem< self.tempo_animacao*4+1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0 

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.tempo_animacao*2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x,self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
        
class cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x= x
        self.altura = 0
        self.pos_topo = 0
        self.base = 0
        self.Cano_topo = pygame.tranform.flip(Imagem_cano, False, True)
        self.Cano_base = Imagem_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50,450)
        self.pos_topo = self.altura - self.Cano_topo.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade
    
    def desenhar(self, tela):
        tela.blit(self.Cano_topo, (self.x, self.pos_topo))
        tela.blit(self.Cano_base, (self.x, self.pos_base))
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.Cano_topo)
        base_mask = pygame.mask.from_surface(self.Cano_base)

        distancia_topo = (self.x - passaro.x,  self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False
    
class chao:
    velocidade = 5
    largura = Imagem_chao.get_width()
    imagem = Imagem_chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0 
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura 
        if self.x2 +self.largura<0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos): 
    tela.blit(Imagem_ambiente, (0,0))
    for passaros in passaros:
            passaro.desenhar(tela)
    for cano in canos:
            cano.desenhar(tela)
        
    texto = Fonte.render(f"Pontuação:(pontos)", 1, (255, 25, 25))
    tela.blit(texto, (Tela_largura -10 -texto.get_widtch9, 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [passaro(230,350)]
    chao = chao(730)
    canos = [cano(700)]
    tela = pygame.display.set_mode((tela_altura, tela_altura))
    pontos = 0 
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
                        
        for passaro in passaros:
            passaro.mover()
        chao.mover()
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                        passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                        cano. passou = True
                        adicionar_cano= True
            cano.mover()
            if cano.x + cano.Cano_topo.get_widrh()<0:
                    remover_canos.apend(cano    )

        if adicionar_cano:
            pontos+= 1
            canos.append(cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if(passaro.y + passaro.imagem.get_height())> chao.y or passaro.y < 0:
                    passaros.pop(i)

        desenhar_tela(tela, passaros,canos,chao, pontos)

if __name__ =='__main__':
    main()
                    
