import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import time
import threading

from data_reader import read_csv
from data_processor import process_data
from plot_utilities import draw_plot
from accuracy_utils import calculate_accuracy  # Import the accuracy function

class StockPredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Price Prediction")
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        self.data = None
        self.predictions = None
        self.add_widgets()

    def add_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.upload_icon = Image.open("file_icon.png").resize((50, 50), Image.Resampling.LANCZOS)
        self.upload_icon = ImageTk.PhotoImage(self.upload_icon)
        upload_button = tk.Button(frame, text="Choose Files", image=self.upload_icon, compound=tk.TOP, command=self.upload_file)
        upload_button.pack()

        tk.Label(self.root, text="or drop files here", font=("Arial", 12)).pack()
        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.pack()

        tk.Button(self.root, text="Show Actual & Predicted Data", command=self.show_actual_predicted_data).pack(pady=10)
        tk.Button(self.root, text="Quit", command=self.root.quit).pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.progress_label.config(text="Uploading... 0%")
            threading.Thread(target=self.process_file, args=(file_path,)).start()

    def process_file(self, file_path):
        try:
            for i in range(1, 101):
                self.progress_label.config(text=f"Uploading... {i}%")
                self.root.update_idletasks()
                time.sleep(0.02)

            header, data = read_csv(file_path)

            # Set target thresholds for MSE, MAE, and R²
            target_mse = 400.0  # Example target MSE
            target_mae = 10.0   # Example target MAE
            target_r2 = 0.8     # Example target R²
            max_retries = 5     # Limit the number of retraining attempts
            attempts = 0

            while attempts < max_retries:
                self.data, self.predictions = process_data(data)
                y, y_pred = self.predictions
                mae, mse, r2 = calculate_accuracy(y, y_pred)

                # Display accuracy metrics
                print(f"Attempt {attempts + 1}:")
                print(f"Mean Absolute Error (MAE): {mae}")
                print(f"Mean Squared Error (MSE): {mse}")
                print(f"R-squared (R^2): {r2}")

                # Check if MSE, MAE, and R² meet the targets
                if mse <= target_mse and mae <= target_mae and r2 >= target_r2:
                    self.progress_label.config(text="File uploaded and data processed successfully.")
                    messagebox.showinfo("Success", f"Model trained successfully with MAE: {mae:.2f}, MSE: {mse:.2f}, R²: {r2:.2f}")
                    break

                attempts += 1
                messagebox.showwarning("Retraining", f"Accuracy below target. Retrying... (Attempt {attempts + 1})")

            if attempts == max_retries:
                messagebox.showerror("Error", "Failed to reach the target accuracy after multiple attempts.")
            
            # Optionally show the final accuracy
            messagebox.showinfo("Final Accuracy", f"Final MAE: {mae:.2f}, MSE: {mse:.2f}, R²: {r2:.2f}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {str(e)}")

    def show_actual_predicted_data(self):
        if self.predictions is None:
            messagebox.showerror("Error", "No data to display.")
            return

        y, y_pred = self.predictions
        data_window = tk.Toplevel(self.root)
        data_window.title("Actual & Predicted Data")

        text_box = scrolledtext.ScrolledText(data_window, width=50, height=20, font=("Arial", 10))
        text_box.pack(padx=10, pady=10)
        for i, (actual, pred) in enumerate(zip(y, y_pred)):
            text_box.insert(tk.END, f"Actual: {actual:.2f}, Predicted: {pred:.2f}\n")

        tk.Label(data_window, text="Do you want to plot the data?", font=("Arial", 12)).pack(pady=10)
        tk.Button(data_window, text="Yes", command=lambda: [data_window.destroy(), self.plot_data()]).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(data_window, text="No", command=data_window.destroy).pack(side=tk.RIGHT, padx=20, pady=10)

    def plot_data(self):
        if self.predictions is not None:
            y, y_pred = self.predictions
            draw_plot(self.canvas, y, y_pred)

            legend_x = 500  
            legend_y = 20   

            # Clear any existing legend elements on the canvas, if needed
            self.canvas.delete("legend")

            # Create a rectangle for the legend background
            self.canvas.create_rectangle(legend_x, legend_y, legend_x + 80, legend_y + 50, fill="white", tags="legend")

            # Add labels for the actual and predicted data lines
            self.canvas.create_text(legend_x + 10, legend_y + 10, text="Actual", fill="blue", anchor="w", tags="legend")
            self.canvas.create_text(legend_x + 10, legend_y + 30, text="Predicted", fill="red", anchor="w", tags="legend")

