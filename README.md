# Clickable Tags Updated

An Anki add-on: **click a tag in the note editor to see every card with that tag.**

In Anki's Browser, clicking a tag in the tag box normally opens it for renaming. With this add-on, one click opens a Browser search for that tag. You can jump from any note to all of its related cards in one step. It's built for heavily tagged decks like AnKing, where one note can carry dozens of UWorld, NBME, Boards & Beyond and system tags.

## How to use

| Action | Result |
|---|---|
| **Click** a tag | The Browser shows every card with that tag, subtags included |
| **Double-click** a tag | Rename it (Anki's usual single-click behavior) |
| **Ctrl/Cmd-click**, **Shift-click** | Select tags, unchanged |
| Trash icon | Delete the tag, unchanged |

- It works wherever the note editor appears: the **Browser**, **Add** and **Edit** windows. From Add or Edit it opens the Browser. Inside the Browser it only changes the search.
- Unsaved edits to the current note are saved before the search runs.
- Shortened tags like `...::WOMENS_HEALTH` are searched by their full name (hover a tag to see the full name).
- **To study those cards:** after clicking a tag, use **Edit → Create Filtered Deck** (Ctrl+G) in the Browser. It starts from the tag search you just ran.

## Install

- **AnkiWeb:** Tools → Add-ons → Get Add-ons, then paste the code from the add-on's AnkiWeb page.
- **From file:** Tools → Add-ons → Install from file… and choose `clickable_tags_updated.ankiaddon`.

Restart Anki after installing. No setup or card template changes are needed.

## Compatibility

- Windows, macOS and Linux: it's plain Python and JavaScript with no platform-specific code.
- Requires **Anki 24.06 or later**: that release added the `data-addon-tag` attribute this add-on relies on. Tested on Anki 26.09.
- Read-only: it never changes notes, tags or note types.
- A separate add-on written from scratch, not a fork of the original Clickable Tags. It pairs with **Clickable Tags v3.0**, which makes tags clickable on the review screen. This add-on only changes the editor, so they don't overlap.

## How it works

Anki's tag editor gives each tag button a `data-addon-tag` attribute. The add-on adds a small script to the editor. On a plain click, the script sends that tag to Python, which opens the Browser with the search `"tag:<name>"`. A short delay lets a double-click fall through to Anki's normal rename behavior.

One gotcha: the editor displays `::` as the look-alike character `∷` (U+2237), and the attribute holds that displayed form. The add-on converts it back to `::` before searching. Otherwise every hierarchical tag would match 0 cards.

## Files

- `__init__.py`: hooks and Browser search
- `web/clickable_tags_updated.js`: click handling inside the editor
- `manifest.json`: package info for `.ankiaddon` installs
- `LICENSE`: full AGPL-3.0 text
- `build_ankiaddon.py`: builds the `.ankiaddon` package (`python build_ankiaddon.py`)
- `ANKIWEB_DESCRIPTION.md`: the text used on the AnkiWeb listing

## Support

Found a bug or have an idea? [Open an issue](https://github.com/JungleTrouble/anki-clickable-tags-updated/issues).

## License

Copyright (C) 2026 Clickable Tags Updated contributors.

Licensed under the **GNU Affero General Public License v3.0 or later** (AGPL-3.0-or-later), the same license as Anki. See [LICENSE](LICENSE).

## Changelog

- **1.0**: first release.
