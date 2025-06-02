import json
import logging
import os
import pathlib
import tempfile
from typing import Optional

from af3_input.colabfold import run_mmseqs2
from af3_input.utils import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


TQDM_BAR_FORMAT = (
    "{l_bar}{bar}| {n_fmt}/{total_fmt} [elapsed: {elapsed} remaining: {remaining}]"
)
DEEPFOLD_API_URL = os.environ.get(
    "DEEPFOLD_API_URL", "https://df-plm.deepfold.org/api/colab"
)


class MMseqs2Exception(Exception):
    def __init__(self):
        msg = (
            "MMseqs2 API is giving errors."
            " Please confirm your input is a valid protein sequence."
            " If error persists, please try again an hour later."
        )
        super().__init__(msg)


def add_msa_to_json(
    *,
    input_jsonpath: pathlib.Path,
    output_jsonpath: pathlib.Path,
    output_a3mpath: Optional[pathlib.Path],
    use_pairing: bool,
    use_block: bool,
    host_url: str,
):
    # Load a input JSON file.
    with input_jsonpath.open("r") as fp:
        af3_json = json.load(fp)

    # Collect protein sequences.
    sequences = {}
    for json_idx, entry in enumerate(af3_json["sequences"]):
        if "protein" in entry:
            seq = entry["protein"]["sequence"]
            sequences[json_idx] = seq

            unpaired_msa = entry["protein"].get("unpairedMsa", None)
            paired_msa = entry["protein"].get("pairedMsa", None)

            if unpaired_msa is not None or paired_msa is not None:
                logger.warning(f"MSA entry is not empty for sequence: {seq}")

    id_map = list(sequences.keys())
    seqs = [sequences[i] for i in id_map]

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Get paired MSA:
        if use_pairing:
            logger.info(f"Fetch paired+unpaired MSAs from {host_url}")
            a3m_lines, _ = run_mmseqs2(
                x=seqs,
                prefix=tmp_dir,
                use_env=True,
                use_filter=True,
                use_templates=False,
                use_pairing=True,
                pairing_strategy="paired+unpaired" if use_block else "dense",
                host_url=host_url,
                user_agent="AF3",
            )
        else:
            logger.info(f"Fetch unpaired MSAs from {host_url}")
            a3m_lines, _ = run_mmseqs2(
                x=seqs,
                prefix=tmp_dir,
                use_env=True,
                use_filter=True,
                use_templates=False,
                use_pairing=False,
                host_url=host_url,
                user_agent="AF3",
            )

    line = ""
    for msa_idx, json_idx in enumerate(id_map):
        entry = af3_json["sequences"][json_idx]
        entry["protein"]["unpairedMsa"] = a3m_lines[msa_idx]
        entry["protein"]["pairedMsa"] = ""
        if "templates" not in entry["protein"]:
            entry["protein"]["templates"] = []
        line += a3m_lines[msa_idx]
        line += "\x00"

    json_string = json.dumps(af3_json, indent=4)
    print(json_string, file=output_jsonpath.open("w"))

    if output_a3mpath is not None:
        output_a3mpath.write_text(line)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Add MMseqs2 MSA to AlphaFold 3 JSON.")
    parser.add_argument(
        "input_json",
        help="Input AlphaFold 3 JSON file.",
        type=pathlib.Path,
    )
    parser.add_argument(
        "--output_json",
        help="Input AlphaFold 3 JSON file.",
        type=pathlib.Path,
        default=pathlib.Path("/dev/stdout"),
    )
    parser.add_argument(
        "--output_a3m",
        help="Save paired MSA to A3M file.",
        type=pathlib.Path,
        default=None,
    )
    parser.add_argument("--use_pairing", action="store_true")
    parser.add_argument("--host_url", type=str, default=DEEPFOLD_API_URL)
    parser.add_argument("--af2", action="store_true", dest="use_block")

    args = parser.parse_args()
    add_msa_to_json(
        input_jsonpath=args.input_json,
        output_jsonpath=args.output_json,
        output_a3mpath=args.output_a3m,
        use_pairing=args.use_pairing,
        use_block=args.use_block,
        host_url=args.host_url,
    )


if __name__ == "__main__":
    main()
