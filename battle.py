import pygame
import random
import os

pygame.init()

# Definir diretório atual (garante que imagens sejam carregadas corretamente)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Tamanho da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Batalha Pokémon")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_ORANGE = (255, 204, 102)  # Cor laranja claro para o hover

# Fontes
font = pygame.font.SysFont("arial", 24)
dialog_font = pygame.font.SysFont("arial", 20)

# Imagens
background_img = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
player_img = pygame.transform.scale(pygame.image.load("charmander.png"), (150, 150))
enemy_images = {
    "Cárie": pygame.transform.scale(pygame.image.load("carie.png"), (150, 150)),
    "Caspa no Cabelo": pygame.transform.scale(pygame.image.load("caspa.png"), (150, 150)),
    "Acne": pygame.transform.scale(pygame.image.load("acne.png"), (150, 150)),
    "Bactéria do Pé": pygame.transform.scale(pygame.image.load("bacteria_pe.png"), (150, 150)),
    "Gordura na Pele": pygame.transform.scale(pygame.image.load("gordura.png"), (150, 150)),
    "Bactéria de Resfriado": pygame.transform.scale(pygame.image.load("resfriado.png"), (150, 150)),
    # "Mão Podre": pygame.transform.scale(pygame.image.load("mao_podre.png"), (150, 150)),
}

# Variável de Controle
battle_phase = 0  # 0 = jogador escolhe, 1 = jogador ataca, 2 = inimigo ataca, 3 = fim turno
current_item = None
last_dano_jogador = 0
last_ataque_inimigo = ("", 0)



# Classe de Itens
class Item:
    def __init__(self, nome, dano_base, eficacias):
        self.nome = nome
        self.dano_base = dano_base
        self.eficacias = eficacias

    def calcular_dano(self, inimigo_nome):
        return int(self.dano_base * self.eficacias.get(inimigo_nome, 0.2))  # 0.2 se não tiver eficácia definida

# Classe do Inimigo
class EnemyBattle:
    def __init__(self, nome, hp, ataques):
        self.nome = nome
        self.hp = hp
        self.max_hp = hp
        self.ataques = ataques
        self.damage_flash = 0

    def ataque_aleatorio(self):
        for nome, dados in self.ataques.items():
            if random.random() <= dados["probabilidade"]:
                return nome, dados["dano"]
        return "Ataque Fraco", 3

# Criar inimigo
enemies = {
    "Cárie": EnemyBattle("Cárie", 100, {
        "Dente Sujo": {"dano": 5, "probabilidade": 0.4},
        "Mau Hálito": {"dano": 10, "probabilidade": 0.3},
        "Dor e Inflamação": {"dano": 15, "probabilidade": 0.2},
        "Gengivite": {"dano": 25, "probabilidade": 0.1}
    }),
    "Mão Podre": EnemyBattle("Mão Podre", 80, {
        "Mãos Suja": {"dano": 5, "probabilidade": 0.5},
        "Germes": {"dano": 10, "probabilidade": 0.3},
        "Doenças da Pele": {"dano": 12, "probabilidade": 0.15},
        "Infecção": {"dano": 18, "probabilidade": 0.05}
    }),
    "Caspa no Cabelo": EnemyBattle("Caspa no Cabelo", 60, {
        "Caspa": {"dano": 4, "probabilidade": 0.5},
        "Coceira Intensa": {"dano": 8, "probabilidade": 0.3},
        "Queda de Cabelo": {"dano": 12, "probabilidade": 0.15},
        "Lesão no Couro Cabeludo": {"dano": 18, "probabilidade": 0.05}
    }),
    "Acne": EnemyBattle("Acne", 70, {
        "Cravo": {"dano": 6, "probabilidade": 0.4},
        "Espinha": {"dano": 9, "probabilidade": 0.35},
        "Inflamação": {"dano": 14, "probabilidade": 0.2},
        "Cisto": {"dano": 20, "probabilidade": 0.05}
    }),
    "Bactéria de Resfriado": EnemyBattle("Bactéria de Resfriado", 90, {
        "Espirro": {"dano": 5, "probabilidade": 0.4},
        "Nariz Entupido": {"dano": 10, "probabilidade": 0.3},
        "Tosse seca": {"dano": 15, "probabilidade": 0.2},
        "Febre": {"dano": 25, "probabilidade": 0.1}
    }),
    "Bactéria do Pé": EnemyBattle("Bactéria do Pé", 80, {
        "Fungo Pé Sujo": {"dano": 6, "probabilidade": 0.4},
        "Bicho de Pé": {"dano": 12, "probabilidade": 0.3},
        "Unha encravada": {"dano": 18, "probabilidade": 0.2},
        "Infecção Grave": {"dano": 30, "probabilidade": 0.1}
    }),
    "Gordura na Pele": EnemyBattle("Gordura na Pele", 70, {
        "Pele Oleosa": {"dano": 4, "probabilidade": 0.4},
        "Acúmulo de Sebo": {"dano": 8, "probabilidade": 0.3},
        "Obstrução dos Poros": {"dano": 12, "probabilidade": 0.2},
        "Acne com Sebo": {"dano": 18, "probabilidade": 0.1}
    })
}

