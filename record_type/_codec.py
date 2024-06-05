import codecs
import tokenize
from encodings import utf_8
from io import BytesIO, StringIO
from tokenize import TokenInfo


def transform(src: str) -> str:
    tokenize_target = StringIO(src)
    lines = ["", *list(tokenize_target)]
    tokenize_target.seek(0)

    all_tokens = list(tokenize.generate_tokens(tokenize_target.readline))

    for i, token in enumerate(all_tokens[:-2]):
        match (token, all_tokens[i + 1], all_tokens[i + 2]):
            case (TokenInfo(tokenize.NAME, "record"), TokenInfo(tokenize.NAME), TokenInfo(tokenize.OP, "(")):
                # Find and replace all instances of "record RecordName(..." with the record decorator and "def".
                start_row, start_col = token.start
                indent = lines[start_row][:start_col]
                lines[start_row : start_row + 1] = [f"{indent}@record\n", lines[start_row].replace("record", "def", 1)]
            case _:
                pass

    # Add the import to the start of the file.
    lines.insert(2, "from record_type import record\n")

    return "".join(lines)


def untransform(src: bytes) -> bytes:
    tokenize_target = BytesIO(src)
    lines = [b"", *list(tokenize_target)]
    tokenize_target.seek(0)

    all_tokens = list(tokenize.tokenize(tokenize_target.readline))

    for i, token in enumerate(all_tokens[:-3]):
        match (token, all_tokens[i + 1], all_tokens[i + 2], all_tokens[i + 3]):
            case (
                TokenInfo(tokenize.Name, "from"),
                TokenInfo(tokenize.Name, "record_type"),
                TokenInfo(tokenize.Name, "import"),
                TokenInfo(tokenize.Name, "record"),
            ):
                # Find the imports of record from record_type and remove them. Probably a bit too much.
                start_row = token.start[0]
                del lines[start_row]
            case (
                TokenInfo(tokenize.OP, "@"),
                TokenInfo(tokenize.Name, "record"),
                TokenInfo(tokenize.NEWLINE),
                TokenInfo(tokenize.Name, "def"),
            ):
                # Find all places with the @record decorator + "def" and replace them with "record".
                start_row = token.start[0]
                end_row = all_tokens[i + 3].start[0]
                lines[start_row:end_row] = [lines[end_row].replace(b"def", b"record", 1)]
            case _:
                pass

    return b"".join(lines)


def decode(input: bytes, errors: str = "strict", /) -> tuple[str, int]:
    source, read = utf_8.decode(input, errors)
    return transform(source), read


def encode(input: str, errors: str = "strict", /) -> tuple[bytes, int]:
    encoded, written = utf_8.encode(input, errors)
    return untransform(encoded), written


def search_function(name: str) -> codecs.CodecInfo | None:
    if name == "record":
        return codecs.CodecInfo(
            encode=encode,
            decode=decode,
            incrementalencoder=utf_8.IncrementalEncoder,
            incrementaldecoder=utf_8.IncrementalDecoder,
            streamreader=utf_8.StreamReader,
            streamwriter=utf_8.StreamWriter,
            name=name,
        )
    return None


def register() -> None:
    codecs.register(search_function)


def unregister() -> None:
    codecs.unregister(search_function)
