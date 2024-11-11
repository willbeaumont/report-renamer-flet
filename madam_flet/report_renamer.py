import datetime
import os
import shutil

from madam_flet.logger import Logger
from madam_flet.recording import Recording

logger = Logger.get_logger(__name__)


class ReportRenamer:
    def __init__(self, witness_name, source_dir, destination_dir="", file_type=".WAV"):
        self.witness_name = witness_name
        self.source_dir = source_dir
        self.file_type = file_type
        self.recording_date = self.__get_recording_date()
        self.destination_dir = self.__get_destination_dir(destination_dir)
        self.__init_destination_dir()

        self.recordings = self.__get_recordings()
        self.number_of_recordings = len(self.recordings)

    def short_destination(self):
        home_dir = os.path.expanduser("~")
        return self.destination_dir.replace(home_dir, "~")

    def __get_destination_dir(self, destination, default_prefix="renamed_recordings"):
        if not destination:
            parent_dir = os.path.dirname(self.source_dir)
            return os.path.join(parent_dir, f"{default_prefix}_{self.recording_date}")

        return destination

    def __init_destination_dir(self):
        if not os.path.isdir(self.destination_dir):
            os.makedirs(self.destination_dir)
            logger.info("Destination directory not found, created: %s", self.short_destination())

    def __get_recordings(self):
        recordings = []
        for root, dirs, files in os.walk(self.source_dir):
            if files and not dirs:
                recordings.extend(
                    [
                        Recording(
                            root_dir=root,
                            file_name=file,
                            witness_name=self.witness_name,
                            recording_date=self.recording_date,
                        )
                        for file in files
                        if file.endswith(self.file_type)
                    ]
                )

        return recordings

    def move_recording(self, recording: Recording):
        source_path = os.path.join(recording.root_dir, recording.file_name)

        new_file_name = recording.get_recording_name() + self.file_type
        destination_path = os.path.join(self.destination_dir, new_file_name)

        shutil.copy(source_path, destination_path)

        logger.info(
            "Moved %s to %s",
            source_path[len(recording.root_dir) + 1 :],
            destination_path[len(self.destination_dir) + 1 :],
        )

    @staticmethod
    def __get_recording_date() -> str:
        # get the system date
        return datetime.datetime.now().strftime("%m%d%y")  # noqa: DTZ005
