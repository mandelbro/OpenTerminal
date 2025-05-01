# import sublime
# import sublime_plugin
# import os
# from .panel import TerminalPanel
# print("OpenTerminal plugin loaded")

# class OpenTerminalCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         print("OpenTerminal plugin running")
#         # Get project root
#         window = self.view.window()
#         if not window:
#             return
#         folders = window.folders()
#         if not folders:
#             return
#         project_root = folders[0]

#         # Create terminal panel
#         TerminalPanel.create(window, project_root)

# class OpenTerminalListener(sublime_plugin.EventListener):
#     def on_window_command(self, window, command_name, args):
#         if command_name == "open_terminal":
#             print("OpenTerminal plugin listening")
#             # Handle custom logic here if needed
#             pass
