# visualization_utils.py
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# Global Style Configuration
# ==========================================
WARNING_COLOR = "#D62728"

PALETTE = [
    "#4E79A7",
    "#F28E2B",
    "#E15759",
    "#76B7B2",
    "#59A14F",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7"
]

TITLE_SIZE = 18
LABEL_SIZE = 14
TICK_SIZE  = 12
FIG_WIDTH  = 12
FIG_HEIGHT = 6


# ==========================================
# Helpers
# ==========================================

def set_plot_style():
    """Apply a professional style for all plots."""
    sns.set_theme(
        style="whitegrid",
        palette=PALETTE,
        context="notebook"
    )
    plt.rcParams.update({
        "figure.figsize":      (FIG_WIDTH, FIG_HEIGHT),
        "figure.dpi":          120,
        "axes.titlesize":      TITLE_SIZE,
        "axes.labelsize":      LABEL_SIZE,
        "xtick.labelsize":     TICK_SIZE,
        "ytick.labelsize":     TICK_SIZE,
        "axes.titleweight":    "bold",
        "axes.spines.top":     False,
        "axes.spines.right":   False,
        "legend.frameon":      False,
        "font.family":         "sans-serif",
        "font.sans-serif":     ["Segoe UI", "Arial", "DejaVu Sans"]
    })


def setup_axes(title, xlabel='', ylabel='Frequency'):
    """Standardize title and axis labels. Call plt.tight_layout() yourself after."""
    plt.title(title, pad=15)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def save_figure(filename, path="outputs/graphs"):
    """
    Save the current figure.

    Parameters
    ----------
    filename : str  — name with extension, e.g. 'age_dist.png'
    path     : str  — directory to save into (default: 'figures/')
    """
    plt.savefig(
        f"{path}{filename}",
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )


def get_highlight_colors(values, highlight="crimson", default="steelblue") -> list:
    """Return a color list that accents the max value."""
    max_val = max(values)
    return [highlight if v == max_val else default for v in values]