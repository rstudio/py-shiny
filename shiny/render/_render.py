# Needed for types imported only during TYPE_CHECKING with Python 3.7 - 3.9
# See https://www.python.org/dev/peps/pep-0655/#usage-in-python-3-11
from __future__ import annotations

# TODO-barret; change the name of the returned function from renderer function in the overload. If anything, use `_`.
# TODO-barret; See if @overload will work on the returned already-overloaded function
#  * From initial attempts, it does not work. :-(
#  * TODO-barret; Make a helper method to return all types (and function?) that could be used to make the overload signatures manually
# TODO-barret; Changelog that RenderFunction no longer exists.
# TODO-barret; Should `Renderer` be exported?
# TODO-barret; Test for `"`@reactive.event()` must be applied before `@render.xx` .\n"``
# TODO-barret; Test for `"`@output` must be applied to a `@render.xx` function.\n"`
# TODO-barret; Rename `RendererDecorator` to `Renderer`?; Rename `Renderer` to something else
# TODO-barret; Add in `IT` to RendererDecorator to enforce return type


# W/ Rich:
# The function is called a "render handler" as it handles the "render function" and returns a rendered result.

# result of `@renderer` is "renderer function"

# Names:
# * `_value_fn` -> `_handler`
# * `value: IT` -> `fn: RenderFn[IT]`


__all__ = (
    "text",
    "plot",
    "image",
    "table",
    "ui",
)

import base64
import inspect
import os
import sys
import typing

# import random
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Callable,
    Generic,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
    runtime_checkable,
)

# # These aren't used directly in this file, but they seem necessary for Sphinx to work
# # cleanly.
# from htmltools import Tag  # pyright: ignore[reportUnusedImport] # noqa: F401
# from htmltools import Tagifiable  # pyright: ignore[reportUnusedImport] # noqa: F401
# from htmltools import TagList  # pyright: ignore[reportUnusedImport] # noqa: F401
from htmltools import TagChild

if TYPE_CHECKING:
    from ..session import Session
    from ..session._utils import RenderedDeps
    import pandas as pd

from .. import _utils
from .._namespaces import ResolvedId
from .._typing_extensions import Concatenate, ParamSpec, TypedDict
from ..types import ImgData
from ._try_render_plot import try_render_matplotlib, try_render_pil, try_render_plotnine

# Input type for the user-spplied function that is passed to a render.xx
IT = TypeVar("IT")
# Output type after the Renderer.__call__ method is called on the IT object.
OT = TypeVar("OT")
# Param specification for render_fn function
P = ParamSpec("P")
# Generic type var
T = TypeVar("T")


# ======================================================================================
# Type definitions
# ======================================================================================


# class RenderFnSync(Generic[IT]):
#     def __call__(self) -> IT:
#         ...


# class RenderFnAsync(Generic[IT]):
#     async def __call__(self) -> IT:
#         ...


RenderFnSync = Callable[[], IT]
RenderFnAsync = Callable[[], Awaitable[IT]]
RenderFn = RenderFnSync[IT] | RenderFnAsync[IT]
HandlerFn = Callable[Concatenate["RenderMeta", RenderFnAsync[IT], P], Awaitable[OT]]


_RenderArgsSync = Tuple[RenderFnSync[IT], HandlerFn[IT, P, OT]]
_RenderArgsAsync = Tuple[RenderFnAsync[IT], HandlerFn[IT, P, OT]]
_RenderArgs = Union[_RenderArgsSync[IT, P, OT], _RenderArgsAsync[IT, P, OT]]

RenderDecoSync = Callable[[RenderFnSync[IT]], "RendererSync[OT]"]
RenderDecoAsync = Callable[[RenderFnAsync[IT]], "RendererAsync[OT]"]
RenderDeco = Callable[
    [Union[RenderFnSync[IT], RenderFnAsync[IT]]],
    Union["RendererSync[OT]", "RendererAsync[OT]"],
]


# ======================================================================================
# Helper classes
# ======================================================================================


# Meta information to give `hander()` some context
class RenderMeta(TypedDict):
    is_async: bool
    session: Session
    name: str


