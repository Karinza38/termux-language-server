r"""Portage's ebuild
====================
"""

from typing import Any

from lsp_tree_sitter.misc import get_soup

from .._metainfo import SOURCE, project
from .licenses import ATOM


def init_schema() -> dict[str, dict[str, Any]]:
    r"""Init schema.

    :rtype: dict[str, dict[str, Any]]
    """
    filetype = "ebuild"
    schema = {
        "$id": (
            f"{SOURCE}/blob/main/"
            f"src/termux_language_server/assets/json/{filetype}.json"
        ),
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$comment": (
            "Don't edit this file directly! It is generated by "
            f"`{project} --generate-schema={filetype}`."
        ),
        "type": "object",
        "properties": {},
    }
    for dl in get_soup("ebuild").find_all("dl")[20:-2]:
        for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd"), strict=False):
            if dt.strong is None or dt.strong.text.endswith(":"):
                continue
            name = dt.strong.text.split()[0]
            description = dd.text.replace("\n", " ").strip()
            example = dt.text.replace("\n", " ")
            if name != example:
                description = f"""```sh
{example}
```
{description}"""
            schema["properties"][name] = {
                "description": description,
            }
            if name.isupper():
                schema["properties"][name]["type"] = "string"
            else:
                schema["properties"][name]["const"] = 0
    schema["properties"]["LICENSE"]["pattern"] = rf"{ATOM}(( |\n){ATOM})*"
    return {filetype: schema}
