from __future__ import annotations

import re
import warnings
from pathlib import Path
from typing import Any, Optional

from brand_yml import Brand
from htmltools import HTMLDependency

from .._versions import bootstrap
from ._theme import Theme
from ._theme_presets import ShinyThemePreset, shiny_theme_presets

color_map = {
    "foreground": ["brand--foreground", "body-color", "pre-color"],
    "background": ["brand--background", "body-bg"],
    "primary": ["primary"],
    "secondary": ["secondary", "body-secondary-color", "body-secondary"],
    "tertiary": ["body-tertiary-color", "body-tertiary"],
    "success": ["success"],
    "info": ["info"],
    "warning": ["warning"],
    "danger": ["danger"],
    "light": ["light"],
    "dark": ["dark"],
}
"""Maps brand.color fields to Bootstrap Sass variables"""

bootstrap_colors = {
    # https://github.com/twbs/bootstrap/blob/6e1f75/scss/_variables.scss#L38-L49
    "5": [
        "white",
        "black",
        "blue",
        "indigo",
        "purple",
        "pink",
        "red",
        "orange",
        "yellow",
        "green",
        "teal",
        "cyan",
    ]
}
"""
Colors known to Bootstrap

When these colors are named in `colors.palette`, we'll map the brand's colors to the
corresponding Bootstrap color Sass variable.

* [Bootstrap 5 - Colors](https://getbootstrap.com/docs/5.3/customize/color/#color-sass-maps)
"""

# TODO: test that these Sass variables exist in Bootstrap
typography_map = {
    "base": {
        "family": "font-family-base",
        "size": "font-size-base",
        "line_height": "line-height-base",
        "weight": "font-weight-base",
    },
    "headings": {
        "family": "headings-font-family",
        "line_height": "headings-line-height",
        "weight": "headings-font-weight",
        "color": "headings-color",
        "style": "headings-style",
    },
    "monospace": {
        "family": "font-family-monospace",
        "size": "code-font-size",
    },
    "monospace_inline": {
        "family": "font-family-monospace-inline",
        "color": "code-color",
        "background_color": "code-bg",
        "size": "code-inline-font-size",
        "weight": "code-font-weight",
    },
    "monospace_block": {
        "family": "font-family-monospace-block",
        "line_height": "pre-line-height",
        "color": "pre-color",
        "background_color": "pre-bg",
    },
    "link": {
        "background_color": "link-bg",
        "color": "link-color",
        "weight": "link-weight",
        "decoration": "link-decoration",
    },
}
"""Maps brand.typography fields to corresponding Bootstrap Sass variables"""


class BrandBootstrap:
    """Convenience class for storing Bootstrap defaults from a brand instance"""

    def __init__(
        self,
        version: Any = bootstrap,
        preset: Any = "shiny",
        **kwargs: str | int | bool | float | None,
    ):
        if not isinstance(version, (str, int)):
            raise ValueError(
                f"Bootstrap version must be a string or integer, not {version!r}."
            )

        v_major = str(version).split(".")[0]
        bs_major = str(bootstrap).split(".")[0]

        if v_major != bs_major:
            # TODO (bootstrap-update): Assumes Shiny ships one version of Bootstrap
            warnings.warn(
                f"Shiny does not current support Bootstrap version {v_major}. "
                f"Using Bootstrap v{bs_major} instead.",
                stacklevel=4,
            )
            v_major = bs_major

        if not isinstance(preset, str) or preset not in shiny_theme_presets:
            raise ValueError(
                f"{preset!r} is not a valid Bootstrap preset provided by Shiny. "
                f"Valid presets are {shiny_theme_presets}."
            )

        self.version = v_major
        self.preset: ShinyThemePreset = preset
        self.defaults = kwargs

    @classmethod
    def from_brand(cls, brand: Brand):
        defaults: dict[str, str | int | bool | float | None] = {}

        if brand.defaults:
            if brand.defaults and "bootstrap" in brand.defaults:
                defaults.update(brand.defaults["bootstrap"])
            if "shiny" in brand.defaults and "theme" in brand.defaults["shiny"]:
                defaults.update(brand.defaults["shiny"]["theme"])

        return cls(**defaults)


