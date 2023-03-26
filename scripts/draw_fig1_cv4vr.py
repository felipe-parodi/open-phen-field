"""
Script to draw individual examples of 
subject trajectories from the top-down 
2D bbox dataset.

Usage: python3 draw_fig1_cv4vr.py
"""

import argparse
import glob
import os

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
    subject : str
        Subject ID.
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

    # Parse arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pkl", type=str, default=None)
    parser.add_argument(
        "--datadir",
        type=str,
        default="/data2/fparodi/human/cv4vr/",
        help="Path to data directory",
    )
    parser.add_argument("--subject", type=int, default=1, help="Subject ID")
    parser.add_argument(
        "--outdir",
        type=str,
        default="/data2/fparodi/human/cv4vr/figures/",
        help="Path to output directory",
    )
    parser.add_argument(
        "--anxiety",
        type=str,
        default="low_anxiety",
        help="pick from high_anxiety, low_anxiety, moderate_anxiety",
    )
    args = parser.parse_args()

    if args.pkl is not None:
        data_dir = args.pkl
        out_dir = args.outdir
        # subject is first 2 characters of pkl file:
        subject = args.pkl.split("/")[-1][:2]
        # if subject is not a number, it's a 1-digit subject number:
        if not subject.isdigit():
            subject = args.pkl.split("/")[-1][:1]
        print("Subject is: ", subject)
        centers, _ = compute_centers(args.pkl)
        plot_centers(centers, subject, out_dir)
    else:
        # Set up paths:
        subject = args.subject
        out_dir = args.outdir
        anxiety = args.anxiety
        data_dir = args.datadir

        # make outdir if it doesn't exist:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        # Load data:
        pkl_file_path = data_dir + anxiety

        # search for subject in pkl_file_path
        pkl_file = glob.glob(pkl_file_path + "/*" + str(subject) + "*.pkl")
        # if basename starts with subject number, then it's the right file
        pkl_file = [f for f in pkl_file if os.path.basename(f).startswith(str(subject))]

        # Compute and plot centers:
        centers, _ = compute_centers(pkl_file[0])
        plot_centers(centers, subject, out_dir)

if __name__ == "__main__":
    main()