# Criar itens
itens = {
    "Escova de Dente": Item("Escova de Dente", 15, {
        "Cárie": 4,
        "Mão Podre": 0.5,
        "Caspa no Cabelo": 0.5,
        "Acne": 0.5,
        "Bactéria de Resfriado": 1,
        "Bactéria do Pé": 0.5,
        "Gordura na Pele": 0.5
    }),
    "Pasta de Dente": Item("Pasta de Dente", 20, {
        "Cárie": 4,
        "Mão Podre": 0.5,
        "Caspa no Cabelo": 0.5,
        "Acne": 0.5,
        "Bactéria de Resfriado": 0.5,
        "Bactéria do Pé": 0.5,
        "Gordura na Pele": 0.5
    }),
    "Álcool 70%": Item("Álcool 70%", 25, {
        "Cárie": 0.5,
        "Mão Podre": 4,
        "Caspa no Cabelo": 0.5,
        "Acne": 0.5,
        "Bactéria de Resfriado": 2.5,
        "Bactéria do Pé": 1.5,
        "Gordura na Pele": 1
    }),
    "Sabão Líquido": Item("Sabão Líquido", 18, {
        "Gordura na Pele": 4,
        "Caspa no Cabelo": 1,
        "Mão Podre": 4,
        "Acne": 3,
        "Bactéria de Resfriado":2.5,
        "Cárie": 0.5,
        "Bactéria do Pé": 2
    }),
    "Água Comum": Item("Água Comum", 10, {
        "Gordura na Pele": 1.5,
        "Caspa no Cabelo": 1,
        "Mão Podre": 2,
        "Acne": 1,
        "Bactéria de Resfriado": 0.5,
        "Cárie": 1,
        "Bactéria do Pé": 1
    }),
    "Escova para Corpo": Item("Escova para Corpo", 12, {
        "Gordura na Pele": 4,
        "Caspa no Cabelo": 0.5,
        "Mão Podre": 2,
        "Acne": 1,
        "Bactéria de Resfriado": 0.5,
        "Cárie": 0.5,
        "Bactéria do Pé": 2
    }),
    "Lenço Umidecido": Item("Lenço Umidecido", 15, {
        "Gordura na Pele": 1.5,
        "Caspa no Cabelo": 0.5,
        "Mão Podre": 3,
        "Acne": 1,
        "Bactéria de Resfriado": 3,
        "Cárie": 0.5,
        "Bactéria do Pé": 0.5
    }),
    "Shampoo": Item("Shampoo", 16, {
        "Gordura na Pele": 1.5,
        "Caspa no Cabelo": 4,
        "Mão Podre": 2,
        "Acne": 1,
        "Bactéria de Resfriado": 0.5,
        "Cárie": 0.5,
        "Bactéria do Pé": 1
    }),
}

# Função para selecionar ataques eficientes e aleatórios
def selecionar_ataques_eficazes_e_aleatorios(inimigo_nome):
    ataques_eficazes = []
    ataques_aleatorios = []

    # Seleciona os dois ataques mais eficientes contra o inimigo
    for item in itens.values():
        if inimigo_nome in item.eficacias:
            ataques_eficazes.append((item, item.eficacias[inimigo_nome]))

    # Ordena os ataques eficazes por sua eficácia (do maior para o menor)
    ataques_eficazes.sort(key=lambda x: x[1], reverse=True)

    # Seleciona os dois ataques mais eficientes
    ataques_eficazes = [ataques_eficazes[0][0], ataques_eficazes[1][0]] if len(ataques_eficazes) > 1 else [ataques_eficazes[0][0]]

    # Seleciona aleatoriamente os outros dois ataques
    ataques_restantes = [item for item in itens.values() if item not in ataques_eficazes]
    ataques_aleatorios = random.sample(ataques_restantes, 2)

    # Combina os ataques eficazes e aleatórios
    ataques_selecionados = ataques_eficazes + ataques_aleatorios
    return ataques_selecionados

