// Copyright (C) 2026 Clickable Tags Updated contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Clickable Tags Updated: click a tag in the note editor to see every card with that tag.
// Single click  -> open the Browser searching that tag
// Double click  -> Anki's normal behaviour (rename the tag)
// Ctrl/Cmd/Shift/Alt + click and the delete icon are left untouched.
(() => {
    if (window.__clickableTagsUpdatedLoaded) {
        return;
    }
    window.__clickableTagsUpdatedLoaded = true;

    const PREFIX = "clickableTagsUpdated:";
    const DOUBLE_CLICK_WINDOW_MS = 250;

    let pendingTimer = null;
    let passThrough = false;

    const send = (tag) => {
        const bridge = window.pycmd || window.bridgeCommand;
        if (typeof bridge === "function") {
            bridge(PREFIX + JSON.stringify({ tag }));
        }
    };

    // Use composedPath so this also works if the tag editor sits in a shadow root.
    const findTagButton = (event) => {
        const path = typeof event.composedPath === "function" ? event.composedPath() : [];
        for (const node of path) {
            if (!(node instanceof Element)) {
                continue;
            }
            if (node.classList.contains("badge")) {
                return null; // delete icon: keep Anki's behaviour
            }
            if (node.matches("button.tag[data-addon-tag]")) {
                return node;
            }
        }
        return null;
    };

    const clearPending = () => {
        if (pendingTimer !== null) {
            clearTimeout(pendingTimer);
            pendingTimer = null;
        }
    };

    document.addEventListener(
        "click",
        (event) => {
            if (passThrough) {
                return;
            }
            if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) {
                return; // tag selection shortcuts
            }
            const button = findTagButton(event);
            if (!button) {
                return;
            }
            const tag = button.getAttribute("data-addon-tag") || "";
            if (!tag) {
                return; // empty / in-progress tag
            }

            event.preventDefault();
            event.stopImmediatePropagation();

            if (event.detail >= 2) {
                // Second click of a double click: hand a normal click to Anki so it opens the rename box.
                clearPending();
                passThrough = true;
                try {
                    button.click();
                } finally {
                    passThrough = false;
                }
                return;
            }

            clearPending();
            pendingTimer = setTimeout(() => {
                pendingTimer = null;
                send(tag);
            }, DOUBLE_CLICK_WINDOW_MS);
        },
        true,
    );

    const style = document.createElement("style");
    style.textContent = "button.tag[data-addon-tag] { cursor: pointer; }";
    document.head.appendChild(style);
})();
