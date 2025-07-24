"""
Enhanced Weather Quiz Controller - Manages quiz logic ONLY for CSV data

This controller coordinates between the quiz generator (which creates questions from data)
and the GUI display (which shows questions to users). It handles the entire quiz experience
including question flow, scoring, answer validation, and results display.

The controller is optimized for performance and includes beginner-friendly comments
to help understand how interactive quiz systems work.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import traceback
from typing import List, Dict, Any, Optional

from .quiz_generator import WeatherQuizGenerator


class WeatherQuizController:
    """
    Enhanced Controller for the Weather Quiz feature - CSV DATA ONLY
    
    This class manages the entire quiz experience:
    - Loading and validating CSV weather data
    - Generating questions based on real data analysis
    - Managing quiz state (current question, score, etc.)
    - Handling user interactions (answers, navigation)
    - Displaying results and explanations
    
    Think of this as the "brain" that coordinates between data analysis and user interface.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the quiz controller with necessary components.
        
        Args:
            app: Main application object (provides GUI container and utilities)
            gui_controller: GUI management system (handles page navigation and widgets)
        """
        # Store references to main app components
        self.app = app
        self.gui = gui_controller
        
        # Initialize the quiz generator (handles CSV data analysis and question creation)
        self.quiz_generator = WeatherQuizGenerator()
        
        # Quiz state variables - track the current quiz session
        self.current_questions: List[Dict[str, Any]] = []  # List of question dictionaries
        self.current_question_index: int = 0  # Which question we're currently showing (0-based)
        self.user_answers: List[Dict[str, Any]] = []  # Store all user responses with metadata
        self.score: int = 0  # Number of correct answers
        self.quiz_started: bool = False  # Has the user started answering questions?
        self.quiz_completed: bool = False  # Has the user finished all questions?
        
        # GUI components - these will hold references to visual elements
        self.question_widgets: List = []  # List of GUI widgets for current question
        self.quiz_frame: Optional[tk.Frame] = None  # Main container for quiz content
        self.data_stats: Optional[Dict[str, Any]] = None  # Information about available data
        
        # Load data statistics at startup to check if CSV data is available
        self._load_data_stats()
        
    def _load_data_stats(self):
        """
        Load statistics about the available CSV data.
        
        This method checks what data is available and provides information
        for display to users. It helps determine if the quiz can function properly.
        """
        try:
            # Get basic data information from the quiz generator
            self.data_stats = self.quiz_generator.get_data_stats()
            
            # Also check data quality to warn about potential issues
            data_quality_info = self.quiz_generator.validate_data_quality()
            self.data_stats.update(data_quality_info)
            
            print(f"✓ Data stats loaded: {self.data_stats.get('total_records', 0)} records from {len(self.data_stats.get('cities', []))} cities")
            
        except Exception as e:
            print(f"Error loading data stats: {e}")
            # Create fallback stats indicating no data available
            self.data_stats = {
                "data_available": False, 
                "message": "Error loading data - quiz cannot be generated"
            }
    
    def build_page(self, window_width: int, window_height: int):
        """
        Build the main quiz page interface.
        
        This method creates all the visual elements for the quiz page,
        including the header, data status, and quiz area.
        
        Args:
            window_width: Width of the application window (for responsive layout)
            window_height: Height of the application window (for responsive layout)
        """
        try:
            # Add navigation back button (top-left corner)
            self._add_back_button()
            
            # Create main title header
            self._build_header(window_width)
            
            # Check if we have CSV data available for quiz generation
            if not self.data_stats.get('data_available', False):
                # No data available - show helpful error message instead of quiz
                self._build_no_data_message(window_width, window_height)
                return
            
            # Data is available - create the quiz interface
            self._build_quiz_area(window_width, window_height)
            
            # Start generating quiz questions in background (don't block the GUI)
            self._generate_quiz_async()
            
        except Exception as e:
            print(f"Error building quiz page: {e}")
            traceback.print_exc()
    
    def _add_back_button(self):
        """
        Add a back button to return to the main application page.
        
        This provides consistent navigation throughout the app and ensures
        users can always return to the main menu.
        """
        back_button = tk.Button(
            self.app,
            text="← Back",  # Left arrow indicates "go back"
            command=lambda: self.gui.show_page("main"),  # Navigate to main page
            bg="grey",
            fg="black",
            font=("Arial", 12, "bold"),
            relief="raised",  # 3D raised appearance
            borderwidth=2,
            width=8,
            height=1,
            activeforeground="black",  # Color when button is pressed
            activebackground="lightgrey",
            highlightthickness=0  # Remove focus outline
        )
        back_button.place(x=50, y=30, anchor="center")
        
        # Register button with GUI system for cleanup when page changes
        self.gui.widgets.append(back_button)
    
    def _build_header(self, window_width: int):
        """
        Build the quiz page header with title.
        
        Creates a clean, centered title that scales with window size.
        
        Args:
            window_width: Width of window for responsive font sizing
        """
        # Calculate responsive font size based on window width
        title_font_size = int(32 + window_width/40)
        
        title_label = self._create_black_label(
            self.app,
            text="🌤️ Weather Quiz",
            font=("Arial", title_font_size, "bold"),
            x=window_width/2,  # Center horizontally
            y=70  # Fixed vertical position
        )
        self.gui.widgets.append(title_label)
    
    def _build_no_data_message(self, window_width: int, window_height: int):
        """
        Build error message when CSV data is not available.
        
        This provides helpful guidance to users about what's needed
        for the quiz to work properly.
        
        Args:
            window_width: Window width for centering
            window_height: Window height for vertical centering
        """
        center_y = window_height // 2
        
        # Main error message with icon
        error_title = self._create_colored_label(
            self.app,
            text="📊 No Weather Data Available",
            font=("Arial", 24, "bold"),
            x=window_width/2,
            y=center_y - 80,
            color="red"
        )
        self.gui.widgets.append(error_title)
        
        # Detailed explanation of the problem
        explanation_text = (
            "The weather quiz requires CSV data to generate questions.\n\n"
            "Please ensure the 'combined.csv' file is present in the 'data' directory\n"
            "with weather records from multiple cities."
        )
        
        explanation_label = self._create_black_label(
            self.app,
            text=explanation_text,
            font=("Arial", 14),
            x=window_width/2,
            y=center_y,
            justify="center"
        )
        self.gui.widgets.append(explanation_label)
        
        # Technical requirements for developers
        requirements_text = (
            "Required CSV columns:\n"
            "• city\n"
            "• temperature_2m_max (°F)\n"
            "• temperature_2m_min (°F)\n"
            "• rain_sum (inch)\n"
            "• wind_speed_10m_max (mp/h)\n"
            "• relative_humidity_2m_mean (%)"
        )
        
        requirements_label = self._create_black_label(
            self.app,
            text=requirements_text,
            font=("Arial", 12),
            x=window_width/2,
            y=center_y + 80,
            justify="center"
        )
        self.gui.widgets.append(requirements_label)
    
    def _build_quiz_area(self, window_width: int, window_height: int):
        """
        Build the main quiz display area with proper responsive sizing.
        
        Creates a centered container where quiz questions and interactions
        will be displayed.
        
        Args:
            window_width: Total window width
            window_height: Total window height
        """
        # Calculate responsive dimensions and positioning
        quiz_start_y = 100  # Start below header
        quiz_height = window_height - 180  # Leave space for header and footer
        quiz_width = min(window_width - 60, 800)  # Max width of 800px, with margins
        quiz_x = (window_width - quiz_width) // 2  # Center horizontally
        
        # Create main quiz container frame
        canvas_bg_color = self._get_canvas_bg_color()
        self.quiz_frame = tk.Frame(
            self.app,
            bg=canvas_bg_color,
            relief="solid",  # Visible border
            borderwidth=2,
            highlightthickness=0
        )
        self.quiz_frame.place(
            x=quiz_x,
            y=quiz_start_y,
            width=quiz_width,
            height=quiz_height
        )
        self.gui.widgets.append(self.quiz_frame)
        
        # Show initial loading message while questions are being generated
        loading_label = self._create_black_label(
            self.quiz_frame,
            text="🧠 Analyzing CSV Data...\nGenerating questions from real weather patterns!",
            font=("Arial", 16),
            x=quiz_width//2,
            y=quiz_height//2
        )
    
    def _generate_quiz_async(self):
        """
        Generate quiz questions in a background thread.
        
        This prevents the GUI from freezing while the system analyzes
        CSV data and creates questions. Uses threading to run data
        processing in the background.
        """
        def generate_questions_background():
            """
            Background function that does the actual question generation.
            
            This runs in a separate thread so the GUI stays responsive
            while potentially time-consuming data analysis happens.
            """
            try:
                # Check if there are any data quality issues to warn about
                if (self.data_stats and 'issues' in self.data_stats and 
                    self.data_stats['issues']):
                    print("Data quality issues found:")
                    for issue in self.data_stats['issues']:
                        print(f"  - {issue}")
                
                # Generate questions using CSV data analysis
                print("Starting question generation from CSV data...")
                self.current_questions = self.quiz_generator.generate_quiz()
                
                # Check if question generation was successful
                if not self.current_questions:
                    error_message = (
                        "Unable to generate questions from CSV data.\n"
                        "Please check that the data file contains sufficient records "
                        "from multiple cities."
                    )
                    # Update GUI on main thread (required for thread safety)
                    self.app.after(0, lambda: self._show_error(error_message))
                    return
                
                print(f"✓ Generated {len(self.current_questions)} questions successfully")
                
                # Update UI on main thread (thread safety requirement)
                self.app.after(0, self._display_quiz_start)
                
            except Exception as e:
                error_message = f"Error generating quiz from CSV data: {str(e)}"
                print(f"Quiz generation error: {e}")
                traceback.print_exc()
                
                # Show error on main thread
                self.app.after(0, lambda: self._show_error(error_message))
        
        # Start background thread for question generation
        # daemon=True means thread will close when main program closes
        generation_thread = threading.Thread(target=generate_questions_background, daemon=True)
        generation_thread.start()
        print("Started background question generation thread")
    
    def _display_quiz_start(self):
        """
        Display the quiz start screen with data information and controls.
        
        This shows users information about the data being analyzed and
        provides options to start the quiz or view all possible questions.
        """
        try:
            # Clear any existing content in the quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            # Get frame dimensions for responsive layout
            frame_width = self.quiz_frame.winfo_width() or 600
            frame_height = self.quiz_frame.winfo_height() or 400
            
            # Welcome message indicating quiz is ready
            welcome_label = self._create_black_label(
                self.quiz_frame,
                text="📊 CSV Data Quiz Ready!",
                font=("Arial", 28, "bold"),
                x=frame_width//2,
                y=frame_height//2 - 100
            )
            
            # Show information about the data being analyzed
            if self.data_stats and self.data_stats.get('data_available', False):
                city_count = len(self.data_stats['cities'])
                record_count = self.data_stats['total_records']
                
                # Create data summary text
                cities_display = ', '.join(self.data_stats['cities'][:5])  # Show first 5 cities
                if city_count > 5:
                    cities_display += '...'  # Indicate there are more cities
                
                data_info_text = (
                    f"Analyzing {record_count:,} weather records from {city_count} cities:\n"
                    f"{cities_display}"
                )
            else:
                data_info_text = "Processing weather data..."
            
            data_info_label = self._create_black_label(
                self.quiz_frame,
                text=data_info_text,
                font=("Arial", 12),
                x=frame_width//2,
                y=frame_height//2 - 50,
                justify="center"
            )
            
            # Instructions for the user
            instructions_text = (
                f"Answer {len(self.current_questions)} questions based entirely on patterns\n"
                f"found in the real weather data.\n\n"
                f"Ready to test your data analysis skills?"
            )
            
            instructions_label = self._create_black_label(
                self.quiz_frame,
                text=instructions_text,
                font=("Arial", 14),
                x=frame_width//2,
                y=frame_height//2,
                justify="center"
            )
            
            # Main start button
            start_button = tk.Button(
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
            start_button.place(x=frame_width//2 - 80, y=frame_height//2 + 60, anchor="center")
            
            # Secondary button to preview all questions
            preview_button = tk.Button(
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
            preview_button.place(x=frame_width//2 + 80, y=frame_height//2 + 60, anchor="center")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _show_all_questions(self):
        """
        Show all possible questions that can be generated from the CSV data.
        
        This is useful for educators or users who want to understand
        what types of analysis the system can perform on the data.
        """
        try:
            # Get all possible questions from the generator
            all_possible_questions = self.quiz_generator.get_all_possible_questions()
            
            if not all_possible_questions:
                messagebox.showinfo(
                    "No Questions", 
                    "No questions could be generated from the current CSV data."
                )
                return
            
            # Create detailed text showing all questions organized by category
            questions_text = "All Possible Questions from CSV Data\n"
            questions_text += f"Generated from {len(self.data_stats.get('cities', []))} cities\n"
            questions_text += "=" * 70 + "\n\n"
            
            # Group questions by category for better organization
            current_category = ""
            for question_number, question_info in enumerate(all_possible_questions, 1):
                # Add category header when category changes
                if question_info['category'] != current_category:
                    current_category = question_info['category']
                    questions_text += f"\n{current_category} Questions:\n"
                    questions_text += "-" * 40 + "\n"
                
                # Add question details
                questions_text += f"Q{question_number}: {question_info['question']}\n"
                questions_text += f"Choices: {', '.join(question_info['choices'])}\n"
                questions_text += f"Answer: {question_info['correct_answer']}\n"
                questions_text += f"Explanation: {question_info['explanation']}\n\n"
            
            # Display in scrollable popup window
            popup_title = f"All CSV Questions ({len(all_possible_questions)} total)"
            self._show_info_popup(popup_title, questions_text)
            
        except Exception as e:
            self._show_error(f"Error generating questions list: {str(e)}")
    
    def _start_quiz(self):
        """
        Start the actual quiz by resetting state and showing first question.
        
        This initializes all quiz tracking variables and displays the first question.
        """
        try:
            # Reset all quiz state variables for a fresh start
            self.quiz_started = True
            self.current_question_index = 0
            self.user_answers = []
            self.score = 0
            self.quiz_completed = False
            
            print(f"Starting quiz with {len(self.current_questions)} questions")
            
            # Display the first question
            self._display_current_question()
            
        except Exception as e:
            self._show_error(str(e))
    
    def _display_current_question(self):
        """
        Display the current question with answer choices and navigation.
        
        This is the main question display function that shows:
        - Progress indicator
        - Question text  
        - Multiple choice answers
        - Navigation buttons
        """
        try:
            # Clear previous question content
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            # Check if quiz is complete
            if self.current_question_index >= len(self.current_questions):
                self._display_quiz_results()
                return
            
            # Get current question data
            current_question = self.current_questions[self.current_question_index]
            frame_width = self.quiz_frame.winfo_width() or 600
            frame_height = self.quiz_frame.winfo_height() or 400
            
            # Create progress indicator with current score
            progress_text = f"Question {self.current_question_index + 1} of {len(self.current_questions)}"
            if self.current_question_index > 0:
                current_score_percentage = round((self.score / self.current_question_index) * 100)
                progress_text += f" | Score: {self.score}/{self.current_question_index} ({current_score_percentage}%)"
            
            progress_label = self._create_black_label(
                self.quiz_frame,
                text=progress_text,
                font=("Arial", 12, "bold"),
                x=frame_width//2,
                y=20
            )
            
            # Display the question text with text wrapping
            question_text = current_question["question"]
            question_label = self._create_black_label(
                self.quiz_frame,
                text=question_text,
                font=("Arial", 14, "bold"),
                x=frame_width//2,
                y=60,
                justify="center",
                wraplength=frame_width - 40  # Wrap text to fit in frame
            )
            
            # Create radio buttons for answer choices
            self.selected_answer = tk.StringVar()  # Tracks which answer is selected
            
            choice_start_y = 120
            choice_spacing = 40  # Vertical space between choices
            
            # Create radio button for each answer choice
            for choice_index, choice_text in enumerate(current_question["choices"]):
                choice_letter = chr(65 + choice_index)  # A, B, C, D
                
                radio_button = tk.Radiobutton(
                    self.quiz_frame,
                    text=f"{choice_letter}. {choice_text}",
                    variable=self.selected_answer,
                    value=choice_text,
                    font=("Arial", 12),
                    fg="black",
                    bg=self._get_canvas_bg_color(),
                    selectcolor="lightblue",  # Color when selected
                    activebackground=self._get_canvas_bg_color(),
                    activeforeground="black",
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0,
                    wraplength=frame_width - 80,  # Wrap long answer text
                    justify="left",
                    anchor="w"  # Left-align text
                )
                radio_button.place(x=40, y=choice_start_y + choice_index * choice_spacing, anchor="w")
            
            # Create navigation buttons
            button_y = frame_height - 60
            
            # Next/Submit button (changes text on last question)
            if self.current_question_index == len(self.current_questions) - 1:
                button_text = "🏁 Finish Quiz"
                button_color = "lightcoral"
            else:
                button_text = "➡️ Next Question"
                button_color = "lightblue"
            
            next_button = tk.Button(
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
            next_button.place(x=frame_width//2, y=button_y, anchor="center")
            
            # Back button (only show if not on first question)
            if self.current_question_index > 0:
                back_button = tk.Button(
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
                back_button.place(x=frame_width//2 - 120, y=button_y, anchor="center")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _go_back_question(self):
        """
        Go back to the previous question.
        
        This allows users to review and change their answers, providing
        a better user experience for the quiz.
        """
        if self.current_question_index > 0:
            self.current_question_index -= 1
            
            # Remove the most recent answer if going back
            # This prevents having answers for questions we haven't reached yet
            if len(self.user_answers) > self.current_question_index:
                removed_answer = self.user_answers.pop()
                # Adjust score if we're removing a correct answer
                if removed_answer['is_correct']:
                    self.score -= 1
            
            print(f"Going back to question {self.current_question_index + 1}")
            self._display_current_question()
    
    def _answer_question(self):
        """
        Process the user's answer and advance to the next question.
        
        This method:
        - Validates that an answer was selected
        - Checks if the answer is correct
        - Updates the score
        - Stores the answer for later review
        - Advances to the next question
        """
        try:
            # Validate that user selected an answer
            if not hasattr(self, 'selected_answer') or not self.selected_answer.get():
                messagebox.showwarning(
                    "No Answer Selected", 
                    "Please select an answer before continuing."
                )
                return
            
            # Get question and answer information
            current_question = self.current_questions[self.current_question_index]
            user_answer = self.selected_answer.get()
            correct_answer = current_question["correct_answer"]
            is_correct = user_answer == correct_answer
            
            print(f"Question {self.current_question_index + 1}: User answered '{user_answer}', correct answer is '{correct_answer}' - {'✓' if is_correct else '✗'}")
            
            # Handle updating existing answers (when user goes back and forth)
            if len(self.user_answers) > self.current_question_index:
                # User is changing a previous answer
                old_answer = self.user_answers[self.current_question_index]
                if old_answer['is_correct']:
                    self.score -= 1  # Remove point from old correct answer
                
                # Update the existing answer record
                self.user_answers[self.current_question_index] = {
                    "question": current_question["question"],
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "explanation": current_question["explanation"],
                    "is_correct": is_correct
                }
            else:
                # This is a new answer
                self.user_answers.append({
                    "question": current_question["question"],
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "explanation": current_question["explanation"],
                    "is_correct": is_correct
                })
            
            # Update score for correct answers
            if is_correct:
                self.score += 1
            
            # Move to next question
            self.current_question_index += 1
            
            print(f"Current score: {self.score}/{self.current_question_index}")
            
            # Display next question (or results if finished)
            self._display_current_question()
            
        except Exception as e:
            self._show_error(str(e))
    
    # Additional helper methods for UI creation and management
    def _create_black_label(self, parent, text, font, x, y, anchor="center", **kwargs):
        """Create a label with black text and transparent background."""
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
        """Create a label with specified color text and transparent background."""
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
        """Get the current canvas background color."""
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"
        except:
            return "#87CEEB"
    
    def _show_error(self, error_msg):
        """Show error message with CSV data context."""
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
        """Show information in a popup window with scrollable text."""
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
    
    def _display_quiz_results(self):
        """
        Display comprehensive quiz results with score and performance analysis.
        
        This creates a detailed results screen showing:
        - Final score and percentage
        - Performance feedback
        - Action buttons for review and retrying
        """
        try:
            # Clear quiz frame
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            
            self.quiz_completed = True
            frame_width = self.quiz_frame.winfo_width() or 600
            frame_height = self.quiz_frame.winfo_height() or 400
            
            # Calculate final percentage score
            percentage = round((self.score / len(self.current_questions)) * 100)
            
            # Determine performance feedback based on score
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
            
            # Results header with performance emoji
            results_header = self._create_colored_label(
                self.quiz_frame,
                text=f"{emoji} CSV Quiz Complete! {emoji}",
                font=("Arial", 24, "bold"),
                x=frame_width//2,
                y=frame_height//2 - 120,
                color=color
            )
            
            # Score display
            score_label = self._create_black_label(
                self.quiz_frame,
                text=f"Final Score: {self.score}/{len(self.current_questions)} ({percentage}%)",
                font=("Arial", 20, "bold"),
                x=frame_width//2,
                y=frame_height//2 - 80
            )
            
            # Performance message
            message_label = self._create_colored_label(
                self.quiz_frame,
                text=message,
                font=("Arial", 16),
                x=frame_width//2,
                y=frame_height//2 - 40,
                color=color
            )
            
            # Data source information
            city_count = len(self.data_stats.get('cities', []))
            data_label = self._create_black_label(
                self.quiz_frame,
                text=f"Based on real weather data from {city_count} cities",
                font=("Arial", 12),
                x=frame_width//2,
                y=frame_height//2 - 10
            )
            
            # Action buttons
            button_y = frame_height//2 + 20
            button_spacing = 140
            
            # Review answers button
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
            
            # Retry quiz button
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
            
            # Share score button
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
            
            print(f"Quiz completed! Final score: {self.score}/{len(self.current_questions)} ({percentage}%)")
            
        except Exception as e:
            self._show_error(str(e))
    
    def _show_detailed_results(self):
        """Show comprehensive answer review with CSV data insights."""
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
        """Share CSV quiz results to clipboard."""
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
        """Restart the quiz with new CSV-based questions."""
        try:
            # Reset all quiz state
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
    
    def handle_theme_change(self):
        """Handle theme changes by updating background colors."""
        try:
            canvas_bg = self._get_canvas_bg_color()
            if self.quiz_frame:
                self.quiz_frame.configure(bg=canvas_bg)
        except Exception as e:
            pass
    
    def cleanup(self):
        """Clean up resources when quiz page is closed."""
        try:
            if self.quiz_frame:
                for widget in self.quiz_frame.winfo_children():
                    widget.destroy()
        except Exception as e:
            pass