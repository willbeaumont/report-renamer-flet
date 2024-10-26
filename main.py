import os
import time

import flet as ft

from madam_flet.logger import Logger
from madam_flet.report_renamer import ReportRenamer

logger = Logger.get_logger(__name__)

WITNESS_FIELD_LABEL = "Enter the witness name (LastName_FirstInitial)"
SELECT_FOLDER_LABEL = "Select source folder"
SELECT_FOLDER_DEFAULT = "No source folder selected..."
SELECT_FOLDER_BUTTON = "Open Folder"
MOVE_FILES_BUTTON = "Move Recordings"


class MadamCourtReporter(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        # state
        self.page = page
        self.status = ft.TextField(label="Status", read_only=True, value=" ")
        self.destination_dir = ""
        self.progress_ring = ft.ProgressRing(width=16, height=16, stroke_width=2)
        self.progress_row = ft.Row(
            [
                self.progress_ring,
                ft.Text("Moving files..."),
            ],
            visible=False,
        )

        # input
        self.witness = ft.TextField(label=WITNESS_FIELD_LABEL)
        self.source_dir = ft.TextField(
            label=SELECT_FOLDER_LABEL,
            read_only=True,
            value=SELECT_FOLDER_DEFAULT,
        )

        # actions
        self.file_picker = self.__init_file_picker()
        self.source_dir_button = ft.ElevatedButton(SELECT_FOLDER_BUTTON, on_click=self.file_picker.get_directory_path)
        self.move_files_button = ft.ElevatedButton(MOVE_FILES_BUTTON, on_click=self.__move_files)

        # layout
        self.content = ft.Column(
            controls=[
                self.__container(args=[self.witness]),
                self.__container(args=[self.source_dir, self.source_dir_button]),
                self.__container(
                    args=[
                        self.status,
                        self.progress_row,
                        self.move_files_button,
                    ],
                    height=140,
                ),
            ],
        )

    def __init_file_picker(self) -> ft.FilePicker:
        file_picker = ft.FilePicker(on_result=lambda e: self.__on_dialog_result(e, text_field=self.source_dir))
        self.page.overlay.append(file_picker)
        return file_picker

    def __toggle_loading_visibility(self) -> None:
        self.move_files_button.visible = not self.move_files_button.visible
        self.progress_row.visible = not self.progress_row.visible
        self.page.update()

    def __on_dialog_result(self, e: ft.FilePickerResultEvent, text_field: ft.TextField):
        if e.path:
            text_field.value = os.path.realpath(e.path)
            self.page.update()

    def __get_name(self) -> str:
        if self.witness.value == "":
            self.__update_status("Please enter a witness name.", ft.colors.RED)
            return ""
        return self.witness.value

    def __get_source_dir(self) -> str:
        if self.source_dir.value == SELECT_FOLDER_DEFAULT:
            msg = "Please select a valid source folder."

            # append error message if status value exists
            if self.status.value:
                status_without_period = self.status.value[:-1]
                msg_without_please = msg[7:]
                self.__update_status(f"{status_without_period} and {msg_without_please}", ft.colors.RED)
            else:
                self.__update_status(msg, ft.colors.RED)

            return ""
        return self.source_dir.value

    def __update_status(self, message: str, color: str = "") -> None:
        self.status.value = message
        if color:
            self.status.color = color
        self.page.update()

    def __update_progress_ring(self, report_renamer: ReportRenamer, progress: int) -> None:
        self.progress_ring.value = (progress + 1) / report_renamer.number_of_recordings
        self.__update_status(f"{int(progress * 100 / report_renamer.number_of_recordings)}% complete...")

    def __move_files(self, _):
        self.__update_status("")
        witness_name = self.__get_name()
        source_dir = self.__get_source_dir()

        if witness_name and source_dir:
            try:
                renamer = ReportRenamer(witness_name, source_dir)
                self.__toggle_loading_visibility()

                self.__update_status("0% complete...", ft.colors.GREEN)
                for index, recording in enumerate(renamer.recordings):
                    renamer.move_recording(recording)
                    self.__update_progress_ring(renamer, index)

                self.__update_status("Recordings moved successfully!")
                self.__toggle_loading_visibility()

                time.sleep(2)
                self.__update_status(f"Saved here: {renamer.short_destination()}")

            except Exception:
                self.__update_status("Error moving recordings...")
                logger.exception("Error occurred in __move_files")

    def __container(self, args, height=None):
        return ft.Container(
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=10,
            padding=15,
            content=ft.Column(
                spacing=20,
                controls=[*args],
            ),
            height=height,
        )


def main(page: ft.Page):
    page.title = "Madam Court Reporter"
    page.window.height = 420
    page.add(MadamCourtReporter(page))


ft.app(main)
