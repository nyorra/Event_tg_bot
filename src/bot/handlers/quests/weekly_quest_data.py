quests = {
    1: {
        "brand": "nyorra",
        "task": (
            ""
        ),
        "instructions": (
            ""
        ),
        "brand_description": "",
        "brand_link": "",
        "photo": "",
    },
    2: {
        "brand": ":",
        "task": (
            ""
        ),
        "instructions": (
            ""
        ),
        "brand_description": "",
        "brand_link": "",
        "photo": "",
    },
    3: {
        "brand": "",
        "task": (
            ""
        ),
        "instructions": (
            ""
        ),
        "brand_description": "",
        "brand_link": "",
        "photo": "",
    },
    4: {
        "brand": "",
        "task": (
            ""
        ),
        "instructions": (
            ""
        ),
        "brand_description": "",
        "brand_link": "",
        "photo": "",
    },
    5: {
        "brand": "",
        "task": (
            ""
        ),
        "instructions": (
            ""
        ),
        "brand_description": "",
        "brand_link": "",
        "photo": "",
    },
    6: {
        "brand": "",
        "task": (
            ""
        ),
        "instructions": (
            ""
        ),
        "brand_description": "",
        "brand_link": "<b>Узнать больше о бренде и <a href='https://taplink.cc/amazingred'>откликнуться к нам</a></b>",
        "photo": "",
    },
    7: {
        "brand": "",
        "task": (
            ""
        ),
        "instructions": (
            ""
        ),
        "brand_description": "",
        "brand_link": "",
        "photo": "",
    },
    8: {
        "brand": "",
        "task": (
            ""
        ),
        "instructions": (
            ""
        ),
        "brand_description": "",
        "brand_link": "",
        "photo": "",
    },
}


def get_weekly_data(week_number: int) -> dict:
    return quests.get(
        week_number,
        {
            "brand": "",
            "task": "Странно, но задания куда-то пропали.. Уже чиним!",
            "instructions": "Загляни позже!",
        },
    )
