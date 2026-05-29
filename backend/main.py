import os
import shutil
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt

# =========================
# FILE TYPES
# =========================
FILE_TYPES = {
    "Images": [".jpg", ".png", ".jpeg", ".gif"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Music": [".mp3", ".wav"],
    "Documents": [".pdf", ".txt", ".docx"],
    "Programs": [".exe", ".msi", ".zip"]
}

# =========================
# ANALYTICS GRAPH
# =========================
def show_graph(file_count):

    if not file_count:
        return

    labels = list(file_count.keys())
    values = list(file_count.values())

    plt.style.use("dark_background")
    plt.figure(figsize=(7, 4))

    colors = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"]

    plt.bar(labels, values, color=colors)

    plt.title("📊 File Organization Report")
    plt.xlabel("Categories")
    plt.ylabel("Files")

    plt.show()

# =========================
# ORGANIZE FILES (PRO VERSION)
# =========================
def organize_files():

    folder = filedialog.askdirectory()

    if not folder:
        return

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    total = len(files)

    if total == 0:
        messagebox.showinfo("Info", "No files found in this folder.")
        return

    progress["value"] = 0
    progress["maximum"] = total

    file_count = {}
    moved = 0

    for file in files:

        file_path = os.path.join(folder, file)

        placed = False

        for category, extensions in FILE_TYPES.items():

            if file.lower().endswith(tuple(extensions)):

                target_folder = os.path.join(folder, category)
                os.makedirs(target_folder, exist_ok=True)

                shutil.move(file_path, os.path.join(target_folder, file))

                file_count[category] = file_count.get(category, 0) + 1
                placed = True
                break

        if not placed:

            others = os.path.join(folder, "Others")
            os.makedirs(others, exist_ok=True)

            shutil.move(file_path, os.path.join(others, file))

            file_count["Others"] = file_count.get("Others", 0) + 1

        moved += 1
        progress["value"] = moved
        root.update_idletasks()

    status_label.config(
        text=f"✅ Organized {moved} files successfully!",
        fg="#10b981"
    )

    show_graph(file_count)

# =========================
# DUPLICATE FILE DETECTOR
# =========================
def find_duplicates():

    folder = filedialog.askdirectory()

    if not folder:
        return

    hashes = {}
    duplicates = []

    for root_dir, dirs, files in os.walk(folder):

        for file in files:

            path = os.path.join(root_dir, file)

            try:
                with open(path, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()

                if file_hash in hashes:
                    duplicates.append(path)
                else:
                    hashes[file_hash] = path

            except:
                pass

    if duplicates:
        messagebox.showinfo(
            "Duplicates Found",
            "\n\n".join(duplicates)
        )
    else:
        messagebox.showinfo(
            "Result",
            "✅ No duplicate files found!"
        )

# =========================
# SMART SUGGESTION
# =========================
def suggest():

    folder = filedialog.askdirectory()

    if not folder:
        return

    files = os.listdir(folder)

    images = len([f for f in files if f.endswith((".jpg", ".png", ".jpeg"))])
    videos = len([f for f in files if f.endswith((".mp4", ".mkv"))])

    if images > 20:
        messagebox.showinfo("Suggestion", "📸 You have many images. Organizing is recommended!")

    elif videos > 10:
        messagebox.showinfo("Suggestion", "🎥 You have many videos. Clean up space!")

    else:
        messagebox.showinfo("Suggestion", "✨ Your folder looks clean!")

# =========================
# GUI SETUP
# =========================
root = tk.Tk()
root.title("Smart File Organizer PRO+")
root.geometry("650x550")
root.config(bg="#0f172a")

# Title
title = tk.Label(
    root,
    text="📂 Smart File Organizer PRO+",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#0f172a"
)
title.pack(pady=20)

# Buttons
tk.Button(
    root,
    text="📁 Organize Folder",
    command=organize_files,
    bg="#3b82f6",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=5
).pack(pady=10)

tk.Button(
    root,
    text="🔍 Find Duplicates",
    command=find_duplicates,
    bg="#8b5cf6",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=5
).pack(pady=10)

tk.Button(
    root,
    text="💡 Smart Suggestion",
    command=suggest,
    bg="#10b981",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=5
).pack(pady=10)

# Progress Bar
progress = ttk.Progressbar(root, orient="horizontal", length=450, mode="determinate")
progress.pack(pady=20)

# Status Label
status_label = tk.Label(
    root,
    text="Waiting for action...",
    fg="orange",
    bg="#0f172a",
    font=("Arial", 11, "bold")
)
status_label.pack(pady=10)

# Footer
footer = tk.Label(
    root,
    text="Made with Python ❤️",
    fg="gray",
    bg="#0f172a"
)
footer.pack(side="bottom", pady=20)

# Run app
root.mainloop()