class ThemeBrand(Theme):
    def __init__(
        self,
        brand: Brand,
        *,
        include_paths: Optional[str | Path | list[str | Path]] = None,
    ):

        name: str = "brand"
        if brand.meta and brand.meta.name:
            name = brand.meta.name.full or brand.meta.name.short or name

        brand_bootstrap = BrandBootstrap.from_brand(brand)

        # Initialize theme ------------------------------------------------------------
        super().__init__(
            name=name,
            preset=brand_bootstrap.preset,
            include_paths=include_paths,
        )
        self.brand = brand

        # brand.color -----------------------------------------------------------------
        sass_vars_colors: dict[str, str] = {}
        if brand.color:
            # Map values in colors to their Sass variable counterparts
            for field, theme_color in brand.color.to_dict(include="theme").items():
                if field not in color_map:
                    print(f"skipping color.{field} not mapped")
                    continue

                for sass_var in color_map[field]:
                    sass_vars_colors[sass_var] = theme_color

            # Map the brand color palette to Bootstrap's named colors, e.g. $red, $blue.
            bs_color_vars = bootstrap_colors[brand_bootstrap.version]
            for field, palette_color in brand.color.to_dict(include="palette").items():
                if field in bs_color_vars:
                    sass_vars_colors[field] = palette_color

        # brand.typography ------------------------------------------------------------
        sass_vars_typography: dict[str, str] = {}
        if brand.typography:
            for field in brand.typography.model_fields.keys():
                if field == "fonts":
                    continue
                type_prop = getattr(brand.typography, field)
                if type_prop is None:
                    continue
                for k, v in type_prop.model_dump(exclude_none=True).items():
                    if k in typography_map[field]:
                        sass_vars_typography[typography_map[field][k]] = v
                    else:
                        # TODO: Need to catch these and map to appropriate Bootstrap vars
                        print(f"skipping {field}.{k} not mapped")

        sass_vars_brand_colors: dict[str, str] = {}
        css_vars_brand_colors: list[str] = []

        if brand.color and brand.color.palette is not None:
            for p_var, p_value in brand.color.palette.items():
                p_var = sanitize_sass_var_name(p_var)

                # Create color variables from palette, `$brand-{name}: {value}`
                sass_vars_brand_colors.update({f"brand-{p_var}": p_value})
                # Create CSS variables from palette, `--brand-{name}: {value}`
                css_vars_brand_colors.append(f"--brand-{p_var}: {p_value};")

        sass_vars_brand: dict[str, str] = {
            **sass_vars_brand_colors,
            **sass_vars_colors,
            **sass_vars_typography,
        }
        sass_vars_brand = {k: v for k, v in sass_vars_brand.items()}

        # Defaults are added in reverse order, so each chunk appears above the next
        # layer of defaults. The intended order in the final output is:
        # 1. Brand Sass vars (colors, typography)
        # 2. Brand Bootstrap Sass vars
        # 3. Fallback vars needed by additional Brand rules
        self.add_defaults(
            # Variables we create to augment Bootstrap's variables
            **{
                "code-font-weight": "normal",
                "link-bg": None,
                "link-weight": None,
                "gray-100": "mix($white, $black, 90%)",
                "gray-200": "mix($white, $black, 80%)",
                "gray-300": "mix($white, $black, 70%)",
                "gray-400": "mix($white, $black, 60%)",
                "gray-500": "mix($white, $black, 50%)",
                "gray-600": "mix($white, $black, 40%)",
                "gray-700": "mix($white, $black, 30%)",
                "gray-800": "mix($white, $black, 20%)",
                "gray-900": "mix($white, $black, 10%)",
            }
        )
        self.add_defaults(**brand_bootstrap.defaults)
        self.add_defaults(**sass_vars_brand)
        # Brand Rules ----
        self.add_rules(":root {", *css_vars_brand_colors, "}")
        # Additional rules to fill in Bootstrap styles for Brand parameters
        self.add_rules(
            """
            // https://github.com/twbs/bootstrap/blob/5c2f2e7e/scss/_root.scss#L82
            :root {
                --#{$prefix}link-bg: #{$link-bg};
                --#{$prefix}link-weight: #{$link-weight};
            }
            // https://github.com/twbs/bootstrap/blob/5c2f2e7e/scss/_reboot.scss#L244
            a {
                background-color: var(--#{$prefix}link-bg);
                font-weight: var(--#{$prefix}link-weight);
            }
            code {
                font-weight: $code-font-weight;
            }
            """
        )

    def _html_dependencies(self) -> list[HTMLDependency]:
        theme_deps = super()._html_dependencies()

        if not self.brand.typography:
            return theme_deps

        # We're going to put the fonts dependency _inside_ the theme's tempdir, which
        # relies on the theme's dependency having `all_files=True`. We do this because
        # Theme handles the tempdir lifecycle and we want the fonts dependency to be
        # handled in the same way.
        temp_dir = self._get_css_tempdir()
        temp_path = Path(temp_dir) / "fonts"
        temp_path.mkdir(parents=True, exist_ok=True)

        fonts_dep = self.brand.typography.fonts_html_dependency(
            path_dir=temp_path,
            name=f"{self._dep_name()}-fonts",
            version=self._version,
        )

        if fonts_dep is None:
            return theme_deps

        return [fonts_dep, *theme_deps]


def sanitize_sass_var_name(x: str) -> str:
    x = re.sub(r"""['"]""", "", x)
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", x)
