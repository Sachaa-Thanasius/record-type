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
        # Find and replace all instances of "struct RecordName(..." with the decorator and "def".
        if (
            token.type == tokenize.NAME
            and token.string == "struct"
            and all_tokens[i + 1].type == tokenize.NAME
            and all_tokens[i + 2].type == tokenize.OP
            and all_tokens[i + 2].string == "("
        ):
            start_row, start_col = token.start
            indent = lines[start_row][:start_col]
            lines[start_row : start_row + 1] = [f"{indent}@record\n", lines[start_row].replace("struct", "def", 1)]

    # Add the import to the start of the file.
    lines.insert(2, "from record_type import record\n")

    return "".join(lines)


def untransform(src: bytes) -> bytes:
    tokenize_target = BytesIO(src)
    lines = [b"", *list(tokenize_target)]
    tokenize_target.seek(0)

    all_tokens = list(tokenize.tokenize(tokenize_target.readline))

    for i, token in enumerate(all_tokens[:-2]):
        match (token, *all_tokens[i + 1 : i + 3]):
            case (
                tokenize.TokenInfo(tokenize.Name, "from"),
                tokenize.TokenInfo(tokenize.Name, "record_type"),
                tokenize.TokenInfo(tokenize.Name, "import"),
                tokenize.TokenInfo(tokenize.Name, "record"),
            ):
                # Find the imports of record from record_type and remove them.
                start_row = token.start[0]
                del lines[start_row]
            case (
                tokenize.TokenInfo(tokenize.OP, "@"),
                tokenize.TokenInfo(tokenize.Name, "record"),
                tokenize.TokenInfo(tokenize.NEWLINE),
                tokenize.TokenInfo(tokenize.Name, "def"),
            ):
                # Find all places with the @record decorator + "def" and replace them with "struct".
                start_row = token.start[0]
                end_row = all_tokens[i + 3].start[0]
                lines[start_row:end_row] = [lines[end_row].replace(b"def", b"struct", 1)]
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
