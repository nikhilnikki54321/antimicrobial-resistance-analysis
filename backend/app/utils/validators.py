def validate_predict_input(data):
    errors = []

    if "age" not in data or not isinstance(data["age"], (int, float)):
        errors.append("age is required and must be a number")
    elif data["age"] <= 0 or data["age"] > 120:
        errors.append("age must be between 1 and 120")

    if "gender" not in data or data["gender"] not in (0, 1):
        errors.append("gender is required (0=Female, 1=Male)")

    for field in ["diabetes", "hypertension", "hospital_before"]:
        if field in data and data[field] not in (0, 1):
            errors.append(f"{field} must be 0 or 1")

    if "infection_freq" in data:
        if not isinstance(data["infection_freq"], (int, float)):
            errors.append("infection_freq must be a number")
        elif data["infection_freq"] < 0:
            errors.append("infection_freq must be >= 0")

    return errors
