import random
import pygame


pygame.init()


WINDOW_WIDTH, WINDOW_HEIGHT = 900, 700 
ROWS, COLS = 10, 4
CELL_SIZE = 50
PADDING = 10
GRID_OFFSET_X = (WINDOW_WIDTH - (COLS * (CELL_SIZE + PADDING))) // 2
GRID_OFFSET_Y = 100
COLOR_SELECTION_OFFSET = WINDOW_WIDTH - 100
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BUTTON_X, BUTTON_Y = COLOR_SELECTION_OFFSET - 160, GRID_OFFSET_Y + 6 * (CELL_SIZE + PADDING)  # À côté de la sélection des couleurs

# Couleurs
COLORS = {
    "rouge": (255, 0, 0),
    "bleu": (0, 0, 255),
    "vert": (0, 255, 0),
    "jaune": (255, 255, 0),
    "noir": (0, 0, 0),
    "blanc": (255, 255, 255),
    "gris": (200, 200, 200),
    "vert_clair": (144, 238, 144),  # Couleur pour les positions correctes
    "orange": (255, 165, 0)        # Couleur pour les couleurs correctes mais mal placées
}
COLOR_NAMES = ['rouge', 'bleu', 'vert', 'jaune', 'noir', 'blanc']

# Configurer la fenêtre
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mastermind")

# Polices
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Fonction pour permettre à l'utilisateur de choisir la combinaison secrète
def get_secret_combination():
    colors = COLOR_NAMES[:6]
    while True:
        user_input = input("Entrez la combinaison secrète de 4 couleurs (rouge, bleu, vert, jaune, noir, blanc) séparées par des espaces: ").strip().lower().split()
        if len(user_input) == 4 and all(color in colors for color in user_input):
            return user_input
        else:
            print("Entrée invalide. Assurez-vous d'entrer exactement 4 couleurs parmi les suivantes: rouge, bleu, vert, jaune, noir, blanc. Essayez de nouveau.")

# Obtenir une combinaison utilisateur pour chaque tentative
def get_user_combination():
    colors = COLOR_NAMES[:6]
    while True:
        user_input = input("Entrez une combinaison de 4 couleurs (rouge, bleu, vert, jaune, noir, blanc) séparées par des espaces: ").strip().lower().split()
        if len(user_input) == 4 and all(color in colors for color in user_input):
            return user_input
        else:
            print("Entrée invalide. Assurez-vous d'entrer exactement 4 couleurs parmi les suivantes: rouge, bleu, vert, jaune, noir, blanc. Essayez de nouveau.")

def give_feedback(secret, guess):
    correct_position = 0
    correct_colors = 0
    secret_copy = secret[:]
    guess_copy = guess[:]

    for i in range(len(secret)):
        if guess[i] == secret[i]:
            correct_position += 1
            secret_copy[i] = None
            guess_copy[i] = None

    for g in guess_copy:
        if g and g in secret_copy:
            correct_colors += 1
            secret_copy[secret_copy.index(g)] = None

    return '*' * correct_position + '-' * correct_colors

