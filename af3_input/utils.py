import logging
import sys


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the minimum logging level

    # Create a stream handler (output to console)
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setLevel(logging.DEBUG)

    # Set the custom formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


def read_iter(fasta_string: str):
    header = None
    seq_str_list = []
    for line in fasta_string.splitlines():
        line = line.strip()
        # Ignore empty and comment lines.
        if len(line) == 0 or line[0] == ";":
            continue
        if line[0] == ">":
            # New entry.
            if header is not None:
                yield header, "".join(seq_str_list)
            # Track new header and reset sequence.
            header = line[1:]
            seq_str_list = []
        else:
            seq_str_list.append(line)
    # Yield final entry.
    if header is not None:
        yield header, "".join(seq_str_list)
