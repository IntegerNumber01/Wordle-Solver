import pygame
from wordle_bot import WordleBot

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption("Wordle Solver")

GREEN = (96, 140, 82)
YELLOW = (177, 160, 67)
GRAY = (58, 58, 60)
WHITE = (216, 218, 220)


def render_grid(x_cells, y_cells, cell_size, top_left_x, top_left_y):
    rectangles = []

    for x in range(top_left_x, (x_cells * cell_size) + top_left_x, cell_size):
        for y in range(top_left_y, (y_cells * cell_size) + top_left_y, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect, 1)
            rectangles.append(rect)

    return rectangles


def render_disabled_cover(x, y, width, height, r, g, b, a):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((r, g, b, a))
    screen.blit(surface, (x, y))


def render_buttons():
    # Render clear color button
    clear_color_rect = pygame.Rect(410, 0, 30, 30)
    pygame.draw.rect(screen, WHITE, clear_color_rect, 1)
    pygame.draw.line(screen, WHITE, (410, 0), (440, 30))

    # Render green button
    green_rect = pygame.Rect(440, 0, 30, 30)
    pygame.draw.rect(screen, GREEN, green_rect)

    # Render yellow button
    yellow_rect = pygame.Rect(470, 0, 30, 30)
    pygame.draw.rect(screen, YELLOW, yellow_rect)

    guess_button = pygame.Rect(0, 0, 90, 30)
    pygame.draw.rect(screen, WHITE, guess_button)
    # print(normal_font.size('GUESS'))
    render_text('GUESS', 12.5, 0, normal_font)

    refresh_button = pygame.Rect(100, 0, 44, 30)
    # print(normal_font.size('↻'))
    pygame.draw.rect(screen, WHITE, refresh_button)
    render_text("↻", 112.5, 4, refresh_icon_font)

    clear_button = pygame.Rect(154, 0, 89, 30)
    # print(normal_font.size('CLEAR'))
    pygame.draw.rect(screen, WHITE, clear_button)
    render_text("CLEAR", 166.5, 0, normal_font)

    # Render disabled covers
    # GUESS BUTTON
    if guess_disabled:
        render_disabled_cover(0, 0, 90, 30, *GRAY, 220)
    # REFRESH BUTTON
    if refresh_disabled:
        render_disabled_cover(100, 0, 44, 30, *GRAY, 220)

    return green_rect, yellow_rect, clear_color_rect, guess_button, refresh_button, clear_button


def render_colors_on_grid(greens, yellows):
    for coord in greens:
        pygame.draw.rect(screen, GREEN, (coord[0], coord[1], cell_size, cell_size))

    for coord in yellows:
        pygame.draw.rect(screen, YELLOW, (coord[0], coord[1], cell_size, cell_size))


def render_text(text, x, y, font, color='black'):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def calculate_color_place_val():
    '''
    Takes the lists containing the coordinates of the selected colors
    and converts them into lists with place values for the `guess()` function
    to read
    '''
    green = []
    yellow = []
    gray = []

    for i in range(len(entered_words)):
        green.append('')
        yellow.append('')
        # gray.append('')

    # GREEN
    for coord in selected_greens:
        x = coord[0]
        y = coord[1]

        x -= grid_start_x
        y -= grid_start_y

        green[int(y / cell_size)] += str(int(x / cell_size))

    # Sort each value to be in ascending order
    for i, value in enumerate(green):
        value = list(value)
        value.sort()
        # Convert list back into string
        value = ''.join(value)

        green[i] = value

    # YELLOW
    for coord in selected_yellows:
        x = coord[0]
        y = coord[1]

        x -= grid_start_x
        y -= grid_start_y

        yellow[int(y / cell_size)] += str(int(x / cell_size))

    # Sort each value to be in ascending order
    for i, value in enumerate(yellow):
        value = list(value)
        value.sort()
        # Convert list back into string
        value = ''.join(value)

        yellow[i] = value

    # Calculate grays
    for i in range(len(green)):
        gray.append(bot.calculate_gray_left(green[i], yellow[i]))

    return green, yellow, gray


def remove_empty_rows():
    for i in range(len(entered_words)):
        if entered_words[-1] == '':
            entered_words.pop(-1)
            guessed_green_vals.pop(-1)
            guessed_yellow_vals.pop(-1)
            guessed_gray_vals.pop(-1)


letter_font = pygame.font.Font('C:/Windows/Fonts/DOSIS-REGULAR.ttf', 50)
normal_font = pygame.font.Font('C:/Windows/Fonts/DOSIS-REGULAR.ttf', 25)
refresh_icon_font = pygame.font.Font("C:/Windows/Fonts/seguiemj.ttf", 25)

bot = WordleBot()
entered_words = ['']
row = 0

x_cells = 5
y_cells = 6
cell_size = 60
grid_start_x, grid_start_y = 100, 100

