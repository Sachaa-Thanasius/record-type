import inspect
import typing


def _make_var_positional_annotation(annotation: typing.Any) -> typing.Any:
    """Convert the type annotation for *args to an appropriate one for a record."""

    if isinstance(annotation, str):
        return f"tuple[{annotation}]"
    return tuple[annotation]


def _make_var_keyword_annotation(annotation: typing.Any) -> typing.Any:
    """Convert the type annotation for **kwargs to an appropriate one for a record."""

    if isinstance(annotation, str):
        if annotation.startswith("Unpack["):
            return annotation.removeprefix("Unpack[").removesuffix("]")
        return f"dict[str, {annotation}]"
    # typing.Unpack explicitly refuses to work with isinstance() and
    # issubclass() due to returning different things depending on what is
    # passed into the constructor.
    if isinstance(annotation, typing.Unpack[typing.TypedDict].__class__):  # type: ignore
        return annotation.__args__[0]
    return dict[str, annotation]


class Record:
    __slots__ = ("_record_cached_hash", "_record_cached_repr")

    def __eq__(self, other: object) -> bool:
        """Check for equality.

        Changed to use nominal subtyping for speed testing.
        """

        if isinstance(other, type(self)):
            for attr in self.__slots__:  # noqa: SIM110 # all() is too slow.
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        return NotImplemented

    def __hash__(self) -> int:
        try:
            return self._record_cached_hash
        except AttributeError:
            object.__setattr__(self, "_record_cached_hash", hash(tuple(getattr(self, name) for name in self.__slots__)))
            return self._record_cached_hash

    def __setattr__(self, name: str, value: object, /) -> typing.Never:
        msg = f"{type(self).__name__} object does not support attribute assignment."
        raise TypeError(msg)

    def __delattr__(self, name: str, /) -> typing.Never:
        msg = f"{type(self).__name__} object does not support attribute deletion."
        raise TypeError(msg)

    def __repr__(self) -> str:
        try:
            return self._record_cached_repr
        except AttributeError:
            init_signature = inspect.signature(self.__init__)
            args: list[str] = []
            # Using the bound `__init__()` means `inspect` takes care of `self`.
            for parameter in init_signature.parameters.values():
                param_repr = repr(getattr(self, parameter.name))
                param_kind = parameter.kind
                if param_kind is parameter.POSITIONAL_ONLY:
                    args.append(param_repr)
                elif param_kind in (parameter.POSITIONAL_OR_KEYWORD, parameter.KEYWORD_ONLY):
                    args.append(f"{parameter.name}={param_repr}")
                elif param_kind is parameter.VAR_POSITIONAL:
                    args.append(f"*{param_repr}")
                elif param_kind is parameter.VAR_KEYWORD:
                    args.append(f"**{param_repr}")
                else:
                    typing.assert_never(param_kind)
            object.__setattr__(self, "_record_cached_repr", f"{type(self).__name__}({', '.join(args)})")
            return self._record_cached_repr


def record(func: typing.Callable[..., None]):  # noqa: ANN201
    """Create a record type."""
    name = func.__name__
    func_signature = inspect.signature(func)
    if func_signature.return_annotation not in {inspect.Signature.empty, None}:
        msg = "return type annotation can only be 'None' or unset"
        raise TypeError(msg)

    self_parameter = inspect.Parameter("self", inspect.Parameter.POSITIONAL_ONLY)
    init_signature = func_signature.replace(
        parameters=(
            self_parameter,
            *(
                param.replace(default=param.empty, annotation=param.empty)
                for param in func_signature.parameters.values()
            ),
        )
    )

    parameters = (f"object.__setattr__(self, {name!r}, {name})" for name in func_signature.parameters)
    init_body = (f"\n{' ' * 4}").join(parameters) or "pass"

    # Take a page from collections.namedtuple's implementation: creating a new class is faster with type than exec.
    init_syntax = f"def __init__{init_signature}:\n    {init_body}"
    globals_: dict[str, typing.Any] = {"__builtins__": {"object": object}}
    exec(init_syntax, globals_)  # noqa: S102
    record_init = globals_["__init__"]

    proposed_annotations = func.__annotations__.copy()
    try:
        del proposed_annotations["return"]
    except KeyError:
        pass

    # The return annotations was guaranteed earlier.
    record_init.__annotations__ = func.__annotations__ | {"return": None}
    record_init.__defaults__ = func.__defaults__
    record_init.__kwdefaults__ = func.__kwdefaults__

    record_slots = tuple(func_signature.parameters)

    # Buid annotations dict from scratch to keep the iteration order.
    cls_annotations: dict[str, object] = {}
    for parameter in func_signature.parameters.values():
        if parameter.name not in proposed_annotations:
            continue
        annotation = proposed_annotations[parameter.name]
        if parameter.kind == parameter.VAR_POSITIONAL:
            annotation = _make_var_positional_annotation(annotation)
        elif parameter.kind == parameter.VAR_KEYWORD:
            annotation = _make_var_keyword_annotation(annotation)

        cls_annotations[parameter.name] = annotation

    match_args: list[str] = []
    for parameter in func_signature.parameters.values():
        if parameter.kind in {parameter.VAR_POSITIONAL, parameter.KEYWORD_ONLY, parameter.VAR_KEYWORD}:
            break
        match_args.append(parameter.name)

    cls_namespace = {
        "__qualname__": func.__qualname__,
        "__module__": func.__module__,
        "__doc__": func.__doc__,
        "__slots__": record_slots,
        "__match_args__": tuple(match_args),
        "__annotations__": cls_annotations,
        "__init__": record_init,
    }

    return type(name, (Record,), cls_namespace)
