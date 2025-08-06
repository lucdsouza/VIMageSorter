import os, time
import tkinter as tk
from PIL import Image, ImageTk


class VIMageSorterApp:
    _bg = "black"
    _mainc = "lightblue"
    _font = ("Consolas", 14)
    _sml_font = ("Consolas", 10)

    def __init__(self, root):
        self.root = root
        self.root.title("VIMage Sorter")
        self.root.configure(bg=self._bg)
        self.root.geometry("800x600")
        self.root.minsize(800, 600)

        #Counters
        self.done_count=0
        self.left_count=0
        self.image_count=0
        self.video_count=0

        #Top status bar
        self._status_var = tk.StringVar()
        self._update_status_text()
        self._status_label = tk.Label(
            self.root,
            textvariable=self._status_var,
            bg=self._bg,
            fg=self._mainc,
            font=self._font,
        )
        self._status_label.pack(side="top", fill="x", pady=5)
       
        # Main canvas area
        self._file_area = tk.Frame(
            self.root,
            bg=self._bg,
        )
        self._file_area.pack(expand=True, fill="both")

        self._canvas = tk.Canvas(
            self._file_area,
            bg=self._bg,
            highlightthickness=0,
        )
        self._canvas.pack(expand=True, fill="both")

        # Draw canvas placeholder
        self._draw_canvas_placeholder()

        # Info frame
        self._info_frame = tk.Frame(self._file_area, bg=self._bg)
        self._info_frame.pack(
            side="right",
            fill="y",
            padx=5,
            pady=5,
        )

        # Labels
        self._size_label = tk.Label(
            self._info_frame,
            text="Size: ",
            bg=self._bg,
            fg=self._mainc,
            font=self._sml_font,
        )
        self._type_label = tk.Label(
            self._info_frame,
            text="Type: ",
            bg=self._bg,
            fg=self._mainc,
            font=self._sml_font,
        )
        self._res_label = tk.Label(
            self._info_frame,
            text="Resolution: ",
            bg=self._bg,
            fg=self._mainc,
            font=self._sml_font,
        )
        self._created_dt_label = tk.Label(
            self._info_frame,
            text="Created: ",
            bg=self._bg,
            fg=self._mainc,
            font=self._sml_font,
        )

        self._size_label.pack(anchor="w")
        self._type_label.pack(anchor="w")
        self._res_label.pack(anchor="w")
        self._created_dt_label.pack(anchor="w")

        # Command input area, default hidden
        self._cmd_frame = tk.Frame(self.root, bg=self._bg)
        self._cmd_entry = tk.Entry(
            self._cmd_frame,
            bg=self._bg,
            fg=self._mainc,
            insertbackground=self._mainc,
            font=self._sml_font,
            relief="flat",
        )
        self._cmd_entry.pack(fill="x", padx=10, pady=5)
        self._cmd_frame.pack(side="bottom", fill="x")
        self._cmd_frame.pack_forget()
        
        # File path
        self._path_label = tk.Label(
            self._file_area,
            text="",
            bg=self._bg,
            fg=self._mainc,
            font=self._sml_font,
        )
        self._path_label.pack(side="bottom", fill="x", padx=5, pady=3)

        # Bind keys
        self.root.bind("<Configure>", self._on_resize)
        self.root.bind("<Key>", self._on_keypress)
        self.root.bind("r", self._rotate_img)
        self.root.bind("u", self._undo)
        self.root.bind("d", self._delete_file)
        self.root.bind("n", self._skip)
        self.root.bind("o", lambda event: self._display_img("/home/auggie/library/inbox/downloads/wallpaper.jpg"))
        self._cmd_entry.bind("<Return>", self._on_cmd_enter)
        self._cmd_entry.bind("<Escape>", self._on_cmd_escape)

        self.in_cmd_mode = False

    def _update_status_text(self):
        text = (f"Done: {self.done_count}/{self.left_count}\t\tImages: {self.image_count} | Videos: {self.video_count}")

        self._status_var.set(text)

    def _draw_canvas_placeholder(self):
        if hasattr(self, '_cur_img'):
            return

        self._canvas.delete("all")
        w = self._canvas.winfo_width() or 800
        h = self._canvas.winfo_height() or 600

        center_x = w // 2
        center_y = h // 2
        size = min(w, h) // 10

        # Plus sign
        self._canvas.create_line(
            center_x,
            center_y - size,
            center_x,
            center_y + size,
            fill=self._mainc,
            width=4,
        )
        self._canvas.create_line(
            center_x - size,
            center_y,
            center_x + size,
            center_y,
            fill=self._mainc,
            width=4,
        )

    def _on_resize(self, event):
        if hasattr(self, "_cur_img"):
            self._display_img("/home/auggie/library/inbox/downloads/wallpaper.jpg")

        else:
            self._draw_canvas_placeholder()

    def _on_keypress(self, event):
        if self.in_cmd_mode:
            return

        if event.char == ":":
            self._enter_cmd_mode()

    def _enter_cmd_mode(self):
        self.in_cmd_mode = True
        self._cmd_entry.delete(0, "end")
        self._cmd_frame.pack(side="bottom", fill="x")
        self._cmd_entry.focus_set()

    def _exit_cmd_mode(self):
        self.in_cmd_mode = False
        self._cmd_frame.pack_forget()
        self.root.focus_set()

    def _on_cmd_enter(self, event):
        cmd_text = self._cmd_entry.get().strip()
        print(f"Cmd entered: {cmd_text}")
        self._exit_cmd_mode()

    def _on_cmd_escape(self, event):
        self._exit_cmd_mode()

    def _rotate_img(self, event):
        if self.in_cmd_mode:
            return

        print("Rotate action triggered")

    def _undo(self, event):
        if self.in_cmd_mode:
            return

        print("Undo action triggered")

    def _delete_file(self, event):
        if self.in_cmd_mode:
            return

        print("Delete action triggered")

    def _skip(self, event):
        if self.in_cmd_mode:
            return

        print("Skip action triggered")

    def _display_img(self, img_path):
        img = Image.open(img_path)
        w, h = img.size
        cw = self._canvas.winfo_width()
        ch = self._canvas.winfo_height()

        # Resize image to fit canvas
        scale = min(cw / w, ch / h, 1) # Avoid upscaling

        if scale < 1:
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.LANCZOS)
            nw, nh = new_size

        self._cur_img = ImageTk.PhotoImage(img)

        self._canvas.delete("all")
        self._canvas.create_image(
            cw//2,
            ch//2,
            image=self._cur_img,
        )
        
        # update info labels
        self._size_label.config(text=f"Size: {os.path.getsize(img_path)/1024:.2f} KB")
        self._type_label.config(text=f"Type: {os.path.splitext(img_path)[1].lstrip('.').upper()}")
        self._res_label.config(text=f"Resolution: {w}x{h}")
        timestamp = time.ctime(os.path.getctime(img_path))
        self._created_dt_label.config(text=f"Created: {timestamp}")
        self._path_label.config(text=f"{img_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VIMageSorterApp(root)

    root.mainloop()

