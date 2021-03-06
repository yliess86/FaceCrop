# -*- coding: utf-8 -*-
"""facetool.__main__"""
from facetool.annotator import FaceAnnotator
from facetool.masker import BackgroundMasker
from facetool.visualizer import FaceVisualizer
from facetool.xdoger import XDoGer
from typing import Tuple
from typing import List

import argparse


# Define Command Parser
parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(dest="action")

# Define Annotate Command Arguments
annotate = sub_parsers.add_parser("annotate")
annotate.add_argument(
    "--video", type=str, required=True,
    help="video path to be annotated (mp4 by preference `video.mp4`)"
)
annotate.add_argument(
    "--annotations", type=str, required=True,
    help="annotations saving path (save to csv `annotations.csv`)"
)
annotate.add_argument(
    "--dbatch_size", type=int, required=True,
    help="batch_size for the detector inference"
)
annotate.add_argument(
    "--lbatch_size", type=int, required=True,
    help="batch_size for the landmark video loader"
)
annotate.add_argument(
    "--n_process", type=int, required=True,
    help="number of threads used for lanrmarking"
)
annotate.add_argument(
    "--size", type=int, default=[320, 155], nargs=2, action="store",
    help="resize the video for the detector"
)
annotate.add_argument(
    "-d", "--device", type=str, default="cpu",
    help="device to run detector on, `cpu` or `cuda`"
)

# Define Visualize Command Arguments
visualize = sub_parsers.add_parser("visualize")
visualize.add_argument(
    "--video", type=str, required=True,
    help="video path (mp4 by preference `video.mp4`)"
)
visualize.add_argument(
    "--annotations", type=str, required=True,
    help="annotations path (csv `annotations.csv`)"
)
visualize.add_argument(
    "--save", type=str, default=None,
    help="visualization saving path (gif `visualization.gif`)"
)
visualize.add_argument(
    "--size", type=int, default=[640, 360], nargs=2, action="store",
    help="resize the video to save gif"
)

# Define Masker Command Arguments
mask = sub_parsers.add_parser("mask")
mask.add_argument(
    "--video", type=str, required=True,
    help="video path to be masked (mp4 by preference `video.mp4`)"
)
mask.add_argument(
    "--mask", type=str, required=True,
    help="mask video output path (mp4 by preference `mask.mp4`)"
)
mask.add_argument(
    "--batch_size", type=int, required=True,
    help="batch_size for the segmentation model"
)
mask.add_argument(
    "-d", "--device", type=str, default="cpu",
    help="device to run the segmentation model on, `cpu` or `cuda`"
)

# Define xDoG Command Arguments
xdog = sub_parsers.add_parser("xdog")
xdog.add_argument(
    "--video", type=str, required=True,
    help="video path to be contoured (mp4 by preference `video.mp4`)"
)
xdog.add_argument(
    "--contour", type=str, required=True,
    help="contour video output path (mp4 by preference `contour.mp4`)"
)
xdog.add_argument(
    "--batch_size", type=int, required=True,
    help="batch_size for the segmentation model"
)
xdog.add_argument(
    "-d", "--device", type=str, default="cpu",
    help="device to run the segmentation model on, `cpu` or `cuda`"
)
xdog.add_argument(
    "--sigma1", type=float, default=1.8,
    help="sigma of the first gaussian blur filter"
)
xdog.add_argument(
    "--sigma2", type=float, default=2.5,
    help="sigma of the second gaussian blur filter"
)
xdog.add_argument(
    "--sharpen", type=float, default=28.0,
    help="sharpens the gaussians before computing difference"
)
xdog.add_argument(
    "--phi", type=float, default=1.051,
    help="phi parameter for soft thresholding"
)
xdog.add_argument(
    "--eps", type=float, default=10.7,
    help="epsilon parameter for soft thresholding"
)

# Parse and Process Commands
args = parser.parse_args()
if args.action == "annotate":
    face_annotator = FaceAnnotator(
        dbatch_size=args.dbatch_size, lbatch_size=args.lbatch_size,
        size=args.size, n_process=args.n_process, device=args.device
    )

    # Annotate Video and Save DataFrame
    annotations = face_annotator(args.video)
    annotations.to_csv(args.annotations)

elif args.action == "visualize":
    FaceVisualizer.visualize(
        args.video, args.annotations, save=args.save, size=args.size
    )

elif args.action == "mask":
    bckg_masker = BackgroundMasker(args.batch_size, args.device)
    bckg_masker(args.video, args.mask)

elif args.action == "xdog":
    xdoger = XDoGer(
        args.batch_size, args.device,
        args.sigma1, args.sigma2,
        args.sharpen, args.phi, args.eps
    )
    xdoger(args.video, args.contour)