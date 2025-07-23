"""
Enhanced Weather Quiz Controller - Manages quiz logic and GUI interactions
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import traceback

from .quiz_generator import WeatherQuizGenerator


class WeatherQuizController:
    """
    Enhanced Controller for the Weather Quiz feature
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
        """Build the enhanced quiz page"""
        try:
            self._add_back_button()
            self._build_header(window_width)
            self._build_data_info_section(window_width)
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
        # Main title - simplified
        title_main = self._create_black_label(
            self.app,
            text="🌤️ Weather Quiz",
            font=("Arial", int(32 + window_width/40), "bold"),
            x=window_width/2,
            y=70
        )
        self.gui.widgets.append(title_main)
    
    def _build_data_info_section(self, window_width):
        """Build section showing data information - REMOVED"""
        # Remove all data info sections to clean up the interface
        pass
    
    def _build_quiz_area(self, window_width, window_height):
        """Build the main quiz display area with proper centering"""
        quiz_y = 120  # Start higher since we removed subheadings
        quiz_height = window_height - 160  # More space
        quiz_width = min(window_width - 60, 800)  # Limit max width
        quiz_x = (window_width - quiz_width) // 2  # Center horizontally
        
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
        
        # Loading message - centered in frame
        loading_label = self._create_black_label(
            self.quiz_frame,
            text="🧠 Loading Quiz...\nGenerating questions!",
            font=("Arial", 16),
            x=quiz_width//2,
            y=quiz_height//2
        )
    
    def _generate_quiz_async(self):
        """Generate quiz questions in background thread"""
        def generate():
            try:
                # Show data validation results
                if self.data_stats and 'issues' in self.data_stats and self.data_stats['issues']:
                    print("Data quality issues found:")
                    for issue in self.data_stats['issues']:
                        print(f"  - {issue}")
                
                # Generate questions
                self.current_questions = self.quiz_generator.generate_quiz()
                
                # Update UI on main thread
                self.app.after(0, self._display_quiz_start)
                
            except Exception as e:
                error_msg = f"Error generating quiz: {str(e)}"
                print(f"Quiz generation error: {e}")
                traceback.print_exc()
                self.app.after(0, lambda: self._show_error(error_msg))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _display_quiz_start(self):
        """Display enhanced quiz start screen with proper centering"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            frame_width = self.quiz_frame.winfo_width() or 600
            frame_height = self.quiz_frame.winfo_height() or 400
            
            # Welcome message - centered
            welcome_label = self._create_black_label(
                self.quiz_frame,
                text="🌤️ Quiz Ready!",
                font=("Arial", 28, "bold"),
                x=frame_width//2,
                y=frame_height//2 - 80
            )
            
            # Simplified instructions - centered
            if self.data_stats and self.data_stats.get('data_available', False):
                city_count = len(self.data_stats['cities'])
                instructions_text = f"Answer {len(self.current_questions)} questions based on weather data.\n\nReady to test your knowledge?"
            else:
                instructions_text = f"Answer {len(self.current_questions)} weather questions.\n\nReady to test your knowledge?"
            
            instructions = self._create_black_label(
                self.quiz_frame,
                text=instructions_text,
                font=("Arial", 14),
                x=frame_width//2,
                y=frame_height//2 - 20,
                justify="center"
            )
            
            # Start quiz button - centered
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
            start_btn.place(x=frame_width//2, y=frame_height//2 + 60, anchor="center")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _show_data_details(self):
        """Show detailed information about the data being used"""
        if not self.data_stats or not self.data_stats.get('data_available', False):
            messagebox.showinfo("Data Info", "No detailed weather data available.\nUsing general weather knowledge questions.")
            return
        
        # Create detailed info text
        info_text = "🌍 Weather Data Details\n"
        info_text += "=" * 50 + "\n\n"
        
        info_text += f"📊 Dataset Overview:\n"
        info_text += f"  • Total Records: {self.data_stats['total_records']:,}\n"
        info_text += f"  • Cities Included: {len(self.data_stats['cities'])}\n"
        info_text += f"  • Date Range: {self.data_stats['date_range']['start']} to {self.data_stats['date_range']['end']}\n\n"
        
        info_text += f"🌡️ Temperature Extremes:\n"
        info_text += f"  • Highest: {self.data_stats['temperature_range']['max_f']}°F\n"
        info_text += f"  • Lowest: {self.data_stats['temperature_range']['min_f']}°F\n\n"
        
        info_text += f"🏙️ Cities in Dataset:\n"
        for i, city in enumerate(self.data_stats['cities'], 1):
            info_text += f"  {i}. {city}\n"
        
        info_text += f"\n📈 Data Quality: {self.data_stats.get('quality', 'Unknown').title()}\n"
        
        if 'issues' in self.data_stats and self.data_stats['issues']:
            info_text += f"\n⚠️ Data Notes:\n"
            for issue in self.data_stats['issues']:
                info_text += f"  • {issue}\n"
        
        info_text += f"\n🎯 Quiz questions will analyze real patterns from this data!"
        
        # Show in a popup window
        self._show_info_popup("Weather Data Details", info_text)
    
    def _show_info_popup(self, title, text):
        """Show information in a popup window with scrollable text"""
        popup = tk.Toplevel(self.app)
        popup.title(title)
        popup.geometry("600x500")
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
        """Display the current question with enhanced formatting and proper centering"""
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
            
            # Question text with better formatting and wrapping
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
            
            # Answer choices with better spacing and centering
            self.selected_answer = tk.StringVar()
            
            choice_start_y = 120
            choice_spacing = 40
            
            for i, choice in enumerate(question["choices"]):
                radio_btn = tk.Radiobutton(
                    self.quiz_frame,
                    text=f"{chr(65 + i)}. {choice}",  # A. B. C. D.
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
            
            # Navigation buttons - centered at bottom
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
        """Display enhanced quiz results and score with centered layout"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            self.quiz_completed = True
            frame_width = self.quiz_frame.winfo_width() or 600
            frame_height = self.quiz_frame.winfo_height() or 400
            
            # Calculate percentage
            percentage = round((self.score / len(self.current_questions)) * 100)
            
            # Results header with emoji and message
            if percentage >= 90:
                emoji = "🏆"
                message = "Outstanding! Weather expert!"
                color = "gold"
            elif percentage >= 80:
                emoji = "🌟"
                message = "Excellent! Great knowledge!"
                color = "green"
            elif percentage >= 70:
                emoji = "☀️"
                message = "Great job! Solid understanding!"
                color = "blue"
            elif percentage >= 60:
                emoji = "⛅"
                message = "Good work! Keep learning!"
                color = "orange"
            elif percentage >= 40:
                emoji = "🌧️"
                message = "Not bad! Keep studying!"
                color = "purple"
            else:
                emoji = "❄️"
                message = "Keep exploring weather science!"
                color = "red"
            
            # Centered results display
            results_header = self._create_colored_label(
                self.quiz_frame,
                text=f"{emoji} Quiz Complete! {emoji}",
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
            
            # Action buttons - centered horizontally
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
        """Show comprehensive answer review with correct answers displayed"""
        try:
            results_text = "🌤️ Weather Quiz - Detailed Results\n"
            results_text += "=" * 60 + "\n\n"
            
            results_text += f"📊 Overall Performance: {self.score}/{len(self.current_questions)} ({round((self.score/len(self.current_questions))*100)}%)\n\n"
            
            for i, answer_data in enumerate(self.user_answers):
                results_text += f"❓ Question {i+1}:\n"
                results_text += f"{answer_data['question']}\n\n"
                
                results_text += f"✅ Correct Answer: {answer_data['correct_answer']}\n"
                results_text += f"👤 Your Answer: {answer_data['user_answer']}\n"
                
                if answer_data['is_correct']:
                    results_text += "🎉 CORRECT! Well done!\n"
                else:
                    results_text += "❌ Incorrect - See explanation below\n"
                
                results_text += f"💡 Explanation: {answer_data['explanation']}\n"
                results_text += "-" * 50 + "\n\n"
            
            # Performance analysis
            correct_count = sum(1 for ans in self.user_answers if ans['is_correct'])
            percentage = (correct_count / len(self.user_answers)) * 100
            
            results_text += "📈 Performance Summary:\n"
            results_text += f"✅ Correct: {correct_count}/{len(self.user_answers)}\n"
            results_text += f"❌ Incorrect: {len(self.user_answers) - correct_count}/{len(self.user_answers)}\n"
            results_text += f"📊 Accuracy: {percentage:.1f}%\n\n"
            
            if percentage >= 80:
                results_text += "🏆 Excellent understanding of weather patterns!\n"
            elif percentage >= 60:
                results_text += "👍 Good grasp of meteorological concepts!\n"
            elif percentage >= 40:
                results_text += "📚 Room for improvement - keep learning!\n"
            else:
                results_text += "🎯 Focus on weather fundamentals for better results!\n"
            
            if self.data_stats and self.data_stats.get('data_available', False):
                results_text += f"\n📊 Quiz based on real data from: {', '.join(self.data_stats['cities'])}"
            
            # Show in popup
            self._show_info_popup("Detailed Quiz Results", results_text)
            
        except Exception as e:
            self._show_error(str(e))
    
    def _share_results(self):
        """Share quiz results"""
        try:
            percentage = round((self.score / len(self.current_questions)) * 100)
            
            share_text = f"🌤️ Weather Quiz Results\n\n"
            share_text += f"Score: {self.score}/{len(self.current_questions)} ({percentage}%)\n"
            
            if percentage >= 80:
                share_text += f"🏆 Excellent weather knowledge!"
            elif percentage >= 60:
                share_text += f"☀️ Good understanding of weather patterns!"
            else:
                share_text += f"🌧️ Keep learning about meteorology!"
            
            if self.data_stats and self.data_stats.get('data_available', False):
                share_text += f"\n\nBased on real weather data from {len(self.data_stats['cities'])} cities worldwide!"
            
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
            
            frame_width = self.quiz_frame.winfo_reqwidth() or 600
            frame_height = self.quiz_frame.winfo_reqheight() or 400
            
            loading_label = self._create_black_label(
                self.quiz_frame,
                text="🔄 Generating fresh questions...\nAnalyzing different weather patterns!",
                font=("Arial", 16),
                x=frame_width/2,
                y=frame_height/2
            )
            
            # Generate new quiz
            self._generate_quiz_async()
            
        except Exception as e:
            self._show_error(str(e))
    
    def _show_error(self, error_msg):
        """Show error message with better formatting"""
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            frame_width = self.quiz_frame.winfo_reqwidth() or 600
            frame_height = self.quiz_frame.winfo_reqheight() or 400
            
            error_label = self._create_colored_label(
                self.quiz_frame,
                text=f"❌ Quiz Error\n\n{error_msg}\n\nPlease try again or return to the main page.",
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