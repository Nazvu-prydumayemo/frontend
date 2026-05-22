from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import TYPE_CHECKING

from textual import on
from textual.containers import Container, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Button, DirectoryTree, Static

from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.inputs import TextInput
from tuiapp.widgets.modals.base_modal import BaseModal

if TYPE_CHECKING:
    from textual.app import ComposeResult


class ExportDataModal(BaseModal):
    small: reactive[bool] = reactive(False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._selected_dir = Path.cwd()

    def watch_small(self, is_small: bool) -> None:
        try:
            self.query_one("#modal-container", Container).styles.width = "100%" if is_small else 60
        except NoMatches:
            pass

    def on_resize(self) -> None:
        self.small = self.size.width <= 64

    def compose_modal(self) -> ComposeResult:
        yield Static("Export Your Data", id="modal-title")
        yield Static("Select a directory and enter a filename:", id="modal-description")
        yield Static(f"Directory: {self._selected_dir}", id="selected-dir")
        yield DirectoryTree(path=self._selected_dir, id="directory-tree")

        with Vertical(classes="field"):
            yield Static("Filename", classes="field-label")
            yield TextInput(value="user_data_export.json", id="filename-input")

        with Container(id="buttons-container"):
            yield PrimaryButton("Export", variant="success", id="export")
            yield SecondaryButton("Cancel", variant="warning", id="close")

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        self._selected_dir = event.path
        self.query_one("#selected-dir", Static).update(f"Directory: {self._selected_dir}")

    @on(Button.Pressed, "#close")
    def cancel(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#export")
    async def export(self) -> None:
        filename = self.query_one("#filename-input", TextInput).value.strip()
        if not filename:
            self.notify("Please enter a filename", title="Export Data", severity="warning")
            return

        filepath = self._selected_dir / filename

        result = await self.app.account.export_data()  # type: ignore

        if result.status != "success" or result.data_export is None:
            self.notify(result.message, title="Export Data", severity="error")
            return

        data = result.data_export.model_dump(mode="json")

        def _write() -> None:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        await asyncio.to_thread(_write)

        self.notify(f"Data exported to {filepath}", title="Export Data")
        self.app.pop_screen()
