""" Script to preprocess the images using UniRes.

This script preprocess the list of images indicated in the inputted id list (tsv file).

Based on /dgx1a/nfs/home/mbrudfors/Projects/unires/preproc.py
"""
import argparse
import json
import sys
from pathlib import Path
from typing import List

import nibabel as nib
from tqdm import tqdm
from unires.run import preproc
from unires.struct import settings

nib.Nifti1Header.quaternion_threshold = -1e-06


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--start", type=int, help="Starting subject index to process.")
    parser.add_argument("--stop", type=int, help="Stopping subject index to process.")
    parser.add_argument(
        "--pipeline_name",
        type=str,
        default="super-res",
        help="Name of the preprocessing pipeline."
    )
    parser.add_argument(
        "--ids_filename",
        type=str,
        default="/project/data/ids.json",
        help=""
    )
    args = parser.parse_args()

    return args


def run_unires(
        img_path_list: List,
        dir_out: str,
) -> None:
    config = settings()
    config.atlas_rigid = True
    config.common_output = True
    config.crop = True
    config.dir_out = dir_out
    config.do_atlas_align = True
    config.do_coreg = True
    config.do_res_origin = True
    config.fov = "head"
    config.max_iter = 0
    config.prefix = ""
    config.pow = 256
    config.vx = 1

    try:
        _ = preproc(img_path_list, config)[0]
    except Exception as e:
        print("GOT AN ERROR!")
        print(e)


def main(args):
    print("Arguments:")
    for k, v in vars(args).items():
        print(f"  {k}: {v}")

    target_dir = Path("/target/")
    pipeline_dir = target_dir / args.pipeline_name
    pipeline_dir.mkdir(exist_ok=True)

    with open(args.ids_filename) as json_file:
        subjects_list = json.load(json_file)["participants"]

    subjects_list = subjects_list[args.start: args.stop]
    for scan_session in tqdm(subjects_list, total=len(subjects_list), file=sys.stdout, disable=True):
        for img_path in scan_session["image_paths"]:
            img_path = Path(img_path)
            if not img_path.is_file():
                print(f"{str(img_path)} do not exists")

        if len(scan_session["image_paths"]) > 0:
            subject_dir = pipeline_dir / scan_session["participant_id"] / scan_session["session_id"] / "anat"

            # Check if subject already preprocessed
            if subject_dir.is_dir():
                existing_files = list(subject_dir.glob("*.nii.gz"))
                if len(existing_files) > 0:
                    continue

            subject_dir.mkdir(exist_ok=True, parents=True)

            run_unires(scan_session["image_paths"], str(subject_dir))
        else:
            print("Empty session list!")


if __name__ == "__main__":
    args = parse_args()
    main(args)
