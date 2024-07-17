# hku-msc-captstone

## Production Environment
Web App: https://20091g059.pythonanywhere.com/ 
API endpoint: https://test-generation-uh7bect6ia-de.a.run.app/ask-ai 

### Creating your own API key
- https://aistudio.google.com/app/apikey
- Or use the default one directly in the web app

## Local Testing and Development
### VPN
Google Gemini LLM is not supported in HK local IP address.
Use a VPN to change your address:
- Proton VPN (Free) or any other VPN will suffice
- [Proton VPN: Secure, fast VPN service in 90+ countries](https://protonvpn.com/)

### Start localhost
Run: `flask --app main --debug run`
Endpoint: http://127.0.0.1:5000/ask-ai

### Adding external library
Add library to `requirements.txt`
Run: `pip install -r requirements.txt` on project root directory

### Deploy to cloud host
Login to Google Cloud CLI
Run: `gcloud run deploy test-generation --image asia-east1-docker.pkg.dev/msc-capstone-2024/cloud-run-source-deploy/test-generation`
Pick Region 2: asia-east1

## Sample JSON Input to the API
```JSON
{
    "apiKey": "AIzaSyDbsRqw8z3CKFJ-g-uiiPiHfBCevbqPayg",
    "code": "def analyze_student_grades(students):\n    # Calculate average grades for each student\n    for student in students:\n        student['average'] = np.mean(student['grades'])\n    # Find the highest and lowest average grades\n    highest_avg = max(students, key=lambda x: x['average'])['average']\n    lowest_avg = min(students, key=lambda x: x['average'])['average']\n    # Normalize the grades\n    for student in students:\n        student['normalized_grades'] = [(grade - lowest_avg) / (highest_avg - lowest_avg) for grade in student['grades']]\n    # Prepare the summary\n    summary = {'students': students, 'highest_average': highest_avg, 'lowest_average': lowest_avg,}\n    return summary",
    "data": {
        "inputType": "{'name': 'Alice', 'grades': [88, 76, 92, 85]}",
        "boundary": "grades should be positive numbers less than infinity"
    },
    "result": {
        "expectedOutput": "A summary including the average grades, highest/lowest averages, and normalized grades"
    }
}
```

## Sample JSON Output from the API
``` JSON
{
    "metrics": {
        "coverage": "{\n  \"meta\": {\n    \"format\": 2,\n    \"version\": \"7.5.3\",\n    \"timestamp\": \"2024-07-13T11:03:00.515304\",\n    \"branch_coverage\": true,\n    \"show_contexts\": false\n  },\n  \"files\": {\n    \"coverage_module.py\": {\n      \"executed_lines\": [\n        2,\n        3,\n        5,\n        19,\n        20,\n        23,\n        28,\n        33,\n        38,\n        43\n      ],\n      \"summary\": {\n        \"covered_lines\": 10,\n        \"num_statements\": 32,\n        \"percent_covered\": 26.19047619047619,\n        \"percent_covered_display\": \"26\",\n        \"missing_lines\": 22,\n        \"excluded_lines\": 0,\n        \"num_branches\": 10,\n        \"num_partial_branches\": 1,\n        \"covered_branches\": 1,\n        \"missing_branches\": 9\n      },\n      \"missing_lines\": [\n        7,\n        8,\n        10,\n        11,\n        13,\n        14,\n        16,\n        17,\n        21,\n        24,\n        25,\n        26,\n        29,\n        30,\n        31,\n        34,\n        35,\n        36,\n        39,\n        40,\n        41,\n        44\n      ],\n      \"excluded_lines\": [],\n      \"executed_branches\": [\n        [\n          43,\n          -1\n        ]\n      ],\n      \"missing_branches\": [\n        [\n          7,\n          8\n        ],\n        [\n          7,\n          10\n        ],\n        [\n          10,\n          -10\n        ],\n        [\n          10,\n          11\n        ],\n        [\n          11,\n          -11\n        ],\n        [\n          11,\n          13\n        ],\n        [\n          13,\n          14\n        ],\n        [\n          13,\n          16\n        ],\n        [\n          43,\n          44\n        ]\n      ]\n    }\n  },\n  \"totals\": {\n    \"covered_lines\": 10,\n    \"num_statements\": 32,\n    \"percent_covered\": 26.19047619047619,\n    \"percent_covered_display\": \"26\",\n    \"missing_lines\": 22,\n    \"excluded_lines\": 0,\n    \"num_branches\": 10,\n    \"num_partial_branches\": 1,\n    \"covered_branches\": 1,\n    \"missing_branches\": 9\n  }\n}",
        "execution_time": 0.006150960922241211,
        "memory_usage": 202453
    },
    "sample_data": [
        {
            "grades": [
                88,
                76,
                92,
                85
            ],
            "name": "Alice"
        },
        {
            "grades": [
                95,
                98,
                90,
                92
            ],
            "name": "Bob"
        },
        {
            "grades": [
                70,
                75,
                80,
                85
            ],
            "name": "Charlie"
        },
        {
            "grades": [
                100,
                99,
                98,
                97
            ],
            "name": "David"
        },
        {
            "grades": [
                65,
                68,
                72,
                75
            ],
            "name": "Eve"
        },
        {
            "grades": [
                82,
                88,
                80,
                84
            ],
            "name": "Frank"
        },
        {
            "grades": [
                91,
                93,
                95,
                97
            ],
            "name": "Grace"
        },
        {
            "grades": [
                78,
                82,
                76,
                80
            ],
            "name": "Henry"
        },
        {
            "grades": [
                90,
                85,
                92,
                88
            ],
            "name": "Isabella"
        },
        {
            "grades": [
                60,
                62,
                65,
                68
            ],
            "name": "Jack"
        },
        {
            "grades": [
                87,
                89,
                91,
                93
            ],
            "name": "Katie"
        },
        {
            "grades": [
                72,
                74,
                76,
                78
            ],
            "name": "Liam"
        },
        {
            "grades": [
                94,
                96,
                98,
                100
            ],
            "name": "Mia"
        },
        {
            "grades": [
                81,
                83,
                85,
                87
            ],
            "name": "Noah"
        },
        {
            "grades": [
                67,
                70,
                73,
                76
            ],
            "name": "Olivia"
        },
        {
            "grades": [
                92,
                90,
                88,
                86
            ],
            "name": "Peter"
        },
        {
            "grades": [
                79,
                81,
                83,
                85
            ],
            "name": "Quinn"
        },
        {
            "grades": [
                63,
                66,
                69,
                72
            ],
            "name": "Ryan"
        },
        {
            "grades": [
                84,
                86,
                88,
                90
            ],
            "name": "Sophia"
        },
        {
            "grades": [
                75,
                77,
                79,
                81
            ],
            "name": "Thomas"
        },
        {
            "grades": [
                97,
                95,
                93,
                91
            ],
            "name": "Uma"
        },
        {
            "grades": [
                61,
                64,
                67,
                70
            ],
            "name": "Victor"
        },
        {
            "grades": [
                80,
                82,
                84,
                86
            ],
            "name": "Wendy"
        },
        {
            "grades": [
                73,
                76,
                79,
                82
            ],
            "name": "Xavier"
        }
    ],
    "suggestions": [
        "**Performance Bottlenecks:**\n - The code iterates over the `students` list multiple times: once to calculate averages, once to find highest/lowest, and again to normalize. This can be optimized by calculating averages, finding highest/lowest, and normalizing all in a single pass.\n - The `max` and `min` operations on the entire `students` list are O(n) operations. If the number of students is large, these operations could become a bottleneck. Consider using a data structure that keeps track of the highest and lowest averages as you process the students, potentially using a heap or a sorted list.",
        "**Potential Security Vulnerabilities:**\n - None. The code primarily deals with data manipulation and doesn't directly interact with external sources or systems that could introduce security risks.",
        "**Potential Bugs:**\n - **Division by Zero:** If the `highest_avg` and `lowest_avg` are equal (all students have the same average), the normalization calculation would lead to division by zero. Consider handling this case by either returning an error or setting the normalized grades to zero.",
        " - **Modification of Input:** The function modifies the input `students` list by adding `average` and `normalized_grades` fields. This might not be desirable if the original list needs to be preserved. Consider making a copy of the `students` list before modifying it.",
        "**General Improvement of Code Style:**\n - **Descriptive Variable Names:** Use more descriptive variable names. For example, instead of `x` in the lambda function, use `student`.\n - **Docstrings:** Add a docstring to explain the function's purpose, parameters, and return value.\n - **Readability:** Add more descriptive comments to explain the logic of the code.  Consider breaking down the normalization logic into a separate function for better readability and reusability.\n - **Return a Tuple:** Instead of modifying the input list and returning a dictionary, consider returning a tuple containing the modified student list and the summary. This separates the input and output, making the function more predictable and less prone to side effects."
    ],
    "test_suite": "\nimport unittest\nimport numpy as np\n\ndef analyze_student_grades(students):\n    # Calculate average grades for each student\n    for student in students:\n        student['average'] = np.mean(student['grades'])\n    # Find the highest and lowest average grades\n    highest_avg = max(students, key=lambda x: x['average'])['average']\n    lowest_avg = min(students, key=lambda x: x['average'])['average']\n    # Normalize the grades\n    for student in students:\n        student['normalized_grades'] = [(grade - lowest_avg) / (highest_avg - lowest_avg) for grade in student['grades']]\n    # Prepare the summary\n    summary = {'students': students, 'highest_average': highest_avg, 'lowest_average': lowest_avg,}\n    return summary\n\nclass TestAnalyzeStudentGrades(unittest.TestCase):\n    def test_empty_students(self):\n        students = []\n        self.assertEqual(analyze_student_grades(students), {'students': [], 'highest_average': None, 'lowest_average': None})\n\n    def test_single_student(self):\n        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}]\n        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(1.0), np.float64(0.0), np.float64(1.0), np.float64(0.5)]}], 'highest_average': np.float64(85.25), 'lowest_average': np.float64(85.25)}\n        self.assertEqual(analyze_student_grades(students), expected_output)\n\n    def test_multiple_students(self):\n        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}, {'name': 'Bob', 'grades': [95, 98, 90, 92]}]\n        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(0.0), np.float64(-1.0), np.float64(1.0), np.float64(0.0)]}, {'name': 'Bob', 'grades': [95, 98, 90, 92], 'average': np.float64(93.75), 'normalized_grades': [np.float64(1.0), np.float64(1.0), np.float64(0.0), np.float64(0.5)]}], 'highest_average': np.float64(93.75), 'lowest_average': np.float64(85.25)}\n        self.assertEqual(analyze_student_grades(students), expected_output)\n\n    def test_different_grade_ranges(self):\n        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}, {'name': 'Bob', 'grades': [65, 68, 72, 75]}]\n        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(1.0), np.float64(0.0), np.float64(1.0), np.float64(0.5)]}, {'name': 'Bob', 'grades': [65, 68, 72, 75], 'average': np.float64(70.0), 'normalized_grades': [np.float64(0.0), np.float64(0.5), np.float64(1.0), np.float64(1.0)]}], 'highest_average': np.float64(85.25), 'lowest_average': np.float64(70.0)}\n        self.assertEqual(analyze_student_grades(students), expected_output)\n\n    def test_identical_grades(self):\n        students = [{'name': 'Alice', 'grades': [85, 85, 85, 85]}, {'name': 'Bob', 'grades': [85, 85, 85, 85]}]\n        expected_output = {'students': [{'name': 'Alice', 'grades': [85, 85, 85, 85], 'average': np.float64(85.0), 'normalized_grades': [np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0)]}, {'name': 'Bob', 'grades': [85, 85, 85, 85], 'average': np.float64(85.0), 'normalized_grades': [np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0)]}], 'highest_average': np.float64(85.0), 'lowest_average': np.float64(85.0)}\n        self.assertEqual(analyze_student_grades(students), expected_output)\n\nif __name__ == '__main__':\n    unittest.main()\n",
    "unit_tests": {
        "failed_tests": [
            "def test_different_grade_ranges(self):\n        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}, {'name': 'Bob', 'grades': [65, 68, 72, 75]}]\n        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(1.0), np.float64(0.0), np.float64(1.0), np.float64(0.5)]}, {'name': 'Bob', 'grades': [65, 68, 72, 75], 'average': np.float64(70.0), 'normalized_grades': [np.float64(0.0), np.float64(0.5), np.float64(1.0), np.float64(1.0)]}], 'highest_average': np.float64(85.25), 'lowest_average': np.float64(70.0)}\n        self.assertEqual(analyze_student_grades(students), expected_output)\n",
            "def test_identical_grades(self):\n        students = [{'name': 'Alice', 'grades': [85, 85, 85, 85]}, {'name': 'Bob', 'grades': [85, 85, 85, 85]}]\n        expected_output = {'students': [{'name': 'Alice', 'grades': [85, 85, 85, 85], 'average': np.float64(85.0), 'normalized_grades': [np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0)]}, {'name': 'Bob', 'grades': [85, 85, 85, 85], 'average': np.float64(85.0), 'normalized_grades': [np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0)]}], 'highest_average': np.float64(85.0), 'lowest_average': np.float64(85.0)}\n        self.assertEqual(analyze_student_grades(students), expected_output)\n",
            "def test_multiple_students(self):\n        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}, {'name': 'Bob', 'grades': [95, 98, 90, 92]}]\n        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(0.0), np.float64(-1.0), np.float64(1.0), np.float64(0.0)]}, {'name': 'Bob', 'grades': [95, 98, 90, 92], 'average': np.float64(93.75), 'normalized_grades': [np.float64(1.0), np.float64(1.0), np.float64(0.0), np.float64(0.5)]}], 'highest_average': np.float64(93.75), 'lowest_average': np.float64(85.25)}\n        self.assertEqual(analyze_student_grades(students), expected_output)\n",
            "def test_single_student(self):\n        students = [{'name': 'Alice', 'grades': [88, 76, 92, 85]}]\n        expected_output = {'students': [{'name': 'Alice', 'grades': [88, 76, 92, 85], 'average': np.float64(85.25), 'normalized_grades': [np.float64(1.0), np.float64(0.0), np.float64(1.0), np.float64(0.5)]}], 'highest_average': np.float64(85.25), 'lowest_average': np.float64(85.25)}\n        self.assertEqual(analyze_student_grades(students), expected_output)\n"
        ],
        "passed_tests": []
    },
    "validation_result": "The output appears to be as expected. The results demonstrate correct calculations for: Averages: Each student's average grade is calculated correctly. Normalization: The normalized grades are calculated using the highest and lowest averages as expected, resulting in values between 0 and 1. Summary: The highest and lowest averages are correctly identified and included in the summary.Overall, the code seems to be functioning as intended."
}
```