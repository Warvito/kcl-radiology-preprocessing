""" Wrapper for the preprocessing pipeline """

import argparse
import json
import subprocess
import sys
from pathlib import Path

from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--start", type=int, help="Starting subject index to process.")
    parser.add_argument("--stop", type=int, help="Stopping subject index to process.")
    parser.add_argument("--pipeline_name", type=str, default="runpreproc-v1.0", help="Name of the preprocessing pipeline.")
    parser.add_argument("--ids_filename", type=str, default="/ids_dir/ids.json", help="")
    args = parser.parse_args()

    return args


def run_unires(
    img_path_list: list,
    dir_out: str,
) -> None:
    # Create temporary files with parameters for the pipeline
    with open("/tmp/output_dir.txt", "w") as f:
        f.write(dir_out)

    with open("/tmp/input_files.txt", "w") as f:
        for img_path in img_path_list:
            f.write(f"{str(img_path)}\n")

    try:
        command = f"/opt/spm12/spm12 script {'/workspace/src/registration_script.m'}"
        subprocess.run(command, check=True, stdout=subprocess.PIPE, shell=True)
    except Exception as e:
        print("SPM script registration_script.m failed")
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

    subjects_list = subjects_list[args.start : args.stop]
    pbar = tqdm(subjects_list, total=len(subjects_list), file=sys.stdout, disable=False)
    for scan_session in pbar:
        for img_path in scan_session["image_paths"]:
            img_path = Path(img_path)
            if not img_path.is_file():
                print(f"{str(img_path)} is not a file.")

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
    pbar.close()

if __name__ == "__main__":
    args = parse_args()
    main(args)
