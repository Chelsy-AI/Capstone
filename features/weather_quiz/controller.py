"""
Minimal Weather Quiz Controller - Simplified for debugging
This version focuses on basic functionality to ensure the database works correctly.
"""

import tkinter as tk
from tkinter import messagebox
import traceback
from typing import List, Dict, Any, Optional

# Import the database functions directly to test
try:
    from .questions_database import get_all_questions, get_random_questions
    DATABASE_AVAILABLE = True
    print("✓ Database import successful")
except ImportError as e:
    print(f"❌ Database import failed: {e}")
    DATABASE_AVAILABLE = False


class WeatherQuizController:
    """Simplified quiz controller for debugging."""
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller
        
        # Quiz state
        self.current_questions: List[Dict[str, Any]] = []
        self.current_question_index: int = 0
        self.user_answers: List[Dict[str, Any]] = []
        self.score: int = 0
        self.quiz_started: bool = False
        
        # GUI components
        self.quiz_frame: Optional[tk.Frame] = None
        
        # Test database immediately
        self._test_database()
        
    def _test_database(self):
        """Test if the database is working."""
        print("Testing database...")
        
        if not DATABASE_AVAILABLE:
            print("❌ Database module not available")
            return
        
        try:
            all_questions = get_all_questions()
            print(f"✓ Database has {len(all_questions)} questions")
            
            if len(all_questions) > 0:
                print(f"✓ First question: {all_questions[0]['question'][:50]}...")
                
                # Test random selection
                random_questions = get_random_questions(3)
                print(f"✓ Random selection works: {len(random_questions)} questions selected")
            else:
                print("❌ Database is empty")
                
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            traceback.print_exc()
    
    def _get_text(self, key):
        """Get translated text using the language controller."""
        try:
            # Try multiple ways to access the language controller
            lang_controller = None
            
            # Method 1: Direct attribute
            if hasattr(self.app, 'language_controller'):
                lang_controller = self.app.language_controller
            
            # Method 2: Through GUI controller
            elif hasattr(self.gui, 'language_controller'):
                lang_controller = self.gui.language_controller
            
            # Method 3: Look for language_ctrl
            elif hasattr(self.app, 'language_ctrl'):
                lang_controller = self.app.language_ctrl
            
            if lang_controller and hasattr(lang_controller, 'get_text'):
                return lang_controller.get_text(key)
            
            # Fallback to hardcoded English if no language controller
            fallback_translations = {
                'weather_quiz_title': 'Weather Quiz',
                'back': '← Back',
                'quiz_ready': 'Quiz Ready!',
                'quiz_description': 'This comprehensive weather quiz is based on meteorological data from five major global cities: Phoenix, Ahmedabad, Denver, Columbus, and Lebrija. Test your knowledge of climate patterns, temperature variations, and weather phenomena.',
                'click_start_to_begin': 'Click Start to begin the quiz!',
                'start_quiz': 'Start Quiz'
            }
            
            return fallback_translations.get(key, key)
            
        except Exception as e:
            print(f"Translation error for key '{key}': {e}")
            # Return English fallback
            fallback_translations = {
                'weather_quiz_title': 'Weather Quiz',
                'back': '← Back',
                'quiz_ready': 'Quiz Ready!',
                'quiz_description': 'This comprehensive weather quiz is based on meteorological data from five major global cities: Phoenix, Ahmedabad, Denver, Columbus, and Lebrija. Test your knowledge of climate patterns, temperature variations, and weather phenomena.',
                'click_start_to_begin': 'Click Start to begin the quiz!',
                'start_quiz': 'Start Quiz'
            }
            return fallback_translations.get(key, key)
    
    def build_page(self, window_width: int, window_height: int):
        """Build a simplified quiz page for testing."""
        try:
            print(f"Building quiz page: {window_width}x{window_height}")
            
            # Add back button
            self._add_back_button()
            
            # Add title with language support
            title_text = f"🌤️ {self._get_text('weather_quiz_title')}"
            title_label = tk.Label(
                self.app,
                text=title_text,
                font=("Arial", 24, "bold"),
                fg="black",
                bg="#87CEEB"
            )
            title_label.place(x=window_width//2, y=70, anchor="center")
            self.gui.widgets.append(title_label)
            
            # Create main quiz area
            self._build_quiz_area(window_width, window_height)
            
            # Test loading questions
            self._load_quiz_questions()
            
        except Exception as e:
            print(f"❌ Error building page: {e}")
            traceback.print_exc()
            self._show_error(f"Page build error: {str(e)}")
    
    def _add_back_button(self):
        """Add back button."""
        back_text = self._get_text('back')
        back_button = tk.Button(
            self.app,
            text=back_text,
            command=lambda: self.gui.show_page("main"),
            bg="grey",
            fg="black",
            font=("Arial", 12, "bold"),
            width=8,
            height=1
        )
        back_button.place(x=50, y=30, anchor="center")
        self.gui.widgets.append(back_button)
    
    def _build_quiz_area(self, window_width: int, window_height: int):
        """Build the quiz display area."""
        try:
            quiz_start_y = 120
            quiz_height = window_height - 200
            quiz_width = min(window_width - 100, 700)
            quiz_x = (window_width - quiz_width) // 2
            
            self.quiz_frame = tk.Frame(
                self.app,
                bg="#87CEEB",
                relief="solid",
                borderwidth=2
            )
            self.quiz_frame.place(
                x=quiz_x,
                y=quiz_start_y,
                width=quiz_width,
                height=quiz_height
            )
            self.gui.widgets.append(self.quiz_frame)
            
            print(f"✓ Quiz frame created: {quiz_width}x{quiz_height} at ({quiz_x}, {quiz_start_y})")
            
        except Exception as e:
            print(f"❌ Error creating quiz area: {e}")
            traceback.print_exc()
    
    def _load_quiz_questions(self):
        """Load and test quiz questions."""
        try:
            print("Loading quiz questions...")
            
            if not DATABASE_AVAILABLE:
                self._show_message("❌ Database Not Available", 
                                   "The questions database could not be imported.\n"
                                   "Check that questions_database.py exists and is valid.")
                return
            
            # Test loading questions
            all_questions = get_all_questions()
            if not all_questions:
                self._show_message("❌ No Questions Found", 
                                   "The database returned no questions.\n"
                                   "Check the questions_database.py file.")
                return
            
            # Load 5 random questions
            self.current_questions = get_random_questions(5)
            if not self.current_questions:
                self._show_message("❌ Random Selection Failed", 
                                   "Could not select random questions from database.")
                return
            
            print(f"✓ Loaded {len(self.current_questions)} questions successfully")
            
            # Show success message with start option
            self._show_quiz_ready()
            
        except Exception as e:
            print(f"❌ Error loading questions: {e}")
            traceback.print_exc()
            self._show_message("❌ Loading Error", f"Error loading questions: {str(e)}")
    
    def _show_quiz_ready(self):
        """Show quiz ready screen."""
        try:
            # Clear frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            # Force update to get actual dimensions
            self.quiz_frame.update_idletasks()
            frame_width = self.quiz_frame.winfo_width()
            frame_height = self.quiz_frame.winfo_height()
            
            # Use minimum dimensions if frame dimensions are too small
            if frame_width < 200:
                frame_width = 600
            if frame_height < 200:
                frame_height = 400
            
            print(f"Frame dimensions: {frame_width}x{frame_height}")
            
            # Success message with language support
            success_text = f"✅ {self._get_text('quiz_ready')}"
            success_label = tk.Label(
                self.quiz_frame,
                text=success_text,
                font=("Arial", 20, "bold"),
                fg="green",
                bg="#87CEEB"
            )
            success_label.pack(pady=(50, 20))
            
            # Quiz description with language support
            description_text = self._get_text('quiz_description')
            description_label = tk.Label(
                self.quiz_frame,
                text=description_text,
                font=("Arial", 14),
                fg="black",
                bg="#87CEEB",
                justify="center",
                wraplength=frame_width - 40
            )
            description_label.pack(pady=10)
            
            # Click start message with language support
            click_start_text = self._get_text('click_start_to_begin')
            click_start_label = tk.Label(
                self.quiz_frame,
                text=click_start_text,
                font=("Arial", 12, "bold"),
                fg="black",
                bg="#87CEEB",
                justify="center"
            )
            click_start_label.pack(pady=(20, 10))
            
            # Start button with language support
            start_text = f"🚀 {self._get_text('start_quiz')}"
            start_button = tk.Button(
                self.quiz_frame,
                text=start_text,
                command=self._start_quiz,
                bg="lightgreen",
                fg="black",
                font=("Arial", 16, "bold"),
                width=15,
                height=2
            )
            start_button.pack(pady=20)
            
        except Exception as e:
            print(f"❌ Error showing quiz ready: {e}")
            traceback.print_exc()
    
    def _start_quiz(self):
        """Start the actual quiz."""
        try:
            print("Starting quiz...")
            self.quiz_started = True
            self.current_question_index = 0
            self.user_answers = []
            self.score = 0
            
            self._display_current_question()
            
        except Exception as e:
            print(f"❌ Error starting quiz: {e}")
            traceback.print_exc()
            self._show_message("❌ Start Error", f"Error starting quiz: {str(e)}")
    
    def _display_current_question(self):
        """Display the current question."""
        try:
            # Clear frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            # Check if quiz complete
            if self.current_question_index >= len(self.current_questions):
                self._show_results()
                return
            
            current_q = self.current_questions[self.current_question_index]
            
            # Force update to get actual dimensions
            self.quiz_frame.update_idletasks()
            frame_width = self.quiz_frame.winfo_width()
            frame_height = self.quiz_frame.winfo_height()
            
            if frame_width < 200:
                frame_width = 600
            if frame_height < 200:
                frame_height = 400
            
            # Progress
            progress_text = f"Question {self.current_question_index + 1} of {len(self.current_questions)}"
            progress_label = tk.Label(
                self.quiz_frame,
                text=progress_text,
                font=("Arial", 12, "bold"),
                fg="black",
                bg="#87CEEB"
            )
            progress_label.pack(pady=(10, 20))
            
            # Question
            question_label = tk.Label(
                self.quiz_frame,
                text=current_q["question"],
                font=("Arial", 14, "bold"),
                fg="black",
                bg="#87CEEB",
                wraplength=frame_width - 40,
                justify="center"
            )
            question_label.pack(pady=10)
            
            # Answer choices frame
            choices_frame = tk.Frame(self.quiz_frame, bg="#87CEEB")
            choices_frame.pack(pady=20, fill="x", padx=20)
            
            self.selected_answer = tk.StringVar()
            
            for i, choice in enumerate(current_q["choices"]):
                radio = tk.Radiobutton(
                    choices_frame,
                    text=f"{chr(65+i)}. {choice}",
                    variable=self.selected_answer,
                    value=choice,
                    font=("Arial", 12),
                    fg="black",
                    bg="#87CEEB",
                    anchor="w",
                    wraplength=frame_width - 80,
                    justify="left"
                )
                radio.pack(anchor="w", pady=5)
            
            # Next button
            next_button = tk.Button(
                self.quiz_frame,
                text="Next →",
                command=self._answer_question,
                bg="lightblue",
                fg="black",
                font=("Arial", 14, "bold"),
                width=12,
                height=1
            )
            next_button.pack(pady=30)
            
        except Exception as e:
            print(f"❌ Error displaying question: {e}")
            traceback.print_exc()
            self._show_message("❌ Display Error", f"Error displaying question: {str(e)}")
    
    def _answer_question(self):
        """Process answer and move to next question."""
        try:
            if not hasattr(self, 'selected_answer') or not self.selected_answer.get():
                messagebox.showwarning("No Answer", "Please select an answer.")
                return
            
            current_q = self.current_questions[self.current_question_index]
            user_answer = self.selected_answer.get()
            is_correct = user_answer == current_q["correct_answer"]
            
            if is_correct:
                self.score += 1
            
            self.user_answers.append({
                "question": current_q["question"],
                "user_answer": user_answer,
                "correct_answer": current_q["correct_answer"],
                "is_correct": is_correct
            })
            
            self.current_question_index += 1
            self._display_current_question()
            
        except Exception as e:
            print(f"❌ Error processing answer: {e}")
            traceback.print_exc()
            self._show_message("❌ Answer Error", f"Error processing answer: {str(e)}")
    
    def _show_results(self):
        """Show quiz results."""
        try:
            # Clear frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            percentage = round((self.score / len(self.current_questions)) * 100)
            
            # Results
            results_text = f"🎉 Quiz Complete!\n\nScore: {self.score}/{len(self.current_questions)} ({percentage}%)"
            results_label = tk.Label(
                self.quiz_frame,
                text=results_text,
                font=("Arial", 18, "bold"),
                fg="green",
                bg="#87CEEB",
                justify="center"
            )
            results_label.pack(pady=(80, 40))
            
            # Restart button
            restart_button = tk.Button(
                self.quiz_frame,
                text="🔄 New Quiz",
                command=self._restart_quiz,
                bg="lightgreen",
                fg="black",
                font=("Arial", 14, "bold"),
                width=12,
                height=2
            )
            restart_button.pack(pady=20)
            
        except Exception as e:
            print(f"❌ Error showing results: {e}")
            traceback.print_exc()
    
    def _restart_quiz(self):
        """Restart the quiz."""
        try:
            self.quiz_started = False
            self.current_question_index = 0
            self.user_answers = []
            self.score = 0
            
            # Load new questions
            self._load_quiz_questions()
            
        except Exception as e:
            print(f"❌ Error restarting quiz: {e}")
            traceback.print_exc()
    
    def _show_message(self, title: str, message: str):
        """Show a message in the quiz frame."""
        try:
            # Clear frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            # Title
            title_label = tk.Label(
                self.quiz_frame,
                text=title,
                font=("Arial", 18, "bold"),
                fg="red" if "❌" in title else "black",
                bg="#87CEEB"
            )
            title_label.pack(pady=(60, 20))
            
            # Message
            message_label = tk.Label(
                self.quiz_frame,
                text=message,
                font=("Arial", 12),
                fg="black",
                bg="#87CEEB",
                justify="center",
                wraplength=500
            )
            message_label.pack(pady=20)
            
        except Exception as e:
            print(f"❌ Error showing message: {e}")
            messagebox.showerror("Error", f"{title}\n\n{message}")
    
    def _show_error(self, error_msg: str):
        """Show error message."""
        self._show_message("❌ Error", error_msg)
    
    def handle_theme_change(self):
        """Handle theme changes."""
        pass
    
    def cleanup(self):
        """Clean up resources."""
        try:
            if self.quiz_frame:
                for widget in self.quiz_frame.winfo_children():
                    widget.destroy()
        except Exception as e:
            pass