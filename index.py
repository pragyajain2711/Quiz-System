import tkinter as tk
from tkinter import messagebox
import random

# Create the main window
root = tk.Tk()
root.title("Python Quiz")
root.geometry('800x600')
root.configure(bg="#f0f0f0")

# Global Variables
c = 0  # Score Counter
current_question = 0  # Track question index
username = ""
timer_seconds = 20  # Increased timer per question
questions = [
    ("Which of them is a keyword in Python?", ["range", "def", "Val", "to"], 1),
    ("Which of the following is a built-in function?", ["factorial()", "print()", "seed()", "sqrt()"], 1),
    ("Which is NOT a core Python datatype?", ["Tuple", "Dictionary", "Lists", "Class"], 3),
    ("Who developed Python?", ["Wick Van Rossum", "Rasmus Lerdorf", "Guido Van Rossum", "Niene Stom"], 2),
    ("Which extension is used for Python files?", [".python", ".p", ".pl", ".py"], 3),
]
random.shuffle(questions)  # Shuffle questions for variety
user_answers = [None] * len(questions)

# Frames
start_frame = tk.Frame(root, bg="#f0f0f0")
quiz_frame = tk.Frame(root, bg="#f0f0f0")
scoreboard_frame = tk.Frame(root, bg="#f0f0f0")

# Function to start the quiz
def start_quiz():
    global username
    username = entry.get()
    if username.strip():
        start_frame.pack_forget()
        quiz_frame.pack()
        load_question()
    else:
        label_error.config(text="Please enter a username!", fg="red")

# Function to load a question
def load_question():
    global current_question, timer_seconds
    if current_question < len(questions):
        timer_seconds = 20  # Reset timer for each question
        question, options, _ = questions[current_question]
        label_question.config(text=f"Q{current_question + 1}: {question}")

        # Update Progress Bar
        progress_label.config(text=f"Question {current_question + 1} of {len(questions)}")

        for i in range(4):
            buttons[i].config(text=options[i], bg="#007acc", command=lambda i=i: select_answer(i))

        update_timer()
    else:
        show_scoreboard()

# Function to select an answer
def select_answer(selected_index):
    global user_answers
    user_answers[current_question] = selected_index
    for i in range(4):
        buttons[i].config(bg="#007acc")  # Reset button color
    buttons[selected_index].config(bg="green")  # Highlight selected answer
    root.after(500, next_question)  # Move to next question after selection

# Function to update the timer
def update_timer():
    global timer_seconds
    if timer_seconds > 0:
        timer_label.config(text=f"Time left: {timer_seconds} sec", fg="red")
        timer_seconds -= 1
        root.after(1000, update_timer)
    else:
        next_question()  # Automatically move to the next question if no answer is selected

# Function to go to the next question
def next_question():
    global current_question
    if user_answers[current_question] is None:
        user_answers[current_question] = -1  # Mark as unanswered
    current_question += 1
    load_question()

# Function to go to the previous question
def previous_question():
    global current_question
    if current_question > 0:
        current_question -= 1
        load_question()

# Function to quit the quiz
def quit_quiz():
    response = messagebox.askyesno("Quit", "Are you sure you want to quit the quiz?")
    if response:
        root.destroy()

# Function to display the scoreboard
def show_scoreboard():
    global c
    quiz_frame.pack_forget()
    scoreboard_frame.pack()

    # Calculate Score
    for i, (question, options, correct_index) in enumerate(questions):
        if user_answers[i] == correct_index:
            c += 1

    label_score.config(text=f"{username}, Your Final Score: {c}/{len(questions)}", fg="green", font=("Arial", 30, "bold"))

    result_text = "Correct Answers:\n"
    for i, (question, options, correct_index) in enumerate(questions):
        user_answer_text = f"Your Answer: {options[user_answers[i]]}" if user_answers[i] != -1 else "Not Answered"
        correct_text = f"Correct Answer: {options[correct_index]}"
        result_text += f"Q{i+1}: {user_answer_text} | {correct_text}\n"

    label_result.config(text=result_text, font=("Arial", 14))

# Start Screen UI
label_title = tk.Label(start_frame, text="Welcome to Python Quiz", font=("Arial", 40, "bold"), bg="#f0f0f0", fg="#333")
label_title.pack(pady=20)

label_username = tk.Label(start_frame, text="Enter Username:", font=("Arial", 20), bg="#f0f0f0")
label_username.pack()

entry = tk.Entry(start_frame, font=("Arial", 20), width=20)
entry.pack(pady=10)

label_error = tk.Label(start_frame, text="", font=("Arial", 14), bg="#f0f0f0")
label_error.pack()

start_button = tk.Button(start_frame, text="Start Quiz", font=("Arial", 18), bg="green", fg="white", command=start_quiz)
start_button.pack(pady=20)

start_frame.pack()

# Quiz Screen UI
label_question = tk.Label(quiz_frame, text="", font=("Arial", 24, "bold"), bg="#f0f0f0", wraplength=700)
label_question.pack(pady=20)

progress_label = tk.Label(quiz_frame, text="", font=("Arial", 16), bg="#f0f0f0", fg="blue")
progress_label.pack()

buttons = []
for _ in range(4):
    btn = tk.Button(quiz_frame, text="", font=("Arial", 18), width=20, height=2, bg="#007acc", fg="white")
    btn.pack(pady=10)
    buttons.append(btn)

timer_label = tk.Label(quiz_frame, text="", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="red")
timer_label.pack(pady=10)

button_frame = tk.Frame(quiz_frame, bg="#f0f0f0")
button_frame.pack(pady=20)

prev_button = tk.Button(button_frame, text="Previous", font=("Arial", 16), bg="gray", fg="white", command=previous_question)
prev_button.grid(row=0, column=0, padx=10)

next_button = tk.Button(button_frame, text="Next", font=("Arial", 16), bg="blue", fg="white", command=next_question)
next_button.grid(row=0, column=1, padx=10)

quit_button = tk.Button(button_frame, text="Quit", font=("Arial", 16), bg="red", fg="white", command=quit_quiz)
quit_button.grid(row=0, column=2, padx=10)

# Scoreboard Screen UI
label_score = tk.Label(scoreboard_frame, text="", font=("Arial", 28, "bold"), bg="#f0f0f0", fg="#333")
label_score.pack(pady=20)

label_result = tk.Label(scoreboard_frame, text="", font=("Arial", 14), bg="#f0f0f0", justify="left")
label_result.pack(pady=10)

root.mainloop()
