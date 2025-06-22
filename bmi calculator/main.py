import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as msg
import json

# Global app theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Fonts (system default)
font_heading = ("Arial", 20, "bold")
font_body = ("Segoe UI", 14)

# Function to save data to JSON
def save_data(age, gender, height, weight, bmi):
    entry = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "bmi": bmi
    }
    try:
        with open("bmi_history.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)
    with open("bmi_history.json", "w") as f:
        json.dump(data, f, indent=4)

# Main App Class
class BMIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator Dashboard")
        self.geometry("500x650")
        self.resizable(False, False)

        self.frames = {}
        for F in (DashboardScreen, InputScreen, ResultScreen, CalorieCalculator):
            frame = F(self, self.show_frame)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(DashboardScreen)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

# Frame 1: Dashboard
class DashboardScreen(ctk.CTkFrame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.configure(fg_color="#ffffff")

        ctk.CTkLabel(self, text="🏠 Dashboard", font=font_heading).pack(pady=20)
        ctk.CTkLabel(self, text="Welcome to your BMI app!", font=font_body).pack(pady=10)

        ctk.CTkButton(self, text="➕ Start New BMI Check", command=lambda: switch_frame(InputScreen), corner_radius=12, width=220).pack(pady=10)
        ctk.CTkButton(self, text="📊 View Last Result", command=self.view_last, corner_radius=12, width=220).pack(pady=10)
        ctk.CTkButton(self, text="🔥 Maintenance Calorie Calculator", command=lambda: switch_frame(CalorieCalculator), corner_radius=12, width=220).pack(pady=10)

    def view_last(self):
        try:
            with open("bmi_history.json", "r") as f:
                data = json.load(f)
                if data:
                    last_entry = data[-1]
                    bmi = round(last_entry["bmi"], 2)
                    self.master.frames[ResultScreen].update_result(bmi)
                    self.master.show_frame(ResultScreen)
                else:
                    msg.showinfo("No Data", "No previous data found.")
        except FileNotFoundError:
            msg.showinfo("No File", "No previous data file found.")

# Frame 2: Input
class InputScreen(ctk.CTkFrame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame
        self.configure(fg_color="#f0f8ff")

        ctk.CTkLabel(self, text="Enter Your Details", font=font_heading).pack(pady=20)

        self.age = ctk.CTkEntry(self, placeholder_text="Age", corner_radius=10)
        self.age.pack(pady=10)

        self.gender = ctk.CTkComboBox(self, values=["Male", "Female"], corner_radius=10)
        self.gender.set("Male")
        self.gender.pack(pady=10)

        self.height = ctk.CTkEntry(self, placeholder_text="Height (cm)", corner_radius=10)
        self.height.pack(pady=10)

        self.weight = ctk.CTkEntry(self, placeholder_text="Weight (kg)", corner_radius=10)
        self.weight.pack(pady=10)

        ctk.CTkButton(self, text="Calculate BMI", command=self.calculate_bmi, corner_radius=12).pack(pady=20)
        ctk.CTkButton(self, text="🏠 Back to Dashboard", command=lambda: switch_frame(DashboardScreen), corner_radius=10).pack(pady=10)

    def calculate_bmi(self):
        try:
            h = float(self.height.get()) / 100
            w = float(self.weight.get())
            age = int(self.age.get())
            gender = self.gender.get()
            bmi = w / (h ** 2)
            save_data(age, gender, h * 100, w, round(bmi, 2))
            self.master.frames[ResultScreen].update_result(round(bmi, 2))
            self.switch_frame(ResultScreen)
        except:
            msg.showerror("Input Error", "Please enter valid numerical values.")

# Frame 3: Results
class ResultScreen(ctk.CTkFrame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame
        self.configure(fg_color="#e0f7fa")

        self.label = ctk.CTkLabel(self, text="", font=font_heading)
        self.label.pack(pady=40)

        self.tips = ctk.CTkLabel(self, text="", wraplength=350, font=font_body, justify="left")
        self.tips.pack(pady=10)

        ctk.CTkButton(self, text="🏠 Back to Dashboard", command=lambda: switch_frame(DashboardScreen), corner_radius=12).pack(pady=20)

    def update_result(self, bmi):
        if bmi < 16:
            status = "Severe Thinness"
            advice = "Include more healthy fats and calories. Seek professional medical advice."
        elif 16 <= bmi < 17:
            status = "Moderate Thinness"
            advice = "Add protein-rich foods and small frequent meals."
        elif 17 <= bmi < 18.5:
            status = "Mild Thinness"
            advice = "Try resistance training and nutrient-dense meals."
        elif 18.5 <= bmi < 25:
            status = "Normal"
            advice = "Maintain your current lifestyle. Great job!"
        elif 25 <= bmi < 30:
            status = "Overweight"
            advice = "Start moderate cardio and reduce refined sugar."
        else:
            status = "Obese"
            advice = "Focus on fiber-rich foods, walk daily, and consult a doctor."

        self.label.configure(text=f"Your BMI: {bmi}\nStatus: {status}")
        self.tips.configure(text=f"Tips: {advice}")

# Frame 4: Calorie Calculator
class CalorieCalculator(ctk.CTkFrame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame
        self.configure(fg_color="#fff3e0")

        ctk.CTkLabel(self, text="🧮 Maintenance Calorie Calculator", font=font_heading).pack(pady=20)

        self.weight = ctk.CTkEntry(self, placeholder_text="Weight (kg)", corner_radius=10)
        self.weight.pack(pady=10)

        self.height = ctk.CTkEntry(self, placeholder_text="Height (cm)", corner_radius=10)
        self.height.pack(pady=10)

        self.age = ctk.CTkEntry(self, placeholder_text="Age", corner_radius=10)
        self.age.pack(pady=10)

        self.gender = ctk.CTkComboBox(self, values=["Male", "Female"], corner_radius=10)
        self.gender.set("Male")
        self.gender.pack(pady=10)

        self.activity_level = ctk.CTkComboBox(self, values=[
            "Sedentary (little/no exercise)",
            "Lightly active (1-3 days/week)",
            "Moderately active (3-5 days/week)",
            "Very active (6-7 days/week)",
            "Extremely active (physical job & workout)"
        ], corner_radius=10)
        self.activity_level.set("Moderately active (3-5 days/week)")
        self.activity_level.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="", font=font_body)
        self.result_label.pack(pady=20)

        ctk.CTkButton(self, text="Calculate Calories", command=self.calculate_calories, corner_radius=12).pack(pady=10)
        ctk.CTkButton(self, text="🏠 Back to Dashboard", command=lambda: switch_frame(DashboardScreen), corner_radius=12).pack(pady=10)

    def calculate_calories(self):
        try:
            weight = float(self.weight.get())
            height = float(self.height.get())
            age = int(self.age.get())
            gender = self.gender.get()
            activity = self.activity_level.get()

            if gender == "Male":
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            multiplier_map = {
                "Sedentary (little/no exercise)": 1.2,
                "Lightly active (1-3 days/week)": 1.375,
                "Moderately active (3-5 days/week)": 1.55,
                "Very active (6-7 days/week)": 1.725,
                "Extremely active (physical job & workout)": 1.9
            }

            maintenance = round(bmr * multiplier_map.get(activity, 1.55))
            tips = ""
            if activity == "Sedentary (little/no exercise)":
                tips = "Try walking 20–30 mins a day to start."
            elif activity == "Lightly active (1-3 days/week)":
                tips = "Great start! Try to increase consistency."
            elif activity == "Moderately active (3-5 days/week)":
                tips = "You're on a healthy path. Keep it up!"
            elif activity == "Very active (6-7 days/week)":
                tips = "You're doing great! Consider rest days."
            elif activity == "Extremely active (physical job & workout)":
                tips = "Ensure enough recovery & nutrition."

            self.result_label.configure(text=f"Estimated Calories: {maintenance} kcal/day\nTip: {tips}")
        except:
            msg.showerror("Input Error", "Please enter valid values.")

# Run the app
if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()
