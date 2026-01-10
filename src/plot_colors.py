import matplotlib.pyplot as plt
import matplotlib.patches as patches

def display_dark_academia_palette():
    # Define the Dark Academia Color Palette
    palette = {
        "Obsidian Ink": "#1B1B1B",
        "Charcoal Wool": "#363636",
        "Worn Leather": "#5D4037",
        "Velvet Burgundy": "#58181F",
        "Ivy League Green": "#1F2823",
        "Midnight Study": "#202A36",
        "Autumn Tweed": "#9E7E52",
        "Antique Gold": "#BFA255",
        "Aged Parchment": "#E4D7C2"
    }

    # Setup the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    n_colors = len(palette)

    # Hide axes
    ax.set_xlim(0, n_colors)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Draw color swatches
    for i, (name, hex_code) in enumerate(palette.items()):
        # Create rectangle for color
        rect = patches.Rectangle((i, 0), 1, 1, linewidth=0, facecolor=hex_code)
        ax.add_patch(rect)

        # Add Name label
        ax.text(i + 0.5, -0.1, name, ha='center', va='top',
                fontsize=10, fontname='serif', color='#1B1B1B')

        # Add Hex code label
        ax.text(i + 0.5, -0.2, hex_code, ha='center', va='top',
                fontsize=9, fontfamily='monospace', color='#363636')

    # Title
    plt.text(n_colors / 2, 1.15, "Dark Academia Palette",
             ha='center', va='center', fontsize=16, fontname='serif', weight='bold')

    # Adjust layout to prevent clipping of labels
    plt.subplots_adjust(bottom=0.25, top=0.85)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    display_dark_academia_palette()
