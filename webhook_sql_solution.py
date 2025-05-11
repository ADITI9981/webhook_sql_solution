import requests
import json
import datetime

# API URLs
API_URL = 'https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON'
SUBMISSION_URL = 'https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON'

# User Data
USER_DATA = {
    "name": "John Doe",
    "regNo": "REG12347",
    "email": "john@example.com"
}

def generate_webhook():
    """
    Generates a webhook and retrieves the access token.
    """
    try:
        response = requests.post(API_URL, json=USER_DATA)
        response.raise_for_status()
        data = response.json()
        webhook_url = data.get('webhook')
        access_token = data.get('accessToken')
        print("Webhook URL:", webhook_url)
        print("Access Token:", access_token)
        return webhook_url, access_token
    except requests.RequestException as e:
        print("Error generating webhook:", e)
        return None, None

def solve_sql_problem(reg_no):
    """
    Constructs the SQL query based on the regNo's last digit.
    """
    # Determine the problem based on the last digit
    last_digit = int(reg_no[-1])
    if last_digit % 2 == 0:
        print("Assigned Question 2")
        problem_url = "https://drive.google.com/file/d/1PO1ZvmDqAZJv77XRYsVben11Wp2HVb/view?usp=sharing"
    else:
        print("Assigned Question 1")
        problem_url = "https://drive.google.com/file/d/1q8F8g0EpyNzd5BWk-voe5CKbsxoskJWY/view?usp=sharing"

    print("Problem URL:", problem_url)

    # Construct SQL Query
    sql_query = '''
        SELECT 
            p.AMOUNT AS SALARY,
            CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
            (YEAR(CURDATE()) - YEAR(e.DOB)) AS AGE,
            d.DEPARTMENT_NAME
        FROM PAYMENTS p
        JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
        JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
        WHERE DAY(p.PAYMENT_TIME) != 1
        ORDER BY p.AMOUNT DESC
        LIMIT 1;
    '''

    return sql_query

def submit_solution(webhook_url, access_token, sql_query):
    """
    Submits the SQL solution to the webhook URL using the access token.
    """
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    data = {"finalQuery": sql_query}

    try:
        response = requests.post(webhook_url, headers=headers, json=data)
        response.raise_for_status()
        print("Solution submitted successfully.")
    except requests.RequestException as e:
        print("Error submitting solution:", e)

def main():
    """
    Main function to execute the workflow.
    """
    webhook_url, access_token = generate_webhook()
    if webhook_url and access_token:
        sql_query = solve_sql_problem(USER_DATA['regNo'])
        submit_solution(webhook_url, access_token, sql_query)

if __name__ == "__main__":
    main()
