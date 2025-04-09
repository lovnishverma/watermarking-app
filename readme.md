---

```markdown
# 🖼️ Python Watermarking GUI App

A powerful and user-friendly Python GUI application to batch watermark images with advanced customization. Supports drag-and-drop, live preview, transparency control, rotation, padding, user preference saving, and more.

---

## 🔧 Features

- ✅ **Drag and Drop** images and watermark logo  
- ✅ **Interactive Logo Resizing**  
- ✅ **Transparency (Opacity) Slider**  
- ✅ **Rotation and Padding** controls  
- ✅ **Batch Processing** of multiple images  
- ✅ **Preview** before applying watermark  
- ✅ **Organized UI** with clean layout  
- ✅ **Custom Output Directory Selection**  
- ✅ **Undo (Preview Reset) Functionality**  
- ✅ **Tooltips** for all controls  
- ✅ **User Preference Saving** (logo path, opacity, rotation, padding, etc.)  
- ✅ **Error Handling** with popup dialogs  
- ✅ **Progress Indicators**

---

## 📸 Screenshot

![Preview Screenshot](screenshot.png)
---

## 🐍 Requirements

- Python 3.8+
- `Pillow`
- `Tkinter` (usually included with Python)
- `ttkthemes` (optional, for themed widgets)

Install dependencies:

```bash
pip install pillow
```

---

## 🚀 How to Run

1. Clone this repository:

```bash
git clone https://github.com/lovnishverma/watermarking-app.git
cd watermarking-app
```

2. Run the app:

```bash
python watermark.py
```

---

## 📦 To Create .exe File (Windows)

Use `pyinstaller`:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon=logo.ico watermark.py
```

- The `.exe` will be in the `dist/` folder.
- Make sure `logo.ico` is in the project root or update the path.

---

## 🧠 How It Works

1. **Drag and drop** images or use "Browse Images"
2. Load a **logo** with "Browse Logo" or drag-and-drop
3. Adjust **opacity**, **scale**, **rotation**, and **padding**
4. Preview the result on one image
5. Set an **output folder** or use the default one
6. Click **"Apply Watermark to All"** to batch watermark images

---

## 💡 Future Enhancements

- [ ] Border/stroke around watermark  
- [ ] Text watermark support  
- [ ] Keyboard shortcuts  
- [ ] Output image resizing  
- [ ] Multiple watermark positions

---

## 👨‍💻 Author

**Lovnish Verma**  
Passionate developer | AI & Backend Engineer | Open Source Contributor  
[GitHub](https://github.com/lovnishverma) • [LinkedIn](https://linkedin.com/in/lovnishverma)

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.
```

---
