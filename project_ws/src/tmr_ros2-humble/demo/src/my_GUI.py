import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess

class BlackScreenApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Black Screen Display")
        self.master.geometry("400x300")
        self.is_displaying = False
        self.is_paused = False

        self.canvas = tk.Canvas(self.master, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_stop_button = tk.Button(self.master, text="Start", command=self.toggle_display,
                                        bg="red", fg="white", relief=tk.RAISED, borderwidth=3)
        self.start_stop_button.config(width=10, height=2, bd=0, highlightthickness=0, highlightbackground="black",
                                    activebackground="green", activeforeground="white")
        self.start_stop_button.pack(side=tk.LEFT, padx=(10, 5), pady=5)  

        self.pause_button = tk.Button(self.master, text="Pause", command=self.toggle_pause,
                                    bg="blue", fg="white", relief=tk.RAISED, borderwidth=3)
        self.pause_button.config(width=10, height=2, bd=0, highlightthickness=0, highlightbackground="black",
                                activebackground="yellow", activeforeground="black")
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.arrow_buttons_frame = tk.Frame(self.master)
        self.arrow_buttons_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        self.up_button = tk.Button(self.arrow_buttons_frame, text="↑", command=self.move_up,
                                bg="grey", fg="white", relief=tk.RAISED, borderwidth=3)
        self.up_button.grid(row=0, column=3) 
        self.up_button.config(state=tk.DISABLED)  

        self.left_button = tk.Button(self.arrow_buttons_frame, text="←", command=self.move_left,
                                    bg="grey", fg="white", relief=tk.RAISED, borderwidth=3)
        self.left_button.grid(row=1, column=2) 
        self.left_button.config(state=tk.DISABLED)  

        self.right_button = tk.Button(self.arrow_buttons_frame, text="→", command=self.move_right,
                                    bg="grey", fg="white", relief=tk.RAISED, borderwidth=3)
        self.right_button.grid(row=1, column=4) 
        self.right_button.config(state=tk.DISABLED)  

        self.down_button = tk.Button(self.arrow_buttons_frame, text="↓", command=self.move_down,
                                    bg="grey", fg="white", relief=tk.RAISED, borderwidth=3)
        self.down_button.grid(row=2, column=3)  
        self.down_button.config(state=tk.DISABLED)  

        self.forward_button = tk.Button(self.arrow_buttons_frame, text="→↑", command=self.move_forward,
                                        bg="grey", fg="white", relief=tk.RAISED, borderwidth=3)
        self.forward_button.grid(row=0, column=5) 
        self.forward_button.config(state=tk.DISABLED)  

        self.backward_button = tk.Button(self.arrow_buttons_frame, text="←↓", command=self.move_backward,
                                        bg="grey", fg="white", relief=tk.RAISED, borderwidth=3)
        self.backward_button.grid(row=2, column=5)  
        self.backward_button.config(state=tk.DISABLED)  

        self.configurations_button = tk.Button(self.master, text="Set Configurations", command=self.show_configurations,
                                    bg="purple", fg="white", relief=tk.RAISED, borderwidth=3)
        self.configurations_button.config(width=15, height=2, bd=0, highlightthickness=0, highlightbackground="black",
                                activebackground="orange", activeforeground="black")
        self.configurations_button.pack(side=tk.BOTTOM, padx=5, pady=5)

    def toggle_display(self):
        if self.is_displaying:
            self.stop_display()
        else:
            self.start_display()

    def start_display(self):
        self.is_displaying = True
        self.start_stop_button.config(text="Stop")
        #subprocess.Popen(["ros2", "topic", "list"])
        subprocess.Popen(["ros2", "run", "demo", "demo_send_script"])
        self.update_display()

    def stop_display(self):
        self.is_displaying = False
        self.start_stop_button.config(text="Start")
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Shutting down...", fill="white",
                                font=("Arial", 12))

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="Resume")
            self.enable_arrow_buttons()
            self.start_stop_button.config(state=tk.DISABLED)
            self.canvas.delete("all")
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Pausing robotic arm...", fill="white",
                                    font=("Arial", 12))
        else:
            self.pause_button.config(text="Pause")
            self.disable_arrow_buttons()
            self.start_stop_button.config(state=tk.NORMAL)
            self.update_display()
            self.resume_arm()

    def enable_arrow_buttons(self):
        self.up_button.config(state=tk.NORMAL)
        self.left_button.config(state=tk.NORMAL)
        self.right_button.config(state=tk.NORMAL)
        self.down_button.config(state=tk.NORMAL)
        self.forward_button.config(state=tk.NORMAL)
        self.backward_button.config(state=tk.NORMAL)

    def disable_arrow_buttons(self):
        self.up_button.config(state=tk.DISABLED)
        self.left_button.config(state=tk.DISABLED)
        self.right_button.config(state=tk.DISABLED)
        self.down_button.config(state=tk.DISABLED)
        self.forward_button.config(state=tk.DISABLED)
        self.backward_button.config(state=tk.DISABLED)

    def resume_arm(self):
        if not self.is_paused:
            self.canvas.delete("all")
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Resuming robotic arm...", fill="white",
                                    font=("Arial", 12))
            self.master.after(2000, self.update_display)

    def update_display(self):
        if not self.is_displaying or self.is_paused:
            return
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 400, 300, fill="black")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Moving robotic arm...", fill="white",
                                font=("Arial", 12))
        self.master.after(2000, self.update_display)

    def move_up(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Moving up", fill="white", font=("Arial", 12))

    def move_down(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Moving down", fill="white", font=("Arial", 12))

    def move_left(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Moving left", fill="white", font=("Arial", 12))

    def move_right(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Moving right", fill="white", font=("Arial", 12))

    def move_forward(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Moving forward", fill="white", font=("Arial", 12))

    def move_backward(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Moving backward", fill="white", font=("Arial", 12))

    def show_configurations(self):
        popup = tk.Toplevel(self.master)
        popup.title("Configurations")
        label = tk.Label(popup, text="Previously Set Configurations:")
        label.pack(padx=20, pady=10)

        # Access database to retrieve previously set configurations
        configurations = self.retrieve_configurations_from_database()

        if configurations:
            for config in configurations:
                config_name = config[0]  # Get the name of the configuration
                config_button = tk.Button(popup, text=config_name, command=lambda name=config_name, up=config[1], down=config[2], left=config[3], right=config[4], sku=config[5], popup=popup: self.print_configuration(name, up, down, left, right, sku, popup))
                config_button.pack(padx=20, pady=5)

        new_config_button = tk.Button(popup, text="New Configuration", command=lambda: self.create_new_configuration_popup(popup))
        new_config_button.pack(padx=20, pady=10)

    def retrieve_configurations_from_database(self):
        conn = sqlite3.connect('my_database.db') # Change 'your_database_name.db' to your database name
        c = conn.cursor()
        c.execute("SELECT name, up_pose, down_pose, left_pose, right_pose, sku_number FROM configurations")
        configurations = c.fetchall()
        conn.close()
        return configurations

    def print_configuration(self, name, up_pose, down_pose, left_pose, right_pose, sku_number, popup):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        text = f"Configuration: {name}\nUp Pose: {up_pose}\nDown Pose: {down_pose}\nLeft Pose: {left_pose}\nRight Pose: {right_pose}\nSKU Number: {sku_number}"
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text=text, fill="white", font=("Arial", 12))
        popup.destroy()  # Close the popup after selecting a configuration

    def save_configuration(self, up_pose, down_pose, left_pose, right_pose, sku_number, popup, parent_popup):
        if not all([up_pose, down_pose, left_pose, right_pose, sku_number]):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        conn = sqlite3.connect('my_database.db')
        c = conn.cursor()
        
        # Retrieve the last configuration name from the database
        c.execute("SELECT MAX(name) FROM configurations")
        last_config = c.fetchone()[0]

        # Increment the last configuration name to create a new one
        if last_config is not None:
            new_config_num = int(last_config.split()[-1]) + 1
            new_config_name = f"Configuration {new_config_num}"
        else:
            new_config_name = "Configuration 1"
        
        # Insert the new configuration into the database
        c.execute("INSERT INTO configurations (name, up_pose, down_pose, left_pose, right_pose, sku_number) VALUES (?, ?, ?, ?, ?, ?)", (new_config_name, up_pose, down_pose, left_pose, right_pose, sku_number))
        conn.commit()
        conn.close()

        # Print the saved configuration onto the display
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        text = f"Configuration: {new_config_name}\nUp Pose: {up_pose}\nDown Pose: {down_pose}\nLeft Pose: {left_pose}\nRight Pose: {right_pose}\nSKU Number: {sku_number}"
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text=text, fill="white", font=("Arial", 12))

        popup.destroy()  # Close the current popup
        parent_popup.destroy()  # Close the parent popup

    def create_new_configuration_popup(self, parent_popup):
        new_popup = tk.Toplevel(self.master)
        new_popup.title("New Configuration")

        up_label = tk.Label(new_popup, text="Up Pose:")
        up_label.grid(row=0, column=0, padx=5, pady=5)
        up_entry = tk.Entry(new_popup)
        up_entry.grid(row=0, column=1, padx=5, pady=5)

        down_label = tk.Label(new_popup, text="Down Pose:")
        down_label.grid(row=1, column=0, padx=5, pady=5)
        down_entry = tk.Entry(new_popup)
        down_entry.grid(row=1, column=1, padx=5, pady=5)

        left_label = tk.Label(new_popup, text="Left Pose:")
        left_label.grid(row=2, column=0, padx=5, pady=5)
        left_entry = tk.Entry(new_popup)
        left_entry.grid(row=2, column=1, padx=5, pady=5)

        right_label = tk.Label(new_popup, text="Right Pose:")
        right_label.grid(row=3, column=0, padx=5, pady=5)
        right_entry = tk.Entry(new_popup)
        right_entry.grid(row=3, column=1, padx=5, pady=5)

        sku_label = tk.Label(new_popup, text="SKU Number:")
        sku_label.grid(row=4, column=0, padx=5, pady=5)
        sku_entry = tk.Entry(new_popup)
        sku_entry.grid(row=4, column=1, padx=5, pady=5)

        save_button = tk.Button(new_popup, text="Save Configuration", command=lambda: self.save_configuration(up_entry.get(), down_entry.get(), left_entry.get(), right_entry.get(), sku_entry.get(), new_popup, parent_popup))
        save_button.grid(row=5, columnspan=2, padx=5, pady=10)

def main():
    root = tk.Tk()
    app = BlackScreenApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
