import logging


class TqdmHandler(logging.StreamHandler):
    def __init__(self) -> None:
        logging.StreamHandler.__init__(self)

    def emit(self, record: logging.LogRecord) -> None:
        from tqdm.auto import tqdm

        msg = self.format(record)
        tqdm.write(msg)


def setup_logger():
    logger = logging.getLogger()

    if logger.handlers:
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[TqdmHandler()],
        force=True,
    )

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
