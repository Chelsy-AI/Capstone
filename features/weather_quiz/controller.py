"""
Weather Quiz Controller - Manages quiz logic and GUI interactions
"""

import tkinter as tk
from tkinter import messagebox
import threading
import traceback

from .quiz_generator import WeatherQuizGenerator


class WeatherQuizController:
    """
    Controller for the Weather Quiz feature
    Manages quiz generation, display, scoring, and user interactions
    """
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller
        
        # Quiz state
        self.quiz_generator = WeatherQuizGenerator()
        self.current_questions = []
        self.current_question_index = 0
        self.user_answers = []
        self.score = 0
        self.quiz_started = False
        self.quiz_completed = False
        
        # GUI components
        self.question_widgets = []
        self.quiz_frame = None
        
    def build_page(self, window_width, window_height):
        """Build the quiz page"""
        try:
            self._add_back_button()
            self._build_header(window_width)
            self._build_quiz_area(window_width, window_height)
            
            # Start generating quiz in background
            self._generate_quiz_async()
            
        except Exception as e:
            traceback.print_exc()
    
    def _add_back_button(self):
        """Add back button to return to main page"""
        back_btn = tk.Button(
            self.app,
            text="← Back",
            command=lambda: self.gui.show_page("main"),
            bg="grey",
            fg="black",
            font=("Arial", 12, "bold"),
            relief="raised",
            borderwidth=2,
            width=8,
            height=1,
            activeforeground="black",
            activebackground="lightgrey",
            highlightthickness=0
        )
        back_btn.place(x=50, y=30, anchor="center")
        self.gui.widgets.append(back_btn)
    
    def _build_header(self, window_width):
        """Build quiz header with title and info"""
        # Main title
        title_main = self._create_black_label(
            self.app,
            text="Weather Quiz Challenge",
            font=("Arial", int(28 + window_width/40), "bold"),
            x=window_width/2,
            y=80
        )
        self.gui.widgets.append(title_main)
        
        # Subtitle
        subtitle = self._create_black_label(
            self.app,
            text="Test your weather knowledge with real data!",
            font=("Arial", int(16 + window_width/80)),
            x=window_width/2,
            y=120
        )
        self.gui.widgets.append(subtitle)
        
        # Info button
        info_btn = tk.Button(
            self.app,
            text="i",
            command=self._show_quiz_info,
            bg="lightblue",
            fg="black",
            font=("Arial", int(16 + window_width/80), "bold"),
            relief="raised",
            borderwidth=2,
            width=3,
            height=1,
            activeforeground="black",
            activebackground="lightcyan",
            highlightthickness=0
        )
        info_btn.place(x=window_width/2 + 280, y=80, anchor="center")
        self.gui.widgets.append(info_btn)
    
    def _build_quiz_area(self, window_width, window_height):
        """Build the main quiz display area"""
        quiz_y = 170
        quiz_height = window_height - 220
        quiz_width = window_width - 100
        
        # Create frame for quiz content
        canvas_bg = self._get_canvas_bg_color()
        self.quiz_frame = tk.Frame(
            self.app,
            bg=canvas_bg,
            relief="solid",
            borderwidth=2,
            highlightthickness=0
        )
        self.quiz_frame.place(
            x=50,
            y=quiz_y,
            width=quiz_width,
            height=quiz_height
        )
        self.gui.widgets.append(self.quiz_frame)
        
        # Loading message
        loading_label = self._create_black_label(
            self.quiz_frame,
            text="🧠 Generating your weather quiz...\nPlease wait while we analyze the data!",
            font=("Arial", 16),
            x=quiz_width/2,
            y=quiz_height/2
        )
    
    def _generate_quiz_async(self):
        """Generate quiz questions in background thread"""
        def generate():
            try:
                # Generate questions
                self.current_questions = self.quiz_generator.generate_quiz()
                
                # Update UI on main thread
                self.app.after(0, self._display_quiz_start)
                
            except Exception as e:
                error_msg = f"Error generating quiz: {str(e)}"
                self.app.after(0, lambda: self._show_error(error_msg))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _display_quiz_start(self):
        """Display quiz start screen"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            frame_width = self.quiz_frame.winfo_reqwidth() or 600
            frame_height = self.quiz_frame.winfo_reqheight() or 400
            
            # Welcome message
            welcome_label = self._create_black_label(
                self.quiz_frame,
                text="🌤️ Weather Quiz Ready!",
                font=("Arial", 24, "bold"),
                x=frame_width/2,
                y=100
            )
            
            # Instructions
            instructions = self._create_black_label(
                self.quiz_frame,
                text=f"You'll answer {len(self.current_questions)} questions about weather patterns.\nEach question is based on real weather data.\n\nReady to test your meteorological knowledge?",
                font=("Arial", 14),
                x=frame_width/2,
                y=180,
                justify="center"
            )
            
            # Start button
            start_btn = tk.Button(
                self.quiz_frame,
                text="🚀 Start Quiz",
                command=self._start_quiz,
                bg="lightgreen",
                fg="black",
                font=("Arial", 16, "bold"),
                relief="raised",
                borderwidth=3,
                width=15,
                height=2,
                activeforeground="black",
                activebackground="lightblue",
                highlightthickness=0
            )
            start_btn.place(x=frame_width/2, y=280, anchor="center")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _start_quiz(self):
        """Start the quiz"""
        try:
            self.quiz_started = True
            self.current_question_index = 0
            self.user_answers = []
            self.score = 0
            self.quiz_completed = False
            
            self._display_current_question()
            
        except Exception as e:
            self._show_error(str(e))
    
    def _display_current_question(self):
        """Display the current question"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            if self.current_question_index >= len(self.current_questions):
                self._display_quiz_results()
                return
            
            question = self.current_questions[self.current_question_index]
            frame_width = self.quiz_frame.winfo_reqwidth() or 600
            
            # Progress indicator
            progress_text = f"Question {self.current_question_index + 1} of {len(self.current_questions)}"
            progress_label = self._create_black_label(
                self.quiz_frame,
                text=progress_text,
                font=("Arial", 12, "bold"),
                x=frame_width/2,
                y=30
            )
            
            # Question text
            question_label = self._create_black_label(
                self.quiz_frame,
                text=question["question"],
                font=("Arial", 16, "bold"),
                x=frame_width/2,
                y=80,
                justify="center"
            )
            
            # Answer choices
            self.selected_answer = tk.StringVar()
            
            for i, choice in enumerate(question["choices"]):
                radio_btn = tk.Radiobutton(
                    self.quiz_frame,
                    text=choice,
                    variable=self.selected_answer,
                    value=choice,
                    font=("Arial", 14),
                    fg="black",
                    bg=self._get_canvas_bg_color(),
                    selectcolor="lightblue",
                    activebackground=self._get_canvas_bg_color(),
                    activeforeground="black",
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0
                )
                radio_btn.place(x=50, y=140 + i * 40, anchor="w")
            
            # Next button
            next_btn = tk.Button(
                self.quiz_frame,
                text="Next Question →",
                command=self._answer_question,
                bg="lightblue",
                fg="black",
                font=("Arial", 14, "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=1,
                activeforeground="black",
                activebackground="lightgreen",
                highlightthickness=0
            )
            next_btn.place(x=frame_width/2, y=350, anchor="center")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _answer_question(self):
        """Process the user's answer and move to next question"""
        try:
            if not hasattr(self, 'selected_answer') or not self.selected_answer.get():
                messagebox.showwarning("No Answer", "Please select an answer before continuing.")
                return
            
            question = self.current_questions[self.current_question_index]
            user_answer = self.selected_answer.get()
            correct_answer = question["correct_answer"]
            
            # Store user's answer
            self.user_answers.append({
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "explanation": question["explanation"],
                "is_correct": user_answer == correct_answer
            })
            
            # Update score
            if user_answer == correct_answer:
                self.score += 1
            
            # Move to next question
            self.current_question_index += 1
            self._display_current_question()
            
        except Exception as e:
            self._show_error(str(e))
    
    def _display_quiz_results(self):
        """Display quiz results and score"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            self.quiz_completed = True
            frame_width = self.quiz_frame.winfo_reqwidth() or 600
            
            # Calculate percentage
            percentage = round((self.score / len(self.current_questions)) * 100)
            
            # Results header
            if percentage >= 80:
                emoji = "🌟"
                message = "Excellent! You're a weather expert!"
            elif percentage >= 60:
                emoji = "☀️"
                message = "Good job! You know your weather!"
            elif percentage >= 40:
                emoji = "⛅"
                message = "Not bad! Keep learning about weather!"
            else:
                emoji = "🌧️"
                message = "Keep studying! Weather is fascinating!"
            
            results_header = self._create_black_label(
                self.quiz_frame,
                text=f"{emoji} Quiz Complete! {emoji}",
                font=("Arial", 20, "bold"),
                x=frame_width/2,
                y=50
            )
            
            score_label = self._create_black_label(
                self.quiz_frame,
                text=f"Your Score: {self.score}/{len(self.current_questions)} ({percentage}%)",
                font=("Arial", 18, "bold"),
                x=frame_width/2,
                y=90
            )
            
            message_label = self._create_black_label(
                self.quiz_frame,
                text=message,
                font=("Arial", 14),
                x=frame_width/2,
                y=130
            )
            
            # Buttons
            review_btn = tk.Button(
                self.quiz_frame,
                text="📊 Review Answers",
                command=self._show_detailed_results,
                bg="lightblue",
                fg="black",
                font=("Arial", 12, "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=1,
                activeforeground="black",
                activebackground="lightcyan",
                highlightthickness=0
            )
            review_btn.place(x=frame_width/2 - 100, y=200, anchor="center")
            
            retry_btn = tk.Button(
                self.quiz_frame,
                text="🔄 Try Again",
                command=self._restart_quiz,
                bg="lightgreen",
                fg="black",
                font=("Arial", 12, "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=1,
                activeforeground="black",
                activebackground="lightblue",
                highlightthickness=0
            )
            retry_btn.place(x=frame_width/2 + 100, y=200, anchor="center")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _show_detailed_results(self):
        """Show detailed answer review"""
        try:
            results_text = "🌤️ Weather Quiz Results Review\n"
            results_text += "=" * 50 + "\n\n"
            
            for i, answer_data in enumerate(self.user_answers):
                results_text += f"Question {i+1}: {answer_data['question']}\n"
                results_text += f"Your Answer: {answer_data['user_answer']}\n"
                results_text += f"Correct Answer: {answer_data['correct_answer']}\n"
                
                if answer_data['is_correct']:
                    results_text += "✅ Correct!\n"
                else:
                    results_text += "❌ Incorrect\n"
                
                results_text += f"Explanation: {answer_data['explanation']}\n"
                results_text += "-" * 30 + "\n\n"
            
            results_text += f"Final Score: {self.score}/{len(self.current_questions)} ({round((self.score/len(self.current_questions))*100)}%)"
            
            messagebox.showinfo("Quiz Results Review", results_text)
            
        except Exception as e:
            self._show_error(str(e))
    
    def _restart_quiz(self):
        """Restart the quiz with new questions"""
        try:
            self.quiz_started = False
            self.quiz_completed = False
            self.current_question_index = 0
            self.user_answers = []
            self.score = 0
            
            # Clear quiz frame and show loading
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            loading_label = self._create_black_label(
                self.quiz_frame,
                text="🔄 Generating new quiz questions...",
                font=("Arial", 16),
                x=300,
                y=200
            )
            
            # Generate new quiz
            self._generate_quiz_async()
            
        except Exception as e:
            self._show_error(str(e))
    
    def _show_quiz_info(self):
        """Show information about the quiz"""
        info_text = """🌤️ Weather Quiz Information

📊 About This Quiz:
• 5 smart questions based on real weather data
• Questions analyze patterns from actual CSV files
• Multiple choice format with explanations
• Instant feedback and scoring

🧠 Question Types:
• Temperature trends and comparisons
• Weather pattern analysis
• Seasonal variations
• Data interpretation challenges
• Fun weather facts

🎯 Scoring:
• 80%+ = Weather Expert ⭐
• 60%+ = Weather Enthusiast ☀️
• 40%+ = Weather Student ⛅
• <40% = Keep Learning! 🌧️

📈 Educational Value:
Each question teaches you something new about weather patterns and helps you understand meteorological concepts through real data analysis.

Good luck with your weather knowledge challenge!"""
        
        messagebox.showinfo("Weather Quiz Info", info_text)
    
    def _show_error(self, error_msg):
        """Show error message"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            error_label = self._create_black_label(
                self.quiz_frame,
                text=f"❌ Error: {error_msg}\n\nPlease try refreshing or go back to the main page.",
                font=("Arial", 14),
                x=300,
                y=200,
                justify="center"
            )
            
        except Exception as e:
            pass
    
    def _create_black_label(self, parent, text, font, x, y, anchor="center", **kwargs):
        """Create a label with black text and transparent background"""
        canvas_bg = self._get_canvas_bg_color()
        
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg="black",
            bg=canvas_bg,
            anchor=anchor,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            **kwargs
        )
        
        label.place(x=x, y=y, anchor=anchor)
        return label
    
    def _get_canvas_bg_color(self):
        """Get the current canvas background color"""
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"
        except:
            return "#87CEEB"
    
    def handle_theme_change(self):
        """Handle theme changes"""
        try:
            canvas_bg = self._get_canvas_bg_color()
            if self.quiz_frame:
                self.quiz_frame.configure(bg=canvas_bg)
        except Exception as e:
            pass
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.quiz_frame:
                for widget in self.quiz_frame.winfo_children():
                    widget.destroy()
        except Exception as e:
            pass