# Fonction pour dessiner la grille de jeu avec des cercles
def draw_grid(offset_y):
    for row in range(ROWS):
        for col in range(COLS):
            center_x = GRID_OFFSET_X + col * (CELL_SIZE + PADDING) + CELL_SIZE // 2
            center_y = GRID_OFFSET_Y + row * (CELL_SIZE + PADDING) + offset_y + CELL_SIZE // 2
            pygame.draw.circle(screen, COLORS["gris"], (center_x, center_y), CELL_SIZE // 2)
            pygame.draw.circle(screen, COLORS["noir"], (center_x, center_y), CELL_SIZE // 2, 2)

# Fonction pour dessiner les tentatives et les indices
def draw_attempts(attempts, feedback, offset_y):
    for row, attempt in enumerate(attempts):
        for col, color in enumerate(attempt):
            center_x = GRID_OFFSET_X + col * (CELL_SIZE + PADDING) + CELL_SIZE // 2
            center_y = GRID_OFFSET_Y + row * (CELL_SIZE + PADDING) + offset_y + CELL_SIZE // 2
            pygame.draw.circle(screen, COLORS[color], (center_x, center_y), CELL_SIZE // 2)
        # Dessiner les indices
        fb = feedback[row]
        for i, char in enumerate(fb):
            color = COLORS["vert_clair"] if char == '*' else COLORS["orange"]
            pygame.draw.circle(screen, color, (GRID_OFFSET_X + COLS * (CELL_SIZE + PADDING) + i * 20 + 20, GRID_OFFSET_Y + row * (CELL_SIZE + PADDING) + offset_y + CELL_SIZE // 2), 8)

# Fonction pour dessiner la sélection de couleurs
def draw_color_selection(selected_color):
    for i, color in enumerate(COLOR_NAMES[:6]):  # Afficher uniquement les 6 couleurs de jeu
        center_x = COLOR_SELECTION_OFFSET + CELL_SIZE // 2
        center_y = GRID_OFFSET_Y + i * (CELL_SIZE + PADDING) + CELL_SIZE // 2
        pygame.draw.circle(screen, COLORS[color], (center_x, center_y), CELL_SIZE // 2)
        if color == selected_color:
            pygame.draw.circle(screen, COLORS["noir"], (center_x, center_y), CELL_SIZE // 2, 3)
        else:
            pygame.draw.circle(screen, COLORS["noir"], (center_x, center_y), CELL_SIZE // 2, 1)

# Fonction pour dessiner le bouton de vérification avec effet hover
def draw_check_button(hover):
    button_color = COLORS["gris"] if not hover else COLORS["vert_clair"]
    pygame.draw.rect(screen, button_color, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    text = font.render("Vérifier", True, COLORS["noir"])
    screen.blit(text, (BUTTON_X + (BUTTON_WIDTH - text.get_width()) // 2, BUTTON_Y + (BUTTON_HEIGHT - text.get_height()) // 2))

# Fonction pour dessiner les labels en bas de la page
def draw_labels():
    labels = [("Bien placé", COLORS["vert_clair"]), ("Mal placé", COLORS["orange"])]
    for i, (label, color) in enumerate(labels):
        pygame.draw.circle(screen, color, (50, WINDOW_HEIGHT - 40 - i * 20), 8)
        text = small_font.render(label, True, COLORS["noir"])
        screen.blit(text, (70, WINDOW_HEIGHT - 45 - i * 20))

# Fonction pour afficher un message de victoire
def draw_victory_message():
    text = font.render("Félicitations! Vous avez gagné!", True, COLORS["rouge"])
    screen.blit(text, ((WINDOW_WIDTH - text.get_width()) // 2, WINDOW_HEIGHT // 2))

# Fonction principale
def mastermind_game():
    secret_combination = get_secret_combination()
    attempts = []
    feedback = []
    current_attempt = [""] * COLS  # Liste pour stocker les couleurs choisies par tentative
    selected_color = COLOR_NAMES[0]
    offset_y = 0
    current_row = 0
    won = False

    running = True
    while running:
        screen.fill(COLORS["blanc"])
        draw_grid(offset_y)
        draw_attempts(attempts, feedback, offset_y)
        draw_color_selection(selected_color)
        draw_labels()
        if won:
            draw_victory_message()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover = BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT
        draw_check_button(hover)

        for col in range(COLS):
            if current_attempt[col] != "":
                center_x = GRID_OFFSET_X + col * (CELL_SIZE + PADDING) + CELL_SIZE // 2
                center_y = GRID_OFFSET_Y + current_row * (CELL_SIZE + PADDING) + offset_y + CELL_SIZE // 2
                pygame.draw.circle(screen, COLORS[current_attempt[col]], (center_x, center_y), CELL_SIZE // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hover and not won:
                    if "" not in current_attempt:
                        attempts.append(current_attempt[:])
                        fb = give_feedback(secret_combination, current_attempt)
                        feedback.append(fb)
                        current_attempt = [""] * COLS
                        current_row += 1
                        if fb == '****':
                            won = True
                        elif len(attempts) == 10:
                            print(f"Vous avez épuisé toutes vos tentatives. La combinaison secrète était: {' '.join(secret_combination)}")
                            running = False
                else:
                    mouse_x, mouse_y = event.pos
                    if COLOR_SELECTION_OFFSET <= mouse_x <= COLOR_SELECTION_OFFSET + CELL_SIZE:
                        selected_color = COLOR_NAMES[(mouse_y - GRID_OFFSET_Y) // (CELL_SIZE + PADDING)]
                    elif GRID_OFFSET_X <= mouse_x <= GRID_OFFSET_X + COLS * (CELL_SIZE + PADDING) and GRID_OFFSET_Y <= mouse_y - offset_y <= GRID_OFFSET_Y + ROWS * (CELL_SIZE + PADDING):
                        col = (mouse_x - GRID_OFFSET_X) // (CELL_SIZE + PADDING)
                        row = (mouse_y - GRID_OFFSET_Y - offset_y) // (CELL_SIZE + PADDING)
                        if row == current_row:
                            current_attempt[col] = selected_color
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    offset_y = min(0, offset_y + CELL_SIZE + PADDING)
                elif event.key == pygame.K_DOWN:
                    offset_y = max(-(len(attempts) - ROWS) * (CELL_SIZE + PADDING), offset_y - CELL_SIZE - PADDING)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    mastermind_game()
