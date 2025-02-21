import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import messagebox
import requests  # Ensure requests is imported
from IPGeolocation import IPGeolocationApp  # Adjust this import based on your file name

class TestIPGeolocationApp(unittest.TestCase):

    @patch("requests.get")
    def test_find_location_valid_ip(self, mock_get):
        # Prepare a mock response for a successful API call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ip": "8.8.8.8",
            "city": "Mountain View",
            "state_prov": "California",
            "country_name": "United States",
            "latitude": 37.4056,
            "longitude": -122.0775,
            "isp": "Google LLC"
        }
        mock_get.return_value = mock_response

        # Create the Tkinter root window
        root = tk.Tk()
        app = IPGeolocationApp(root)

        # Set the IP entry text to the valid IP address
        app.ip_entry.insert(tk.END, "8.8.8.8")
        
        # Call the method directly
        app.find_location()

        # Check if the output is correct
        self.assertIn("IP Address: 8.8.8.8", app.output_text.get("1.0", tk.END))
        self.assertIn("City: Mountain View", app.output_text.get("1.0", tk.END))
        self.assertIn("Country: United States", app.output_text.get("1.0", tk.END))

    @patch("requests.get")
    def test_find_location_invalid_ip(self, mock_get):
        # Simulate a failed API call due to invalid IP address
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid IP address"}
        mock_get.return_value = mock_response

        # Create the Tkinter root window
        root = tk.Tk()
        app = IPGeolocationApp(root)

        # Set the IP entry text to an invalid IP address
        app.ip_entry.insert(tk.END, "invalid_ip")

        # Mock messagebox to verify if error message shows up
        messagebox.showerror = MagicMock()

        # Call the method directly
        app.find_location()

        # Check if error message is displayed
        messagebox.showerror.assert_called_with("Error", "Invalid IP address")

    @patch("requests.get")
    def test_find_location_empty_ip(self, mock_get):
        # Create the Tkinter root window
        root = tk.Tk()
        app = IPGeolocationApp(root)

        # Set the IP entry to an empty string
        app.ip_entry.delete(0, tk.END)

        # Mock messagebox to verify if error message shows up
        messagebox.showerror = MagicMock()

        # Call the method directly
        app.find_location()

        # Check if the error message is displayed
        messagebox.showerror.assert_called_with("Error", "Please enter a valid IP address.")

    @patch("requests.get")
    def test_find_location_request_exception(self, mock_get):
        # Simulate a network exception (e.g., timeout)
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Create the Tkinter root window
        root = tk.Tk()
        app = IPGeolocationApp(root)

        # Set the IP entry text to a valid IP address
        app.ip_entry.insert(tk.END, "8.8.8.8")

        # Mock messagebox to verify if error message shows up
        with patch("tkinter.messagebox.showerror") as mock_showerror:
            app.find_location()

            # Check if error message is displayed for request failure
            mock_showerror.assert_called_with("Error", "Request failed: Network error")

if __name__ == "__main__":
    unittest.main()
