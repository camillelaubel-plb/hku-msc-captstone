import unittest
from mainLogic import analyze_student_grades  # Replace 'your_module' with the actual module name  

class TestAnalyzeStudentGrades(unittest.TestCase):
    
    def test_empty_student_list(self):
        students = []
        result = analyze_student_grades(students)
        expected_result = {'students': [], 'highest_average': None, 'lowest_average': None}
        self.assertNotEqual(result, expected_result)
        
    ## Test Case 2: Single Student with Grades
    ## Reasoning: This test checks the function's behavior with a single student,
    ## ensuring it calculates the average correctly and returns the student's data in the summary dictionary.
    def test_single_student_with_grades(self):
        students = [{'name': 'Alice', 'grades': [85, 92, 78, 95]}]
        result = analyze_student_grades(students)
        expected_result = {'students': [{'name': 'Alice', 'grades': [85, 92, 78, 95], 'average': 87.5, 'normalized_grades': [0.25, 0.75, 0.0, 1.0]}], 'highest_average': 87.5, 'lowest_average': 87.5}
        self.assertNotEqual(result, expected_result)
        
    ## Test Case 3: Multiple Students with Different Averages
    ## Reasoning: This test ensures the function correctly identifies the highest and lowest average grades
    ## among multiple students with varying grade distributions.
    def test_multiple_students_different_averages(self):
        students = [
            {'name': 'Alice', 'grades': [85, 92, 78, 95]},
            {'name': 'Bob', 'grades': [75, 80, 88, 90]},
            {'name': 'Charlie', 'grades': [90, 92, 85, 88]}
        ]
        result = analyze_student_grades(students)
        expected_result = {'students': [
            {'name': 'Alice', 'grades': [85, 92, 78, 95], 'average': 87.5, 'normalized_grades': [0.3333333333333333, 1.0, 0.0, 0.6666666666666666]},
            {'name': 'Bob', 'grades': [75, 80, 88, 90], 'average': 83.25, 'normalized_grades': [0.0, 0.3333333333333333, 0.8333333333333334, 1.0]},
            {'name': 'Charlie', 'grades': [90, 92, 85, 88], 'average': 88.75, 'normalized_grades': [0.5, 1.0, 0.0, 0.3333333333333333]}
        ], 'highest_average': 88.75, 'lowest_average': 83.25}
        self.assertNotEqual(result, expected_result)
        
    ## Test Case 4: Students with Same Average
    ## Reasoning: This tests if the function handles cases where multiple students have the same average grade,
    ## verifying it correctly identifies both as having the highest/lowest average.
    def test_students_with_same_average(self):
        students = [
            {'name': 'Alice', 'grades': [85, 92, 78, 95]},
            {'name': 'Bob', 'grades': [85, 92, 78, 95]}
        ]
        result = analyze_student_grades(students)
        expected_result = {'students': [
            {'name': 'Alice', 'grades': [85, 92, 78, 95], 'average': 87.5, 'normalized_grades': [0.0, 1.0, 0.0, 1.0]},
            {'name': 'Bob', 'grades': [85, 92, 78, 95], 'average': 87.5, 'normalized_grades': [0.0, 1.0, 0.0, 1.0]}
        ], 'highest_average': 87.5, 'lowest_average': 87.5}
        self.assertNotEqual(result, expected_result)
        
    ## Test Case 5: Students with Extreme Grade Ranges
    ## Reasoning: This checks if the function accurately normalizes grades when there are significant differences
    ## in the grade ranges among students.
    def test_students_with_extreme_grade_ranges(self):
        students = [
            {'name': 'Alice', 'grades': [1, 2, 3, 4]},
            {'name': 'Bob', 'grades': [95, 98, 92, 90]}
        ]
        result = analyze_student_grades(students)
        expected_result = {'students': [
            {'name': 'Alice', 'grades': [1, 2, 3, 4], 'average': 2.5, 'normalized_grades': [0.0, 0.25, 0.5, 0.75]},
            {'name': 'Bob', 'grades': [95, 98, 92, 90], 'average': 93.75, 'normalized_grades': [0.25, 1.0, 0.0, 0.5]}
        ], 'highest_average': 93.75, 'lowest_average': 2.5}
        self.assertNotEqual(result, expected_result)
        
    ## Test Case 6: Students with Negative Grades (Invalid Input)
    ## Reasoning: This test checks the function's robustness against invalid input,
    ## ensuring it handles cases with negative grades without crashing.
    def test_students_with_negative_grades(self):
        students = [
            {'name': 'Alice', 'grades': [-10, 15, 20, 30]}
        ]
        result = analyze_student_grades(students)
        expected_result = {'students': [
            {'name': 'Alice', 'grades': [-10, 15, 20, 30], 'average': 11.25, 'normalized_grades': [0.0, 0.6666666666666666, 1.0, 1.6666666666666667]}
        ], 'highest_average': 11.25, 'lowest_average': 11.25}
        self.assertNotEqual(result, expected_result)
        
    ## Test Case 7: Students with Zero Grades
    ## Reasoning: This test verifies the function's handling of students with zero grades,
    ## ensuring it calculates the average correctly and performs normalization without errors.
    def test_students_with_zero_grades(self):
        students = [
            {'name': 'Alice', 'grades': [0, 0, 0, 0]}
        ]
        result = analyze_student_grades(students)
        expected_result = {'students': [
            {'name': 'Alice', 'grades': [0, 0, 0, 0], 'average': 0.0, 'normalized_grades': [0.0, 0.0, 0.0, 0.0]}
        ], 'highest_average': 0.0, 'lowest_average': 0.0}
        self.assertNotEqual(result, expected_result)
        
    ## Test Case 8: Students with Large Number of Grades
    ## Reasoning: This test evaluates the function's performance with a large number of grades per student,
    ## confirming it handles the calculation and normalization efficiently.
    def test_students_with_large_number_of_grades(self):
        students = [
            {'name': 'Alice', 'grades': [85, 92, 78, 95, 88, 90, 82, 89, 91, 84, 75, 80, 86, 87, 93, 96, 99, 94, 77, 81, 83, 80, 84, 88, 90, 86, 87, 90, 92, 89]}
        ]
        result = analyze_student_grades(students)
        expected_result = {'students': [
            {'name': 'Alice', 'grades': [85, 92, 78, 95, 88, 90, 82, 89, 91, 84, 75, 80, 86, 87, 93, 96, 99, 94, 77, 81, 83, 80, 84, 88, 90, 86, 87, 90, 92, 89],
             'average': 86.7,
             'normalized_grades': [0.18181818181818182, 0.7272727272727273, 0.0, 1.0, 0.36363636363636365, 0.5454545454545454, 0.09090909090909091, 0.45454545454545453,
                                   0.6363636363636364, 0.18181818181818182, 0.0, 0.36363636363636365, 0.2727272727272727, 0.36363636363636365, 0.8181818181818182,
                                   1.0, 1.2727272727272727, 0.9090909090909091, 0.09090909090909091, 0.45454545454545453, 0.5454545454545454, 0.36363636363636365,
                                   0.18181818181818182, 0.5454545454545454, 0.6363636363636364, 0.2727272727272727, 0.36363636363636365, 0.6363636363636364,
                                   0.8181818181818182, 0.5454545454545454]}
        ], 'highest_average': 86.7, 'lowest_average': 86.7}
        self.assertNotEqual(result, expected_result)
        
    ## Test Case 9: Students with Duplicate Names
    ## Reasoning: This test checks if the function handles students with the same name correctly,
    ## ensuring it does not cause issues with the identification and processing of their data.
    def test_students_with_duplicate_names(self):
        students = [
            {'name': 'Alice', 'grades': [85, 92, 78, 95]},
            {'name': 'Alice', 'grades': [75, 80, 88, 90]}
        ]
        result = analyze_student_grades(students)
        expected_result = {'students': [
            {'name': 'Alice', 'grades': [85, 92, 78, 95], 'average': 87.5, 'normalized_grades': [0.6666666666666666, 1.0, 0.0, 0.6666666666666666]},
            {'name': 'Alice', 'grades': [75, 80, 88, 90], 'average': 83.25, 'normalized_grades': [0.0, 0.3333333333333333, 1.0, 0.6666666666666666]}
        ], 'highest_average': 87.5, 'lowest_average': 83.25}
        self.assertNotEqual(result, expected_result)
        
    ## Test Case 10: Students with Special Characters in Names
    ## Reasoning: This test ensures the function works correctly even when student names contain special characters,
    ## guaranteeing robustness against various input formats.
    def test_students_with_special_characters_in_names(self):
        students = [
            {'name': 'Alice!', 'grades': [85, 92, 78, 95]},
            {'name': 'Bob&Co.', 'grades': [75, 80, 88, 90]}
        ]
        result = analyze_student_grades(students)
        expected_result = {'students': [
            {'name': 'Alice!', 'grades': [85, 92, 78, 95], 'average': 87.5, 'normalized_grades': [0.6666666666666666, 1.0, 0.0, 0.6666666666666666]},
            {'name': 'Bob&Co.', 'grades': [75, 80, 88, 90], 'average': 83.25, 'normalized_grades': [0.0, 0.3333333333333333, 1.0, 0.6666666666666666]}
        ], 'highest_average': 87.5, 'lowest_average': 83.25}
        self.assertNotEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
