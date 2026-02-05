week_info = {
    1: {
        "brand": "nyorra",
        "brand_description": "text",
        "brand_link": "https://github.com/nyorra",
        "photo": "media/nyorra.png",
    },
    2: {
        "brand": "nyorra1",
        "brand_description": "text1",
        "brand_link": "https://github.com/nyorra",
        "photo": "media/nyorra1.png",
    },
    3: {
        "brand": "nyorra2",
        "brand_description": "text2",
        "brand_link": "https://github.com/nyorra",
        "photo": "media/nyorra2.png",
    },
    4: {
        "brand": "nyorra3",
        "brand_description": "text3",
        "brand_link": "https://github.com/nyorra",
        "photo": "media/nyorra3.png",
    },
    5: {
        "brand": "nyorra4",
        "brand_description": "text4",
        "brand_link": "https://github.com/nyorra",
        "photo": "media/nyorra4.png",
    },
    6: {
        "brand": "nyorra5",
        "brand_description": "text5",
        "brand_link": "https://github.com/nyorra",
        "photo": "media/nyorra.png5",
    },
    7: {
        "brand": "nyorra6",
        "brand_description": "text6",
        "brand_link": "https://github.com/nyorra",
        "photo": "media/nyorra6.png",
    },
    8: {
        "brand": "nyorra7",
        "brand_description7": "text",
        "brand_link": "https://github.com/nyorra",
        "photo": "media/nyorra7.png",
    },
}


def get_week_info(week_number: int) -> dict:
    return week_info.get(
        week_number,
        {
            "brand": "No nyorra",
            "brand_description": "Странно, но задания куда-то пропали.. Уже чиним!",
            "brand_link": "Загляни позже!",
            "photo": "Загляни позже!",
        },
    )
