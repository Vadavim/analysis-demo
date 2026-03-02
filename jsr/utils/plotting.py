import os

def plot_write_image(fig, output_name,
                     width=900, height=500, scale=2):
    # Create directory to store figures (if it doesn't alreadt exist)
    figure_directory = "figures/"
    os.makedirs(figure_directory, exist_ok=True)

    fig.write_image(
        "figures/{}.png".format(output_name),
        width=width,
        height=height,
        scale=scale
    )