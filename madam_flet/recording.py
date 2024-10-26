import os
import re
from enum import Enum

from madam_flet.logger import Logger

logger = Logger.get_logger(__name__)


class RecordingType(Enum):
    PRI = 1
    BU = 2
    UNKOWNN = 3


class Recording:
    def __init__(self, root_dir: str, file_name: str, witness_name: str, recording_date: str):
        self.root_dir = root_dir
        self.file_name = file_name

        self.witness_name = witness_name
        self.recording_date = recording_date
        self.recording_type = self.__get_recording_type()
        self.recording_number = self.__get_recording_number()
        if self.recording_type == RecordingType.PRI.name:
            self.mic_number = self.__get_mic_number()
        else:
            self.mic_number = ""

    def __get_recording_type(self) -> RecordingType:
        multiple_mic = re.search(r"(tr\d+)(\.wav)", self.file_name, re.IGNORECASE)

        if multiple_mic:
            return RecordingType.PRI.name

        return RecordingType.BU.name

    def __get_recording_number(self) -> str:
        folder_name = os.path.basename(self.root_dir)
        recording_number = re.search(r"(?<!\d)0+(\d+)", folder_name)
        if recording_number:
            return recording_number.group(1)

        logger.exception("Could not find recording number: %s", folder_name)
        raise ValueError

    def __get_mic_number(self) -> str:
        mic_number = re.search(r"(tr\d+)(\.wav)", self.file_name, re.IGNORECASE)
        if mic_number:
            return mic_number.group(1)

        logger.exception("Could not find mic number: %s", self.file_name)
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
