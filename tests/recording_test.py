from madam_flet.recording import Recording


def test_rename_files():
    # Arrange
    test_witness_name = "Doe_J"
    test_recording_date = "010124"
    test_file_names = [
        "ZOOM0001_Tr4.WAV",
        "ZOOM0002_Tr3.WAV",
        "ZOOM0003_Tr22.WAV",
        "ZOOM0004_Tr1.WAV",
        "ZOOM0005_Tr1.WAV",
        "ZOOM0006_Tr2.WAV",
        "ZOOM0007_Tr3.WAV",
        "ZOOM00018_Tr4.WAV",
    ]

    expected_file_names = [
        f"{test_witness_name}-{test_recording_date}-PRI-1-Tr4",
        f"{test_witness_name}-{test_recording_date}-PRI-2-Tr3",
        f"{test_witness_name}-{test_recording_date}-PRI-3-Tr22",
        f"{test_witness_name}-{test_recording_date}-PRI-4-Tr1",
        f"{test_witness_name}-{test_recording_date}-PRI-5-Tr1",
        f"{test_witness_name}-{test_recording_date}-PRI-6-Tr2",
        f"{test_witness_name}-{test_recording_date}-PRI-7-Tr3",
        f"{test_witness_name}-{test_recording_date}-PRI-18-Tr4",
    ]

    for i in range(len(test_file_names)):
        # Act
        recording = Recording(
            test_file_names[i],
            test_witness_name,
            test_recording_date,
        )

        # Assert
        assert recording.get_recording_name() == expected_file_names[i]
