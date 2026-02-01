import matplotlib.pyplot as plt

import parallel_coordinate_plot

def main():
    headers: list[str] = ["legs", "arms", "stomachs", "average height (m)", "colour", "tails", "aquatic\nrespiration"]

    content: dict[str, list] = {
        "cow": [4, 0, 4, 1.575, "white", 1, False],
        "pig": [4, 0, 1, 0.75, "pink", 1, False],
        "dog": [4, 0, 1, 0.7, "white", 1, False],
        "snake": [0, 0, 1, 0.6, "green", 1, False],
        "gorilla": [2, 2, 1, 1.5, "black", 0, False],
        "fish": [0, 0, 1, 0.3, "grey", 1, True],
        "nurse shark": [0, 0, 1, 2.5, "brown", 1, True]
    }

    parallel_coordinate_plot.plot(
        headers,
        content,
        legend=True,
        title='Animals',
        markersize=10
    )

    plt.show()

if __name__ == '__main__':
    main()