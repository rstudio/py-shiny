from __future__ import annotations

import copy
import os
import pathlib
import tempfile
from textwrap import dedent
from typing import Optional, Sequence, TypeVar

from htmltools import HTMLDependency
from packaging.version import Version

from .._docstring import no_example
from .._versions import bootstrap
from ._theme_presets import (
    ShinyThemePreset,
    shiny_theme_presets,
    shiny_theme_presets_bundled,
)
from ._utils import path_pkg_www

T = TypeVar("T", bound="Theme")


@no_example()
class Theme:
    """
    Create a custom Shiny theme.

    The `Theme` class allows you to create a custom Shiny theme by providing custom Sass
    code. The theme can be based on one of the available presets, such as `"shiny"` or
    `"bootstrap"`, or a Bootswatch theme. Use the `.add_*()` methods can be chained
    together to add custom Sass functions, defaults, mixins, and rules.

    Pass the `Theme` object directly to the `theme` argument of any Shiny page function,
    such as :func:`~shiny.ui.page_sidebar` or :func:`~shiny.ui.page_navbar`. In Shiny
    Express apps, use the `theme` argument of :func:`~shiny.express.ui.page_opts` to set
    the app theme.

    Customized themes require the [libsass package](https://pypi.org/project/libsass/),
    and are compiled to CSS when the theme is used. The `Theme` class caches the
    compiled CSS, but you can speed up app loading (and avoid the runtime `libsass`
    dependency) by pre-compiling the theme CSS and saving it to a file. To do this, use
    the `.to_css()` method to render the theme to a single minified CSS string. Once
    saved to a file, the CSS can be used in any Shiny app by passing the file path to
    the `theme` argument described above.

    Parameters
    ----------
    preset
        The name of the preset to use as a base. `"shiny"` is the default theme for
        Shiny apps and `"bootstrap"` uses standard Bootstrap 5 styling. Bootswatch theme
        presets are also available. Use `Theme.available_presets()` to see the full
        list.
    name
        A custom name for the theme. If not provided, the preset name will be used.
    include_paths
        Additional paths to include when looking for Sass files used in `@import`
        statements the theme. This can be a single path as a string or
        :class:`pathlib.Path`, or a list of paths. The paths should point to directories
        containing additional Sass files that the theme depends on.

    Raises
    ------
    ValueError
        If the `preset` is not a valid theme preset.
    """

    def __init__(
        self,
        preset: ShinyThemePreset = "shiny",
        name: Optional[str] = None,
        include_paths: Optional[str | pathlib.Path | list[str | pathlib.Path]] = None,
    ):
        check_is_valid_preset(preset)
        self._preset: ShinyThemePreset = preset
        self.name = name
        self._version = bootstrap
        self._include_paths: list[str] = []

        if isinstance(include_paths, (str, pathlib.Path)):
            self._include_paths.append(str(include_paths))
        elif isinstance(include_paths, Sequence):
            for path in include_paths:
                self._include_paths.append(str(path))

        # User-provided Sass code
        self._functions: list[str] = []
        self._defaults: list[str] = []
        self._mixins: list[str] = []
        self._rules: list[str] = []

        # _css is either:
        # 1. "precompiled" indicating it's okay to use precompiled preset.min.css
        # 2. "" indicating that the CSS has not been compiled yet
        # 3. A string containing the compiled CSS for the current theme
        self._css: str = "precompiled" if preset in shiny_theme_presets_bundled else ""

        # If the theme has been customized and rendered once, we store the tempdir
        # so that we can re-use the already compiled CSS file.
        self._css_temp_srcdir: Optional[str] = None

    @classmethod
    def available_presets(cls) -> tuple[ShinyThemePreset, ...]:
        """
        Get a list of available theme presets.
        """
        return shiny_theme_presets

    @property
    def preset(self) -> ShinyThemePreset:
        return self._preset

    @preset.setter
    def preset(self, value: ShinyThemePreset) -> None:
        check_is_valid_preset(value)
        self._preset = value

        has_customizations = (
            len(self._functions) > 0
            or len(self._defaults) > 0
            or len(self._mixins) > 0
            or len(self._rules) > 0
        )

        if has_customizations:
            self._css = ""
        else:
            self._css = "precompiled" if value in shiny_theme_presets_bundled else ""

        self._css_temp_srcdir = None

    def add_functions(self: T, *args: str) -> T:
        """
        Add custom Sass functions to the theme.

        Sass code added via this method will be placed **after** the function
        declarations from the theme preset, allowing you to override or extend the
        default functions.

        Parameters
        ----------
        *args
            The Sass functions to add as a single or multiple strings.
        """
        self._css = ""
        self._functions.extend(dedent_array(args))
        return self

    def add_defaults(
        self: T, *args: str, **kwargs: str | float | int | bool | None
    ) -> T:
        """
        Add custom default values to the theme.

        Sass code added via this method will be placed **before** the default values of
        the theme preset, allowing you to override or extend the default values.

        Parameters
        ----------
        *args
            Sass code, as a single or multiple strings, containing default value
            declarations to add.
        **kwargs
            Keyword arguments containing default value declarations to add. The keys
            should be Sass variable names using underscore casing that will be
            transformed automatically to kebab-case. For example,
            `.add_defaults(primary_color="#ff0000")` is equivalent to
            `.add_defaults("$primary-color: #ff0000;")`.
        """
        if len(args) > 0 and len(kwargs) > 0:
            # Python forces positional arguments to come _before_ kwargs, but default
            # argument order might matter. To be safe, we force users to pick one order.
            raise ValueError("Cannot provide both positional and keyword arguments")
        elif len(args) == 0 and len(kwargs) == 0:
            return self

        defaults: list[str] = list(args)

        if len(kwargs) > 0:
            for key, value in kwargs.items():
                key.replace("_", "-")
                if isinstance(value, bool):
                    value = "true" if value else "false"
                elif value is None:
                    value = "null"
                defaults.append(f"${key}: {value};")

        # Add args to the front of _defaults
        self._defaults = dedent_array(defaults) + self._defaults
        self._css = ""

        return self

    def add_mixins(self: T, *args: str) -> T:
        """
        Add custom Sass mixins to the theme.

        Sass code added via this method will be placed **after** the mixin declarations
        from the theme preset, allowing you to override or extend the default mixins.

        Parameters
        ----------
        *args
            Sass code, as a single or multiple strings, containing mixins to add.
        """
        self._mixins.extend(dedent_array(args))
        self._css = ""
        return self

    def add_rules(self: T, *args: str) -> T:
        """
        Add custom Sass rules to the theme.

        Sass code added via this method will be placed **after** the rule declarations
        from the theme preset, allowing you to override or extend the default rules.

        Parameters
        ----------
        *args
            Sass code, as a single or multiple strings, containing rules to add.
        """
        self._rules.extend(dedent_array(args))
        self._css = ""
        return self

    def to_sass(self) -> str:
        """
        Returns the custom theme as a single Sass string.

        Returns
        -------
        :
            The custom theme as a single Sass string.
        """
        path_functions = path_pkg_preset(self._preset, "_01_functions.scss")
        path_defaults = path_pkg_preset(self._preset, "_02_defaults.scss")
        path_mixins = path_pkg_preset(self._preset, "_03_mixins.scss")
        path_rules = path_pkg_preset(self._preset, "_04_rules.scss")

        sass_lines = [
            f'@import "{path_functions}";',
            *self._functions,
            *self._defaults,
            f'@import "{path_defaults}";',
            f'@import "{path_mixins}";',
            *self._mixins,
            f'@import "{path_rules}";',
            *self._rules,
        ]

        return "\n".join(sass_lines)

    def to_css(self) -> str:
        """
        Compile the theme to CSS and return the result as a string.

        Returns
        -------
        :
            The compiled CSS for the theme. The value is cached such that previously
            compiled themes are returned immediately. Adding additional custom Sass code
            or changing the preset will invalidate the cache.
        """
        if self._css:
            if self._css == "precompiled":
                return self._read_precompiled_css()
            return copy.copy(self._css)

        check_libsass_installed()
        import sass

        self._css = sass.compile(
            string=self.to_sass(),
            include_paths=self._include_paths,
        )

        return copy.copy(self._css)

    def _read_precompiled_css(self) -> str:
        path = path_pkg_preset(self._preset, "preset.min.css")
        with open(path, "r") as f:
            return f.read()

    def _html_dependency_precompiled(self) -> HTMLDependency:
        return HTMLDependency(
            name=f"shiny-theme-{self._preset}",
            version=self._version,
            source={
                "package": "shiny",
                "subdir": f"www/shared/sass/preset/{self._preset}",
            },
            stylesheet={"href": "preset.min.css"},
            all_files=False,
        )

    def html_dependency(self) -> HTMLDependency:
        """
        Create an `HTMLDependency` object from the theme.

        Returns
        -------
        :
            An :class:`~htmltools.HTMLDependency` object representing the theme. In
            most cases, you should not need to call this method directly. Instead, pass
            the `Theme` object directly to the `theme` argument of any Shiny page
            function.
        """
        if self._css == "precompiled":
            return self._html_dependency_precompiled()

        dep_name = f"shiny-theme-{self.name or self._preset}"
        css_name = f"{dep_name}.min.css"

        # Re-use already compiled CSS file if possible
        if self._css and self._css_temp_srcdir is not None:
            return HTMLDependency(
                name=dep_name,
                version=Version(self._version),
                source={"subdir": self._css_temp_srcdir},
                stylesheet={"href": css_name},
            )

        tmpdir = tempfile.mkdtemp()
        srcdir = os.path.join(tmpdir, dep_name)
        os.mkdir(srcdir)
        css_path = os.path.join(srcdir, css_name)

        with open(css_path, "w") as css_file:
            css_file.write(self.to_css())

        self._css_temp_srcdir = srcdir
        return HTMLDependency(
            name=dep_name,
            version=Version(self._version),
            source={"subdir": srcdir},
            stylesheet={"href": css_name},
        )

    def tagify(self) -> HTMLDependency:
        """
        Create an :class:`~htmltools.HTMLDependency` object from the theme.
        """
        return self.html_dependency()


def dedent_array(x: list[str] | tuple[str, ...]) -> list[str]:
    return [dedent(y) for y in x]


def path_pkg_preset(preset: ShinyThemePreset, *args: str) -> str:
    """
    Returns a path relative to the packaged directory for a given preset.

    Examples
    --------

    ```python
    path_pkg_preset("shiny", "preset.min.css")
    #> "{shiny}/www/shared/sass/preset/shiny/preset.min.css"
    ```
    """
    return os.path.realpath(path_pkg_www("sass", "preset", str(preset), *args))


def check_is_valid_preset(preset: ShinyThemePreset) -> None:
    if preset not in shiny_theme_presets:
        raise ValueError(
            f"Invalid preset '{preset}'.\n"
            + f"""Expected one of: "{'", "'.join(shiny_theme_presets)}".""",
        )


def check_libsass_installed() -> None:
    import importlib.util

    if importlib.util.find_spec("sass") is None:
        raise ImportError(
            "The 'libsass' package is required to compile custom themes. "
            "Please install it with `pip install libsass` or `pip install shiny[theme]`.",
        )
