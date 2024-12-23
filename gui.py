import tkinter as tk
from tkinter import scrolledtext
from weather_service import (
    get_user_location,
    get_weekly_forecast,
    format_forecast
)

class ClimahkGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Climahk - Your Weather Chat")
        
        # Frame to hold the chat display
        self.chat_frame = tk.Frame(self.master)
        self.chat_frame.pack(pady=5, padx=5, fill="both", expand=True)

        # ScrolledText widget to display chat history
        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state='disabled')
        self.chat_display.pack(padx=5, pady=5, fill="both", expand=True)

        # Frame to hold the user input
        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(fill="x")

        # Entry for user message
        self.user_input = tk.Entry(self.input_frame)
        self.user_input.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.user_input.bind("<Return>", self.handle_send)  # Send on Enter

        # Send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.handle_send)
        self.send_button.pack(side="right", padx=5, pady=5)

        # Greet the user in the chat
        self.bot_speak("Welcome to Climahk!\nAsk me about your weather or your location.")
    
    def bot_speak(self, message):
        """
        Append a message from 'Climahk' to the chat display.
        """
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"Climahk: {message}\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def user_speak(self, message):
        """
        Append a message from the user to the chat display.
        """
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"You: {message}\n", "user_text")
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def handle_send(self, event=None):
        """
        Handle user pressing Enter or clicking 'Send' button.
        """
        message = self.user_input.get().strip()
        if not message:
            return  # Don't send empty messages

        # Display the user's message in the chat
        self.user_speak(message)
        self.user_input.delete(0, tk.END)

        # Process the user's message and respond
        self.process_message(message)
    
    def process_message(self, user_message):
        """
        Basic logic to respond to user queries about weather or location.
        """
        user_message_lower = user_message.lower()

        if "location" in user_message_lower or "where am i" in user_message_lower:
            self.respond_with_location()
        elif "forecast" in user_message_lower or "weather" in user_message_lower:
            self.respond_with_forecast()
        else:
            # Default response
            self.bot_speak("I'm here to help with your weather questions. Try asking:\n"
                           " - 'Where am I?' (location)\n"
                           " - 'What's the weather forecast?' or 'What's the forecast for the next week?'")
    
    def respond_with_location(self):
        location = get_user_location()
        city = location['city']
        region = location['region']
        lat, lon = location['lat'], location['lon']
        msg = (f"I believe you're approximately in {city}, {region}.\n"
               f"Latitude: {lat}, Longitude: {lon}\n")
        self.bot_speak(msg)

    def respond_with_forecast(self):
        location = get_user_location()  # Using the user's IP
        city = location['city']
        lat, lon = location['lat'], location['lon']

        weekly_data = get_weekly_forecast(lat, lon)
        if not weekly_data:
            self.bot_speak("I couldn't get the forecast data right now, sorry!")
            return

        self.bot_speak(f"Here is the forecast for {city} over the next 7 days:")
        forecast_texts = format_forecast(weekly_data)
        for day_forecast in forecast_texts:
            self.bot_speak(day_forecast)

def main():
    root = tk.Tk()
    app = ClimahkGUI(root)
    root.geometry("600x400")  # Optional sizing
    root.mainloop()

if __name__ == "__main__":
    main()
