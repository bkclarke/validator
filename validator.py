import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from ttkthemes import ThemedTk
import fnmatch

class FileCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Package Validator")
        self.root.geometry("900x700")
        self.root.set_theme("breeze")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            try:
                icon_image = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon_image)
            except Exception as e:
                print(f"Failed to set icon: {e}")
        else:
            print("Icon file not found, continuing without custom icon.")

        self.config_path = ""
        self.folder_path = ""
        self.last_config_file = os.path.join(os.path.expanduser("~"), ".last_config_path.txt")

        self.notebook = ttk.Notebook(self.root)
        self.compare_tab = ttk.Frame(self.notebook)
        self.edit_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.compare_tab, text="🔍 Compare Files")
        self.notebook.add(self.edit_tab, text="📄 View Config")
        self.notebook.pack(expand=1, fill="both", padx=10, pady=10)

        self.create_compare_tab()
        self.create_edit_tab()
        self.try_load_last_config()

    def create_compare_tab(self):
        top_frame = ttk.Frame(self.compare_tab)
        top_frame.pack(pady=10)

        ttk.Button(top_frame, text="📂 Load Config File", command=self.load_config_file).grid(row=0, column=0, padx=2)
        ttk.Button(top_frame, text="📁 Select Folder", command=self.select_folder).grid(row=0, column=1, padx=2)
        ttk.Button(top_frame, text="🔄 Compare", command=self.compare_files).grid(row=0, column=2, padx=2)

        self.config_label = ttk.Label(self.compare_tab, text="No config file selected", foreground="#0066cc", wraplength=800)
        self.config_label.pack(pady=5)

        self.folder_label = ttk.Label(self.compare_tab, text="No folder selected", foreground="#339966", wraplength=800)
        self.folder_label.pack(pady=5)

        self.output = scrolledtext.ScrolledText(
            self.compare_tab,
            wrap=tk.WORD,
            width=100,
            height=30,
            font=("Consolas", 10),
            state="disabled"  # Make it read-only
        )
        self.output.pack(padx=10, pady=10)

    def create_edit_tab(self):
        top_frame = ttk.Frame(self.edit_tab)
        top_frame.pack(pady=10)

        ttk.Button(top_frame, text="📂 Load Config File", command=self.load_config_file).grid(row=0, column=0, padx=2)
        # Remove the Save Changes button
        # ttk.Button(top_frame, text="💾 Save Changes", command=self.save_config_edits).grid(row=0, column=1, padx=2)

        self.editor = scrolledtext.ScrolledText(
            self.edit_tab,
            wrap=tk.WORD,
            width=100,
            height=35,
            font=("Consolas", 10),
            state="disabled"  # Make it read-only
        )
        self.editor.pack(padx=5, pady=5)

    def load_config_file(self):
        path = filedialog.askopenfilename(title="Select Configuration File", filetypes=[("Text Files", "*.txt")])
        if path:
            self.config_path = path
            self.config_label.config(text=f"📄 Config File: {path}")
            self.folder_label.config(text="")
            self.load_config_into_editor()
            try:
                with open(self.last_config_file, 'w') as f:
                    f.write(self.config_path)
            except Exception as e:
                print(f"Warning: Failed to save last config path: {e}")

    def try_load_last_config(self):
        if os.path.exists(self.last_config_file):
            try:
                with open(self.last_config_file, 'r') as f:
                    last_path = f.read().strip()
                if os.path.exists(last_path):
                    self.config_path = last_path
                    self.config_label.config(text=f"📄 Config File: {last_path}")
                    self.load_config_into_editor()
            except Exception as e:
                print(f"Warning: Failed to load last config path: {e}")

    def load_config_into_editor(self):
        if not self.config_path:
            return
        with open(self.config_path, 'r') as f:
            content = f.read()
            self.editor.config(state="normal")
            self.editor.delete(1.0, tk.END)
            self.editor.insert(tk.END, content)
            self.editor.config(state="disabled")

    def select_folder(self):
        path = filedialog.askdirectory(title="Select Folder to Check")
        if path:
            self.folder_path = path
            self.folder_label.config(text=f"📁 Folder: {path}")

    def compare_files(self):
        self.output.config(state="normal")
        self.output.delete(1.0, tk.END)

        if not self.config_path or not self.folder_path:
            messagebox.showerror("Error", "Please load a config file and select a folder.")
            self.output.config(state="disabled")
            return

        expected_files = set()
        forbidden_items = set()
        ignore_dirs = set()
        pass_dirs = set()
        forbidden_extensions = set()
        warn_missing_dirs = set()
        current_section = None

        with open(self.config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    if "# --- FILES" in line:
                        current_section = "FILES"
                    elif "# --- FORBIDDEN" in line:
                        current_section = "FORBIDDEN"
                    elif "# --- IGNORE" in line:
                        current_section = "IGNORE"
                    elif "# --- PASS" in line:
                        current_section = "PASS"
                    elif "# --- EXTENSIONS" in line:
                        current_section = "EXTENSIONS"
                    elif "# --- WARN_MISSING_DIRS" in line:
                        current_section = "WARN_MISSING_DIRS"
                    continue
                if not line:
                    continue
                if current_section == "FILES":
                    expected_files.add(line.replace("\\", "/"))
                elif current_section == "FORBIDDEN":
                    forbidden_items.add(line)
                elif current_section == "IGNORE":
                    ignore_dirs.add(line.rstrip("/\\") + "/")
                elif current_section == "PASS":
                    pass_dirs.add(line.rstrip("/\\") + "/")
                elif current_section == "EXTENSIONS":
                    forbidden_extensions.add(line.strip())
                elif current_section == "WARN_MISSING_DIRS":
                    warn_missing_dirs.add(line.rstrip("/\\") + "/")

        # Identify missing dirs before walking
        missing_dirs = {
            dir for dir in warn_missing_dirs
            if not os.path.isdir(os.path.join(self.folder_path, dir))
        }

        def is_under_missing_dir(path):
            return any(path.startswith(missing) for missing in missing_dirs)

        # Filter expected files
        def is_under_pass_dir(path):
            return any(path.startswith(p) for p in pass_dirs)

        filtered_expected_files = {
            f for f in expected_files
            if not is_under_missing_dir(f) and not is_under_pass_dir(f)
        }
        
        actual_files = set()
        forbidden_violations = []
        extension_violations = []
        all_actual_files = set()
        empty_dirs = []
        zero_kb_files = []

        for dirpath, dirnames, filenames in os.walk(self.folder_path):
            rel_dir = os.path.relpath(dirpath, self.folder_path).replace("\\", "/")
            rel_dir_with_slash = rel_dir + "/" if rel_dir != "." else ""

            if any(rel_dir_with_slash == ignored or rel_dir_with_slash.startswith(ignored) for ignored in ignore_dirs):
                continue

            is_ignored_or_passed = any(rel_dir_with_slash.startswith(d) for d in ignore_dirs | pass_dirs)
            compare_files = not any(rel_dir_with_slash.startswith(p) for p in pass_dirs)

            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(dirpath, filename), self.folder_path).replace("\\", "/")
                full_path = os.path.join(self.folder_path, rel_path)

                # ✅ Always check for 0 KB files
                try:
                    if os.path.getsize(full_path) == 0:
                        zero_kb_files.append(rel_path)
                except Exception as e:
                    print(f"Error checking size of {full_path}: {e}")

                if is_under_missing_dir(rel_path):
                    continue

                if compare_files:
                    if any(forbidden in filename for forbidden in forbidden_items):
                        forbidden_violations.append((rel_path, [f for f in forbidden_items if f in filename]))

                    if any(fnmatch.fnmatch(rel_path, expected) for expected in filtered_expected_files):
                        actual_files.add(rel_path)

                    if any(filename.endswith(ext) for ext in forbidden_extensions):
                        extension_violations.append((rel_path, [ext for ext in forbidden_extensions if filename.endswith(ext)]))

                # ✅ This must come last, and not be skipped if 0 KB check is needed
                if not is_ignored_or_passed:
                    all_actual_files.add(rel_path)


            if not filenames and not dirnames and not is_ignored_or_passed:
                empty_dirs.append(rel_dir)

        matched_expected = set()
        for expected in filtered_expected_files:
            if any(fnmatch.fnmatch(actual, expected) for actual in actual_files):
                matched_expected.add(expected)

        missing_files = filtered_expected_files - matched_expected
        unexpected_files = all_actual_files - actual_files

        if not missing_files and not unexpected_files and not forbidden_violations and not extension_violations and not empty_dirs:
            self.output.insert(tk.END, "✅ All expected files are present. No forbidden terms, forbidden extensions, or empty folders found.\n")
        else:
            if missing_files:
                self.output.insert(tk.END, "❌ Missing Files:\n")
                for file in sorted(missing_files):
                    self.output.insert(tk.END, f"  - {file}\n")

            if unexpected_files:
                self.output.insert(tk.END, "\n⚠️ Extra/Unexpected Files:\n")
                for file in sorted(unexpected_files):
                    self.output.insert(tk.END, f"  - {file}\n")

            if forbidden_violations:
                self.output.insert(tk.END, "\n🚫 Forbidden Terms Found in Filenames:\n")
                for file, terms in forbidden_violations:
                    for term in terms:
                        self.output.insert(tk.END, f"  - {file} (contains '{term}')\n")

            if extension_violations:
                self.output.insert(tk.END, "\n🚫 Forbidden Extensions Found:\n")
                for file, exts in extension_violations:
                    for ext in exts:
                        self.output.insert(tk.END, f"  - {file} (ends with '{ext}')\n")

            if zero_kb_files:
                self.output.insert(tk.END, "\n🕳️ Empty (0 KB) Files Found:\n")
                for file in sorted(zero_kb_files):
                    self.output.insert(tk.END, f"  - {file}\n")

            if empty_dirs:
                self.output.insert(tk.END, "\n📁 Empty Directories Found:\n")
                for d in sorted(empty_dirs):
                    self.output.insert(tk.END, f"  - {d}\n")

        if missing_dirs:
            self.output.insert(tk.END, "\n⚠️ Warning: Missing Directories:\n")
            for d in sorted(missing_dirs):
                self.output.insert(tk.END, f"  - {d}\n")

        # Identify all actual directories (relative paths with trailing slash)
        all_actual_dirs = set()
        for dirpath, dirnames, _ in os.walk(self.folder_path):
            rel_dir = os.path.relpath(dirpath, self.folder_path).replace("\\", "/")
            rel_dir_with_slash = rel_dir + "/" if rel_dir != "." else ""
            if rel_dir_with_slash:
                all_actual_dirs.add(rel_dir_with_slash)

        # Remove ignored and pass-through dirs from consideration
        filtered_actual_dirs = {
            d for d in all_actual_dirs
            if not any(d.startswith(ignored) for ignored in ignore_dirs | pass_dirs)
        }

        # Unexpected = any present dir not in WARN_MISSING_DIRS
        unexpected_dirs = filtered_actual_dirs - warn_missing_dirs

        if unexpected_dirs:
            self.output.insert(tk.END, "\n🚨 Unexpected Directories Found: \n")
            for d in sorted(unexpected_dirs):
                self.output.insert(tk.END, f"  - {d}\n")

        self.output.config(state="disabled")

    def save_config_edits(self):
        if not self.config_path:
            messagebox.showerror("Error", "No config file loaded.")
            return

        content = self.editor.get(1.0, tk.END).strip()

        try:
            with open(self.config_path, 'w') as f:
                f.write(content)
            messagebox.showinfo("Saved", "Config file saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{str(e)}")

if __name__ == "__main__":
    root = ThemedTk(theme="aquativo")
    app = FileCheckerApp(root)
    root.mainloop()