# Função para aplicar animação de fade in
def fade_in():
    alpha = 255
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    fade_surface.set_alpha(alpha)
    screen.blit(fade_surface, (0, 0))
    pygame.display.flip()
    while alpha > 0:
        alpha -= 5
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

# Função para aplicar animação de fade out
def fade_out():
    alpha = 0
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    fade_surface.set_alpha(alpha)
    screen.blit(fade_surface, (0, 0))
    pygame.display.flip()
    while alpha < 255:
        alpha += 5
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

# Função para exibir a tela final de vitória ou derrota
def show_end_screen(vitoria):
    screen.fill(BLACK)
    message = "Vitória de Nala!" if vitoria else "Derrota de Nala!"
    draw_text(message, WIDTH // 2 - 100, HEIGHT // 2, font, WHITE)
    pygame.display.flip()
    pygame.time.delay(2000)  # Exibe a mensagem por 2 segundos

# Selecionar um inimigo aleatório
enemy = random.choice(list(enemies.values()))
enemy_img = enemy_images[enemy.nome]


# Selecionar ataques baseados no inimigo escolhido
itens_selecionados = selecionar_ataques_eficazes_e_aleatorios(enemy.nome)

# Inicializar variáveis do jogador
player_hp = 100
player_max_hp = 100
player_damage_flash = 0  # Agora corretamente definido

# Funções visuais
def draw_text(text, x, y, font=font, color=BLACK):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))

def draw_hp_bar(name, x, y, hp, max_hp):
    bar_width = 150
    bar_height = 15
    hp_ratio = hp / max_hp


    pygame.draw.rect(screen, DARK_GRAY, (x - 10, y - 40, 180, 60))
    pygame.draw.rect(screen, BLACK, (x - 10, y - 40, 180, 60), 3)
    draw_text(name, x, y - 35)
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, bar_width * hp_ratio, bar_height))
    draw_text(f"HP: {hp}/{max_hp}", x, y + 20)

def draw_dialog_box(message):
    pygame.draw.rect(screen, WHITE, (20, 400, 760, 80))
    pygame.draw.rect(screen, BLACK, (20, 400, 760, 80), 4)
    for i, line in enumerate(message.split('\n')):
        draw_text(line, 40, 410 + i * 25, dialog_font)

def draw_attack_buttons(moves, mouse_pos):
    button_width = 350
    button_height = 40
    y_offset = 490
    x_offset_left = 40
    x_offset_right = 400  # A posição para o segundo conjunto de botões

    for i, move in enumerate(moves):
        # Define a cor do botão
        if i < 2:
            button_rect = pygame.Rect(x_offset_left, y_offset + i * (button_height + 10), button_width, button_height)
        else:
            button_rect = pygame.Rect(x_offset_right, y_offset + (i - 2) * (button_height + 10), button_width, button_height)
        
        # Verifica se o mouse está sobre o botão
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT_ORANGE, button_rect, border_radius=15)
        else:
            pygame.draw.rect(screen, GRAY, button_rect, border_radius=15)
        
        pygame.draw.rect(screen, BLACK, button_rect, 3)  # Borda preta

        draw_text(move.nome, button_rect.x + 10, button_rect.y + 10)

def handle_button_click(mouse_pos, moves):
    global selected_move
    button_width = 350
    button_height = 40
    y_offset = 490
    x_offset_left = 40
    x_offset_right = 400

    for i, move in enumerate(moves):
        if i < 2:
            button_rect = pygame.Rect(x_offset_left, y_offset + i * (button_height + 10), button_width, button_height)
        else:
            button_rect = pygame.Rect(x_offset_right, y_offset + (i - 2) * (button_height + 10), button_width, button_height)

        if button_rect.collidepoint(mouse_pos):
            selected_move = i
            return True
    return False

def ataque_do_jogador(item_usado, inimigo):
    dano = item_usado.calcular_dano(inimigo.nome)
    inimigo.hp -= dano
    inimigo.hp = max(inimigo.hp, 0)
    inimigo.damage_flash = 4
    return dano

def ataque_do_inimigo(inimigo):
    atk_nome, atk_dano = inimigo.ataque_aleatorio()
    global player_hp, player_damage_flash
    player_hp -= atk_dano
    player_hp = max(player_hp, 0)
    player_damage_flash = 4
    return atk_nome, atk_dano

