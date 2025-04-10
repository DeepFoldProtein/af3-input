# AlphaFold 3 Input Generator

Scripts to add MMseqs2 MSA or plmMSA to the AlphaFold 3 input JSON.

## Installation

To install the requirements, run:

```sh
pip install -r requirements.txt
```

## Usage

These scripts are designed to take a prepared [AlphaFold 3](https://github.com/google-deepmind/alphafold3) input JSON file, e.g.:

```json
{
  "name": "2PV7",
  "sequences": [
    {
      "protein": {
        "id": ["A", "B"],
        "sequence": "GMRESYANENQFGFKTINSDIHKIVIVGGYGKLGGLFARYLRASGYPISILDREDWAVAESILANADVVIVSVPINLTLETIERLKPYLTENMLLADLTSVKREPLAKMLEVHTGAVLGLHPMFGADIASMAKQVVVRCDGRFPERYEWLLEQIQIWGAKIYQTNATEHDHNMTYIQALRHFSTFANGLHLSKQPINLANLLALSSPIYRLELAMIGRLFAQDAELYADIIMDKSENLAVIETLKQTYDEALTFFENNDRQGFIDAFHKVRDWFGDYSEQFLKESRQLLQQANDLKQG"
      }
    }
  ],
  "modelSeeds": [1],
  "dialect": "alphafold3",
  "version": 1
}
```

### Adding MMseqs2 MSA

To add MMseqs2 MSA to the AlphaFold 3 input JSON, you can use the `mmseqs.py` script.

```sh
python -m af3_input.mmseqs <input_json> \
    [--output_json <output_json>] \
    [--host_url <host_url>]
```

- `<input_json>`: Path to the input AlphaFold 3 JSON file.
- `<output_json>`: (Optional) Path to the output JSON file. (Default: `/dev/stdout`.)
- `<host_url>`: (Optional) URL to MMseqs API server. (Default: `https://api.colabfold.com/`)

### Adding plmMSA MSA

To add plmMSA MSA to the AlphaFold 3 input JSON, you can use the `add_plmmsa_msa.py` script.

```sh
python -m af3_input.plmmsa --input_json <input_json> \
    [--output_json <output_json>] \
    [--host_url <host_url>] \
    [--use_pairing]
```

- `<input_json>`: Path to the input AlphaFold 3 JSON file.
- `<output_json>`: (Optional) Path to the output JSON file. (Default: `/dev/stdout`.)
- `<host_url>`: (Optional) URL to MMseqs API server. (Default: `https://deepfold.com/api/colab`)
- `--use_pairing`: Use paired MSA.