# TODO-barret remove; wch √
class _CallCounter(Generic[IT]):
    def assert_call_count(self, total_calls: int = 1):
        if self._call_count != total_calls:
            raise RuntimeError(
                f"The total number of calls (`{self._call_count}`) to '{self._render_fn_name}' in the '{self._handler_fn_name}' handler did not equal `{total_calls}`."
            )

    def __init__(
        self,
        *,
        render_fn: RenderFnAsync[IT],
        handler_fn: HandlerFn[IT, P, OT],
    ):
        self._call_count: int = 0
        self._render_fn = render_fn
        self._render_fn_name = render_fn.__name__
        self._handler_fn_name = handler_fn.__name__

    async def __call__(self) -> IT:
        self._call_count += 1
        return await self._render_fn()


# ======================================================================================
# Renderer / RendererSync / RendererAsync base class
# ======================================================================================


# A Renderer object is given a user-provided function (`handler_fn`) which returns an
# `OT`.
class Renderer(Generic[OT]):
    """
    Output Renderer

    Base class to build :class:`~shiny.render.RendererSync` and :class:`~shiny.render.RendererAsync`.


    When the `.__call__` method is invoked, the handler function (which defined by
    package authors) is called. The handler function is given `meta` information, the
    (app-supplied) render function, and any keyword arguments supplied to the decorator.

    The render function should return type `IT` and has parameter specification of type
    `P`. The handler function should return type `OT`. Note that in many cases but not
    all, `IT` and `OT` will be the same. `None` values must always be defined in `IT` and `OT`.


    Properties
    ----------
    is_async
        If `TRUE`, the app-supplied render function is asynchronous
    meta
        A named dictionary of values: `is_async`, `session` (the :class:`~shiny.Session`
        object), and `name` (the name of the output being rendered)

    """

    def __call__(self) -> OT:
        raise NotImplementedError

    def __init__(self, *, name: str, doc: str | None) -> None:
        """\
        Renderer init method

        Arguments
        ---------
        name
            Name of original output function. Ex: `my_txt`
        doc
            Documentation of the output function. Ex: `"My text output will be displayed verbatim".
        """
        self.__name__ = name
        self.__doc__ = doc

    @property
    def is_async(self) -> bool:
        raise NotImplementedError()

    @property
    def meta(self) -> RenderMeta:
        return RenderMeta(
            is_async=self.is_async,
            session=self._session,
            name=self._name,
        )

    def _set_metadata(self, session: Session, name: str) -> None:
        """\
        When `Renderer`s are assigned to Output object slots, this method is used to
        pass along Session and name information.
        """
        self._session: Session = session
        self._name: str = name


