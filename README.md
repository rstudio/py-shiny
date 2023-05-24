Shiny for Python
================

Shiny for Python is the best way to build fast, beautiful web applications in Python. You can build quickly with Shiny and create simple interactive visualizations and prototype applications in an afternoon. But unlike other frameworks targeted at data scientists, Shiny does not limit your app's growth. Shiny remains extensible enough to power large, mission-critical applications.

To learn more about Shiny see the [Shiny for Python website](https://shiny.rstudio.com/py/). If you're new to the framework we recommend these resources:

-   Why [Shiny is better](https://posit.co/blog/why-shiny-for-python/) than Dash and Streamlit.

-   How [reactive programming](https://shiny.rstudio.com/py/docs/reactive-programming.html) can help you build better applications.

-   How to [use modules](https://shiny.rstudio.com/py/docs/workflow-modules.html) to efficiently develop large applications.

-   Hosting applications for free on [shinyapps.io](https://shiny.rstudio.com/py/docs/deploy.html#deploy-to-shinyapps.io-cloud-hosting), [Hugging Face](https://shiny.posit.co/blog/posts/shiny-on-hugging-face/), or [Shinylive](https://shiny.rstudio.com/py/docs/shinylive.html).

## Join the conversation

If you have questions about Shiny for Python, or want to help us decide what to work on next, [join us on Discord](https://discord.gg/yMGCamUMnS).

## Getting started

To get started with shiny follow the [installation instructions](https://shiny.rstudio.com/py/docs/install.html) or just install it from pip.

``` sh
pip install shiny
```

To install the latest development version from this repository:

``` sh
pip install https://github.com/rstudio/py-shiny/tarball/main
```

You can create and run your first application with:

```         
shiny create .
shiny run app.py --reload
```

## Development

If you want to do development on Shiny for Python:

``` sh
pip install -e ".[dev,test]"
```

Additionally, you can install pre-commit hooks which will automatically reformat and lint the code when you make a commit:

``` sh
pre-commit install

# To disable:
# pre-commit uninstall
```
