"""
Script to draw anxiety group
trajectories from the top-down 
2D bbox dataset.

Usage: python3 draw_fig2_cv4vr.py
"""

import argparse
import os

import numpy as np

from cv4vrfxns import compute_centers, plot_centers


def main():
    """
    Main function which computes centers and draws trajectories.

    Usage: python3 drawcv4vrtrajectories.py
    Provide:
        1. Path to the directory containing the pickle files and pkl; or
        2. Subject and anxiety group.

    Parameters
    ----------
    pkl : str
        Path to pickle file with bbox data.
    outdir : str
        Path to output directory.
    datadir : str
        Path to data directory.
    anxiety : str
        Anxiety level.

    Returns
    -------
    centers : np.ndarray
        Array of shape (n_frames, 2) with x and y coordinates of centers of bounding boxes.

    pdf_plot : pdf
        PDF of plot.
    png_plot : png
        PNG of plot.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datadir",
        type=str,
        default="/data2/fparodi/human/cv4vr/",
        help="Path to data directory",
    )
    parser.add_argument(
        "--anxiety",
        type=str,
        default="low_anxiety",
        help="pick from high_anxiety, low_anxiety, moderate_anxiety",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="/data2/fparodi/human/cv4vr/figures/",
        help="Path to output directory",
    )
    args = parser.parse_args()

    data_dir = args.datadir
    anxiety = args.anxiety
    out_dir = args.outdir
    path2pklfiles = os.path.join(data_dir, anxiety)

    # Get all pickle files:
    pkl_files = [file for file in os.listdir(path2pklfiles) if file.endswith(".pkl")]

    # compute centers for each pkl file:
    centers_lst = []
    for file in pkl_files:
        # print(path2pklfiles+file)
        centers, _ = compute_centers(path2pklfiles + "/" + file)
        # centers = np.append(centers)
        centers_lst.append(centers)

    # combine all centers:
    centers = np.concatenate(centers_lst, axis=0)
    print("The shape of the centers array is: ", centers.shape)

    # plot centers:
    plot_centers(centers, anxiety, out_dir)

if __name__ == "__main__":
    main()