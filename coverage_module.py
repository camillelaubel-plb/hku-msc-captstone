
import unittest
import numpy as np

def analyze_student_grades(students):
    # Calculate average grades for each student
    for student in students:
        student['average'] = np.mean(student['grades'])
    # Find the highest and lowest average grades
    highest_avg = max(students, key=lambda x: x['average'])['average']
    lowest_avg = min(students, key=lambda x: x['average'])['average']
    # Normalize the grades
    for student in students:
        student['normalized_grades'] = [(grade - lowest_avg) / (highest_avg - lowest_avg) for grade in student['grades']]
    # Prepare the summary
    summary = {'students': students, 'highest_average': highest_avg, 'lowest_average': lowest_avg,}
    return summary

class TestAnalyzeStudentGrades(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(analyze_student_grades([]), {'students': [], 'highest_average': None, 'lowest_average': None})

    def test_single_student(self):
        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}]
        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(1.0), np.float64(0.0), np.float64(1.0), np.float64(0.5)]}], 'highest_average': np.float64(85.25), 'lowest_average': np.float64(85.25)}
        self.assertEqual(analyze_student_grades(students), expected_output)

    def test_multiple_students(self):
        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}, {'name': 'Bob', 'grades': [95, 98, 91, 93]}]
        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(0.0), np.float64(-1.0), np.float64(0.5), np.float64(0.0)]}, {'name': 'Bob', 'grades': [95, 98, 91, 93], 'average': np.float64(94.25), 'normalized_grades': [np.float64(1.0), np.float64(1.0), np.float64(0.5), np.float64(0.0)]}], 'highest_average': np.float64(94.25), 'lowest_average': np.float64(85.25)}
        self.assertEqual(analyze_student_grades(students), expected_output)

    def test_students_with_different_average(self):
        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}, {'name': 'Bob', 'grades': [95, 98, 91, 93]}, {'name': 'Charlie', 'grades': [72, 84, 78, 80]}]
        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(0.45454545454545453), np.float64(-0.5454545454545454), np.float64(0.9090909090909091), np.float64(0.0)]}, {'name': 'Bob', 'grades': [95, 98, 91, 93], 'average': np.float64(94.25), 'normalized_grades': [np.float64(1.0), np.float64(1.0), np.float64(0.5), np.float64(0.0)]}, {'name': 'Charlie', 'grades': [72, 84, 78, 80], 'average': np.float64(78.5), 'normalized_grades': [np.float64(-0.8181818181818182), np.float64(0.0), np.float64(-0.2727272727272727), np.float64(-0.18181818181818182)]}], 'highest_average': np.float64(94.25), 'lowest_average': np.float64(78.5)}
        self.assertEqual(analyze_student_grades(students), expected_output)

    def test_students_with_same_average(self):
        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}, {'name': 'Bob', 'grades': [88, 76, 92, 85]}]
        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(1.0), np.float64(0.0), np.float64(1.0), np.float64(0.5)]}, {'name': 'Bob', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(1.0), np.float64(0.0), np.float64(1.0), np.float64(0.5)]}], 'highest_average': np.float64(85.25), 'lowest_average': np.float64(85.25)}
        self.assertEqual(analyze_student_grades(students), expected_output)

if __name__ == '__main__':
    unittest.main()
