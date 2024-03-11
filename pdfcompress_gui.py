import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter

class PDFCompressorApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Compressor")

        self.label = tk.Label(master, text="Выберите PDF-файл:")
        self.label.pack()

        self.button_browse = tk.Button(master, text="Обзор", command=self.browse_file)
        self.button_browse.pack()

        self.label_filename = tk.Label(master, text="")
        self.label_filename.pack()

        self.label_quality = tk.Label(master, text="Выберите качество изображения:")
        self.label_quality.pack()

        self.scale_quality = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL)
        self.scale_quality.set(50)
        self.scale_quality.pack()

        self.label_quality2 = tk.Label(master, text="Выберите степень сжатия файла (от 0 до 10):")
        self.label_quality2.pack()

        self.scale_quality2 = tk.Scale(master, from_=0, to=10, orient=tk.HORIZONTAL)
        self.scale_quality2.set(5)
        self.scale_quality2.pack()

        self.button_compress = tk.Button(master, text="Сжать", command=self.compress_pdf)
        self.button_compress.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.label_filename.config(text=f"Выбран файл: {file_path}")
            self.file_path = file_path

    def compress_pdf(self):
        if hasattr(self, 'file_path'):
            quality = self.scale_quality.get()
            quality2 = self.scale_quality2.get()
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if output_path:
                input_pdf = PdfReader(self.file_path)
                output_pdf = PdfWriter()
                for page in input_pdf.pages:
                    output_pdf.add_page(page)
                for page in output_pdf.pages:
                    page.compress_content_streams(level=quality2)
                    for img in page.images:
                        img.replace(img.image, quality=quality)
                with open(output_path, "wb") as output_file:
                    output_pdf.write(output_file)

                messagebox.showinfo("Готово", "PDF успешно сжат!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCompressorApp(root)
    root.mainloop()
