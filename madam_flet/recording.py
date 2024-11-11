import os
import re
from enum import Enum

from madam_flet.logger import Logger

logger = Logger.get_logger(__name__)


class RecordingType(Enum):
    UNSPECIFIED = 1
    PRI = 2
    BU = 3


class Recording:
    def __init__(self, root_dir: str, file_name: str, witness_name: str, recording_date: str):
        self.root_dir = root_dir
        self.file_name = file_name
        self.witness_name = witness_name
        self.recording_date = recording_date

        self.recording_type = self.__get_recording_type(file_name)
        self.recording_number = self.__get_recording_number(root_dir)
        if self.recording_type == RecordingType.PRI.name:
            self.mic_number = self.__get_mic_number(file_name)
        else:
            self.mic_number = ""

    @staticmethod
    def __get_recording_type(file_name) -> RecordingType:
        multiple_mic = re.search(r"(tr\d+)(\.wav)", file_name, re.IGNORECASE)

        if multiple_mic:
            return RecordingType.PRI.name

        return RecordingType.BU.name

    @staticmethod
    def __get_recording_number(root_dir) -> str:
        folder_name = os.path.basename(root_dir)
        recording_number = re.search(r"(?<!\d)0+(\d+)", folder_name)
        if recording_number:
            return recording_number.group(1)

        logger.exception("Could not find recording number: %s", folder_name)
        raise ValueError

    @staticmethod
    def __get_mic_number(file_name) -> str:
        mic_number = re.search(r"(tr\d+)(\.wav)", file_name, re.IGNORECASE)
        if mic_number:
            return mic_number.group(1)

        logger.exception("Could not find mic number: %s", file_name)
        raise ValueError

    def get_recording_name(self) -> str:
        attribute_order = [
            "witness_name",
            "recording_date",
            "recording_type",
            "recording_number",
            "mic_number",
        ]
        values = [getattr(self, attr) for attr in attribute_order if getattr(self, attr)]
        return "-".join(values)
