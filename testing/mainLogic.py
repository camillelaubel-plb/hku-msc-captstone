import numpy as np

def analyze_student_grades(students):
    if not students:
        # Check if the students list is empty
        return {'students': [], 'highest_average': None, 'lowest_average': None}
    
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
    summary = {
        'students': students,
        'highest_average': highest_avg,
        'lowest_average': lowest_avg,
    }
    
    return summary
