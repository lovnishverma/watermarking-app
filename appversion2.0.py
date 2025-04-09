import os
import json
from tkinter import (
    Label, Button, filedialog, StringVar, OptionMenu,
    DoubleVar, Scale, Entry, Listbox, END, Checkbutton, BooleanVar, messagebox
)
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageEnhance

SETTINGS_FILE = "settings.json"

class WatermarkApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("AUSVIC Logo Watermarker")
        self.geometry("620x620")
        self.configure(padx=10, pady=10)

        self.image_paths = []
        self.logo_path = StringVar()
        self.output_dir = StringVar()
        self.position = StringVar(value="bottom-right")
        self.scale = DoubleVar(value=20)
        self.opacity = DoubleVar(value=100)
        self.repeat_logo = BooleanVar(value=False)

        self.load_settings()
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        Label(self, text="🎯 Drag & Drop Product Images Below or Click to Browse:").pack()
        self.image_listbox = Listbox(self, height=6, width=60, selectmode="multiple")
        self.image_listbox.pack(pady=5)
        self.image_listbox.drop_target_register(DND_FILES)
        self.image_listbox.dnd_bind("<<Drop>>", self.drop_files)

        Button(self, text="📂 Browse Images", command=self.browse_images).pack(pady=5)
        Button(self, text="❌ Remove Selected", command=self.remove_selected_images).pack(pady=2)

        Label(self, text="🖼 Drag & Drop AUSVIC Logo or Click to Browse:").pack()
        self.logo_entry = Entry(self, textvariable=self.logo_path, width=60)
        self.logo_entry.pack()
        self.logo_entry.drop_target_register(DND_FILES)
        self.logo_entry.dnd_bind("<<Drop>>", self.drop_logo)
        Button(self, text="📁 Browse Logo", command=self.browse_logo).pack(pady=5)

        Label(self, text="📤 Output Directory:").pack()
        Entry(self, textvariable=self.output_dir, width=60, state="readonly").pack()
        Button(self, text="📁 Choose Folder", command=self.browse_output_dir).pack(pady=5)

        Label(self, text="📌 Position:").pack()
        OptionMenu(self, self.position, "top-left", "top-right", "bottom-left", "bottom-right", "center").pack()

        Label(self, text="📏 Logo Size (% of image width):").pack()
        Scale(self, from_=5, to=100, orient="horizontal", variable=self.scale).pack()

        Label(self, text="🌫 Logo Opacity (%):").pack()
        Scale(self, from_=0, to=100, orient="horizontal", variable=self.opacity).pack()

        Checkbutton(self, text="🔁 Repeat logo across image", variable=self.repeat_logo).pack(pady=5)

        Button(self, text="✅ Apply AUSVIC Watermark to All", command=self.apply_batch_watermark).pack(pady=10)

    def drop_files(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                if file not in self.image_paths:
                    self.image_paths.append(file)
                    self.image_listbox.insert(END, os.path.basename(file))

    def drop_logo(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith(".png"):
                self.logo_path.set(file)

    def browse_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        for f in files:
            if f not in self.image_paths:
                self.image_paths.append(f)
                self.image_listbox.insert(END, os.path.basename(f))

    def remove_selected_images(self):
        selected_indices = list(self.image_listbox.curselection())
        if not selected_indices:
            messagebox.showinfo("No Selection", "Please select image(s) to remove.")
            return
        for i in reversed(selected_indices):
            self.image_listbox.delete(i)
            del self.image_paths[i]

    def browse_logo(self):
        file = filedialog.askopenfilename(filetypes=[("PNG Logo", "*.png")])
        if file:
            self.logo_path.set(file)

    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def apply_batch_watermark(self):
        logo_file = self.logo_path.get()
        output_folder = self.output_dir.get()

        if not self.image_paths:
            messagebox.showwarning("Missing Images", "Please add product images.")
            return
        if not logo_file:
            messagebox.showwarning("Missing Logo", "Please select the AUSVIC logo.")
            return
        if not output_folder:
            messagebox.showwarning("Missing Output Folder", "Please select an output directory.")
            return

        errors = []
        for img_path in self.image_paths:
            try:
                filename = os.path.basename(img_path)
                name, ext = os.path.splitext(filename)
                out_path = os.path.join(output_folder, name + "_watermarked.jpg")
                add_logo_watermark(
                    img_path,
                    logo_file,
                    out_path,
                    self.position.get(),
                    self.scale.get(),
                    self.opacity.get(),
                    self.repeat_logo.get()
                )
            except Exception as e:
                errors.append(f"{filename}: {str(e)}")

        if errors:
            messagebox.showerror("Partial Success", f"Some files failed:\n\n" + "\n".join(errors))
        else:
            messagebox.showinfo("Success", "✅ All images watermarked successfully!")

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                    self.logo_path.set(data.get("logo_path", ""))
                    self.output_dir.set(data.get("output_dir", ""))
                    self.position.set(data.get("position", "bottom-right"))
                    self.scale.set(data.get("scale", 20))
                    self.opacity.set(data.get("opacity", 100))
                    self.repeat_logo.set(data.get("repeat_logo", False))
            except Exception as e:
                messagebox.showerror("Error", f"⚠ Error loading settings: {e}")

    def save_settings(self):
        data = {
            "logo_path": self.logo_path.get(),
            "output_dir": self.output_dir.get(),
            "position": self.position.get(),
            "scale": self.scale.get(),
            "opacity": self.opacity.get(),
            "repeat_logo": self.repeat_logo.get()
        }
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"⚠ Error saving settings: {e}")

    def on_close(self):
        self.save_settings()
        self.destroy()


def add_logo_watermark(image_path, logo_path, output_path, position, scale_percent, opacity_percent, repeat_logo=False):
    base_image = Image.open(image_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    base_width, base_height = base_image.size
    logo_width = int((base_width * scale_percent) / 100)
    logo_aspect_ratio = logo.height / logo.width
    logo_height = int(logo_width * logo_aspect_ratio)
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    if opacity_percent < 100:
        alpha = logo.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity_percent / 100)
        logo.putalpha(alpha)

    watermarked = base_image.copy()

    if repeat_logo:
        for y in range(0, base_height, logo_height + 50):
            for x in range(0, base_width, logo_width + 50):
                watermarked.paste(logo, (x, y), logo)
    else:
        positions = {
            "top-left": (10, 10),
            "top-right": (base_width - logo_width - 10, 10),
            "bottom-left": (10, base_height - logo_height - 10),
            "bottom-right": (base_width - logo_width - 10, base_height - logo_height - 10),
            "center": ((base_width - logo_width) // 2, (base_height - logo_height) // 2)
        }
        pos = positions.get(position, positions["bottom-right"])
        watermarked.paste(logo, pos, logo)

    watermarked.convert("RGB").save(output_path)

if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
