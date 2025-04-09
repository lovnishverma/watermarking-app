import os
import json
from PIL import Image, ImageTk, ImageEnhance
from tkinter import (
    Label, Button, filedialog, StringVar, OptionMenu, Frame,
    DoubleVar, Scale, Entry, Listbox, END, Checkbutton, BooleanVar,
    messagebox, LabelFrame, Toplevel
)
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk

SETTINGS_FILE = "settings.json"

class WatermarkApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("🖋 AUSVIC Logo Watermarker")
        self.geometry("650x700")
        self.configure(padx=10, pady=10)

        # Variables
        self.image_paths = []
        self.logo_path = StringVar()
        self.output_dir = StringVar()
        self.position = StringVar(value="bottom-right")
        self.scale = DoubleVar(value=20)
        self.opacity = DoubleVar(value=100)
        self.repeat_logo = BooleanVar(value=False)

        # Load saved preferences
        self.load_settings()
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # === Preview Button ===
        Button(self, text="🔍 Preview Watermark", command=self.preview_watermark).pack(pady=5)

        # === Image Frame ===
        image_frame = LabelFrame(self, text="📸 Product Images")
        image_frame.pack(fill="x", pady=5)

        Label(image_frame, text="🎯 Drag & Drop Images or Click to Browse:").pack()
        self.image_listbox = Listbox(image_frame, height=6, width=60, selectmode="multiple")
        self.image_listbox.pack(pady=5)
        self.image_listbox.drop_target_register(DND_FILES)
        self.image_listbox.dnd_bind("<<Drop>>", self.drop_files)

        btn_frame = Frame(image_frame)
        btn_frame.pack()
        Button(btn_frame, text="📂 Browse Images", command=self.browse_images).pack(side="left", padx=5)
        Button(btn_frame, text="❌ Remove Selected", command=self.remove_selected_images).pack(side="left")

        # === Logo Frame ===
        logo_frame = LabelFrame(self, text="🖼 AUSVIC Logo")
        logo_frame.pack(fill="x", pady=10)

        Label(logo_frame, text="Drag & Drop PNG Logo or Click to Browse:").pack()
        self.logo_entry = Entry(logo_frame, textvariable=self.logo_path, width=60)
        self.logo_entry.pack()
        self.logo_entry.drop_target_register(DND_FILES)
        self.logo_entry.dnd_bind("<<Drop>>", self.drop_logo)
        Button(logo_frame, text="📁 Browse Logo", command=self.browse_logo).pack(pady=5)

        # === Output Directory ===
        output_frame = LabelFrame(self, text="📤 Output Directory")
        output_frame.pack(fill="x", pady=10)

        Entry(output_frame, textvariable=self.output_dir, width=60, state="readonly").pack(pady=2)
        Button(output_frame, text="📁 Choose Folder", command=self.browse_output_dir).pack()

        # === Settings Frame ===
        settings_frame = LabelFrame(self, text="⚙️ Watermark Settings")
        settings_frame.pack(fill="x", pady=10)

        Label(settings_frame, text="📌 Position:").pack()
        OptionMenu(settings_frame, self.position, "top-left", "top-right", "bottom-left", "bottom-right", "center").pack()

        Label(settings_frame, text="📏 Logo Size (% of image width):").pack()
        Scale(settings_frame, from_=5, to=100, orient="horizontal", variable=self.scale).pack()

        Label(settings_frame, text="🌫 Logo Opacity (%):").pack()
        Scale(settings_frame, from_=0, to=100, orient="horizontal", variable=self.opacity).pack()

        Checkbutton(settings_frame, text="🔁 Repeat logo across image", variable=self.repeat_logo).pack(pady=5)

        # === Progress Bar ===
        self.progress = ttk.Progressbar(self, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=5)

        # === Final Button ===
        Button(self, text="✅ Apply AUSVIC Watermark to All", command=self.apply_batch_watermark).pack(pady=10)

    def browse_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        for f in files:
            if f not in self.image_paths:
                self.image_paths.append(f)
                self.image_listbox.insert(END, os.path.basename(f))

    def remove_selected_images(self):
        selected = list(self.image_listbox.curselection())
        if not selected:
            messagebox.showinfo("No Selection", "Please select image(s) to remove.")
            return
        for i in reversed(selected):
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

    def preview_watermark(self):
        if not self.image_paths:
            messagebox.showwarning("No Images", "Please add at least one image to preview.")
            return
        if not self.logo_path.get():
            messagebox.showwarning("Missing Logo", "Please select the AUSVIC logo.")
            return

        try:
            img = self.get_preview_image(
                self.image_paths[0],
                self.logo_path.get(),
                self.position.get(),
                self.scale.get(),
                self.opacity.get(),
                self.repeat_logo.get()
            )
            self.show_preview_window(img)
        except Exception as e:
            messagebox.showerror("Preview Error", f"Failed to preview watermark:\n{e}")

    def get_preview_image(self, image_path, logo_path, position, scale_percent, opacity_percent, repeat_logo):
        base_image = Image.open(image_path).convert("RGBA")
        logo = Image.open(logo_path).convert("RGBA")

        base_width, base_height = base_image.size
        logo_width = int((base_width * scale_percent) / 100)
        logo_aspect = logo.height / logo.width
        logo_height = int(logo_width * logo_aspect)
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

        if opacity_percent < 100:
            alpha = logo.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity_percent / 100)
            logo.putalpha(alpha)

        result = base_image.copy()
        if repeat_logo:
            for y in range(0, base_height, logo_height + 50):
                for x in range(0, base_width, logo_width + 50):
                    result.paste(logo, (x, y), logo)
        else:
            positions = {
                "top-left": (10, 10),
                "top-right": (base_width - logo_width - 10, 10),
                "bottom-left": (10, base_height - logo_height - 10),
                "bottom-right": (base_width - logo_width - 10, base_height - logo_height - 10),
                "center": ((base_width - logo_width) // 2, (base_height - logo_height) // 2)
            }
            pos = positions.get(position, positions["bottom-right"])
            result.paste(logo, pos, logo)

        return result.convert("RGB")

    def show_preview_window(self, image):
        win = Toplevel(self)
        win.title("🔍 Watermark Preview")

        preview_img = image.copy()
        preview_img.thumbnail((500, 500), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(preview_img)

        lbl = Label(win, image=tk_image)
        lbl.image = tk_image
        lbl.pack(padx=10, pady=10)

        Button(win, text="Close", command=win.destroy).pack(pady=5)

    def apply_batch_watermark(self):
        if not self.image_paths:
            messagebox.showwarning("Missing Images", "Please add product images.")
            return
        if not self.logo_path.get():
            messagebox.showwarning("Missing Logo", "Please select the AUSVIC logo.")
            return
        if not self.output_dir.get():
            messagebox.showwarning("Missing Output Folder", "Please choose an output directory.")
            return

        total = len(self.image_paths)
        self.progress["maximum"] = total
        self.progress["value"] = 0
        self.update_idletasks()

        errors = []
        for idx, img_path in enumerate(self.image_paths):
            try:
                filename = os.path.basename(img_path)
                name, ext = os.path.splitext(filename)
                out_path = os.path.join(self.output_dir.get(), f"{name}_watermarked.jpg")
                add_logo_watermark(
                    img_path, self.logo_path.get(), out_path,
                    self.position.get(), self.scale.get(), self.opacity.get(),
                    self.repeat_logo.get()
                )
            except Exception as e:
                errors.append(f"{filename}: {e}")
            finally:
                self.progress["value"] += 1
                self.update_idletasks()

        self.progress["value"] = 0
        if errors:
            messagebox.showerror("Partial Success", "\n".join(errors))
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
                messagebox.showerror("Load Error", f"Failed to load settings: {e}")

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
            messagebox.showerror("Save Error", f"Failed to save settings: {e}")

    def on_close(self):
        self.save_settings()
        self.destroy()

# === Core Watermark Function ===
def add_logo_watermark(image_path, logo_path, output_path, position, scale_percent, opacity_percent, repeat_logo=False):
    base = Image.open(image_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    base_w, base_h = base.size
    logo_w = int((base_w * scale_percent) / 100)
    logo_h = int(logo_w * (logo.height / logo.width))
    logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

    if opacity_percent < 100:
        alpha = logo.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity_percent / 100)
        logo.putalpha(alpha)

    result = base.copy()

    if repeat_logo:
        for y in range(0, base_h, logo_h + 50):
            for x in range(0, base_w, logo_w + 50):
                result.paste(logo, (x, y), logo)
    else:
        positions = {
            "top-left": (10, 10),
            "top-right": (base_w - logo_w - 10, 10),
            "bottom-left": (10, base_h - logo_h - 10),
            "bottom-right": (base_w - logo_w - 10, base_h - logo_h - 10),
            "center": ((base_w - logo_w) // 2, (base_h - logo_h) // 2)
        }
        pos = positions.get(position, positions["bottom-right"])
        result.paste(logo, pos, logo)

    result.convert("RGB").save(output_path)

# === Run App ===
if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