guessed_green_vals = []
guessed_yellow_vals = []
guessed_gray_vals = []

selected_greens = []
selected_yellows = []
green_selection = False
yellow_selection = False
color_eraser = False

bot_word = None
status = None

guess_disabled = False
refresh_disabled = False

grid_rectangles = render_grid(x_cells, y_cells, cell_size,
                              grid_start_x, grid_start_y)
green_rect, yellow_rect, clear_color_rect, guess_button_rect, refresh_button_rect, clear_button_rect = render_buttons()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key == 'space':
                pass
            elif key == 'return':
                if row < 5:
                    row += 1
                    entered_words.append('')
            elif key == 'backspace':
                entered_words[row] = entered_words[row][:-1]
            elif not len(entered_words[row]) == 5:
                entered_words[row] = entered_words[row] + key
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos
            clear_selectors = True
            for rect in grid_rectangles:
                if rect.collidepoint(mouse):
                    if green_selection:
                        selected_greens.append(rect.topleft)

                        # Remove the coord from yellow list if nessesary
                        if rect.topleft in selected_yellows:
                            selected_yellows.remove(rect.topleft)
                    elif yellow_selection:
                        selected_yellows.append(rect.topleft)

                        # Remove the coord from green list if nessesary
                        if rect.topleft in selected_greens:
                            selected_greens.remove(rect.topleft)
                    elif color_eraser:
                        if rect.topleft in selected_greens:
                            selected_greens.remove(rect.topleft)
                        if rect.topleft in selected_yellows:
                            selected_yellows.remove(rect.topleft)
                    clear_selectors = False

            if green_rect.collidepoint(mouse):
                green_selection = True
                yellow_selection = False
                color_eraser = False
            elif yellow_rect.collidepoint(mouse):
                yellow_selection = True
                green_selection = False
                color_eraser = False
            elif clear_color_rect.collidepoint(mouse):
                yellow_selection = False
                green_selection = False
                color_eraser = True
            elif clear_button_rect.collidepoint(mouse):
                green_selection = False
                yellow_selection = False
                color_eraser = False

                guess_disabled = False
                refresh_disabled = False

                status = None

                guessed_green_vals = []
                guessed_yellow_vals = []
                guessed_gray_vals = []

                entered_words = ['']

                selected_greens = []
                selected_yellows = []

                row = 0

                bot.reset()
            elif refresh_button_rect.collidepoint(mouse):
                green_selection = False
                yellow_selection = False
                color_eraser = False

                bot.word_fail(bot_word)

                bot_word = bot.guess(guessed_green_vals, guessed_yellow_vals,
                                     guessed_gray_vals, entered_words)

                if bot_word == "E":
                    refresh_disabled = True
                    status = "OUT OF WORDS"
                else:
                    entered_words.pop(-1)
                    guessed_green_vals.pop(-1)
                    guessed_yellow_vals.pop(-1)
                    guessed_gray_vals.pop(-1)

                    guessed_green_vals, guessed_yellow_vals, guessed_gray_vals = calculate_color_place_val()
                    entered_words.append(bot_word)
            elif guess_button_rect.collidepoint(mouse):
                green_selection = False
                yellow_selection = False
                color_eraser = False

                remove_empty_rows()
                guessed_green_vals, guessed_yellow_vals, guessed_gray_vals = calculate_color_place_val()
                bot_word = bot.guess(guessed_green_vals, guessed_yellow_vals,
                                     guessed_gray_vals, entered_words)

                if not bot_word == "E" and len(entered_words) < 6:
                    entered_words.append(bot_word)
                    row += 1
                else:
                    guess_disabled = True
                    refresh_disabled = True
                    status = "OUT OF WORDS"
            elif clear_selectors:
                green_selection = False
                yellow_selection = False
                color_eraser = False

    screen.fill((18, 18, 19))

    render_colors_on_grid(selected_greens, selected_yellows)
    render_grid(x_cells, y_cells, cell_size, grid_start_x, grid_start_y)
    render_buttons()

    for row, text in enumerate(entered_words):
        for i, letter in enumerate(text):
            letter_width = letter_font.size(letter)[0]
            letter_height = letter_font.size(letter)[1]
            x = grid_start_x + ((cell_size - letter_width) / 2) + (cell_size * i)
            y = grid_start_y + ((cell_size - letter_height) / 2) + (cell_size * row)
            render_text(letter.upper(), x, y, letter_font, WHITE)

    if status is not None:
        width = normal_font.size(status)[0]
        render_text(status, (500 - width) / 2, 540, normal_font, WHITE)

    pygame.display.flip()

    # print(entered_words)
    # print(guessed_green_vals)
    # print(guessed_yellow_vals)
    # print(guessed_gray_vals)
    # print('?????????????????????')

pygame.quit()