# Include
class RendererRun(Renderer[OT]):
    def __init__(
        self,
        # Use single arg to minimize overlap with P.kwargs
        _render_args: _RenderArgs[IT, P, OT],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        # `*args` must be in the `__init__` signature
        # Make sure there no `args`!
        _assert_no_args(args)

        # Unpack args
        render_fn, handler_fn = _render_args
        if not _utils.is_async_callable(handler_fn):
            raise TypeError(
                self.__class__.__name__ + " requires an async handler function"
            )
        super().__init__(
            name=render_fn.__name__,
            doc=render_fn.__doc__,
        )

        # Given we use `_utils.run_coro_sync(self._run())` to call our method,
        # we can act as if `render_fn` and `handler_fn` are always async
        self._render_fn = _utils.wrap_async(render_fn)
        self._handler_fn = _utils.wrap_async(handler_fn)

        self._args = args
        self._kwargs = kwargs

    async def _run(self) -> OT:
        render_fn_w_counter = _CallCounter(
            render_fn=self._render_fn,
            handler_fn=self._handler_fn,
        )
        ret = await self._handler_fn(
            # RendererMeta
            self.meta,
            # Callable[[], Awaitable[IT]]
            render_fn_w_counter,
            # P
            *self._args,
            **self._kwargs,
        )
        # TODO-future; Should we assert the call count? Should we check against non-missing values?
        render_fn_w_counter.assert_call_count(1)
        return ret


# Using a second class to help clarify that it is of a particular type
class RendererSync(RendererRun[OT]):
    @property
    def is_async(self) -> bool:
        return False

    def __init__(
        self,
        # Use single arg to minimize overlap with P.kwargs
        _render_args: _RenderArgsSync[IT, P, OT],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        render_fn = _render_args[0]
        if _utils.is_async_callable(render_fn):
            raise TypeError(
                self.__class__.__name__ + " requires a synchronous render function"
            )
        # super == RendererRun
        super().__init__(
            _render_args,
            *args,
            **kwargs,
        )

    def __call__(self) -> OT:
        return _utils.run_coro_sync(self._run())


# The reason for having a separate RendererAsync class is because the __call__
# method is marked here as async; you can't have a single class where one method could
# be either sync or async.
class RendererAsync(RendererRun[OT]):
    @property
    def is_async(self) -> bool:
        return True

    def __init__(
        self,
        # Use single arg to minimize overlap with P.kwargs
        _render_args: _RenderArgsAsync[IT, P, OT],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        render_fn = _render_args[0]
        if not _utils.is_async_callable(render_fn):
            raise TypeError(
                self.__class__.__name__ + " requires an asynchronous render function"
            )
        # super == RendererRun
        super().__init__(
            _render_args,
            *args,
            **kwargs,
        )

    async def __call__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
    ) -> OT:
        return await self._run()


# ======================================================================================
# Restrict the value function
# ======================================================================================


def _assert_no_args(args: tuple[object]) -> None:
    if len(args) > 0:
        raise RuntimeError("`args` should not be supplied")


# assert: No variable length positional values;
# * We need a way to distinguish between a plain function and args supplied to the next function. This is done by not allowing `*args`.
# assert: All kwargs of handler_fn should have a default value
# * This makes calling the method with both `()` and without `()` possible / consistent.
def _assert_handler_fn(handler_fn: HandlerFn[IT, P, OT]) -> None:
    params = inspect.Signature.from_callable(handler_fn).parameters

    for i, param in zip(range(len(params)), params.values()):
        # # Not a good test as `param.annotation` has type `str`:
        # if i == 0:
        #   print(type(param.annotation))
        #   assert isinstance(param.annotation, RendererMeta)

        # Make sure there are no more than 2 positional args
        if i >= 2 and param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            raise TypeError(
                "`handler_fn=` must not contain more than 2 positional parameters"
            )
        # Make sure there are no `*args`
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            raise TypeError(
                f"No variadic parameters (e.g. `*args`) can be supplied to `handler_fn=`. Received: `{param.name}`"
            )
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            # Do not allow for a kwarg to be named `_render_fn` or `_render_args`
            if param.name == "_render_fn":
                raise ValueError(
                    "In `handler_fn=`, parameters can not be named `_render_fn`"
                )
            if param.name == "_render_args":
                raise ValueError(
                    "In `handler_fn=`, parameters can not be named `_render_args`"
                )
            # Make sure kwargs have default values
            if param.default is inspect.Parameter.empty:
                raise TypeError(
                    f"In `handler_fn=`, parameter `{param.name}` did not have a default value"
                )


# ======================================================================================
# Renderer decorator
# ======================================================================================


def renderer_components(
    handler_fn: HandlerFn[IT, P, OT],
) -> RendererComponents[IT, OT, P]:
    """\
    Renderer generator

    TODO-barret; Docs go here!
    """
    return renderer_components(handler_fn)


class RendererComponents(Generic[IT, OT, P]):
    def __init__(
        self,
        renderer: Callable[
            Concatenate[
                Optional[RenderFn[IT]],
                P,
            ],
            # RendererSync[OT] | RendererAsync[OT],
            Renderer[OT],
        ],
    ) -> None:
        super().__init__()
        self.type_fn = RenderFn[IT]
        self.type_renderer = Renderer[OT]

        self.renderer = renderer


# class RendererDecorator(Generic[IT, OT]):
#     # @overload
#     # def __call__(self, _render_fn: RenderFnSync[IT]) -> RendererSync[OT]:
#     #     ...

#     # @overload
#     # def __call__(self, _render_fn: RenderFnAsync[IT]) -> RendererAsync[OT]:
#     #     ...

#     def __call__(
#         self, _render_fn: RenderFnSync[IT] | RenderFnAsync[IT]
#     ) -> RendererSync[OT] | RendererAsync[OT]:
#         ...


def coyp_doc(doc: str | None):
    def inner(obj: T) -> T:
        obj.__doc__ = doc or ""
        return obj

    return inner


class RendererDecorator(Generic[IT, OT, P]):
    """
    Renderer Decorator class docs go here!
    """

    @property
    def type_renderer_fn(self):
        return RenderFn[IT]

    @property
    def type_renderer(self):
        return Renderer[OT]

    @property
    def type_decorator(self):
        # return RenderDeco[IT, OT]
        return Callable[[RenderFn[IT]], Renderer[OT]]

    @property
    def type_impl_fn(self):
        return Optional[RenderFn[IT]]

    @property
    def type_impl(self):
        return Renderer[OT] | Callable[[RenderFn[IT]], Renderer[OT]]
        #    RenderDeco[IT, OT]

    # @property
    # def types(self):
    #     return {
    #         "return_renderer_decorator": RenderDeco[IT, OT],
    #         "arg_render_fn_sync": RenderFnSync[IT],
    #         "return_renderer_sync": RendererSync[OT],
    #         "arg_render_fn_async": RenderFnAsync[IT],
    #         "return_renderer_async": RendererAsync[OT],
    #     }

    def __init__(
        self,
        fn: Callable[
            Concatenate[
                Optional[RenderFn[IT]],
                P,
            ],
            # RendererSync[OT] | RendererAsync[OT],
            Renderer[OT] | RenderDeco[IT, OT],
        ],
        # doc: str | None = None,
    ) -> None:
        # self.__name__ = handler_fn.__name__
        # self.__func__.__doc__ = handler_fn.__doc__
        self._fn = fn
        # self.__doc__ = doc
        import functools

        functools.update_wrapper(self, fn, updated=())

    # @property
    # def __doc__(self):
    #     return "C doc"

    # @functools.wraps(handler_fn)
    @overload
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> RenderDeco[IT, OT]:
        ...

    # @overload
    # def __call__(self, _render_fn: RenderFnAsync[IT]) -> RendererAsync[OT]:
    #     ...

    # @overload
    # def __call__(self, _render_fn: RenderFnSync[IT]) -> RendererSync[OT]:
    #     ...

    @overload
    def __call__(self, _fn: RenderFn[IT]) -> Renderer[OT]:
        ...

    def __call__(  # type: ignore[reportGeneralTypeIssues]
        self,
        _render_fn: Optional[RenderFnSync[IT] | RenderFnAsync[IT]] = None,
        *args: P.args,  # Equivalent to `*` after assertions in `_assert_handler_fn()`
        **kwargs: P.kwargs,
    ):
        return self._fn(_render_fn, *args, **kwargs)

    @property
    def impl(self):
        return self._fn

    @property
    def fn(
        self,
        # ) -> Callable[
        #     Concatenate[
        #         Optional[RenderFn[IT]],
        #         P,
        #     ],
        #     # RendererSync[OT] | RendererAsync[OT],
        #     Renderer[OT],
        # ]:
    ):
        @overload
        def bear(
            *args: P.args, **kwargs: P.kwargs
        ) -> Callable[[RenderFn[IT]], Renderer[OT]]:
            ...

        @overload
        def bear(_fn: RenderFn[IT]) -> Renderer[OT]:
            ...

        def bear(_fn: RenderFn[IT], *args: P.args, **kwargs: P.kwargs) -> Renderer[OT]:
            return self._fn(_fn, *args, **kwargs)

        bear.__doc__ = self._fn.__doc__

        return bear

    # def fn(  # type: ignore[reportGeneralTypeIssues]
    #     self,
    #     _render_fn: Optional[RenderFnSync[IT] | RenderFnAsync[IT]] = None,
    #     *args: P.args,  # Equivalent to `*` after assertions in `_assert_handler_fn()`
    #     **kwargs: P.kwargs,
    # ):
    #     return self._fn(_render_fn, *args, **kwargs)


def renderer(
    handler_fn: HandlerFn[IT, P, OT],
    # ) -> Union[Callable[P, RendererDecorator[IT, OT]], RendererDecorator[IT, OT]]:
) -> RendererDecorator[IT, OT, P]:
    """\
    Renderer components generator

    TODO-barret; Docs go here!
    """
    _assert_handler_fn(handler_fn)

    # @overload
    # # @functools.wraps(
    # #     handler_fn, assigned=("__module__", "__name__", "__qualname__", "__doc__")
    # # )
    # def _(*args: P.args, **kwargs: P.kwargs) -> RenderDeco[IT, OT]:
    #     ...

    # @overload
    # # @functools.wraps(
    # #     handler_fn, assigned=("__module__", "__name__", "__qualname__", "__doc__")
    # # )
    # # RenderDecoSync[IT, OT]
    # def _(
    #     _render_fn: RenderFnSync[IT],
    # ) -> RendererSync[OT]:
    #     ...

    # @overload
    # # @functools.wraps(
    # #     handler_fn, assigned=("__module__", "__name__", "__qualname__", "__doc__")
    # # )
    # # RenderDecoAsync[IT, OT]
    # # RendererDecoAsync[OT]
    # # RendererDecoAsync[OT]
    # def _(
    #     _render_fn: RenderFnAsync[IT],
    # ) -> RendererAsync[OT]:
    #     ...

    # Ignoring the type issue on the next line of code as the overloads for
    # `renderer_deco` are not consistent with the function definition.
    # Motivation:
    # * https://peps.python.org/pep-0612/ does allow for prepending an arg (e.g.
    #   `_render_fn`).
    # * However, the overload is not happy when both a positional arg (e.g.
    #   `_render_fn`) is dropped and the variadic args (`*args`) are kept.
    # * The variadic args CAN NOT be dropped as PEP612 states that both components of
    #   the `ParamSpec` must be used in the same function signature.
    # * By making assertions on `P.args` to only allow for `*`, we _can_ make overloads
    #   that use either the single positional arg (e.g. `_render_fn`) or the `P.kwargs`
    #   (as `P.args` == `*`)
    # @functools.wraps(
    #     handler_fn, assigned=("__module__", "__name__", "__qualname__", "__doc__")
    # )
    def _(  # type: ignore[reportGeneralTypeIssues]
        _render_fn: Optional[RenderFnSync[IT] | RenderFnAsync[IT]] = None,
        *args: P.args,  # Equivalent to `*` after assertions in `_assert_handler_fn()`
        # *,
        **kwargs: P.kwargs,
    ):
        #  -> (
        #     RenderDecoSync[IT, OT]
        #     | RenderDecoAsync[IT, OT]
        #     | RendererSync[OT]
        #     | RendererAsync[OT]
        # ):
        # `args` **must** be in `renderer_decorator` definition.
        # Make sure there no `args`!
        _assert_no_args(args)

        def render_fn_sync(
            fn_sync: RenderFnSync[IT],
        ) -> RendererSync[OT]:
            return RendererSync(
                (fn_sync, handler_fn),
                *args,
                **kwargs,
            )

        def render_fn_async(
            fn_async: RenderFnAsync[IT],
        ) -> RendererAsync[OT]:
            return RendererAsync(
                (fn_async, handler_fn),
                *args,
                **kwargs,
            )

        @overload
        def as_render_fn(
            fn: RenderFnSync[IT],
        ) -> RendererSync[OT]:
            ...

        @overload
        def as_render_fn(
            fn: RenderFnAsync[IT],
        ) -> RendererAsync[OT]:
            ...

        def as_render_fn(
            fn: RenderFnSync[IT] | RenderFnAsync[IT],
        ) -> RendererSync[OT] | RendererAsync[OT]:
            if _utils.is_async_callable(fn):
                return render_fn_async(fn)
            else:
                # `fn` is not Async, cast as Sync
                fn = cast(RenderFnSync[IT], fn)
                return render_fn_sync(fn)

        if _render_fn is None:
            return as_render_fn
        return as_render_fn(_render_fn)

    # r_overloads = typing.get_overloads(renderer_decorator)
    # print(list(r_overloads))
    # for r_overload in r_overloads:
    #     for key in (
    #         "__module__",
    #         "__name__",
    #         "__qualname__",
    #         "__doc__",
    #         # "__annotations__",
    #     ):
    #         print(key, getattr(r_overload, key), getattr(handler_fn, key))
    #     #     # print(r_overload.__builtins__)
    #     print(
    #         r_overload.__name__,
    #         r_overload.__qualname__,
    #         # r_overload.__dir__(),
    #         # r_overload.__hash__(),
    #         # r_overload.__str__(),
    #         # r_overload.__repr__(),
    #         # r_overload.__annotations__,
    #         # r_overload.__builtins__,
    #     )
    #     r_overload.__name__ = handler_fn.__name__
    # r_overload.__doc__ = handler_fn.__doc__
    # print(r_overload.__name__, r_overload.__doc__)
    # # import pdb

    # pdb.set_trace()

    # import inspect

    # curframe = inspect.currentframe()
    # if curframe:
    #     curframe.f_locals["bearit"] = renderer_decorator
    #     print(curframe, curframe.f_locals)
    #     return curframe.f_locals["bearit"]

    # Copy over name an docs
    # renderer_decorator.__doc__ = handler_fn.__doc__
    # renderer_decorator.__name__ = handler_fn.__name__
    # # Lie and give it a pretty qualifying name
    # renderer_decorator.__qualname__ = renderer_decorator.__qualname__.replace(
    #     "renderer_decorator",
    #     handler_fn.__name__,
    # )

    # # TODO-barret; Fix name of decorated function. Hovering over method name does not work
    # ren_func = getattr(renderer_decorator, "__func__", renderer_decorator)
    # ren_func.__name__ = handler_fn.__name__

    # ret = cast(Barret, renderer_decorator)
    # ret.__name__ = handler_fn.__name__
    # ret.__doc__ = handler_fn.__doc__

    # return ret

    # renderer_decorator.barret = 43  # type: ignore
    # b = f"{43}"
    # key = "barret"
    # setattr(renderer_decorator, key, f"{b}")  # type: ignore

    # return renderer_decorator

    # renderer_decorator.__dict__ = {
    #     "renderer_types": {
    #         "arg_render_fn_sync": RenderFnSync[IT],
    #         "arg_render_fn_async": RenderFnAsync[IT],
    #         "return_renderer_sync": RendererSync[OT],
    #         "return_renderer_async": RendererAsync[OT],
    #         "return_renderer_decorator": RenderDeco[IT, OT],
    #     }
    # }
    # renderer_decorator["renderer_types"]["arg_render_fn_sync"]
    # _.__name__ =

    renderer_decorator = _
    # return renderer_decorator
    # return RendererComponents[IT, OT, P](renderer_decorator)
    ret = RendererDecorator[IT, OT, P](
        renderer_decorator,
        #    doc=handler_fn.__doc__
    )
    ret.__doc__ = handler_fn.__doc__
    ret.__class__.__doc__ = handler_fn.__doc__
    return ret


# ======================================================================================
# RenderText
# ======================================================================================


@renderer
async def text_handler(
    meta: RenderMeta,
    fn: RenderFnAsync[str | None],
    *,
    extra_arg: str = "42",
) -> str | None:
    """
    # Barret
    """
    value = await fn()
    if value is None:
        return None
    return str(value)


text_handler


@overload
def text(*, extra_arg: str = "42") -> text_handler.type_decorator:
    ...


@overload
def text(_fn: text_handler.type_renderer_fn) -> text_handler.type_renderer:
    ...


def text(
    _fn: text_handler.type_impl_fn = None,
    *,
    extra_arg: str = "42",
) -> text_handler.type_impl:
    """
    Reactively render text.

    Returns
    -------
    :
        A decorator for a function that returns a string.

    Tip
    ----
    This decorator should be applied **before** the ``@output`` decorator. Also, the
    name of the decorated function (or ``@output(id=...)``) should match the ``id`` of
    a :func:`~shiny.ui.output_text` container (see :func:`~shiny.ui.output_text` for
    example usage).

    See Also
    --------
    ~shiny.ui.output_text
    """
    return text_handler.impl(_fn, extra_arg=extra_arg)


# TODO-barret; Have `type_imple_fn` be a class to hide all of the grossness of the signature
text


# TODO-barret: Plan of action: If we can get barret2 doc string to be ported, then we use the class with no manual overrides. If we can NOT get the docs string, use manual override approach only
@renderer
async def barret2(
    meta: RenderMeta,
    fn: RenderFnAsync[str],
    *,
    extra_arg: str = "42",
) -> str | None:
    """
    My docs go here!

    Parameters
    ----------
    extra_arg
        My extra arg docs go here!
    """
    return str(await fn())


barret2()
# @output
# @barret2
# def my_name():
#     ...
barret2fn = barret2.fn
barret2


@overload
def barret2_fn(
    *,
    extra_arg: str = "42",
) -> barret2.type_decorator:
    ...


@overload
def barret2_fn(
    _fn: barret2.type_renderer_fn,
) -> barret2.type_renderer:
    ...


def barret2_fn(
    _fn: Optional[barret2.type_renderer_fn] = None,
    *,
    extra_arg: str = "42",
) -> barret2.type_impl:
    return barret2.impl(
        _fn,
        extra_arg=extra_arg,
    )


barret2_fn
text
barret2_fn()


# ======================================================================================
# RenderPlot
# ======================================================================================
# It would be nice to specify the return type of RenderPlotFunc to be something like:
#   Union[matplotlib.figure.Figure, PIL.Image.Image]
# However, if we did that, we'd have to import those modules at load time, which adds
# a nontrivial amount of overhead. So for now, we're just using `object`.
@renderer
async def plot(
    meta: RenderMeta,
    fn: RenderFnAsync[ImgData | None],
    *,
    alt: Optional[str] = None,
    **kwargs: object,
) -> ImgData | None:
    """
    Reactively render a plot object as an HTML image.

    Parameters
    ----------
    alt
        Alternative text for the image if it cannot be displayed or viewed (i.e., the
        user uses a screen reader).
    **kwargs
        Additional keyword arguments passed to the relevant method for saving the image
        (e.g., for matplotlib, arguments to ``savefig()``; for PIL and plotnine,
        arguments to ``save()``).

    Returns
    -------
    :
        A decorator for a function that returns any of the following:

        1. A :class:`matplotlib.figure.Figure` instance.
        2. An :class:`matplotlib.artist.Artist` instance.
        3. A list/tuple of Figure/Artist instances.
        4. An object with a 'figure' attribute pointing to a
           :class:`matplotlib.figure.Figure` instance.
        5. A :class:`PIL.Image.Image` instance.

    It's also possible to use the ``matplotlib.pyplot`` interface; in that case, your
    function should just call pyplot functions and not return anything. (Note that if
    the decorated function is async, then it's not safe to use pyplot. Shiny will detect
    this case and throw an error asking you to use matplotlib's object-oriented
    interface instead.)

    Tip
    ----
    This decorator should be applied **before** the ``@output`` decorator. Also, the
    name of the decorated function (or ``@output(id=...)``) should match the ``id`` of a
    :func:`~shiny.ui.output_plot` container (see :func:`~shiny.ui.output_plot` for
    example usage).

    See Also
    --------
    ~shiny.ui.output_plot
    ~shiny.render.image
    """
    is_userfn_async = meta["is_async"]
    name = meta["name"]
    session = meta["session"]

    ppi: float = 96

    # TODO-barret; Q: These variable calls are **after** `self._render_fn()`. Is this ok?
    inputs = session.root_scope().input

    # Reactively read some information about the plot.
    pixelratio: float = typing.cast(
        float, inputs[ResolvedId(".clientdata_pixelratio")]()
    )
    width: float = typing.cast(
        float, inputs[ResolvedId(f".clientdata_output_{name}_width")]()
    )
    height: float = typing.cast(
        float, inputs[ResolvedId(f".clientdata_output_{name}_height")]()
    )

    x = await fn()

    # Note that x might be None; it could be a matplotlib.pyplot

    # Try each type of renderer in turn. The reason we do it this way is to avoid
    # importing modules that aren't already loaded. That could slow things down, or
    # worse, cause an error if the module isn't installed.
    #
    # Each try_render function should indicate whether it was able to make sense of
    # the x value (or, in the case of matplotlib, possibly it decided to use the
    # global pyplot figure) by returning a tuple that starts with True. The second
    # tuple element may be None in this case, which means the try_render function
    # explicitly wants the plot to be blanked.
    #
    # If a try_render function returns a tuple that starts with False, then the next
    # try_render function should be tried. If none succeed, an error is raised.
    ok: bool
    result: ImgData | None

    if "plotnine" in sys.modules:
        ok, result = try_render_plotnine(
            x,
            width,
            height,
            pixelratio,
            ppi,
            alt,
            **kwargs,
        )
        if ok:
            return result

    if "matplotlib" in sys.modules:
        ok, result = try_render_matplotlib(
            x,
            width,
            height,
            pixelratio=pixelratio,
            ppi=ppi,
            allow_global=not is_userfn_async,
            alt=alt,
            **kwargs,
        )
        if ok:
            return result

    if "PIL" in sys.modules:
        ok, result = try_render_pil(
            x,
            width,
            height,
            pixelratio,
            ppi,
            alt,
            **kwargs,
        )
        if ok:
            return result

    # This check must happen last because
    # matplotlib might be able to plot even if x is `None`
    if x is None:
        return None

    raise Exception(
        f"@render.plot doesn't know to render objects of type '{str(type(x))}'. "
        + "Consider either requesting support for this type of plot object, and/or "
        + " explictly saving the object to a (png) file and using @render.image."
    )


# ======================================================================================
# RenderImage
# ======================================================================================
@renderer
async def image(
    meta: RenderMeta,
    fn: RenderFnAsync[ImgData | None],
    *,
    delete_file: bool = False,
) -> ImgData | None:
    """
    Reactively render a image file as an HTML image.

    Parameters
    ----------
    delete_file
        If ``True``, the image file will be deleted after rendering.

    Returns
    -------
    :
        A decorator for a function that returns an `~shiny.types.ImgData` object.

    Tip
    ----
    This decorator should be applied **before** the ``@output`` decorator. Also, the
    name of the decorated function (or ``@output(id=...)``) should match the ``id`` of
    a :func:`~shiny.ui.output_image` container (see :func:`~shiny.ui.output_image` for
    example usage).

    See Also
    --------
    ~shiny.ui.output_image
    ~shiny.types.ImgData
    ~shiny.render.plot
    """
    res = await fn()
    if res is None:
        return None

    src: str = res.get("src")
    try:
        with open(src, "rb") as f:
            data = base64.b64encode(f.read())
            data_str = data.decode("utf-8")
        content_type = _utils.guess_mime_type(src)
        res["src"] = f"data:{content_type};base64,{data_str}"
        return res
    finally:
        if delete_file:
            os.remove(src)


# ======================================================================================
# RenderTable
# ======================================================================================


@runtime_checkable
class PandasCompatible(Protocol):
    # Signature doesn't matter, runtime_checkable won't look at it anyway
    def to_pandas(self) -> "pd.DataFrame":
        ...


TableResult = Union["pd.DataFrame", PandasCompatible, None]


@renderer
async def table(
    meta: RenderMeta,
    fn: RenderFnAsync[TableResult | None],
    *,
    index: bool = False,
    classes: str = "table shiny-table w-auto",
    border: int = 0,
    **kwargs: object,
) -> RenderedDeps | None:
    """
    Reactively render a Pandas data frame object (or similar) as a basic HTML table.

    Parameters
    ----------
    index
        Whether to print index (row) labels. (Ignored for pandas :class:`Styler`
        objects; call ``style.hide(axis="index")`` from user code instead.)
    classes
        CSS classes (space separated) to apply to the resulting table. By default, we
        use `table shiny-table w-auto` which is designed to look reasonable with Bootstrap 5.
        (Ignored for pandas :class:`Styler` objects; call
        ``style.set_table_attributes('class="dataframe table shiny-table w-auto"')``
        from user code instead.)
    **kwargs
        Additional keyword arguments passed to ``pandas.DataFrame.to_html()`` or
        ``pandas.io.formats.style.Styler.to_html()``.

    Returns
    -------
    :
        A decorator for a function that returns any of the following:

        1. A pandas :class:`DataFrame` object.
        2. A pandas :class:`Styler` object.
        3. Any object that has a `.to_pandas()` method (e.g., a Polars data frame or
           Arrow table).

    Tip
    ----
    This decorator should be applied **before** the ``@output`` decorator. Also, the
    name of the decorated function (or ``@output(id=...)``) should match the ``id`` of
    a :func:`~shiny.ui.output_table` container (see :func:`~shiny.ui.output_table` for
    example usage).

    See Also
    --------
    ~shiny.ui.output_table
    """
    x = await fn()

    if x is None:
        return None

    import pandas
    import pandas.io.formats.style

    html: str
    if isinstance(x, pandas.io.formats.style.Styler):
        html = cast(  # pyright: ignore[reportUnnecessaryCast]
            str,
            x.to_html(  # pyright: ignore[reportUnknownMemberType]
                **kwargs  # pyright: ignore[reportGeneralTypeIssues]
            ),
        )
    else:
        if not isinstance(x, pandas.DataFrame):
            if not isinstance(x, PandasCompatible):
                raise TypeError(
                    "@render.table doesn't know how to render objects of type "
                    f"'{str(type(x))}'. Return either a pandas.DataFrame, or an object "
                    "that has a .to_pandas() method."
                )
            x = x.to_pandas()

        html = cast(  # pyright: ignore[reportUnnecessaryCast]
            str,
            x.to_html(  # pyright: ignore[reportUnknownMemberType]
                index=index,
                classes=classes,
                border=border,
                **kwargs,  # pyright: ignore[reportGeneralTypeIssues]
            ),
        )
    return {"deps": [], "html": html}


# ======================================================================================
# RenderUI
# ======================================================================================
@renderer
async def ui(
    meta: RenderMeta,
    fn: RenderFnAsync[TagChild],
) -> RenderedDeps | None:
    """
    Reactively render HTML content.

    Returns
    -------
    :
        A decorator for a function that returns an object of type `~shiny.ui.TagChild`.

    Tip
    ----
    This decorator should be applied **before** the ``@output`` decorator. Also, the
    name of the decorated function (or ``@output(id=...)``) should match the ``id`` of
    a :func:`~shiny.ui.output_ui` container (see :func:`~shiny.ui.output_ui` for example
    usage).

    See Also
    --------
    ~shiny.ui.output_ui
    """
    ui = await fn()
    if ui is None:
        return None

    return meta["session"]._process_ui(ui)
