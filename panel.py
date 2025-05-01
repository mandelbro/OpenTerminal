# import sublime
# import os

# class TerminalPanel:
#     @classmethod
#     def create(cls, window, project_root):
#         # Create a new panel below the main view
#         panel = window.create_output_panel("terminal")

#         # Set the working directory to the project root
#         cls.set_working_directory(panel, project_root)

#         # Launch terminal (specifically for macOS and iTerm2)
#         if os.name == 'posix':
#             import subprocess
#             subprocess.Popen(['osascript', '-e',
#                 f'tell application "iTerm" to create new session in current window with command "{project_root}"'])

#     @staticmethod
#     def set_working_directory(panel, directory):
#         # Set the working directory for the terminal panel
#         if os.path.isdir(directory):
#             panel.run_command("write_to_panel", {"text": f"cd {directory}\n"})
