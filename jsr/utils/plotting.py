import os
import plotly.graph_objs


def plot_write_image(fig, output_name,
                     width=900, height=500, scale=2):
    """ Writes an image to disk
    Args:
        fig: Plotly figure (go.Figure)
        output_name: Name of output file [.png appended to end] (str)
        width:  width of image in pixels (int)
        height: height of image in pixels (int)
        scale: scale factor for images (int)

    """
    # Create directory to store figures (if it doesn't already exist)
    figure_directory = "figures/"
    os.makedirs(figure_directory, exist_ok=True)

    fig.write_image(
        "figures/{}.png".format(output_name),
        width=width,
        height=height,
        scale=scale
    )

def default_figure_settings(fig: plotly.graph_objs.Figure,
                            x_label: str, y_label: str, title: str):
    """ Default settings for plotly figures
    Args:
        fig: Plotly figure (go.Figure)
        x_label: Label for x-axis (str)
        y_label:  Label for y-axis (str)
        title: Title for plotly figure (str)
    """
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=30),
        xaxis_title=x_label, xaxis_title_font_size=26,
        yaxis_title=y_label, yaxis_title_font_size=26,
        title=title,
        title_y=0.99,
        title_font_size=32,
        font_family="Overpass"
    )
