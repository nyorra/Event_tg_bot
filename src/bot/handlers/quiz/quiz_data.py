quiz_data = {
    1: [
        {
            "question": "",
            "options": [""],
            "answer": 1,
        },
        {
            "question": "",
            "options": [""],
            "answer": 3,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 2,
        },
        {
            "question": "",
            "options": [""],
            "answer": 1,
        },
    ],
    2: [
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 2,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
    ],
    3: [
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": "",
            "options": [""],
            "answer": 0,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [""],
            "answer": 0,
        },
    ],
    4: [
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 2,
        },
    ],
    5: [
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": "",
            "options": [""],
            "answer": 3,
        },
        {
            "question": "",
            "options": [""],
            "answer": 1,
        },
        {
            "question": "",
            "options": [""],
            "answer": 0,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
    ],
    6: [
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": [""],
            "options": [
                "",
            ],
            "answer": 3,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [""],
            "answer": 2,
        },
    ],
    7: [
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 1,
        },
        {
            "question": "",
            "options": [""],
            "answer": 1,
        },
    ],
    8: [
        {
            "question": "",
            "options": [""],
            "answer": 1,
        },
        {
            "question": [""],
            "options": [""],
            "answer": 2,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 0,
        },
        {
            "question": "",
            "options": [""],
            "answer": 3,
        },
        {
            "question": "",
            "options": [
                "",
            ],
            "answer": 2,
        },
    ],
}


def get_weekly_quiz(week_number: int):
    return quiz_data.get(week_number, [])
