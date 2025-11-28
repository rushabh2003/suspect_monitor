from FaceDetectionClass import FaceDetectionApp
import tkinter as tk

# Tkinter starting point
def main():
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
