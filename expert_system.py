import tkinter as tk
from tkinter import messagebox

class ExpertSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Clinical Decision Support System")
        self.root.geometry("750x500")
        self.root.resizable(False, False)
        
        # Color palette for a professional, premium dark medical theme
        self.BG_DARK = "#0B132B"       # Deep tech navy background
        self.PANEL_BG = "#1C2541"      # Dark slate blue for data cards
        self.PRIMARY_TEAL = "#4FD1C5"  # Vibrant glow teal for buttons/highlights
        self.TEXT_LIGHT = "#F8F9FA"    # High contrast white for crisp readability
        self.TEXT_MUTED = "#94A3B8"    # Soft muted blue-gray for labels
        self.ACCENT_RED = "#FF6B6B"    # Bright coral red for positive evaluations
        self.BORDER_COLOR = "#3A4F7C"  # Clean borders for panels

        self.root.configure(bg=self.BG_DARK)
        
        # Rule Base Definition
        self.rules = [
            {"if": ["fever", "cough"], "then": "cold"},
            {"if": ["cold", "loss_of_taste"], "then": "covid_risk"},
            {"if": ["fever", "rash"], "then": "measles"},
            {"if": ["headache", "blurry_vision"], "then": "migraine"}
        ]

        # --- BACKGROUND CANVAS ---
        # Keeps the exact same layout structure as before, using a styled solid canvas background
        self.canvas = tk.Canvas(root, width=750, height=500, bg=self.BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # --- PANELS OVER BACKGROUND ---
        # Left Panel: Patient Symptoms Card
        left_card = tk.Label(root, bg=self.PANEL_BG, bd=0, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        self.canvas.create_window(210, 260, window=left_card, width=340, height=380)
        
        tk.Label(left_card, text="Patient Symptoms", font=("Helvetica", 14, "bold"), bg=self.PANEL_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=20, pady=(20, 5))
        tk.Label(left_card, text="Check observed clinical signs:", font=("Helvetica", 9), bg=self.PANEL_BG, fg=self.TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 10))

        # Checkbox list setup
        self.symptoms = ["fever", "cough", "loss_of_taste", "rash", "headache", "blurry_vision"]
        self.checkbox_vars = {}

        for symptom in self.symptoms:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(
                left_card, 
                text=f"  {symptom.replace('_', ' ').title()}", 
                variable=var, 
                font=("Helvetica", 11), 
                bg=self.PANEL_BG,
                activebackground=self.PANEL_BG,
                fg=self.TEXT_LIGHT,
                selectcolor=self.BG_DARK,  # Changes the checkmark square background color
                activeforeground=self.TEXT_LIGHT,
                anchor="w"
            )
            cb.pack(fill="x", padx=25, pady=5)
            self.checkbox_vars[symptom] = var

        # Diagnose Action Button
        self.btn_diagnose = tk.Button(
            left_card, 
            text="ANALYZE CASE", 
            font=("Helvetica", 11, "bold"), 
            bg=self.PRIMARY_TEAL, 
            fg=self.BG_DARK, 
            activebackground="#38B2AC",
            activeforeground=self.BG_DARK,
            bd=0,
            pady=8,
            command=self.diagnose,
            cursor="hand2"
        )
        self.btn_diagnose.pack(fill="x", side="bottom", padx=25, pady=20)

        # Right Panel: Output Monitoring Card
        right_card = tk.Label(root, bg=self.PANEL_BG, bd=0, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        self.canvas.create_window(540, 260, window=right_card, width=280, height=380)

        tk.Label(right_card, text="Inference Engine Log", font=("Helvetica", 12, "bold"), bg=self.PANEL_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15, pady=15)
        
        self.log_label = tk.Label(
            right_card, 
            text="Awaiting system inputs...\nCheck symptoms and press\n'Analyze Case'.", 
            justify="left", font=("Courier", 9), bg=self.BG_DARK, fg=self.TEXT_MUTED, 
            anchor="nw", bd=1, relief="solid", highlightcolor=self.BORDER_COLOR, padx=8, pady=8
        )
        self.log_label.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Bottom Conclusion Section inside the right card
        conclusion_frame = tk.Frame(right_card, bg="#1F2A4A", bd=0)
        conclusion_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        tk.Label(conclusion_frame, text="FINAL EVALUATION:", font=("Helvetica", 8, "bold"), bg="#1F2A4A", fg=self.TEXT_MUTED).pack(anchor="w", padx=10, pady=(5, 0))
        self.result_label = tk.Label(conclusion_frame, text="None", font=("Helvetica", 12, "bold"), bg="#1F2A4A", fg=self.ACCENT_RED)
        self.result_label.pack(anchor="w", padx=10, pady=(0, 5))

    def diagnose(self):
        facts = set()
        for symptom, var in self.checkbox_vars.items():
            if var.get():
                facts.add(symptom)

        if not facts:
            messagebox.showwarning("Input Missing", "Please tick at least one symptom field.")
            return

        inferences_made = True
        steps_logged = []
        initial_facts = list(facts)

        while inferences_made:
            inferences_made = False
            for rule in self.rules:
                if all(condition in facts for condition in rule["if"]):
                    if rule["then"] not in facts:
                        facts.add(rule["then"])
                        steps_logged.append(f"[MATCH] {str(rule['if'])}\n-> DEDUCED: {rule['then'].upper()}")
                        inferences_made = True

        log_display = "\n\n".join(steps_logged) if steps_logged else "[LOG] Symptoms logged.\nNo rules matched."
        self.log_label.config(text=log_display, fg=self.PRIMARY_TEAL if steps_logged else self.TEXT_MUTED)

        conclusions = [f.replace("_", " ").upper() for f in facts if f not in initial_facts]
        final_text = ", ".join(conclusions) if conclusions else "NEGATIVE"
        self.result_label.config(text=final_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpertSystemUI(root)
    root.mainloop()