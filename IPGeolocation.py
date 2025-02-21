import tkinter as tk
from tkinter import messagebox
import requests
import json

class IPGeolocationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Geolocation Finder")
        self.api_key = "16599bf95fa94f3c954722fd1b6373d7"  # Replace with your actual API key

        # Set background color and font
        self.root.configure(bg="black")
        font = ("Courier New", 12)

        # Labels and Entries
        tk.Label(root, text="Enter IP Address:", bg="black", fg="#00ff00", font=font).grid(row=0, column=0, padx=10, pady=10)
        self.ip_entry = tk.Entry(root, width=30, font=font)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=10)

        # Fetch Button
        tk.Button(root, text="Find location", command=self.find_location, bg="green", fg="black", font=font).grid(row=1, column=0, columnspan=2, pady=10)

        # Output Box with a terminal-like style
        self.output_text = tk.Text(root, height=15, width=50, font=("Courier New", 10), bg="black", fg="lime", wrap=tk.WORD)
        self.output_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Add background effect
        self.root.geometry("600x500")
        self.root.resizable(False, False)

    def find_location(self):
        ip_address = self.ip_entry.get().strip()
        if not ip_address:
            messagebox.showerror("Error", "Please enter a valid IP address.")
            return

        # Call the API
        url = f"https://api.ipgeolocation.io/ipgeo"
        params = {
            "apiKey": self.api_key,
            "ip": ip_address
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()

            if response.status_code == 200:
                self.display_result(data)
            else:
                messagebox.showerror("Error", data.get("message", "Failed to fetch data."))
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    def display_result(self, data):
        self.output_text.delete(1.0, tk.END)  # Clear previous text

        # Format and display data in hacker-like style
        output = (
            f"IP Address: {data.get('ip', 'N/A')}\n"
            f"City: {data.get('city', 'N/A')}\n"
            f"Region: {data.get('state_prov', 'N/A')}\n"
            f"Country: {data.get('country_name', 'N/A')}\n"
            f"Latitude: {data.get('latitude', 'N/A')}\n"
            f"Longitude: {data.get('longitude', 'N/A')}\n"
            f"ISP: {data.get('isp', 'N/A')}\n"
        )

        self.output_text.insert(tk.END, output)

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = IPGeolocationApp(root)
    root.mainloop()
