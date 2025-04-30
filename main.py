import sublime
import sublime_plugin
import subprocess
import sys
import os
import json

class OpenSidebarTerminalCommand(sublime_plugin.TextCommand):
  def run(self, edit, profile_name="default"):
    settings = sublime.load_settings('OpenTerminal.sublime-settings')
    self.profile_name = profile_name

    self.preferred_emulator = settings.get('preferred_emulator')
    self.default_startup_directory = settings.get('default_startup_directory', "project")
    self.custom_startup_directory = settings.get('custom_startup_directory', "")
    self.terminal_profiles = settings.get('terminal_profiles', {})

    self.open_sidebar_terminal()

  def get_terminal_emulator(self):
    if self.preferred_emulator and os.path.exists(self.preferred_emulator):
      return self.preferred_emulator

    os_name = sys.platform

    if os_name == "darwin":  # macOS
      if os.path.exists("/Applications/iTerm.app/Contents/MacOS/iTerm"):
        return "/Applications/iTerm.app/Contents/MacOS/iTerm"
      else:
        return "/usr/bin/osascript"  # Fallback to AppleScript/Terminal
    elif os_name == "win32":  # Windows
      if os.path.exists("C:\\Program Files\\WindowsApps\\Microsoft.WindowsTerminal_*.exe"):
        import glob
        terminal_paths = glob.glob("C:\\Program Files\\WindowsApps\\Microsoft.WindowsTerminal_*.exe")
        if terminal_paths:
          return terminal_paths[0]
      else:
        return "cmd.exe"  # Fallback to cmd
    else:
      return "/bin/bash"  # Default to bash on other systems

  def get_startup_directory(self):
    if self.default_startup_directory == "current_file":
      view = sublime.active_window().active_view()
      if view:
        file_path = view.file_name()
        if file_path:
          return os.path.dirname(file_path)
    elif self.default_startup_directory == "custom":
      return self.custom_startup_directory
    else:  # "project"
      # Try to determine project directory
      project_file = sublime.active_window().project_file()
      if project_file:
        return os.path.dirname(project_file)
    return os.getcwd()

  def open_sidebar_terminal(self):
    emulator = self.get_terminal_emulator()
    startup_dir = self.get_startup_directory()
    profile = self.terminal_profiles.get(self.profile_name, self.terminal_profiles.get("default", {}))

    font = profile.get("font", "monospace")
    font_size = profile.get("font_size", 12)
    color_scheme = profile.get("color_scheme", "default")

    try:
      if emulator == "/usr/bin/osascript":
        command = [
          "osascript",
          "-e",
          f'tell application "Terminal" to do script "cd \'{startup_dir}\'"'
        ]
        subprocess.Popen(command)
      elif emulator == "cmd.exe":
        command = ["cmd.exe", "/k", f"cd /d {startup_dir}"]
        subprocess.Popen(command)
      elif emulator == "/bin/bash":
        command = ["/bin/bash", "-c", f"cd {startup_dir}"]
        subprocess.Popen(command)
      elif emulator.endswith(".exe"):  # Custom executable
        command = [emulator, "-c", f"cd {startup_dir}"]  # Adjust as needed
        subprocess.Popen(command)

      else:
        sublime.message_dialog(f"Unsupported terminal emulator: {emulator}")
        return

    except Exception as e:
      sublime.error_message(f"Error opening terminal: {e}")
