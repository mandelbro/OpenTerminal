import sublime
import sublime_plugin
import sys
import os
import subprocess
print("OpenTerminal plugin loaded")
print(sys.version_info)

class OpenTerminalCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("OpenTerminal plugin running")
        self.show_panel()

    def show_panel(self):
        items = [
            ("Open in Project Directory", "open_project"),
            ("Open in Custom Directory...", "open_custom")
        ]
        self.window = sublime.active_window()
        self.window.show_quick_panel(items, self.on_panel_selected, sublime.MONOSPACE_FONT)

    def on_panel_selected(self, selected_index):
        if selected_index == 0:
            project_path = self.get_project_path()
            if project_path:
                self.open_iterm2(project_path, "") # Empty string for default profile
        elif selected_index == 1:
            self.show_directory_dialog()

    def show_directory_dialog(self):
        self.window.show_input_panel(
            "Enter Directory Path:",
            "",
            self.on_directory_entered,
            None,
            None
        )

    def on_directory_entered(self, directory_path):
        if directory_path:
            # Validate directory exists
            if os.path.isdir(directory_path):
                self.open_iterm2(directory_path, "")
            else:
                sublime.message_dialog("Invalid directory path.")

    def get_project_path(self):
        window = sublime.active_window()
        if not window:
            return None
        # AI: this code is currently broken

        project_file = window.project_file_for_path(window.active_view().path())
        if not project_file:
            return None  # No project open

        print("OpenTerminal project_path {}".format(os.path.dirname(project_file)))

        return os.path.dirname(project_file)
        # please determine the best way to get the project root path. AI!

    def open_iterm2(self, project_path, iterm_profile):
        try:
            command = ['open', '-a', 'iTerm2', '-d', project_path]

            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            sublime.message_dialog("Error opening iTerm2: " + str(e))
        except FileNotFoundError:
            sublime.message_dialog("iTerm2 not found. Please ensure it is installed and in your PATH.")
