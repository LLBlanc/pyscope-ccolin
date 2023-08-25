import inspect
import os
import pathlib
import subprocess
import sys

sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

from urllib.parse import quote

from sphinx_astropy.conf.v2 import *

project = "pyscope"
copyright = "2023, Walter Golay"
author = "Walter Golay"
version = release = "0.1.0"

graphviz_dot = "/usr/local/bin/dot"

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/WWGolay/pyscope",
            "icon": "fa-brands fa-square-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pyscope/",
            "icon": "fa-brands fa-python",
        },
        {
            "name": "macro",
            "url": "https://macroconsortium.org",
            "icon": "fa-solid fa-shuttle-space",
        },
    ]
}

extensions = list(map(lambda x: x.replace("viewcode", "linkcode"), extensions))

intersphinx_mapping["click"] = ("https://click.palletsprojects.com/en/8.1.x/", None)
intersphinx_mapping["astroquery"] = (
    "https://astroquery.readthedocs.io/en/latest/",
    None,
)
intersphinx_mapping["astroplan"] = ("https://astroplan.readthedocs.io/en/latest/", None)


linkcode_revision = "main"
try:
    # lock to commit number
    cmd = "git log -n1 --pretty=%H"
    head = subprocess.check_output(cmd.split()).strip().decode("utf-8")
    linkcode_revision = head

    # if we are on master's HEAD, use master as reference
    cmd = "git log --first-parent master -n1 --pretty=%H"
    master = subprocess.check_output(cmd.split()).strip().decode("utf-8")
    if head == master:
        linkcode_revision = "master"

    # if we have a tag, use tag as reference
    cmd = "git describe --exact-match --tags " + head
    tag = subprocess.check_output(cmd.split(" ")).strip().decode("utf-8")
    linkcode_revision = tag

except subprocess.CalledProcessError:
    pass

linkcode_url = (
    "https://github.com/WWGolay/pyscope/blob/"
    + linkcode_revision
    + "/{filepath}#L{linestart}-L{linestop}"
)


def linkcode_resolve(domain, info):
    if domain != "py" or not info["module"]:
        return None

    modname = info["module"]
    topmodulename = modname.split(".")[0]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    try:
        modpath = pkg_resources.require(topmodulename)[0].location
        filepath = os.path.relpath(inspect.getsourcefile(obj), modpath)
        if filepath is None:
            return
    except Exception:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except OSError:
        return None
    else:
        linestart, linestop = lineno, lineno + len(source) - 1

    return linkcode_url.format(
        filepath=filepath, linestart=linestart, linestop=linestop
    )


extensions.append("sphinx_favicon")

html_logo = "images/pyscope_banner.png"
"""favicons = [
    "images/logo16.png",
    "images/logo32.png",
    "images/logo48.png",
    "images/logo128.png",
    "images/logo256.png",
    "images/pyscope.svg",
    "images/pyscope_transparent.svg"
]"""

extensions.append("sphinx.ext.doctest")

# extensions.append("sphinxcontrib.programoutput")
# extensions.append("sphinx_exec_code")