def show_battle_intro(enemy_name, background_img, player_img, enemy_img):
    intro_texts = [f"Um inimigo apareceu: {enemy_name}!", "Vai, Nala!"]
    for text in intro_texts:
        fade_text(text)
        pygame.time.delay(800)

    # Transição para a tela de combate
    transition_to_battle(background_img, player_img, enemy_img)

def transition_to_battle(background_img, player_img, enemy_img):
    for alpha in range(0, 256, 10):
        screen.fill(BLACK)

        # Plano de fundo
        temp_bg = background_img.copy()
        temp_bg.set_alpha(alpha)
        screen.blit(temp_bg, (0, 0))

        # Personagens
        temp_player = player_img.copy()
        temp_player.set_alpha(alpha)
        screen.blit(temp_player, (150, 220))

        temp_enemy = enemy_img.copy()
        temp_enemy.set_alpha(alpha)
        screen.blit(temp_enemy, (550, 100))

        # Barras de vida e texto
        draw_hp_bar("Nala", 130, 70, player_hp, player_max_hp)
        draw_hp_bar(enemy.nome, 500, 350, enemy.hp, enemy.max_hp)
        draw_dialog_box("A batalha vai começar!")

        pygame.display.flip()
        pygame.time.delay(40)

def fade_text(text):
    font_intro = pygame.font.SysFont("arial", 36)
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    screen.fill(BLACK)
    pygame.display.flip()

    for alpha in range(0, 256, 10):
        screen.blit(fade_surface, (0, 0))
        fade_surface.set_alpha(alpha)
        draw_text_centered(text, font_intro, WHITE)
        pygame.display.flip()
        pygame.time.delay(30)

    pygame.time.delay(600)

    for alpha in range(255, -1, -10):
        screen.blit(fade_surface, (0, 0))
        fade_surface.set_alpha(alpha)
        draw_text_centered(text, font_intro, WHITE)
        pygame.display.flip()
        pygame.time.delay(30)

def draw_text_centered(text, font, color):
    screen.fill(BLACK)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(rendered, rect)



# Loop principal



selected_move = 0
message = "O que Nala fará?"
clock = pygame.time.Clock()
running = True

battle_phase = 0
current_item = None
last_dano_jogador = 0
last_ataque_inimigo = ("", 0)


# Aplica a animação de fade in antes da batalha
fade_in()
show_battle_intro(enemy.nome, background_img, player_img, enemy_img)



while running:
    screen.blit(background_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()  # Posição do mouse

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
             if event.button == 1 and battle_phase == 0:
                if handle_button_click(event.pos, itens_selecionados):
                    current_item = itens_selecionados[selected_move]
                    message = f"Nala escolheu {current_item.nome}!"
                    battle_phase = 1
    

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if battle_phase == 1:
                    # Fase 1: Jogador ataca
                    dano = ataque_do_jogador(current_item, enemy)
                    last_dano_jogador = dano
                    message = f"Nala usou {current_item.nome}!\nCausou {dano} de dano."
                    battle_phase = 2

                elif battle_phase == 2:
                    # Fase 2: Inimigo ataca
                    if enemy.hp > 0:
                        atk_nome, atk_dano = ataque_do_inimigo(enemy)
                        last_ataque_inimigo = (atk_nome, atk_dano)
                        message = f"{enemy.nome} usou {atk_nome}!\nCausou {atk_dano} de dano."
                    else:
                        message = f"{enemy.nome} foi derrotado!"
                    battle_phase = 3

                elif battle_phase == 3:
                    # Fase 3: Fim do turno → volta pro jogador
                    if enemy.hp <= 0 or player_hp <= 0:
                        fade_out()
                        show_end_screen(player_hp > 0)
                        running = False
                    else:
                        message = "O que Nala fará?"
                        battle_phase = 0


    # Mostrar sprites com efeito de dano
    if player_damage_flash % 2 == 1:
        tinted = player_img.copy()
        tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(tinted, (150, 220))
    else:
        screen.blit(player_img, (150, 220))

    if enemy.damage_flash % 2 == 1:
        tinted = enemy_img.copy()
        tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(tinted, (550, 100))
    else:
        screen.blit(enemy_img, (550, 100))

    if player_damage_flash > 0:
        player_damage_flash -= 1
    if enemy.damage_flash > 0:
        enemy.damage_flash -= 1

    # Mostrar barras de vida
    draw_hp_bar("Nala", 130, 70, player_hp, player_max_hp)
    draw_hp_bar(enemy.nome, 500, 350, enemy.hp, enemy.max_hp)

    # Caixas de diálogo e menu
    draw_dialog_box(message)
    draw_attack_buttons(itens_selecionados, mouse_pos)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()