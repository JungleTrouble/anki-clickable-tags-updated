# Copyright (C) 2026 Tag Click Search contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
# Licensed under the GNU Affero General Public License v3 or later; see LICENSE.

"""Tag Click Search

Click a tag in Anki's note editor (Browser, Add, Edit) to open the Browser
showing every card with that tag. Double-click a tag to rename it as usual.
Pure Python + JavaScript, so it behaves the same on Windows, macOS and Linux.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aqt import dialogs, gui_hooks, mw

PREFIX = "tagClickSearch:"
_JS = (Path(__file__).parent / "web" / "tag_click_search.js").read_text(encoding="utf-8")


def _is_editor(context: Any) -> bool:
    # Duck-typed so it works with both the classic Editor and 26.x's NewEditor.
    return all(hasattr(context, attr) for attr in ("web", "call_after_note_saved"))


def _on_editor_did_load_note(editor: Any) -> None:
    web = getattr(editor, "web", None)
    if web is not None:
        web.eval(_JS)  # the script guards itself against loading twice


# The editor's tag box displays "::" as this look-alike character, and the
# data-addon-tag attribute carries the displayed form.
_EDITOR_DELIM = "∷"


def _tag_query(tag: str) -> str:
    # Matches the exact tag plus its subtags. "_" and "*" are left unescaped:
    # as wildcards they still match themselves.
    escaped = tag.replace("\\", "\\\\").replace('"', '\\"')
    return f'"tag:{escaped}"'


def _open_browser_for_tag(tag: str) -> None:
    browser = dialogs.open("Browser", mw, search=(_tag_query(tag),))
    if browser is not None:
        browser.activateWindow()
        browser.raise_()


def _on_js_message(handled: tuple[bool, Any], message: str, context: Any) -> tuple[bool, Any]:
    if not message.startswith(PREFIX):
        return handled
    try:
        payload = json.loads(message[len(PREFIX):])
    except ValueError:
        return (True, None)
    tag = payload.get("tag") if isinstance(payload, dict) else None
    if not isinstance(tag, str) or not tag.strip():
        return (True, None)
    tag = tag.replace(_EDITOR_DELIM, "::").strip()

    if _is_editor(context):
        # Save any edits to the current note before the Browser changes its search.
        context.call_after_note_saved(lambda: _open_browser_for_tag(tag))
    else:
        _open_browser_for_tag(tag)
    return (True, None)


gui_hooks.editor_did_load_note.append(_on_editor_did_load_note)
gui_hooks.webview_did_receive_js_message.append(_on_js_message)
