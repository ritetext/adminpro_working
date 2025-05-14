from drf_yasg import openapi

# Schema for email sending endpoint
email_send_schema = {
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['to', 'subject', 'body'],
        properties={
            'to': openapi.Schema(
                type=openapi.TYPE_STRING, 
                description='Email recipient address'
            ),
            'subject': openapi.Schema(
                type=openapi.TYPE_STRING, 
                description='Email subject'
            ),
            'body': openapi.Schema(
                type=openapi.TYPE_STRING, 
                description='Email body content'
            ),
        }
    ),
    'responses': {
        200: openapi.Response(
            description='Email queued successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Success message'
                    )
                }
            )
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Error message'
                    )
                }
            )
        ),
        500: openapi.Response(
            description='Server error',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Error message'
                    )
                }
            )
        )
    }
}

# Candidate schemas
candidate_list_schema = {
    'operation_summary': 'List Candidates',
    'operation_description': 'List all candidates based on permissions',
    'responses': {
        200: openapi.Response(
            description='Successful retrieval of candidates',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'user': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'phone': openapi.Schema(type=openapi.TYPE_STRING),
                        'address': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            )
        )
    }
}

candidate_create_schema = {
    'operation_summary': 'Create Candidate',
    'operation_description': 'Create a new candidate',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['first_name', 'last_name', 'email'],
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
            'address': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    'responses': {
        201: openapi.Response(
            description='Candidate created successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'phone': openapi.Schema(type=openapi.TYPE_STRING),
                    'address': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        400: openapi.Response(
            description='Invalid input',
            schema=openapi.Schema(type=openapi.TYPE_OBJECT)
        ),
    }
}

candidate_retrieve_schema = {
    'operation_summary': 'Retrieve Candidate',
    'operation_description': 'Get a candidate by ID',
    'responses': {
        200: openapi.Response(
            description='Successful retrieval of candidate',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'phone': openapi.Schema(type=openapi.TYPE_STRING),
                    'address': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        404: openapi.Response(
            description='Candidate not found',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
    }
}

# Exam schemas
exam_list_schema = {
    'operation_summary': 'List Exams',
    'operation_description': 'List all available exams',
    'responses': {
        200: openapi.Response(
            description='Successful retrieval of exams',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'duration_minutes': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'pass_mark': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            )
        )
    }
}

exam_retrieve_schema = {
    'operation_summary': 'Retrieve Exam',
    'operation_description': 'Get an exam by ID with its questions',
    'responses': {
        200: openapi.Response(
            description='Successful retrieval of exam',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'duration_minutes': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'pass_mark': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'questions': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'text': openapi.Schema(type=openapi.TYPE_STRING),
                                'answers': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'text': openapi.Schema(type=openapi.TYPE_STRING),
                                        }
                                    )
                                ),
                            }
                        )
                    ),
                }
            )
        ),
        404: openapi.Response(
            description='Exam not found',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
    }
}

exam_submit_schema = {
    'operation_summary': 'Submit Exam',
    'operation_description': 'Submit answers for an exam',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['answers'],
        properties={
            'answers': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additionalProperties=openapi.Schema(type=openapi.TYPE_INTEGER),
                description='Question IDs mapped to answer IDs'
            ),
        }
    ),
    'responses': {
        200: openapi.Response(
            description='Exam submitted successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'candidate': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'exam': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'is_passed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'date_taken': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                }
            )
        ),
        400: openapi.Response(
            description='Invalid submission',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
    }
}

# Question schemas
question_list_schema = {
    'operation_summary': 'List Questions',
    'operation_description': 'List all questions for an exam',
    'responses': {
        200: openapi.Response(
            description='Successful retrieval of questions',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'exam': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'text': openapi.Schema(type=openapi.TYPE_STRING),
                        'answers': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'text': openapi.Schema(type=openapi.TYPE_STRING),
                                    'is_correct': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                }
                            )
                        ),
                    }
                )
            )
        )
    }
}

question_create_schema = {
    'operation_summary': 'Create Question',
    'operation_description': 'Create a new question for an exam',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['exam', 'text', 'answers'],
        properties={
            'exam': openapi.Schema(type=openapi.TYPE_INTEGER),
            'text': openapi.Schema(type=openapi.TYPE_STRING),
            'answers': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=['text', 'is_correct'],
                    properties={
                        'text': openapi.Schema(type=openapi.TYPE_STRING),
                        'is_correct': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            ),
        }
    ),
    'responses': {
        201: openapi.Response(
            description='Question created successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'exam': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'text': openapi.Schema(type=openapi.TYPE_STRING),
                    'answers': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'text': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_correct': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        )
                    ),
                }
            )
        ),
        400: openapi.Response(
            description='Invalid input',
            schema=openapi.Schema(type=openapi.TYPE_OBJECT)
        ),
    }
}

# Result schemas
result_list_schema = {
    'operation_summary': 'List Results',
    'operation_description': 'List exam results for the current user',
    'responses': {
        200: openapi.Response(
            description='Successful retrieval of results',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'candidate': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'exam': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'is_passed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'date_taken': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                    }
                )
            )
        )
    }
}

result_retrieve_schema = {
    'operation_summary': 'Retrieve Result',
    'operation_description': 'Get an exam result by ID',
    'responses': {
        200: openapi.Response(
            description='Successful retrieval of result',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'candidate': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'exam': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'exam_details': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                            'pass_mark': openapi.Schema(type=openapi.TYPE_NUMBER),
                        }
                    ),
                    'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'is_passed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'date_taken': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                }
            )
        ),
        404: openapi.Response(
            description='Result not found',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
    }
} 