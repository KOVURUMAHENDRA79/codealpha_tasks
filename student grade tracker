'''please run this code "pip install ttkbootstrap openpyxl"
in the terminal. Before running the below code, so that required libraries are installed properly '''
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Listbox, Canvas, Scrollbar, filedialog
from tkinter import N, S, E, W, END
import json
import os
import openpyxl
import logging
from ttkbootstrap.icons import Icon

DATA_FILE = "student_grades.json"
EXCEL_FILE = "student_grades.xlsx"
LOG_FILE = "error_log.txt"

# Configure error logging
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_average(grades):
    if not grades:
        return 0.0
    return sum(grades.values()) / len(grades)

def get_letter_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"

class GradeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Tracker")
        self.data = load_data()
        self.subject_entries = {}

        # Main frame with padding
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky=NSEW)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # Student Name
        ttk.Label(self.main_frame, text="Student Name:").grid(row=0, column=0, pady=5, sticky=W)
        self.name_entry = ttk.Entry(self.main_frame)
        self.name_entry.grid(row=0, column=1, pady=5, sticky=EW)

        # Search bar with icon
        ttk.Label(self.main_frame, text="🔍 Search Student:").grid(row=0, column=2, padx=10, sticky=W)
        self.search_entry = ttk.Entry(self.main_frame)
        self.search_entry.grid(row=0, column=3, pady=5, padx=5, sticky=EW)
        self.search_entry.bind("<KeyRelease>", self.filter_students)

        # Subjects Section
        ttk.Label(self.main_frame, text="Subjects and Grades:").grid(row=1, column=0, pady=5, sticky=W)

        # Scrollable Canvas Frame for subjects
        self.subject_canvas = Canvas(self.main_frame, height=150)
        self.subject_canvas.grid(row=2, column=0, columnspan=2, sticky=EW)

        self.scrollbar = Scrollbar(self.main_frame, orient="vertical", command=self.subject_canvas.yview)
        self.scrollbar.grid(row=2, column=2, sticky=NS)
        self.subject_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.subject_inner_frame = ttk.Frame(self.subject_canvas)
        self.subject_canvas.create_window((0, 0), window=self.subject_inner_frame, anchor="nw")
        self.subject_inner_frame.bind("<Configure>", lambda e: self.subject_canvas.configure(scrollregion=self.subject_canvas.bbox("all")))

        self.add_subject_row()

        self.add_subject_btn = ttk.Button(self.main_frame, text="Add Another Subject", command=self.add_subject_row)
        self.add_subject_btn.grid(row=3, column=0, columnspan=2, pady=5, sticky=EW)

        # Average and Letter Grade Labels
        self.avg_label = ttk.Label(self.main_frame, text="Average: 0.00")
        self.avg_label.grid(row=5, column=0, columnspan=2, pady=5, sticky=W)
        self.letter_label = ttk.Label(self.main_frame, text="Grade: F", foreground="red")
        self.letter_label.grid(row=5, column=1, columnspan=2, pady=5, sticky=E)

        # Save Button
        self.save_btn = ttk.Button(self.main_frame, text="Save Student Data", command=self.save_student_data)
        self.save_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky=EW)

        # Listbox for students
        ttk.Label(self.main_frame, text="Students:").grid(row=1, column=2, padx=10, sticky=W)
        self.student_listbox = Listbox(self.main_frame, height=15)
        self.student_listbox.grid(row=2, column=3, rowspan=4, padx=10, sticky=N+S+EW)
        self.student_listbox.bind('<<ListboxSelect>>', self.on_student_select)

        # Edit/Delete/Export/Backup/Restore Buttons
        self.edit_btn = ttk.Button(self.main_frame, text="Edit Selected", command=self.edit_student)
        self.edit_btn.grid(row=5, column=3, padx=10, pady=5, sticky=EW)

        self.delete_btn = ttk.Button(self.main_frame, text="Delete Selected", command=self.delete_student)
        self.delete_btn.grid(row=6, column=3, padx=10, pady=5, sticky=EW)

        self.export_btn = ttk.Button(self.main_frame, text="Export to Excel", command=self.export_to_excel)
        self.export_btn.grid(row=7, column=3, padx=10, pady=5, sticky=EW)

        # Grid configuration
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(3, weight=1)

        self.populate_student_listbox()

    def add_subject_row(self):
        row = len(self.subject_entries)
        subject_entry = ttk.Entry(self.subject_inner_frame)
        grade_entry = ttk.Entry(self.subject_inner_frame)

        subject_entry.grid(row=row, column=0, padx=5, pady=2, sticky=EW)
        grade_entry.grid(row=row, column=1, padx=5, pady=2, sticky=EW)

        self.subject_entries[row] = (subject_entry, grade_entry)
        grade_entry.bind("<KeyRelease>", lambda e: self.update_average_label())
        grade_entry.bind("<Return>", lambda e: self.add_subject_row())

    def update_average_label(self):
        grades = {}
        subjects_seen = set()
        duplicate_found = False

        for subject_entry, grade_entry in self.subject_entries.values():
            subject = subject_entry.get().strip().lower()
            grade_str = grade_entry.get().strip()
            if subject:
                if subject in subjects_seen:
                    duplicate_found = True
                    continue
                subjects_seen.add(subject)

            if subject and grade_str:
                try:
                    grades[subject] = float(grade_str)
                except ValueError:
                    pass

        avg = calculate_average(grades)
        letter = get_letter_grade(avg)
        self.avg_label.config(text=f"Average: {avg:.2f}")
        color = {"A": "green", "B": "darkorange", "C": "orange", "D": "orangered", "F": "red"}.get(letter, "black")
        self.letter_label.config(text=f"Grade: {letter}", foreground=color)

        if duplicate_found:
            messagebox.showwarning("Duplicate Subject", "Duplicate subject names found. Please correct them.")

    def save_student_data(self):
        try:
            name = self.name_entry.get().strip().title()
            if not name:
                messagebox.showwarning("Missing Name", "Please enter the student's name.")
                return

            grades = {}
            for subject_entry, grade_entry in self.subject_entries.values():
                subject = subject_entry.get().strip()
                grade_str = grade_entry.get().strip()
                if subject and grade_str:
                    try:
                        grades[subject] = float(grade_str)
                    except ValueError:
                        messagebox.showerror("Invalid Grade", f"Grade for {subject} is not a number.")
                        return

            if not grades:
                messagebox.showwarning("No Grades", "Please enter at least one subject and grade.")
                return

            average = calculate_average(grades)
            letter = get_letter_grade(average)

            self.data[name] = {
                "grades": grades,
                "average": average,
                "letter": letter
            }

            save_data(self.data)
            messagebox.showinfo("Success", f"Data for {name} saved successfully!")
            self.clear_entries()
            self.populate_student_listbox()

        except Exception as e:
            logging.error(str(e))
            messagebox.showerror("Error", "An unexpected error occurred.")

    def clear_entries(self):
        self.name_entry.delete(0, END)
        for widgets in self.subject_inner_frame.winfo_children():
            widgets.destroy()
        self.subject_entries = {}
        self.add_subject_row()
        self.avg_label.config(text="Average: 0.00")
        self.letter_label.config(text="Grade: F", foreground="red")

    def populate_student_listbox(self, filter_text=""):
        self.student_listbox.delete(0, END)
        students = sorted(self.data.items(), key=lambda x: x[1]['average'], reverse=True)
        for student_name, info in students:
            if filter_text.lower() in student_name.lower():
                self.student_listbox.insert(END, student_name)

    def filter_students(self, event):
        text = self.search_entry.get().strip()
        self.populate_student_listbox(filter_text=text)

    def on_student_select(self, event):
        pass

    def edit_student(self):
        selected = self.student_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student to edit.")
            return
        student_name = self.student_listbox.get(selected[0])
        self.load_student_into_form(student_name)

    def delete_student(self):
        selected = self.student_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student to delete.")
            return
        student_name = self.student_listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}?")
        if confirm:
            del self.data[student_name]
            save_data(self.data)
            messagebox.showinfo("Deleted", f"{student_name} has been deleted.")
            self.populate_student_listbox()
            self.clear_entries()

    def load_student_into_form(self, student_name):
        info = self.data.get(student_name)
        if not info:
            messagebox.showerror("Error", f"No data found for {student_name}")
            return

        self.clear_entries()
        self.name_entry.insert(0, student_name)
        for i, (subject, grade) in enumerate(info["grades"].items()):
            if i > 0:
                self.add_subject_row()
            subject_entry, grade_entry = self.subject_entries[i]
            subject_entry.insert(0, subject)
            grade_entry.insert(0, str(grade))

        self.avg_label.config(text=f"Average: {info['average']:.2f}")
        color = {"A": "green", "B": "darkorange", "C": "orange", "D": "orangered", "F": "red"}.get(info['letter'], "black")
        self.letter_label.config(text=f"Grade: {info['letter']}", foreground=color)

    def export_to_excel(self):
        if not self.data:
            messagebox.showwarning("No Data", "No student data to export.")
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Student Grades"

        ws.append(["Student Name", "Average", "Letter Grade", "Subjects"])

        for name, info in self.data.items():
            subjects_str = ", ".join(f"{sub}: {grd}" for sub, grd in info["grades"].items())
            ws.append([name, info["average"], info["letter"], subjects_str])

        wb.save(EXCEL_FILE)
        messagebox.showinfo("Exported", f"Data exported to {EXCEL_FILE} successfully!")

if __name__ == "__main__":
    app = ttk.Window(themename="litera")
    GradeTrackerApp(app)
    app.mainloop()
