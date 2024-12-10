
class Options:
    STATUS_MAPPING = {
        "Draft": 1,
        "Ready for Review": 2,
        "Review in Progress": 3,
        "Rework": 4,
        "Obsolete": 5,
        "Future" : 6,
        "Final" : 7,
    }

    IMPORTANCE_MAPPING = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    EXECUTION_TYPE_MAPPING = {
        "Automated": 2,
        "Manual": 1,
    }


    req_Op_Type = {
        "Section": 1,
        "User Requirement Specification": 2,
        "System Requirement Specification": 3,

    }


    req_status_mapping = {
        "Draft": "D",
        "Review": "R",
        "Rework": "W",
        "Implemented": "I",
        "Obsolete": "O",
        "Valid": "V",
        "Finish": "F",
        "Not Testable": "N",
    }

    req_type_mapping = {
        "Informational": 1,
        "Feature":  2,
        "Use Case": 3,
        "Use Interface": 4,
        "Non functional": 5,
        "Constraint": 6,
        "System Function": 7,

    }

