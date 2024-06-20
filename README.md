# hku-msc-captstone

##### For using the Google Gemini API through Jupyter Notebook

First need VPN as most LLM service not supported in HK local IP address
Proton VPN (Free) or any other VPN will do the work
[Proton VPN: Secure, fast VPN service in 90+ countries](https://protonvpn.com/)

After connected to the VPN, then able to execute blocks of the Jupyter notebook

##### Local Testing
Run: `flask --app main --debug run`

##### Deploy to cloud host
Run: `gcloud run deploy test-generation --image asia-east1-docker.pkg.dev/msc-capstone-2024/cloud-run-source-deploy/test-generation`
Pick Region 2: asia-east1

##### Sample JSON input to the API
`{
    "apiKey": "AIzaSyAjfxkxDpd4fo0wVm_pbS1uVJhGOVVNafI",
    "code": "def twoSum(num1, num2): sum_result = num1 + num2 return sum_result",
    "data": {
        "inputType": "numbers",
        "boundary": "positive numbers less than infinity"
    },
    "result": {
        "expectedOutput": "single positive number"
    }
}`

##### Sample JSON output from the API
`{
	"metrics": [],
	"sample_data": [
		{
			"num1": 1,
			"num2": 2
		},
		{
			"num1": 3,
			"num2": 4
		},
		{
			"num1": 5,
			"num2": 6
		},
		{
			"num1": 7,
			"num2": 8
		},
		{
			"num1": 9,
			"num2": 10
		},
		{
			"num1": 11,
			"num2": 12
		},
		{
			"num1": 13,
			"num2": 14
		},
		{
			"num1": 15,
			"num2": 16
		},
		{
			"num1": 17,
			"num2": 18
		},
		{
			"num1": 19,
			"num2": 20
		},
		{
			"num1": 21,
			"num2": 22
		},
		{
			"num1": 23,
			"num2": 24
		},
		{
			"num1": 25,
			"num2": 26
		},
		{
			"num1": 27,
			"num2": 28
		},
		{
			"num1": 29,
			"num2": 30
		},
		{
			"num1": 31,
			"num2": 32
		},
		{
			"num1": 33,
			"num2": 34
		},
		{
			"num1": 35,
			"num2": 36
		},
		{
			"num1": 37,
			"num2": 38
		},
		{
			"num1": 39,
			"num2": 40
		}
	],
	"suggestions": [
		"The code defines a function `twoSum` which calculates the sum of two input numbers. The unit tests cover four scenarios: positive numbers, zero, negative numbers, and large numbers. The code coverage is 100% as all possible execution paths are covered by the tests. \n"
	],
	"unit_tests": "  import unittest  class TestTwoSum(unittest.TestCase):     def test_two_sum_positive(self):         self.assertEqual(twoSum(1, 2), 3)     def test_two_sum_zero(self):         self.assertEqual(twoSum(0, 5), 5)     def test_two_sum_negative(self):         self.assertEqual(twoSum(-1, 2), 1)     def test_two_sum_large_numbers(self):         self.assertEqual(twoSum(1000, 2000), 3000)  if __name__ == '__main__':     unittest.main()  ",
	"validation_result": "Yes, the results are as expected. For each test case, the code correctly calculates the sum of the two input numbers, resulting in a single positive number. \n"
}`