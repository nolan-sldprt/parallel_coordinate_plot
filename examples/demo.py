import matplotlib.pyplot as plt

import parallel_coordinate_plot

def main():
    headers: list[str] = ["legs", "arms", "stomachs", "average height (m)", "colour", "tails"]

    content: dict[str, list] = {
        "cow": [4, 0, 4, 1.575, "white", 1],
        "pig": [4, 0, 1, 0.75, "pink", 1],
        "dog": [4, 0, 1, 0.7, "white", 1],
        "snake": [0, 0, 1, 0.6, "green", 1],
        "gorilla": [2, 2, 1, 1.5, "black", 0]
    }

    parallel_coordinate_plot.plot(
        headers,
        content,
        legend=True,
        title='Animals'
    )

    plt.show()

if __name__ == '__main__':
    main()