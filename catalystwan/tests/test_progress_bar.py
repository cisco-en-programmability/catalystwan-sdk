# Copyright 2024 Cisco Systems, Inc. and its affiliates

import io
import unittest
from unittest.mock import MagicMock

from catalystwan.utils.progress_bar import ProgressBar
from catalystwan.utils.upgrades_helper import SoftwarePackageUploadPayload


class TestProgressBar(unittest.TestCase):
    def test_progress_bar_output(self):
        stream = io.StringIO()
        bar = ProgressBar(label="Uploading: ", width=20, hide=False, expected_size=100, stream=stream)
        bar.show(50)
        output = stream.getvalue()
        self.assertIn("Uploading:", output)
        self.assertIn("50/100", output)

    def test_progress_bar_done(self):
        stream = io.StringIO()
        bar = ProgressBar(width=10, hide=False, expected_size=10, stream=stream)
        bar.show(10)
        bar.done()
        output = stream.getvalue()
        self.assertIn("10/10", output)

    def test_progress_bar_context_manager(self):
        stream = io.StringIO()
        with ProgressBar(width=10, hide=False, expected_size=10, stream=stream) as bar:
            bar.show(5)
        output = stream.getvalue()
        self.assertIn("5/10", output)

    def test_progress_bar_hidden(self):
        stream = io.StringIO()
        bar = ProgressBar(hide=True, expected_size=100, stream=stream)
        bar.show(50)
        bar.done()
        self.assertEqual(stream.getvalue(), "")

    def test_format_time(self):
        self.assertEqual(ProgressBar.format_time(0), "00:00:00")
        self.assertEqual(ProgressBar.format_time(3665), "01:01:05")

    def test_missing_expected_size_raises(self):
        bar = ProgressBar(hide=True)
        with self.assertRaises(ValueError):
            bar.show(10)

    def test_software_package_upload_callback(self):
        mock_encoder = MagicMock()
        mock_encoder._calculate_length.return_value = 1000
        mock_monitor = MagicMock()
        mock_monitor.bytes_read = 500

        callback = SoftwarePackageUploadPayload._create_callback(None, mock_encoder)
        # Calling callback updates progress
        callback(mock_monitor)
