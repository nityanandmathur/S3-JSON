import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# AWS S3 Configuration
BUCKET_NAME = '<BUCKET-NAME>'
FILE_KEY = '<FILE_NAME>.json'

# Initialize S3 client
s3_client = boto3.client('s3')

class S3JsonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("S3 JSON Manager")
        self.json_data = {}

        # Load the JSON file on startup
        self.load_json_from_s3()

        # GUI Buttons
        tk.Button(root, text="Show Content", command=self.show_content, width=20).pack(pady=10)
        tk.Button(root, text="Add Content", command=self.add_content, width=20).pack(pady=10)
        tk.Button(root, text="Delete Content", command=self.delete_content, width=20).pack(pady=10)
        tk.Button(root, text="Refresh Content", command=self.refresh_content, width=20).pack(pady=10)  # New button

    def load_json_from_s3(self):
        try:
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
            self.json_data = json.loads(response['Body'].read())
            messagebox.showinfo("Success", "JSON file loaded successfully.")
        except (NoCredentialsError, PartialCredentialsError):
            messagebox.showerror("Error", "AWS credentials are not configured properly.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON: {e}")

    def save_json_to_s3(self):
        try:
            s3_client.put_object(Bucket=BUCKET_NAME, Key=FILE_KEY, Body=json.dumps(self.json_data, indent=4))
            messagebox.showinfo("Success", "Changes saved to S3 successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON: {e}")

    def show_content(self):
        content_window = tk.Toplevel(self.root)
        content_window.title("JSON Content")

        # Create a frame for the Treeview and scrollbars
        frame = ttk.Frame(content_window)
        frame.pack(expand=True, fill='both')

        # Treeview for displaying JSON data
        tree = ttk.Treeview(frame, columns=("Key", "Value"), show='headings')
        tree.heading("Key", text="Key")
        tree.heading("Value", text="Value")
        tree.column("Key", width=200, anchor='w')
        tree.column("Value", width=400, anchor='w')

        # Scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Place the Treeview and Scrollbars in the frame
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Configure the frame to stretch
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Insert JSON data into the tree
        for key, value in self.json_data.items():
            tree.insert("", "end", values=(key, str(value)))

        # Function to display full value in a new window
        def show_full_value(event):
            selected_item = tree.focus()
            if selected_item:
                key, value = tree.item(selected_item, 'values')
                value_window = tk.Toplevel(content_window)
                value_window.title(f"Value for '{key}'")

                text_widget = tk.Text(value_window, wrap='word')
                text_widget.pack(expand=True, fill='both')

                text_widget.insert('1.0', value)

                # Add a scrollbar to the text widget
                scrollbar = ttk.Scrollbar(value_window, orient='vertical', command=text_widget.yview)
                scrollbar.pack(side='right', fill='y')
                text_widget.configure(yscrollcommand=scrollbar.set)

        # Bind double-click event to show the full value
        tree.bind('<Double-1>', show_full_value)

    def add_content(self):
        key = simpledialog.askstring("Add Content", "Enter the key:")
        if key:
            value = simpledialog.askstring("Add Content", f"Enter the value for '{key}':")
            if value:
                self.json_data[key] = value
                self.save_json_to_s3()

    def delete_content(self):
        key = simpledialog.askstring("Delete Content", "Enter the key to delete:")
        if key and key in self.json_data:
            del self.json_data[key]
            self.save_json_to_s3()
        else:
            messagebox.showerror("Error", "Key not found in JSON data.")

    def refresh_content(self):
        self.load_json_from_s3()

if __name__ == "__main__":
    root = tk.Tk()
    app = S3JsonApp(root)
    root.mainloop()
