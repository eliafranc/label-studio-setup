from pathlib import Path
from tqdm import tqdm
import cv2 as cv
import xml.etree.ElementTree as ET
import argparse
from label_studio_sdk import Client


def get_ls_api_key(file=".api_key.txt"):
    with open(file, "r") as f:
        return f.readline()


def make_task(args, path):
    root_path = Path(args.dataset_root) / Path(path)

    rgb_path = list(root_path.glob("rgb.mp4"))
    audio_path = list(root_path.glob("recording.wav"))
    # event_path = list(root_path.glob("*_events.mp4"))
    # event_raw_path = list(src.glob("*_events.raw"))

    if len(rgb_path) != 1:
        raise ValueError(f"Video missing in {str(root_path)}")
    if len(audio_path) != 1 and args.project_type == 0:
        raise ValueError(f"Audio missing in {str(root_path)}")
    rgb_path = rgb_path[0]
    audio_path = audio_path[0]
    # event_path = event_path[0]
    # event_raw_path = event_raw_path[0]

    rgb_rel_path = rgb_path.relative_to(args.dataset_root)
    audio_rel_path = audio_path.relative_to(args.dataset_root)
    # event_path = os.path.relpath(event_path, dataset_root)
    # event_raw_path = os.path.relpath(event_raw_path, dataset_root)

    vc = cv.VideoCapture(str(rgb_path))
    image_width = int(vc.get(cv.CAP_PROP_FRAME_WIDTH))
    image_height = int(vc.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(vc.get(cv.CAP_PROP_FPS))
    vc.release()

    obj = {
        "data": {
            "video_url": (
                f"http://localhost:8081/StStephan/{str(rgb_rel_path)}"
            ),
            "fps": fps,
            "image_width": image_width,
            "image_height": image_height,
        },
        "annotations": [],
        "predictions": [],
    }

    if args.project_type == 0:
        obj["data"][
            "audio_url"
        ] = f"http://localhost:8081/StStephan/{str(audio_rel_path)}"

    return obj


def main():
    args = parse_args()
    if args.project_type == 0:
        tree = ET.parse("label_config/sequence_config.xml")
    elif args.project_type == 1:
        tree = ET.parse("label_config/bounding_box_config.xml")
    else:
        raise ValueError("Invalid project type")
    root = tree.getroot()
    label_conf = ET.tostring(root, encoding="unicode", method="xml")
    ls_client = Client(args.url, args.apikey)
    ls_project = ls_client.start_project(
        title=args.project_name, label_config=label_conf
    )

    with open(args.dataset_config, "r") as f:
        for i, line in tqdm(enumerate(f)):
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue

            try:
                task = make_task(args, line)
                ls_project.import_tasks([task])

            except ValueError as e:
                continue


def parse_args():
    default_api_key = get_ls_api_key()
    parser = argparse.ArgumentParser(
        description="Generate tasks that can be imported into Label Studio."
    )
    parser.add_argument(
        "-p",
        "--project_name",
        type=str,
        help="Name of the project",
    )
    parser.add_argument(
        "-t",
        "--project_type",
        type=int,
        default=0,
        help=(
            "The project type. 0: For data that should be labeled into"
            " subsequences, 1: For data that should be labeled with bounding"
            " boxes."
        ),
    )
    parser.add_argument(
        "-d",
        "--dataset_root",
        type=str,
        help=(
            "Destination of the dataset root, i.e."
            " /archive/jmandula/Armasuisse/StStephan."
        ),
    )
    parser.add_argument(
        "-c",
        "--dataset_config",
        type=str,
        help=(
            "Destination of the dataset config file, i.e."
            " data_config/recordings_ststephan.txt"
        ),
    )
    parser.add_argument(
        "-n",
        "--dataset_name",
        type=str,
        help=(
            "Name of the dataset, i.e. StStephan. Make sure that the name is"
            " equivalent with the name in the docker-compose file."
        ),
    )
    parser.add_argument(
        "-u", "--url", type=str, default="http://localhost:8080"
    )
    parser.add_argument("-k", "--apikey", type=str, default=default_api_key)

    return parser.parse_args()


if __name__ == "__main__":
    main()
