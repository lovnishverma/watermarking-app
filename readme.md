# 🖼️ Python Watermarking GUI App

A powerful, user-friendly, and fully customizable Python GUI application to batch watermark images. Built with Tkinter and Pillow, this app supports drag-and-drop, live preview, transparency, rotation, padding, user preferences, undo, and more.

---

## 🔧 Features

- ✅ **Drag and Drop** support for images and logo  
- ✅ **Interactive Watermark Preview**  
- ✅ **Resizable Logo with Scaling Slider**  
- ✅ **Transparency (Opacity) Control**  
- ✅ **Rotation & Padding** for precise placement  
- ✅ **Batch Watermarking** for folders  
- ✅ **Undo Functionality** to reset preview  
- ✅ **Custom Output Directory Selection**  
- ✅ **Live Progress Bar** during processing  
- ✅ **Tooltips** for better UX  
- ✅ **Error Handling** with dialogs  
- ✅ **User Preference Saving** (logo path, opacity, rotation, padding, etc.)

---

## 🖼️ Screenshots

![Preview Screenshot](https://github.com/lovnishverma/watermarking-app/assets/preview.png)
*(Update with actual screenshot)*

---

## 🐍 Requirements

- Python 3.8+
- `Pillow`
- `Tkinter` (bundled with Python)
- `ttkthemes` *(optional, for better styling)*

Install dependencies:

```bash
pip install pillow
```

---

## 🚀 Getting Started

1. **Clone the repository:**

```bash
git clone https://github.com/lovnishverma/watermarking-app.git
cd watermarking-app
```

2. **Run the app:**

```bash
python watermark.py
```

---

## 🧠 How It Works

1. **Import Images** via drag-and-drop or file browser  
2. **Load a Logo** using "Browse Logo" or drag-and-drop  
3. **Adjust Settings**:  
   - Opacity slider  
   - Logo scale  
   - Rotation  
   - Padding (Top/Bottom/Left/Right)  
4. **Preview** watermark on the first image  
5. **Choose Output Directory** or use the default  
6. **Apply Watermark to All** images in batch  
7. Use **Undo Preview** to reset the current preview

---

## 📦 Build Windows Executable

Create a standalone `.exe` with `PyInstaller`:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon=logo.ico watermark.py
```

- Executable will be available in `dist/` directory  
- Update `--icon` path if needed

---

## 💾 User Preferences

The app remembers:
- Logo path
- Opacity level
- Rotation and padding
- Last output directory

This ensures a smoother experience in future sessions.

---

## 💡 Planned Features

- [ ] Add watermark **text** option  
- [ ] Add **border/stroke** around watermark  
- [ ] Enable **image resizing** after watermark  
- [ ] **Keyboard shortcuts** for faster control  
- [ ] Support **custom watermark position presets**

---

## 👨‍💻 Author

**Lovnish Verma**  
Developer | Backend & AI Enthusiast | Open Source Contributor  

[GitHub](https://github.com/lovnishverma) • [LinkedIn](https://linkedin.com/in/lovnishverma)

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more info.
```
