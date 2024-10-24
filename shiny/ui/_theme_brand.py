from __future__ import annotations

import os
import re
import warnings
from pathlib import Path
from typing import Any, Optional, Union

from brand_yml import Brand
from htmltools import HTMLDependency

from .._versions import bootstrap as v_bootstrap
from ._theme import Theme
from ._theme_presets import ShinyThemePreset, shiny_theme_presets
from .css import CssUnit, as_css_unit

YamlScalarType = Union[str, int, bool, float, None]


class ThemeBrandUnmappedFieldError(ValueError):
    def __init__(self, field: str):
        self.field = field
        self.message = f"Unmapped brand.yml field: {field}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


def warn_or_raise_unmapped_variable(unmapped: str):
    if os.environ.get("SHINY_BRAND_YML_RAISE_UNMAPPED") == "true":
        raise ThemeBrandUnmappedFieldError(unmapped)
    else:
        warnings.warn(
            f"Shiny's brand.yml theme does not yet support {unmapped}.",
            stacklevel=4,
        )


color_map: dict[str, list[str]] = {
    # Bootstrap uses $gray-900 and $white for the body bg-color by default, and then
    # swaps them for $gray-100 and $gray-900 in dark mode. brand.yml may end up with
    # light/dark variants for foreground/background, see posit-dev/brand-yml#38.
    "foreground": ["brand--foreground", "body-color", "body-bg-dark"],
    "background": ["brand--background", "body-bg", "body-color-dark"],
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

# https://github.com/twbs/bootstrap/blob/6e1f75/scss/_variables.scss#L38-L49
bootstrap_colors: list[str] = [
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
"""
Colors known to Bootstrap

When these colors are named in `colors.palette`, we'll map the brand's colors to the
corresponding Bootstrap color Sass variable.

* [Bootstrap 5 - Colors](https://getbootstrap.com/docs/5.3/customize/color/#color-sass-maps)
"""

# TODO: test that these Sass variables exist in Bootstrap
typography_map: dict[str, dict[str, list[str]]] = {
    "base": {
        "family": ["font-family-base"],
        "size": ["font-size-base"],
        "line_height": ["line-height-base"],
        "weight": ["font-weight-base"],
    },
    "headings": {
        "family": ["headings-font-family"],
        "line_height": ["headings-line-height"],
        "weight": ["headings-font-weight"],
        "color": ["headings-color"],
        "style": ["headings-style"],
    },
    "monospace": {
        "family": ["font-family-monospace"],
        "size": ["code-font-size"],
        "weight": ["code-font-weight"],
    },
    "monospace_inline": {
        "family": ["font-family-monospace-inline"],
        "color": ["code-color", "code-color-dark"],
        "background_color": ["code-bg"],
        "size": ["code-inline-font-size"],
        "weight": ["code-inline-font-weight"],
    },
    "monospace_block": {
        "family": ["font-family-monospace-block"],
        "line_height": ["code-block-line-height"],
        "color": ["pre-color"],
        "background_color": ["pre-bg"],
        "weight": ["code-block-font-weight"],
        "size": ["code-block-font-size"],
    },
    "link": {
        "background_color": ["link-bg"],
        "color": ["link-color", "link-color-dark"],
        "weight": ["link-weight"],
        "decoration": ["link-decoration"],
    },
}
"""Maps brand.typography fields to corresponding Bootstrap Sass variables"""


class BrandBootstrapConfigFromYaml:
    def __init__(
        self,
        path: str,
        version: Any = None,
        preset: Any = None,
        functions: Any = None,
        defaults: Any = None,
        mixins: Any = None,
        rules: Any = None,
    ):

        self.path = path
        self.version = version
        self.preset: str | None = self._validate_str(preset, "preset")
        self.functions: str | None = self._validate_str(functions, "functions")
        self.defaults: dict[str, YamlScalarType] | None = self._validate_defaults(
            defaults
        )
        self.mixins: str | None = self._validate_str(mixins, "mixins")
        self.rules: str | None = self._validate_str(rules, "rules")

    def _validate_str(self, x: Any, param: str) -> str | None:
        if x is None or isinstance(x, str):
            return x

        raise ValueError(
            f"Invalid brand `{self.path}.{param}`. Must be a string or empty."
        )

    def _validate_defaults(self, x: Any) -> dict[str, YamlScalarType] | None:
        if x is None:
            return None

        path = self.path
        if path == "defaults.shiny.theme":
            path += ".defaults"

        if not isinstance(x, dict):
            raise ValueError(f"Invalid brand `{path}`, must be a dictionary.")

        y: dict[Any, Any] = x

        if not all([isinstance(k, str) for k in y.keys()]):
            raise ValueError(f"Invalid brand `{path}`, all keys must be strings.")

        if not all(
            [v is None or isinstance(v, (str, int, float, bool)) for v in y.values()]
        ):
            raise ValueError(f"Invalid brand `{path}`, all values must be scalar.")

        res: dict[str, YamlScalarType] = y
        return res


class BrandBootstrapConfig:
    """Convenience class for storing Bootstrap defaults from a brand instance"""

    def __init__(
        self,
        version: Any = v_bootstrap,
        preset: Any = "shiny",
        functions: str | None = None,
        defaults: dict[str, YamlScalarType] | None = None,
        mixins: str | None = None,
        rules: str | None = None,
    ):
        if not isinstance(version, (str, int)):
            raise ValueError(
                f"Bootstrap version must be a string or integer, not {version!r}."
            )

        v_major = str(version).split(".")[0]
        bs_major = str(v_bootstrap).split(".")[0]

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
        self.functions = functions
        self.defaults = defaults
        self.mixins = mixins
        self.rules = rules

    @classmethod
    def from_brand(cls, brand: Brand):
        if not brand.defaults:
            return cls(version=v_bootstrap, preset="shiny")

        defaults: dict[str, YamlScalarType] = {}

        d_bootstrap = BrandBootstrapConfig._brand_defaults_bootstrap(brand)
        d_shiny = BrandBootstrapConfig._brand_defaults_shiny(brand)

        defaults.update(d_bootstrap.defaults or {})
        defaults.update(d_shiny.defaults or {})

        return cls(
            version=d_shiny.version or d_bootstrap.version or v_bootstrap,
            preset=d_shiny.preset or d_bootstrap.preset or "shiny",
            functions=d_shiny.functions,
            defaults=defaults,
            mixins=d_shiny.mixins,
            rules=d_shiny.rules,
        )

    @staticmethod
    def _brand_defaults_shiny(brand: Brand) -> BrandBootstrapConfigFromYaml:
        if (
            not brand.defaults
            or not isinstance(brand.defaults.get("shiny"), dict)
            or not isinstance(brand.defaults["shiny"].get("theme"), dict)
        ):
            return BrandBootstrapConfigFromYaml(path="defaults.shiny.theme")

        return BrandBootstrapConfigFromYaml(
            path="defaults.shiny.theme",
            **brand.defaults["shiny"]["theme"],
        )

    @staticmethod
    def _brand_defaults_bootstrap(brand: Brand) -> BrandBootstrapConfigFromYaml:
        if not brand.defaults or not isinstance(brand.defaults.get("bootstrap"), dict):
            return BrandBootstrapConfigFromYaml(path="defaults.bootstrap")

        bootstrap: dict[str, Any] = brand.defaults["bootstrap"]
        defaults: dict[str, Any] = {
            k: v for k, v in bootstrap if k not in ("version", "preset")
        }

        return BrandBootstrapConfigFromYaml(
            path="defaults.bootstrap",
            version=bootstrap.get("version"),
            preset=bootstrap.get("preset"),
            **defaults,
        )


class ThemeBrand(Theme):
    def __init__(
        self,
        brand: Brand,
        *,
        include_paths: Optional[str | Path | list[str | Path]] = None,
    ):

        name = self._get_theme_name(brand)
        brand_bootstrap = BrandBootstrapConfig.from_brand(brand)

        # Initialize theme ------------------------------------------------------------
        super().__init__(
            name=name,
            preset=brand_bootstrap.preset,
            include_paths=include_paths,
        )

        self.brand = brand

        # Prep Sass and CSS Variables -------------------------------------------------
        sass_vars_colors, sass_vars_brand, css_vars_brand = (
            ThemeBrand._prepare_color_vars(brand)
        )
        sass_vars_typography = ThemeBrand._prepare_typography_vars(brand)

        # Theme -----------------------------------------------------------------------
        # Defaults are added in reverse order, so each chunk appears above the next
        # layer of defaults. The intended order in the final output is:
        # 1. Brand Sass color and typography vars
        # 2. Brand's Bootstrap Sass vars
        # 3. Gray scale variables from Brand fg/bg or black/white
        # 4. Fallback vars needed by additional Brand rules

        self.add_defaults("", "// *---- brand: end of defaults ----* //", "")
        self._add_sass_ensure_variables()
        self._add_sass_brand_grays()
        self._add_defaults_brand_bootstrap(brand_bootstrap)
        self._add_defaults_typography(sass_vars_typography)
        self._add_defaults_color(sass_vars_colors, sass_vars_brand)

        # Brand rules (now in forwards order)
        self._add_rules_brand_colors(css_vars_brand)
        self._add_sass_brand_rules()
        self._add_brand_bootstrap_other(brand_bootstrap)

    def _get_theme_name(self, brand: Brand) -> str:
        if not brand.meta or not brand.meta.name:
            return "brand"

        return brand.meta.name.short or brand.meta.name.full or "brand"

    @staticmethod
    def _prepare_color_vars(
        brand: Brand,
    ) -> tuple[dict[str, str], dict[str, str], list[str]]:
        """Colors: create a dictionary of Sass variables and a list of brand CSS variables"""
        if not brand.color:
            return {}, []

        mapped: dict[str, str] = {}
        brand_sass_vars: dict[str, str] = {}
        brand_css_vars: list[str] = []

        # Map values in colors to their Sass variable counterparts
        for thm_name, thm_color in brand.color.to_dict(include="theme").items():
            if thm_name not in color_map:
                warn_or_raise_unmapped_variable(f"color.{thm_name}")
                continue

            for sass_var in color_map[thm_name]:
                mapped[sass_var] = thm_color

        brand_color_palette = brand.color.to_dict(include="palette")

        # Map the brand color palette to Bootstrap's named colors, e.g. $red, $blue.
        for pal_name, pal_color in brand_color_palette.items():
            if pal_name in bootstrap_colors:
                mapped[pal_name] = pal_color

            # Create Sass and CSS variables for the brand color palette
            color_var = sanitize_sass_var_name(pal_name)

            # => Sass var: `$brand-{name}: {value}`
            brand_sass_vars.update({f"brand-{color_var}": pal_color})
            # => CSS var: `--brand-{name}: {value}`
            brand_css_vars.append(f"--brand-{color_var}: {pal_color};")

        # We keep Sass and Brand vars separate so we can ensure Brand Sass vars come
        # first in the compiled Sass definitions.
        return mapped, brand_sass_vars, brand_css_vars

    @staticmethod
    def _prepare_typography_vars(brand: Brand) -> dict[str, str]:
        """Typography: Create a list of Bootstrap Sass variables"""
        mapped: dict[str, str] = {}

        if not brand.typography:
            return mapped

        brand_typography = brand.typography.model_dump(
            exclude={"fonts"},
            exclude_none=True,
        )

        for field, prop in brand_typography.items():
            if field not in typography_map:
                warn_or_raise_unmapped_variable(f"typography.{field}")
                continue

            for prop_key, prop_value in prop.items():
                if prop_key in typography_map[field]:
                    if field == "base" and prop_key == "size":
                        prop_value = str(maybe_convert_font_size_to_rem(prop_value))

                    typo_sass_vars = typography_map[field][prop_key]
                    for typo_sass_var in typo_sass_vars:
                        mapped[typo_sass_var] = prop_value
                else:
                    warn_or_raise_unmapped_variable(f"typography.{field}.{prop_key}")

        return mapped

    def _add_sass_ensure_variables(self):
        """Ensure the variables we create to augment Bootstrap's variables exist"""
        self.add_defaults(
            **{
                "code-font-weight": None,
                "code-inline-font-weight": None,
                "code-inline-font-size": None,
                "code-block-font-weight": None,
                "code-block-font-size": None,
                "code-block-line-height": None,
                "link-bg": None,
                "link-weight": None,
            }
        )
        self.add_defaults("// *---- brand: added variables ---* //")

    def _add_sass_brand_grays(self):
        """
        Adds functions and defaults to handle creating a gray scale palette from the
        brand color palette, or the brand's foreground/background colors.
        """
        self.add_functions(
            """
            @function brand-choose-white-black($foreground, $background) {
              $lum_fg: luminance($foreground);
              $lum_bg: luminance($background);
              $contrast: contrast-ratio($foreground, $background);

              @if $contrast  < 4.5 {
                @warn "The contrast ratio of #{$contrast} between the brand's foreground color (#{inspect($foreground)}) and background color (#{inspect($background)}) is very low. Consider picking colors with higher contrast for better readability.";
              }

              $white: if($lum_fg > $lum_bg, $foreground, $background);
              $black: if($lum_fg <= $lum_bg, $foreground, $background);

              // If the brand foreground/background are close enough to black/white, we
              // use those values. Otherwise, we'll mix the white/black from the brand
              // fg/bg with actual white and black to get something much closer.
              @return (
                "white": if(contrast-ratio($white, white) <= 1.15, $white, mix($white, white, 20%)),
                "black": if(contrast-ratio($black, black) <= 1.15, $black, mix($black, black, 20%)),
              );
            }
            """
        )
        self.add_defaults(
            """
            $enable-brand-grays: true !default;
            // Ensure these variables exist so that we can set them inside of @if context
            // They can still be overwritten by the user, even with !default;
            $white: null !default;
            $black: null !default;
            $gray-100: null !default;
            $gray-200: null !default;
            $gray-300: null !default;
            $gray-400: null !default;
            $gray-500: null !default;
            $gray-600: null !default;
            $gray-700: null !default;
            $gray-800: null !default;
            $gray-900: null !default;

            @if $enable-brand-grays {
              @if variable-exists(brand--foreground) and variable-exists(brand--background) {
                $brand-white-black: brand-choose-white-black($brand--foreground, $brand--background);
                @if $white == null {
                  $white: map-get($brand-white-black, "white") !default;
                }
                @if $black == null {
                  $black: map-get($brand-white-black, "black") !default;
                }
              }
              @if $white != null and $black != null {
                $gray-100: mix($white, $black, 90%) !default;
                $gray-200: mix($white, $black, 80%) !default;
                $gray-300: mix($white, $black, 70%) !default;
                $gray-400: mix($white, $black, 60%) !default;
                $gray-500: mix($white, $black, 50%) !default;
                $gray-600: mix($white, $black, 40%) !default;
                $gray-700: mix($white, $black, 30%) !default;
                $gray-800: mix($white, $black, 20%) !default;
                $gray-900: mix($white, $black, 10%) !default;
              }
            }
            """
        )
        self.add_defaults("// *---- brand: automatic gray gradient ----* //")

    def _add_defaults_brand_bootstrap(self, brand_bootstrap: BrandBootstrapConfig):
        if not brand_bootstrap.defaults:
            return

        self.add_defaults(**brand_bootstrap.defaults)
        self.add_defaults(
            "// *---- brand.defaults.bootstrap + brand.defaults.shiny.theme ----* //"
        )

    def _add_defaults_typography(self, sass_vars_typography: dict[str, str]):
        self.add_defaults(**sass_vars_typography)
        self.add_defaults("\n// *---- brand.typography ----* //")

    def _add_sass_brand_rules(self):
        """Additional rules to fill in Bootstrap styles for Brand parameters"""
        self.add_rules(
            """
            // *---- brand: brand rules to augment Bootstrap rules ----* //
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
            code {
              font-weight: $code-inline-font-weight;
              font-size: $code-inline-font-size;
            }
            // https://github.com/twbs/bootstrap/blob/30e01525/scss/_reboot.scss#L287
            pre {
              font-weight: $code-block-font-weight;
              font-size: $code-block-font-size;
              line-height: $code-block-line-height;
            }

            $bslib-dashboard-design: false !default;
            @if $bslib-dashboard-design and variable-exists(brand--background) {
              // When brand makes dark mode, it usually hides card definition, so we add
              // back card borders in dark mode.
              [data-bs-theme="dark"] {
                --bslib-card-border-color: RGBA(255, 255, 255, 0.15);
              }
            }
            """
        )

    def _add_defaults_color(
        self,
        sass_vars_colors: dict[str, str],
        sass_vars_brand: dict[str, str],
    ):
        self.add_defaults(**sass_vars_colors)
        self.add_defaults(**sass_vars_brand)
        self.add_defaults("\n// *---- brand.color ----* //")

    def _add_rules_brand_colors(self, css_vars_colors: list[str]):
        self.add_rules("\n// *---- brand.color.palette ----* //")
        self.add_rules(":root {", *css_vars_colors, "}")

    def _add_brand_bootstrap_other(self, bootstrap: BrandBootstrapConfig):
        if bootstrap.functions:
            self.add_functions(bootstrap.functions)
        if bootstrap.mixins:
            self.add_mixins(bootstrap.mixins)
        if bootstrap.rules:
            self.add_rules(bootstrap.rules)

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


def maybe_convert_font_size_to_rem(x: str) -> CssUnit:
    """
    Convert a font size to rem

    Bootstrap expects base font size to be in `rem`. This function converts `em`, `%`,
    `px`, `pt` to `rem`:

    1. `em` is directly replace with `rem`.
    2. `1%` is `0.01rem`, e.g. `90%` becomes `0.9rem`.
    3. `16px` is `1rem`, e.g. `18px` becomes `1.125rem`.
    4. `12pt` is `1rem`.
    5. `0.1666in` is `1rem`.
    6. `4.234cm` is `1rem`.
    7. `42.3mm` is `1rem`.
    """
    x_og = f"{x}"
    x = as_css_unit(x)

    value, unit = split_css_value_and_unit(x)

    if unit == "rem":
        return x

    if unit == "em":
        return as_css_unit(f"{value}rem")

    scale = {
        "%": 100,
        "px": 16,
        "pt": 12,
        "in": 96 / 16,  # 96 px/inch
        "cm": 96 / 16 * 2.54,  # inch -> cm
        "mm": 16 / 96 * 25.4,  # cm -> mm
    }

    if unit in scale:
        return as_css_unit(f"{float(value) / scale[unit]}rem")

    raise ValueError(
        f"Shiny does not support brand.yml font sizes in {unit} units ({x_og!r})"
    )


def split_css_value_and_unit(x: str) -> tuple[str, str]:
    match = re.match(r"^(-?\d*\.?\d+)([a-zA-Z%]*)$", x)
    if not match:
        raise ValueError(f"Invalid CSS value format: {x}")
    value, unit = match.groups()
    return value, unit
