import codecs
import tokenize
from encodings import utf_8
from io import BytesIO, StringIO


def transform(src: str) -> str:
    tokenize_target = StringIO(src)
    lines = ["", *list(tokenize_target)]
    tokenize_target.seek(0)

    all_tokens = list(tokenize.generate_tokens(tokenize_target.readline))

    for i, token in enumerate(all_tokens[:-2]):
        # Find and replace all instances of "struct RecordName(..." with the record import, decorator, and "def".
        if (
            (token.type == tokenize.NAME and token.string == "struct")
            and all_tokens[i + 1].type == tokenize.NAME
            and (all_tokens[i + 2].type == tokenize.OP and all_tokens[i + 2].string == "(")
        ):
            start_row, start_col = token.start
            indent = lines[start_row][:start_col]
            lines[start_row : start_row + 1] = [
                f"{indent}from record_type import record\n",
                f"{indent}@record\n",
                lines[start_row].replace("struct", "def", 1),
            ]

    return "".join(lines)


def untransform(src: bytes) -> bytes:
    tokenize_target = BytesIO(src)
    lines = [b"", *list(tokenize_target)]
    tokenize_target.seek(0)

    all_tokens = list(tokenize.tokenize(tokenize_target.readline))

    for i, token in enumerate(all_tokens[:-8]):
        # Find and replace all places with the expanded import + decorator + "def" and convert them back to just "struct".
        if (
            token.type == tokenize.NAME
            and token.string == "from"
            and all_tokens[i + 1].type == tokenize.NAME
            and all_tokens[i + 1].string == "record_type"
            and all_tokens[i + 2].type == tokenize.NAME
            and all_tokens[i + 2].string == "import"
            and all_tokens[i + 3].type == tokenize.NAME
            and all_tokens[i + 3].string == "record"
            and all_tokens[i + 4].type == tokenize.NEWLINE
            and all_tokens[i + 5].type == tokenize.OP
            and all_tokens[i + 5].string == "@"
            and all_tokens[i + 6].type == tokenize.NAME
            and all_tokens[i + 6].string == "record"
            and all_tokens[i + 7].type == tokenize.NEWLINE
            and all_tokens[i + 8].type == tokenize.NAME
            and all_tokens[i + 8].string == "def"
        ):
            start_row = token.start[0]
            end_row = all_tokens[i + 8].start[0]
            lines[start_row:end_row] = [lines[end_row].replace(b"def", b"struct", 1)]

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
