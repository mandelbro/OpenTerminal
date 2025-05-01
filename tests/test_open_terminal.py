import unittest
from unittest.mock import patch, MagicMock
import os
import subprocess

# Import modules from your plugin
from .main import OpenTerminalCommand, OpenTerminalListener
from .panel import TerminalPanel

class TestOpenTerminalCommand(unittest.TestCase):
    """Test the OpenTerminalCommand class."""

    @patch('sublime_plugin.TextCommand')
    def setUp(self, mock_text_command):
        self.view = MagicMock()
        self.window = MagicMock()
        self.command = OpenTerminalCommand(self.view)

    def test_run_method_opens_terminal_panel(self):
        """Test that pressing Ctrl + Shift + T opens the terminal panel."""
        # Simulate a window with folders
        self.window.folders.return_value = ['/project_root']
        self.view.window.return_value = self.window

        # Run the command
        self.command.run(MagicMock())

        # Verify that the terminal panel was created
        self.window.create_output_panel.assert_called_once_with("terminal")

    def test_set_working_directory(self):
        """Test that the working directory is set to the project root."""
        # Simulate a window with folders
        self.window.folders.return_value = ['/project_root']
        self.view.window.return_value = self.window

        # Run the command
        self.command.run(MagicMock())

        # Verify that the correct directory was set
        self.assertEqual(
            TerminalPanel.set_working_directory.call_args[0][1],
            '/project_root'
        )

class TestTerminalPanel(unittest.TestCase):
    """Test the TerminalPanel class."""

    def setUp(self):
        self.panel = TerminalPanel()
        self.window = MagicMock()

    @patch('os.path.isdir')
    def test_set_working_directory_valid(self, mock_isdir):
        """Test that the working directory is set correctly."""
        mock_isdir.return_value = True
        self.panel.set_working_directory(self.window, '/project_root')

        # Verify that the correct command was executed
        self.window.run_command.assert_called_once_with(
            'set_working_dir',
            {'directory': '/project_root'}
        )

    @patch('os.path.isdir')
    def test_set_working_directory_invalid(self, mock_isdir):
        """Test that an invalid directory raises an error."""
        mock_isdir.return_value = False
        with self.assertRaises(ValueError):
            self.panel.set_working_directory(self.window, '/invalid_path')

class TestPlatformSpecific(unittest.TestCase):
    """Test platform-specific functionality."""

    @patch('platform.system')
    def test_iTerm2_command_macOS(self, mock_platform):
        """Test that the correct iTerm2 command is used on macOS."""
        mock_platform.return_value = 'Darwin'

        # Run the command
        TerminalPanel.open_terminal_in_iterm2('/project_root')

        # Verify that the correct subprocess call was made
        subprocess.run.assert_called_once_with(
            ['open', '-a', 'iTerm', '/project_root'],
            check=True
        )

if __name__ == '__main__':
    unittest.main()
