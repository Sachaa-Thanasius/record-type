import codecs
import tokenize
from encodings import utf_8
from io import StringIO


def transform_source(src: str) -> str:
    tokenize_target = StringIO(src)
    lines = ["", *list(tokenize_target)]
    tokenize_target.seek(0)

    all_tokens = list(tokenize.generate_tokens(tokenize_target.readline))

    for i, token in enumerate(all_tokens[:-2]):
        if (
            (token.type == tokenize.NAME and token.string == "struct")
            and all_tokens[i + 1].type == tokenize.NAME
            and (all_tokens[i + 2].type == tokenize.OP and all_tokens[i + 2].string == "(")
        ):
            start_row, start_col = token.start
            indent = lines[start_row][:start_col]
            lines[start_row:start_row] = [
                f"{indent}from record_type import record\n",
                f"{indent}@record\n",
                lines[start_row].replace("struct", "def", 1),
            ]

    return "".join(lines)


def encode(input: str, errors: str = "strict", /):  # noqa: ANN202 # Don't want to import typing to annotate this.
    raise NotImplementedError


def decode(input: bytes, errors: str = "strict", /) -> tuple[str, int]:
    source, read = utf_8.decode(input, errors)
    return transform_source(source), read


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
