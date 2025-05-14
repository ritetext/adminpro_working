# AdminPro API

AdminPro is a comprehensive examination platform with a powerful API.

## API Documentation

We provide multiple ways to explore and interact with our API:

### Swagger UI (Interactive Documentation)

Visit `/api/docs/` when the server is running to access the interactive Swagger UI documentation.

```
http://localhost:8000/api/docs/
```

This interactive documentation allows you to:
- Explore all available endpoints
- See request/response formats
- Test API calls directly from your browser
- Understand authentication requirements

### ReDoc (Alternative Documentation UI)

For a more user-friendly layout, visit `/api/redoc/`:

```
http://localhost:8000/api/redoc/
```

### Markdown Documentation

For detailed API usage examples and explanations, see:

- [API_DOCUMENTATION.md](API_DOCUMENTATION.md): Comprehensive guide to all endpoints

### Postman Collection

We also provide a Postman collection for easy API testing:

1. Import the [adminpro_api_postman_collection.json](adminpro_api_postman_collection.json) file into Postman
2. Set up your environment variables:
   - `base_url`: Your API base URL (e.g., `http://localhost:8000`)
   - `jwt_token`: Your authentication token after login

## Authentication

This API uses JWT (JSON Web Token) authentication:

1. Obtain a token by sending a POST request to `/api/auth/jwt/create/`
2. Include the token in the Authorization header of subsequent requests:
   `Authorization: JWT <your_token>`

## Running the API Server

```bash
# Start the development server
python manage.py runserver

# Start on a different port if needed
python manage.py runserver 8001
```

## API Features

- **User Management**: Registration, authentication, and profile management
- **Candidates**: Create and manage candidate profiles
- **Exams**: Create, list, and take exams
- **Questions**: Manage exam questions and answers
- **Results**: View exam results and scores
- **Email Notifications**: Send email notifications

For any API questions, please refer to the documentation or contact the development team. 