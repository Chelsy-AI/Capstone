"""
Simplified Weather Quiz Generator - Randomly selects questions from database
Modified to pull 5 random questions from the static questions database

This module loads pre-defined questions and randomly selects 5 for each quiz session.
All questions are based on real weather data analysis but are now stored statically.
"""

import random
from typing import List, Dict, Any, Optional
from .questions_database import get_all_questions, get_question_count, get_categories


class WeatherQuizGenerator:
    """
    Simplified quiz generator that randomly selects questions from a static database.
    
    This class no longer analyzes CSV data directly. Instead, it pulls from pre-computed
    questions that were created based on comprehensive weather data analysis.
    """
    
    def __init__(self):
        """
        Initialize the quiz generator.
        
        Loads the static question database and verifies questions are available.
        """
        # Load all available questions from the database
        self.all_questions = get_all_questions()
        self.data_loaded = len(self.all_questions) > 0
        
        # Cache for performance
        self._categories = None
        
        if self.data_loaded:
            print(f"✓ Loaded {len(self.all_questions)} pre-computed questions from database")
        else:
            print("❌ No questions available in database")
    
    def generate_quiz(self) -> List[Dict[str, Any]]:
        """
        Generate exactly 5 random quiz questions from the database.
        
        This method randomly selects 5 unique questions from the static database,
        ensuring variety and different quiz experiences each time.
        
        Returns:
            List[Dict]: List of 5 quiz question dictionaries
        """
        # Check if we have enough questions
        if not self.data_loaded or len(self.all_questions) < 5:
            print("❌ Not enough questions in database to generate quiz")
            return []
        
        print(f"Generating 5 random questions from {len(self.all_questions)} available questions")
        
        # Randomly select 5 unique questions
        selected_questions = random.sample(self.all_questions, 5)
        
        # Convert to the format expected by the controller
        quiz_questions = []
        for question_data in selected_questions:
            # Create a copy and remove the ID to match expected format
            quiz_question = {
                "question": question_data["question"],
                "choices": question_data["choices"].copy(),
                "correct_answer": question_data["correct_answer"],
                "explanation": question_data["explanation"],
                "category": question_data["category"]
            }
            quiz_questions.append(quiz_question)
        
        # Log the selected questions for debugging
        print("Selected questions:")
        for i, q in enumerate(quiz_questions, 1):
            print(f"  {i}. [{q['category']}] {q['question'][:60]}...")
        
        return quiz_questions
    
    def get_data_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the available questions database.
        
        Returns:
            Dict containing database statistics and availability info
        """
        if not self.data_loaded:
            return {
                "data_available": False,
                "message": "No questions available in database"
            }
        
        # Count questions by category
        categories = self.get_categories()
        category_counts = {}
        for category in categories:
            category_counts[category] = len([q for q in self.all_questions if q["category"] == category])
        
        return {
            "data_available": True,
            "total_questions": len(self.all_questions),
            "categories": categories,
            "category_breakdown": category_counts,
            "cities": ["Phoenix", "Ahmedabad", "Denver", "Columbus", "Lebrija"],  # Static list from questions
            "total_records": "Pre-computed from comprehensive weather dataset",
            "quiz_capability": "static_database"
        }
    
    def validate_data_quality(self) -> Dict[str, Any]:
        """
        Validate the quality of the questions database.
        
        Returns:
            Dict containing quality assessment and list of issues
        """
        if not self.data_loaded:
            return {"quality": "none", "issues": ["No questions loaded from database"]}
        
        issues = []
        quality = "excellent"
        
        # Check if we have enough questions for variety
        if len(self.all_questions) < 10:
            issues.append(f"Limited question pool: only {len(self.all_questions)} questions")
            quality = "fair"
        
        # Check if we have diverse categories
        categories = self.get_categories()
        if len(categories) < 3:
            issues.append(f"Limited question variety: only {len(categories)} categories")
            quality = "good"
        
        # Check for duplicate questions (basic check)
        question_texts = [q["question"] for q in self.all_questions]
        if len(question_texts) != len(set(question_texts)):
            issues.append("Duplicate questions detected in database")
            quality = "good"
        
        return {"quality": quality, "issues": issues}
    
    def get_categories(self) -> List[str]:
        """
        Get all unique question categories.
        
        Returns:
            List of category names
        """
        if self._categories is None:
            self._categories = list(set(q["category"] for q in self.all_questions))
        return self._categories
    
    def get_all_possible_questions(self) -> List[Dict[str, Any]]:
        """
        Get all possible questions from the database.
        
        This is useful for showing users what types of questions are available.
        
        Returns:
            List of all question dictionaries with category information
        """
        return self.all_questions.copy()  # Return a copy to prevent modification
    
    def get_questions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all questions from a specific category.
        
        Args:
            category: Category name to filter by
            
        Returns:
            List of questions in the specified category
        """
        return [q for q in self.all_questions if q["category"] == category]
    
    def generate_quiz_from_category(self, category: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """
        Generate a quiz with questions from a specific category.
        
        Args:
            category: Category to select questions from
            num_questions: Number of questions to select (default 5)
            
        Returns:
            List of quiz questions from the specified category
        """
        category_questions = self.get_questions_by_category(category)
        
        if len(category_questions) < num_questions:
            print(f"⚠ Only {len(category_questions)} questions available in category '{category}'")
            num_questions = len(category_questions)
        
        if num_questions == 0:
            return []
        
        # Randomly select questions from the category
        selected_questions = random.sample(category_questions, num_questions)
        
        # Convert to quiz format
        quiz_questions = []
        for question_data in selected_questions:
            quiz_question = {
                "question": question_data["question"],
                "choices": question_data["choices"].copy(),
                "correct_answer": question_data["correct_answer"],
                "explanation": question_data["explanation"],
                "category": question_data["category"]
            }
            quiz_questions.append(quiz_question)
        
        return quiz_questions
    
    def get_random_question(self) -> Optional[Dict[str, Any]]:
        """
        Get a single random question from the database.
        
        Returns:
            Single question dictionary or None if no questions available
        """
        if not self.data_loaded:
            return None
        
        return random.choice(self.all_questions)
    
    def search_questions(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for questions containing a specific term.
        
        Args:
            search_term: Term to search for in question text
            
        Returns:
            List of questions containing the search term
        """
        search_term = search_term.lower()
        matching_questions = []
        
        for question in self.all_questions:
            if (search_term in question["question"].lower() or 
                search_term in question["explanation"].lower() or
                any(search_term in choice.lower() for choice in question["choices"])):
                matching_questions.append(question)
        
        return matching_questions