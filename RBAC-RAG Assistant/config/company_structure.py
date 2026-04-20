# Central definition of company structure and access rules

ROLES = [
    "admin",
    "manager",
    "employee",
    "intern"
]

DEPARTMENTS = [
    "design",
    "engineering",
    "ai_data",
    "hr",
    "sales",
    "management"
]

PUBLIC_DEPARTMENTS = [
    "hr"
]

ROLE_ACCESS_RULES = {
    "admin": [
        "design",
        "engineering",
        "ai_data",
        "hr",
        "sales",
        "management"
    ],

    "manager": [
        "design",
        "engineering",
        "ai_data",
        "sales"
    ],

    "employee": [
        "design",
        "engineering",
        "ai_data"
    ],

    "intern": [
        "design",
        "engineering"
    ]
}


def get_accessible_departments(role: str):
    role = role.lower()
    allowed = ROLE_ACCESS_RULES.get(role, [])
    return list(set(allowed + PUBLIC_DEPARTMENTS))