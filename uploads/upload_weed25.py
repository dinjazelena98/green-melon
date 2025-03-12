from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from roboflow import Roboflow
from roboflow.adapters.rfapi import AnnotationSaveError

rf = Roboflow(api_key="qiNHzBuSAMJTdQQUlbfH")
project = rf.workspace().project("green-melon")


def upload_image(image_path: Path, label: str) -> None:
    """Upload image/annot to Roboflow."""
    labels_dir: Path = Path(f"dataset/{label}/labels")
    annot_path: Path = labels_dir / (image_path.stem + ".txt")

    try:
        return print(
            project.single_upload(
                image_path=image_path,
                annotation_path=annot_path,
                annotation_labelmap="labelmap.yml",
                batch_name=f"weed25-{label.replace('_', '-')}",
                tag_names=[f"weed25-{label.replace('_', '-')}"],
                num_retry_uploads=3
            )
        )

    except AnnotationSaveError:
        print(f"Uploading without annotation: {annot_path.name}")
        return print(
            project.single_upload(
                image_path=image_path,
                annotation_labelmap="labelmap.yml",
                batch_name=f"weed25-{label.replace('_', '-')}",
                tag_names=[f"weed25-{label.replace('_', '-')}"],
                num_retry_uploads=3
            )
        )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--label", type=str, required=True)
    args = parser.parse_args()

    image_paths = list(Path(f"dataset/{args.label}/images").glob("*"))

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_image = {
            executor.submit(upload_image, img, args.label): img for img in image_paths
        }

        for future in as_completed(future_to_image):
            img = future_to_image[future]
            result = future.result()