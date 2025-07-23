"""
Enhanced Weather Quiz Controller - Manages quiz logic ONLY for CSV data
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import traceback

from .quiz_generator import WeatherQuizGenerator


class WeatherQuizController:
    """
    Enhanced Controller for the Weather Quiz feature - CSV DATA ONLY
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
        self.data_stats = None
        
        # Get data statistics
        self._load_data_stats()
        
    def _load_data_stats(self):
        """Load data statistics for display"""
        try:
            self.data_stats = self.quiz_generator.get_data_stats()
            data_quality = self.quiz_generator.validate_data_quality()
            self.data_stats.update(data_quality)
        except Exception as e:
            print(f"Error loading data stats: {e}")
            self.data_stats = {"data_available": False, "message": "Error loading data"}
    
    def build_page(self, window_width, window_height):
        """Build the CSV-only quiz page"""
        try:
            self._add_back_button()
            self._build_header(window_width)
            
            # Check if CSV data is available
            if not self.data_stats.get('data_available', False):
                self._build_no_data_message(window_width, window_height)
                return
            
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
        """Build quiz header with title only"""
        title_main = self._create_black_label(
            self.app,
            text="🌤️ Weather Quiz",
            font=("Arial", int(32 + window_width/40), "bold"),
            x=window_width/2,
            y=70
        )
        self.gui.widgets.append(title_main)
    
    def _build_no_data_message(self, window_width, window_height):
        """Build message when no CSV data is available"""
        message_y = window_height // 2
        
        # Error icon and message
        error_label = self._create_colored_label(
            self.app,
            text="📊 No Weather Data Available",
            font=("Arial", 24, "bold"),
            x=window_width/2,
            y=message_y - 80,
            color="red"
        )
        self.gui.widgets.append(error_label)
        
        # Explanation
        explanation = self._create_black_label(
            self.app,
            text="The weather quiz requires CSV data to generate questions.\n\nPlease ensure the 'combined.csv' file is present in the 'data' directory\nwith weather records from multiple cities.",
            font=("Arial", 14),
            x=window_width/2,
            y=message_y,
            justify="center"
        )
        self.gui.widgets.append(explanation)
        
        # Data requirements
        requirements = self._create_black_label(
            self.app,
            text="Required CSV columns:\n• city\n• temperature_2m_max (°F)\n• temperature_2m_min (°F)\n• rain_sum (inch)\n• wind_speed_10m_max (mp/h)\n• relative_humidity_2m_mean (%)",
            font=("Arial", 12),
            x=window_width/2,
            y=message_y + 80,
            justify="center"
        )
        self.gui.widgets.append(requirements)
    
    def _build_quiz_area(self, window_width, window_height):
        """Build the main quiz display area with proper centering"""
        quiz_y = 100  # Start higher since we removed subtitle
        quiz_height = window_height - 180
        quiz_width = min(window_width - 60, 800)
        quiz_x = (window_width - quiz_width) // 2
        
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
            x=quiz_x,
            y=quiz_y,
            width=quiz_width,
            height=quiz_height
        )
        self.gui.widgets.append(self.quiz_frame)
        
        # Loading message
        loading_label = self._create_black_label(
            self.quiz_frame,
            text="🧠 Analyzing CSV Data...\nGenerating questions from real weather patterns!",
            font=("Arial", 16),
            x=quiz_width//2,
            y=quiz_height//2
        )
    
    def _generate_quiz_async(self):
        """Generate quiz questions in background thread - CSV ONLY"""
        def generate():
            try:
                # Validate data quality first
                if self.data_stats and 'issues' in self.data_stats and self.data_stats['issues']:
                    print("Data quality issues found:")
                    for issue in self.data_stats['issues']:
                        print(f"  - {issue}")
                
                # Generate questions from CSV data ONLY
                self.current_questions = self.quiz_generator.generate_quiz()
                
                if not self.current_questions:
                    error_msg = "Unable to generate questions from CSV data.\nPlease check that the data file contains sufficient records from multiple cities."
                    self.app.after(0, lambda: self._show_error(error_msg))
                    return
                
                # Update UI on main thread
                self.app.after(0, self._display_quiz_start)
                
            except Exception as e:
                error_msg = f"Error generating quiz from CSV data: {str(e)}"
                print(f"Quiz generation error: {e}")
                traceback.print_exc()
                self.app.after(0, lambda: self._show_error(error_msg))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _display_quiz_start(self):
        """Display quiz start screen with CSV data info"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            frame_width = self.quiz_frame.winfo_width() or 600
            frame_height = self.quiz_frame.winfo_height() or 400
            
            # Welcome message
            welcome_label = self._create_black_label(
                self.quiz_frame,
                text="📊 CSV Data Quiz Ready!",
                font=("Arial", 28, "bold"),
                x=frame_width//2,
                y=frame_height//2 - 100
            )
            
            # Data info
            if self.data_stats and self.data_stats.get('data_available', False):
                city_count = len(self.data_stats['cities'])
                record_count = self.data_stats['total_records']
                data_info = f"Analyzing {record_count:,} weather records from {city_count} cities:\n{', '.join(self.data_stats['cities'][:5])}{'...' if city_count > 5 else ''}"
            else:
                data_info = "Processing weather data..."
            
            info_label = self._create_black_label(
                self.quiz_frame,
                text=data_info,
                font=("Arial", 12),
                x=frame_width//2,
                y=frame_height//2 - 50,
                justify="center"
            )
            
            # Instructions
            instructions_text = f"Answer {len(self.current_questions)} questions based entirely on patterns\nfound in the real weather data.\n\nReady to test your data analysis skills?"
            
            instructions = self._create_black_label(
                self.quiz_frame,
                text=instructions_text,
                font=("Arial", 14),
                x=frame_width//2,
                y=frame_height//2,
                justify="center"
            )
            
            # Buttons
            start_btn = tk.Button(
                self.quiz_frame,
                text="🚀 Start CSV Quiz",
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
            start_btn.place(x=frame_width//2 - 80, y=frame_height//2 + 60, anchor="center")
            
            # Show all questions button
            show_all_btn = tk.Button(
                self.quiz_frame,
                text="📋 All Questions",
                command=self._show_all_questions,
                bg="lightblue",
                fg="black",
                font=("Arial", 12, "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=2,
                activeforeground="black",
                activebackground="lightcyan",
                highlightthickness=0
            )
            show_all_btn.place(x=frame_width//2 + 80, y=frame_height//2 + 60, anchor="center")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _show_all_questions(self):
        """Show all possible questions that can be generated from the CSV data"""
        try:
            all_questions = self.quiz_generator.get_all_possible_questions()
            
            if not all_questions:
                messagebox.showinfo("No Questions", "No questions could be generated from the current CSV data.")
                return
            
            # Create detailed questions text
            questions_text = f"All Possible Questions from CSV Data\n"
            questions_text += f"Generated from {len(self.data_stats.get('cities', []))} cities\n"
            questions_text += "=" * 70 + "\n\n"
            
            current_category = ""
            for i, q in enumerate(all_questions, 1):
                if q['category'] != current_category:
                    current_category = q['category']
                    questions_text += f"\n{current_category} Questions:\n"
                    questions_text += "-" * 40 + "\n"
                
                questions_text += f"Q{i}: {q['question']}\n"
                questions_text += f"Choices: {', '.join(q['choices'])}\n"
                questions_text += f"Answer: {q['correct_answer']}\n"
                questions_text += f"Explanation: {q['explanation']}\n\n"
            
            # Show in popup
            self._show_info_popup(f"All CSV Questions ({len(all_questions)} total)", questions_text)
            
        except Exception as e:
            self._show_error(f"Error generating questions list: {str(e)}")
    
    def _start_quiz(self):
        """Start the CSV data quiz"""
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
        """Display the current question with enhanced formatting"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            if self.current_question_index >= len(self.current_questions):
                self._display_quiz_results()
                return
            
            question = self.current_questions[self.current_question_index]
            frame_width = self.quiz_frame.winfo_width() or 600
            frame_height = self.quiz_frame.winfo_height() or 400
            
            # Progress indicator with score
            progress_text = f"Question {self.current_question_index + 1} of {len(self.current_questions)}"
            if self.current_question_index > 0:
                current_score_pct = round((self.score / self.current_question_index) * 100)
                progress_text += f" | Score: {self.score}/{self.current_question_index} ({current_score_pct}%)"
            
            progress_label = self._create_black_label(
                self.quiz_frame,
                text=progress_text,
                font=("Arial", 12, "bold"),
                x=frame_width//2,
                y=20
            )
            
            # Question text
            question_text = question["question"]
            question_label = self._create_black_label(
                self.quiz_frame,
                text=question_text,
                font=("Arial", 14, "bold"),
                x=frame_width//2,
                y=60,
                justify="center",
                wraplength=frame_width - 40
            )
            
            # Answer choices
            self.selected_answer = tk.StringVar()
            
            choice_start_y = 120
            choice_spacing = 40
            
            for i, choice in enumerate(question["choices"]):
                radio_btn = tk.Radiobutton(
                    self.quiz_frame,
                    text=f"{chr(65 + i)}. {choice}",
                    variable=self.selected_answer,
                    value=choice,
                    font=("Arial", 12),
                    fg="black",
                    bg=self._get_canvas_bg_color(),
                    selectcolor="lightblue",
                    activebackground=self._get_canvas_bg_color(),
                    activeforeground="black",
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0,
                    wraplength=frame_width - 80,
                    justify="left",
                    anchor="w"
                )
                radio_btn.place(x=40, y=choice_start_y + i * choice_spacing, anchor="w")
            
            # Navigation buttons
            button_y = frame_height - 60
            
            # Next/Submit button
            if self.current_question_index == len(self.current_questions) - 1:
                button_text = "🏁 Finish Quiz"
                button_color = "lightcoral"
            else:
                button_text = "➡️ Next Question"
                button_color = "lightblue"
            
            next_btn = tk.Button(
                self.quiz_frame,
                text=button_text,
                command=self._answer_question,
                bg=button_color,
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
            next_btn.place(x=frame_width//2, y=button_y, anchor="center")
            
            # Back button (if not first question)
            if self.current_question_index > 0:
                back_btn = tk.Button(
                    self.quiz_frame,
                    text="⬅️ Previous",
                    command=self._go_back_question,
                    bg="lightyellow",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    relief="raised",
                    borderwidth=2,
                    width=12,
                    height=1,
                    activeforeground="black",
                    activebackground="lightgrey",
                    highlightthickness=0
                )
                back_btn.place(x=frame_width//2 - 120, y=button_y, anchor="center")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _go_back_question(self):
        """Go back to previous question"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            
            # Remove the last answer if going back
            if len(self.user_answers) > self.current_question_index:
                removed_answer = self.user_answers.pop()
                if removed_answer['is_correct']:
                    self.score -= 1
            
            self._display_current_question()
    
    def _answer_question(self):
        """Process the user's answer and move to next question"""
        try:
            if not hasattr(self, 'selected_answer') or not self.selected_answer.get():
                messagebox.showwarning("No Answer Selected", "Please select an answer before continuing.")
                return
            
            question = self.current_questions[self.current_question_index]
            user_answer = self.selected_answer.get()
            correct_answer = question["correct_answer"]
            is_correct = user_answer == correct_answer
            
            # If we're updating an existing answer (going back and forth)
            if len(self.user_answers) > self.current_question_index:
                old_answer = self.user_answers[self.current_question_index]
                if old_answer['is_correct']:
                    self.score -= 1
                
                self.user_answers[self.current_question_index] = {
                    "question": question["question"],
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "explanation": question["explanation"],
                    "is_correct": is_correct
                }
            else:
                # Store new answer
                self.user_answers.append({
                    "question": question["question"],
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "explanation": question["explanation"],
                    "is_correct": is_correct
                })
            
            # Update score
            if is_correct:
                self.score += 1
            
            # Move to next question
            self.current_question_index += 1
            self._display_current_question()
            
        except Exception as e:
            self._show_error(str(e))
    
    def _display_quiz_results(self):
        """Display quiz results"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            self.quiz_completed = True
            frame_width = self.quiz_frame.winfo_width() or 600
            frame_height = self.quiz_frame.winfo_height() or 400
            
            # Calculate percentage
            percentage = round((self.score / len(self.current_questions)) * 100)
            
            # Results with CSV data emphasis
            if percentage >= 90:
                emoji = "🏆"
                message = "Outstanding data analysis!"
                color = "gold"
            elif percentage >= 80:
                emoji = "🌟"
                message = "Excellent CSV interpretation!"
                color = "green"
            elif percentage >= 70:
                emoji = "☀️"
                message = "Great pattern recognition!"
                color = "blue"
            elif percentage >= 60:
                emoji = "⛅"
                message = "Good data understanding!"
                color = "orange"
            else:
                emoji = "🌧️"
                message = "Keep practicing data analysis!"
                color = "purple"
            
            # Centered results display
            results_header = self._create_colored_label(
                self.quiz_frame,
                text=f"{emoji} CSV Quiz Complete! {emoji}",
                font=("Arial", 24, "bold"),
                x=frame_width//2,
                y=frame_height//2 - 120,
                color=color
            )
            
            score_label = self._create_black_label(
                self.quiz_frame,
                text=f"Final Score: {self.score}/{len(self.current_questions)} ({percentage}%)",
                font=("Arial", 20, "bold"),
                x=frame_width//2,
                y=frame_height//2 - 80
            )
            
            message_label = self._create_colored_label(
                self.quiz_frame,
                text=message,
                font=("Arial", 16),
                x=frame_width//2,
                y=frame_height//2 - 40,
                color=color
            )
            
            # Data source reminder
            data_label = self._create_black_label(
                self.quiz_frame,
                text=f"Based on real weather data from {len(self.data_stats.get('cities', []))} cities",
                font=("Arial", 12),
                x=frame_width//2,
                y=frame_height//2 - 10
            )
            
            # Action buttons
            button_y = frame_height//2 + 20
            button_spacing = 140
            
            review_btn = tk.Button(
                self.quiz_frame,
                text="📋 Review Answers",
                command=self._show_detailed_results,
                bg="lightblue",
                fg="black",
                font=("Arial", 12, "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=2,
                activeforeground="black",
                activebackground="lightcyan",
                highlightthickness=0
            )
            review_btn.place(x=frame_width//2 - button_spacing//2, y=button_y, anchor="center")
            
            retry_btn = tk.Button(
                self.quiz_frame,
                text="🔄 New Quiz",
                command=self._restart_quiz,
                bg="lightgreen",
                fg="black",
                font=("Arial", 12, "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=2,
                activeforeground="black",
                activebackground="lightblue",
                highlightthickness=0
            )
            retry_btn.place(x=frame_width//2 + button_spacing//2, y=button_y, anchor="center")
            
            # Share button centered below
            share_btn = tk.Button(
                self.quiz_frame,
                text="📤 Share Score",
                command=self._share_results,
                bg="lightyellow",
                fg="black",
                font=("Arial", 12, "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=2,
                activeforeground="black",
                activebackground="lightgoldenrod",
                highlightthickness=0
            )
            share_btn.place(x=frame_width//2, y=button_y + 60, anchor="center")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _show_detailed_results(self):
        """Show comprehensive answer review with CSV data insights"""
        try:
            results_text = "🌤️ CSV Weather Quiz - Detailed Results\n"
            results_text += "=" * 60 + "\n\n"
            
            results_text += f"📊 Overall Performance: {self.score}/{len(self.current_questions)} ({round((self.score/len(self.current_questions))*100)}%)\n"
            results_text += f"📈 Data Source: {len(self.data_stats.get('cities', []))} cities, {self.data_stats.get('total_records', 0):,} records\n\n"
            
            for i, answer_data in enumerate(self.user_answers):
                results_text += f"❓ Question {i+1}:\n"
                results_text += f"{answer_data['question']}\n\n"
                
                results_text += f"✅ Correct Answer: {answer_data['correct_answer']}\n"
                results_text += f"👤 Your Answer: {answer_data['user_answer']}\n"
                
                if answer_data['is_correct']:
                    results_text += "🎉 CORRECT! Excellent data analysis!\n"
                else:
                    results_text += "❌ Incorrect - See CSV data explanation below\n"
                
                results_text += f"💡 Data Explanation: {answer_data['explanation']}\n"
                results_text += "-" * 50 + "\n\n"
            
            # Performance analysis
            correct_count = sum(1 for ans in self.user_answers if ans['is_correct'])
            percentage = (correct_count / len(self.user_answers)) * 100
            
            results_text += "📈 CSV Data Analysis Performance:\n"
            results_text += f"✅ Correct: {correct_count}/{len(self.user_answers)}\n"
            results_text += f"❌ Incorrect: {len(self.user_answers) - correct_count}/{len(self.user_answers)}\n"
            results_text += f"📊 Accuracy: {percentage:.1f}%\n\n"
            
            if percentage >= 80:
                results_text += "🏆 Excellent understanding of weather data patterns!\n"
            elif percentage >= 60:
                results_text += "👍 Good grasp of meteorological data analysis!\n"
            elif percentage >= 40:
                results_text += "📚 Room for improvement in data interpretation!\n"
            else:
                results_text += "🎯 Focus on understanding weather data relationships!\n"
            
            results_text += f"\n📊 All questions based on real CSV data from: {', '.join(self.data_stats.get('cities', []))}"
            
            # Show in popup
            self._show_info_popup("Detailed CSV Quiz Results", results_text)
            
        except Exception as e:
            self._show_error(str(e))
    
    def _share_results(self):
        """Share CSV quiz results"""
        try:
            percentage = round((self.score / len(self.current_questions)) * 100)
            
            share_text = f"🌤️ CSV Weather Data Quiz Results\n\n"
            share_text += f"Score: {self.score}/{len(self.current_questions)} ({percentage}%)\n"
            
            if percentage >= 80:
                share_text += f"🏆 Excellent weather data analysis skills!"
            elif percentage >= 60:
                share_text += f"☀️ Good understanding of meteorological patterns!"
            else:
                share_text += f"🌧️ Keep practicing weather data interpretation!"
            
            share_text += f"\n\nBased on real CSV weather data from {len(self.data_stats.get('cities', []))} cities worldwide!"
            share_text += f"\nAnalyzed {self.data_stats.get('total_records', 0):,} weather records"
            
            # Copy to clipboard (if available)
            try:
                self.app.clipboard_clear()
                self.app.clipboard_append(share_text)
                messagebox.showinfo("Score Shared", "Results copied to clipboard!\n\n" + share_text)
            except:
                messagebox.showinfo("Quiz Results", share_text)
                
        except Exception as e:
            self._show_error(str(e))
    
    def _restart_quiz(self):
        """Restart the quiz with new CSV-based questions"""
        try:
            self.quiz_started = False
            self.quiz_completed = False
            self.current_question_index = 0
            self.user_answers = []
            self.score = 0
            
            # Clear quiz frame and show loading
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            frame_width = self.quiz_frame.winfo_reqwidth() or 600
            frame_height = self.quiz_frame.winfo_reqheight() or 400
            
            loading_label = self._create_black_label(
                self.quiz_frame,
                text="🔄 Analyzing CSV data again...\nGenerating fresh questions from weather patterns!",
                font=("Arial", 16),
                x=frame_width/2,
                y=frame_height/2
            )
            
            # Generate new quiz from CSV data
            self._generate_quiz_async()
            
        except Exception as e:
            self._show_error(str(e))
    
    def _show_error(self, error_msg):
        """Show error message with CSV data context"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            frame_width = self.quiz_frame.winfo_reqwidth() or 600
            frame_height = self.quiz_frame.winfo_reqheight() or 400
            
            error_label = self._create_colored_label(
                self.quiz_frame,
                text=f"❌ CSV Quiz Error\n\n{error_msg}\n\nPlease ensure the CSV data file is available\nand contains weather records from multiple cities.",
                font=("Arial", 14),
                x=frame_width/2,
                y=frame_height/2,
                justify="center",
                color="red"
            )
            
            # Retry button
            retry_btn = tk.Button(
                self.quiz_frame,
                text="🔄 Try Again",
                command=self._restart_quiz,
                bg="lightcoral",
                fg="black",
                font=("Arial", 12, "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=1,
                activeforeground="black",
                activebackground="lightpink",
                highlightthickness=0
            )
            retry_btn.place(x=frame_width/2, y=frame_height/2 + 80, anchor="center")
            
        except Exception as e:
            print(f"Error showing error: {e}")
    
    def _show_info_popup(self, title, text):
        """Show information in a popup window with scrollable text"""
        popup = tk.Toplevel(self.app)
        popup.title(title)
        popup.geometry("700x600")
        popup.resizable(True, True)
        
        # Create scrolled text widget
        text_widget = scrolledtext.ScrolledText(
            popup,
            wrap=tk.WORD,
            font=("Courier", 10),
            bg="white",
            fg="black"
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Insert text
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(
            popup,
            text="Close",
            command=popup.destroy,
            bg="lightgrey",
            font=("Arial", 12)
        )
        close_btn.pack(pady=5)
        
        # Center the popup
        popup.transient(self.app)
        popup.grab_set()
    
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
    
    def _create_colored_label(self, parent, text, font, x, y, color="black", anchor="center", **kwargs):
        """Create a label with specified color text and transparent background"""
        canvas_bg = self._get_canvas_bg_color()
        
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg=color,
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