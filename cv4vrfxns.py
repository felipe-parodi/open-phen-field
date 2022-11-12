"""
Script with helper functions for processing bbox data.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def compute_centers(pkl_file):
    """
    Compute centers of bounding boxes for each frame.

    Parameters
    ----------
    pkl_file : str
        Path to pickle file with bbox data.

    Returns
    -------
    centers : np.ndarray
        Array of shape (n_frames, 2) with x and y coordinates of centers of bounding boxes.

    empties : np.ndarray
        List of frames with no bounding boxes.
    """
    empties, centers = [], []  # add empties to list
    pkl_frame = pd.read_pickle(pkl_file)  # load pkl file
    pkl_frame = pkl_frame.rename(columns={0: "bbox"})  # each row is [x1, y1, x2, y2, score]
    # Drop the first and last 5% of the data:
    pkl_frame = pkl_frame.iloc[
        int(len(pkl_frame) * 0.05) : int(len(pkl_frame) * 0.95)
    ]

    for i in range(len(pkl_frame)):  # for each row, keep the first bbox
        try:
            pkl_frame.iloc[i][0] = pkl_frame.iloc[i][0][0]
            pkl_frame.iloc[i][0] = pkl_frame.iloc[i][0][:-1]  # drop score
            x_center = (pkl_frame.iloc[i][0][0] + pkl_frame.iloc[i][0][2]) / 2
            y_center = (pkl_frame.iloc[i][0][1] + pkl_frame.iloc[i][0][3]) / 2
            centers.append([x_center, y_center])
        except IndexError:
            empties.append(i)
            pkl_frame.iloc[i][0] = [0, 0, 0, 0]
    
    # Interpret empty rows
    print("The number of empty rows is: ", len(empties))
    print(
        "The individual was close to the wall for ",
        len(empties) / len(pkl_frame) * 100,
        "% of the time",
    )

    centers = np.array(centers)
    # print("The shape of the centers array is: ", centers.shape)
    # print("The shape of the empties array is: ", len(empties))
    # drop rows with no bounding boxes from centers
    # centers = np.delete(centers, empties, axis=0)  # drop [0,0] from centers

    return centers, empties


def plot_centers(centers, subject, outdir):
    """
    Plot centers of bounding boxes.

    Parameters
    ----------
    centers : np.ndarray
        Array of shape (n_frames, 2) with x and y coordinates of centers of bounding boxes.
    subject : int
        Subject number.

    outdir : str
        Path to output directory.

    Returns
    -------
    pdf_plot : pdf
        PDF of plot.

    png_plot : png
        PNG of plot.
    """
    # plt.figure(figsize=(10,10))
    plt.plot(centers[:, 0], centers[:, 1], "o", color="r", alpha=0.05)
    plt.title("Centers of Bounding Boxes for " + str(subject))
    plt.plot(322, 210, "o", color="b", alpha=0.5)
    plt.text(322, 210, "center", fontsize=12)
    plt.xlabel("South Wall")
    plt.ylabel("West Wall")
    plt.xticks([])
    plt.yticks([])
    # save figure as pdf in outdir
    plt.savefig(
        outdir
        + "/" + "subject"
        + str(subject)
        + "_trajectory.pdf",
        format="pdf",
        dpi=1200,
        transparent=True,
    )
    # save figure as png in outdir
    plt.savefig(
        outdir
        + "/" + "subject"
        + str(subject)
        + "_trajectory.png",
        format="png",
        dpi=1200,
        transparent=True,
    )
    plt.close()
    print("Plots saved to: ", outdir)