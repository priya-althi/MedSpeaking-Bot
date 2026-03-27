def age_warning(age, disease):

    disease = disease.lower()

    if age <= 12:
        return "Child patient: Please consult pediatric doctor if symptoms continue."

    if age >= 60:
        if any(x in disease for x in ["flu", "infection", "pneumonia", "covid"]):
            return "Senior patient: Risk may be higher. Doctor consultation recommended."
        return "Senior patient: Monitor symptoms carefully and seek medical help if condition worsens."

    return ""
