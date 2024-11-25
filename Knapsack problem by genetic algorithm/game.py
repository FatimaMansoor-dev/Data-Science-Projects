import pygame
import sys
from algo import KnapSack  
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BUTTON_COLOR = (102, 0, 102)
BUTTON_HOVER_COLOR = (153, 0, 153)
TEXT_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
ITEM_FONT_COLOR = (50, 50, 50)
PURPLE = (100, 0, 1)
BLUE = (0, 0, 255)
transparent = (0, 0, 0, 0)


# Set up display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Window")

# Fonts
font_large = pygame.font.SysFont("Arial", 60, bold=True, italic=True)
font_medium = pygame.font.SysFont("Arial", 30)
font_small = pygame.font.SysFont("Arial", 20)

# Load background image
bg_image = pygame.image.load("assets/knap2.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))


def display_text(win, text, y_offset, font, color=BLACK):
    for line in text:
        rendered_text = font.render(line, True, color)  # Use the passed color
        WIN.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, y_offset))
        y_offset += 40  # Line spacing
    return y_offset
def game_window():
    ks = KnapSack(10, random.choice([10000, 20000, 16000, 25000, 10100]))
    ks.generate_population()
    budget = ks.budget
    items = ks.get_item_details()
    selected_items = [0] * len(items)
    remaining_budget = budget

    # Get the optimal solution and its value
    best_solution, best_value = ks.run_algorithm(generations=50)

    result_text = ""
    feedback_text = ""
    result_displayed = False

    running = True

    while running:
        # Draw background
        WIN.blit(bg_image, (0, 0))

        # Overlay semi-transparent gradient
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(PURPLE)
        WIN.blit(overlay, (0, 0))

        # Display budget and instructions
        text_color = CYAN
        y_offset = 30
        text = [
            f"Your Budget: Rs. {remaining_budget}",
            "You went to an exhibition with a certain budget. Select items to get maximum value within your budget."
        ]
        y_offset = display_text(WIN, text, y_offset, font_small, text_color)

        # Split items into two columns
        left_items = items[:5]
        right_items = items[5:]

        # Display items in the left column
        for idx, item in enumerate(left_items):
            x, y = 100, 150 + idx * 60
            panel_width, panel_height = 300, 50
            panel_rect = pygame.Rect(x, y, panel_width, panel_height + 20)

            # Highlight if hovered
            if panel_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(WIN, BUTTON_HOVER_COLOR, panel_rect, border_radius=15)
            else:
                pygame.draw.rect(WIN, BUTTON_COLOR, panel_rect, border_radius=15)

            # Highlight if selected
            if selected_items[items.index(item)] > 0:
                pygame.draw.rect(WIN, CYAN, panel_rect, 3, border_radius=15)

            # Item details split into two lines
            item_text_line1 = f"{item['name']} - Price: Rs. {item['price']}"
            item_text_line2 = f"Qty: {item['quantity']} - Value: {item['value']}"

            rendered_text_line1 = font_small.render(item_text_line1, True, WHITE)
            rendered_text_line2 = font_small.render(item_text_line2, True, WHITE)

            # Display the two lines
            WIN.blit(rendered_text_line1, (x + 20, y + 10))
            WIN.blit(rendered_text_line2, (x + 20, y + 30))

        # Display items in the right column
        for idx, item in enumerate(right_items):
            x, y = 450, 150 + idx * 60
            panel_width, panel_height = 300, 50
            panel_rect = pygame.Rect(x, y, panel_width, panel_height + 20)

            # Highlight if hovered
            if panel_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(WIN, BUTTON_HOVER_COLOR, panel_rect, border_radius=15)
            else:
                pygame.draw.rect(WIN, BUTTON_COLOR, panel_rect, border_radius=15)

            # Highlight if selected
            if selected_items[items.index(item)] > 0:
                pygame.draw.rect(WIN, CYAN, panel_rect, 3, border_radius=15)

            # Item details split into two lines
            item_text_line1 = f"{item['name']} - Price: Rs. {item['price']}"
            item_text_line2 = f"Qty: {item['quantity']} - Value: {item['value']}"

            rendered_text_line1 = font_small.render(item_text_line1, True, WHITE)
            rendered_text_line2 = font_small.render(item_text_line2, True, WHITE)

            # Display the two lines
            WIN.blit(rendered_text_line1, (x + 20, y + 10))
            WIN.blit(rendered_text_line2, (x + 20, y + 30))

        # Create the "See Result" button
        button_width, button_height = 200, 50
        button_x = (WIDTH - button_width) // 2
        button_y = HEIGHT - 100
        if button_x < pygame.mouse.get_pos()[0] < button_x + button_width and button_y < pygame.mouse.get_pos()[1] < button_y + button_height:
            pygame.draw.rect(WIN, BUTTON_HOVER_COLOR, (button_x, button_y, button_width, button_height))
        else:
            pygame.draw.rect(WIN, BUTTON_COLOR, (button_x, button_y, button_width, button_height))

        button_text = font_medium.render("See Result", True, TEXT_COLOR)
        WIN.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2, button_y + 10))

        # Event handling
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                feedback_text = ""
                # Check for item selection
                for idx, item in enumerate(items):
                    x, y = (100, 150 + idx * 60) if idx < 5 else (450, 150 + (idx - 5) * 60)
                    panel_rect = pygame.Rect(x, y, 300, 50)
                    if panel_rect.collidepoint(mouse_pos):
                        if item['quantity'] == 0:
                            feedback_text = "Item Sold Out!"
                        elif remaining_budget >= item['price']:
                            selected_items[items.index(item)] += 1
                            remaining_budget -= item['price']
                            item['quantity'] -= 1
                        else:
                            feedback_text = "Insufficient Budget!"

                # Check if "See Result" button was clicked
                # Inside the game_window() function:

                # In the MOUSEBUTTONDOWN event handler:
                if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
                    # Calculate the total value of selected items
                    user_value = sum(selected_items[i] * items[i]['value'] for i in range(len(items)))

                    # Check if the selected items match the optimal solution
                    if selected_items == best_solution:
                        result_text = f"Good Job!  Optimal Value: {best_value}, Your Value: {user_value}"
                    else:
                        result_text = f"Oops, Wrong Answer!  Optimal Value: {best_value}, Your Value: {user_value}"
                    
                    result_displayed = True


        # Display the result message
        if result_displayed:
            result_text_rendered = font_medium.render(result_text, True, TEXT_COLOR)
            WIN.blit(result_text_rendered, (WIDTH // 2 - result_text_rendered.get_width() // 2, HEIGHT - 50))

        pygame.display.update()


def main_menu():
    """Main menu of the game."""
    running = True
    while running:
        WIN.blit(bg_image, (0, 0))  # Draw the background
        mouse_pos = pygame.mouse.get_pos()

        # Draw the title
        title_text = font_large.render("Knapsack Game", True, CYAN)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 370))

        # Draw the play button
        button_width, button_height = 200, 50
        button_x = (WIDTH - button_width) // 2
        button_y = 500
        if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
            pygame.draw.rect(WIN, BUTTON_HOVER_COLOR, (button_x, button_y, button_width, button_height))
        else:
            pygame.draw.rect(WIN, BUTTON_COLOR, (button_x, button_y, button_width, button_height))

        button_text = font_medium.render("Play!", True, TEXT_COLOR)
        WIN.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2, button_y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
                    running = False
                    game_window()  # Go to game window

        pygame.display.update()


# Run the game
main_menu()
