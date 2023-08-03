
<div align="center">

<h1>Walrus</h1>

</div>

Walrus is a FastAPI backend application that utilizes SQLAlchemy ORM to interact with a database. It provides endpoints to manage users, businesses, and reviews, allowing users to create, retrieve, update, and delete records.

![cartoon-walrus-isolated-on-white-background-free-vector](https://github.com/lofyhub/walrus/assets/60175531/0280a472-e605-4144-bb81-506af3b5025b)




## Installation

1. Clone the repository:

```shell
git clone https://github.com/lofyhub/walrus.git
cd walrus
```

Install the dependencies:

```shell
pip install -r requirements.txt
```

## Set up the database:
Configure your database connection in the database/database.py file.
Run the migrations to create the necessary tables:
```shell
python src/create_db.py
```
To run the project, execute the following command:

```shell
python src/main.py
```
This will start the FastAPI server, and you can access the API endpoints through http://localhost:8000.


## API Models

The API utilizes the following SQLAlchemy models for data storage and retrieval:

### User

- **Attributes:**
  - `id` (Integer, primary key): The unique identifier of the user.
  - `name` (String, max length 255, required): The name of the user.
  - `email` (String, max length 255, required): The email address of the user.
  - `tel_number` (String, max length 10, required): The telephone number of the user.
  - `picture` (String, max length 255, required): The URL to the user's picture.
  - `created_at` (DateTime, required): The date and time of user creation.

### Business

- **Attributes:**
  - `id` (Integer, primary key): The unique identifier of the business.
  - `name` (String, max length 255, required): The name of the business.
  - `handle` (String, max length 255, required): The handle of the business.
  - `images` (List of Strings, required): URLs to the images associated with the business.
  - `location` (String, max length 255, required): The location of the business.
  - `opening_hours` (List of Strings, required): The opening hours of the business.
  - `business_description` (String, max length 255, required): The description of the business.
  - `created_at` (DateTime, required): The date and time of business creation.
  - `verified` (Boolean, required): The verification status of the business.
  - `telephone_number` (String, max length 255, required): The telephone number of the business.
  - `category` (String, max length 255, required): The category of the business.
  - `amenities` (List of Strings, required): The amenities provided by the business.
  - `user_id` (Integer, foreign key referencing the User model, required): The ID of the associated user.

### Review

- **Attributes:**
  - `id` (Integer, primary key): The unique identifier of the review.
  - `user_id` (Integer, foreign key referencing the User model, required): The ID of the user who posted the review.
  - `rating` (Integer, required): The rating of the review.
  - `created_at` (DateTime, required): The date and time when the review was created.
  - `text` (Text, required): The text content of the review.
  - `images` (List of Strings, required): URLs to the images associated with the review.
  - `business_id` (Integer, foreign key referencing the Business model, required): The ID of the associated business.

The API uses these models to manage and retrieve user, business, and review data. Each model represents a table in the database, and the relationships between models enable efficient querying and data retrieval.




## API ENDPOINTS


API Documentation - Users Endpoint
============================

This API documentation provides details about the Users endpoint, which allows you to manage user information.

Endpoint: `/users/`

Methods supported: `POST`, `GET`, `PUT`, `DELETE`

Authentication:
- This endpoint requires authentication using OAuth2 with a password bearer token. Include the token in the `Authorization` header using the Bearer scheme.

Save User
----------
Create a new user.

- Method: `POST`
- Path: `/users/`
- Request Body: `UserPayload`
- Response: `SaveResponse`
- Success Response Code: 201 - Created
- Error Response Codes:
  - 403 - Forbidden: If the email or telephone number is already registered.
  - 500 - Internal Server Error: If there is a database error.

Retrieve Users
--------------
Get a list of users.

- Method: `GET`
- Path: `/users/`
- Query Parameters:
  - `skip` (optional): Number of records to skip (default: 0)
  - `limit` (optional): Maximum number of records to retrieve (default: 100)
- Response: List of `UserResponse`
- Success Response Code: 200 - OK
- Error Response Code: 500 - Internal Server Error (in case of a database error)

Update User
-----------
Update an existing user.

- Method: `PUT`
- Path: `/users/{user_id}/`
- Path Parameter:
  - `user_id`: ID of the user to update
- Request Body: `UserPayload`
- Response: `SaveResponse`
- Success Response Code: 200 - OK
- Error Response Codes:
  - 400 - Bad Request: If the user with the specified ID is not found.
  - 403 - Forbidden: If the email cannot be different from the existing one.
  - 500 - Internal Server Error: If there is a database error.

Delete User
-----------
Delete a user.

- Method: `DELETE`
- Path: `/users/{user_id}/`
- Path Parameter:
  - `user_id`: ID of the user to delete
- Response: `SaveResponse`
- Success Response Code: 200 - OK
- Error Response Codes:
  - 404 - Not Found: If the user with the specified ID is not found.
  - 500 - Internal Server Error: If there is a database error.

Please ensure to include the required authentication token in the `Authorization` header for authenticated requests.



## Save Business [POST]

- **Endpoint:** `/businesses/`
- **Description:** Save a new business.
- **Request Body:**
  - `images` (List[UploadFile]): List of uploaded images.
  - `name` (str): Name of the business.
  - `handle` (str): Handle of the business.
  - `location` (str): Location of the business.
  - `opening` (str): Opening hours of the business.
  - `closing` (str): Closing hours of the business.
  - `business_description` (str): Description of the business.
  - `telephone_number` (str): Telephone number of the business.
  - `category` (str): Category of the business.
  - `user_id` (int): User ID associated with the business.
  - `amenities` (List[str]): List of amenities of the business.
- **Response:**
  - `status` (str): Status of the operation.
  - `message` (str): Success message.
- **Status Codes:**
  - `201`: Business saved successfully.
  - `500`: Internal server error.

## Get Businesses [GET]

- **Endpoint:** `/businesses/`
- **Description:** Get a list of businesses.
- **Query Parameters:**
  - `skip` (int, optional): Number of records to skip (default: 0).
  - `limit` (int, optional): Maximum number of records to retrieve (default: 100).
- **Response:**
  - List of business objects:
    - `name` (str): Name of the business.
    - `handle` (str): Handle of the business.
    - `images` (List[str]): List of image paths.
    - `location` (str): Location of the business.
    - `opening_hours` (List[str]): Opening hours of the business.
    - `business_description` (str): Description of the business.
    - `telephone_number` (str): Telephone number of the business.
    - `category` (str): Category of the business.
    - `user_id` (int): User ID associated with the business.
    - `amenities` (List[str]): List of amenities of the business.
    - `verified` (bool): Verification status of the business.
    - `created_at` (str): Creation timestamp of the business.
- **Status Codes:**
  - `200`: Success.
  - `500`: Internal server error.

## Update Business [PUT]

- **Endpoint:** `/businesses/{business_id}/`
- **Description:** Update an existing business.
- **Path Parameters:**
  - `business_id` (int): ID of the business to update.
- **Request Body:**
  - `business_to_update` (ResponseBusiness): Updated business object.
- **Response:**
  - `status` (str): Status of the operation.
  - `message` (str): Success message.
- **Status Codes:**
  - `200`: Business updated successfully.
  - `400`: Business not found.
  - `500`: Internal server error.

## Delete Business [DELETE]

- **Endpoint:** `/businesses/{business_id}/`
- **Description:** Delete a business.
- **Path Parameters:**
  - `business_id` (int): ID of the business to delete.
- **Response:**
  - `status` (str): Status of the operation.
  - `message` (str): Success message.
- **Status Codes:**
  - `200`: Business deleted successfully.
  - `404`: Business not found.
  - `500`: Internal server error.


## Reviews

## Save Review [POST]

- **Endpoint:** `/reviews/`
- **Description:** Save a new review.
- **Request Body:**
  - `images` (List[UploadFile]): List of uploaded images.
  - `text` (str): Review text.
  - `rating` (int): Review rating.
  - `business_id` (str): ID of the associated business.
  - `user_id` (int): ID of the user posting the review.
- **Response:**
  - `status` (str): Status of the operation.
  - `message` (str): Success message.
- **Status Codes:**
  - `201`: Review saved successfully.
  - `500`: Internal server error.

## Get Reviews [GET]

- **Endpoint:** `/reviews/`
- **Description:** Get a list of reviews.
- **Query Parameters:**
  - `skip` (int, optional): Number of records to skip (default: 0).
  - `limit` (int, optional): Maximum number of records to retrieve (default: 100).
- **Response:**
  - List of review objects:
    - `images` (List[str]): List of image paths.
    - `text` (str): Review text.
    - `rating` (int): Review rating.
    - `business_id` (str): ID of the associated business.
    - `user_id` (int): ID of the user who posted the review.
    - `created_at` (str): Creation timestamp of the review.
- **Status Codes:**
  - `200`: Success.
  - `500`: Internal server error.

## Update Review [PUT]

- **Endpoint:** `/reviews/{review_id}/`
- **Description:** Update an existing review.
- **Path Parameters:**
  - `review_id` (int): ID of the review to update.
- **Request Body:**
  - `review_to_update` (ReviewResponse): Updated review object.
- **Response:**
  - `status` (str): Status of the operation.
  - `message` (str): Success message.
- **Status Codes:**
  - `200`: Review updated successfully.
  - `400`: Review not found.
  - `500`: Internal server error.

## Delete Review [DELETE]

- **Endpoint:** `/reviews/{review_id}/`
- **Description:** Delete a review.
- **Path Parameters:**
  - `review_id` (int): ID of the review to delete.
- **Response:**
  - `status` (str): Status of the operation.
  - `message` (str): Success message.
- **Status Codes:**
  - `200`: Review deleted successfully.
  - `404`: Review not found.
  - `500`: Internal server error.


## Contribution

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your contribution.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request, explaining your changes and why they should be merged.

Please ensure that your contributions adhere to the [Code of Conduct](CONTRIBUTING.md) and the coding standards of this project.

## License

This project is licensed under the [GNU AFFERO GENERAL PUBLIC LICENSE 3](./LICENSE)

Please see the [LICENSE](LICENSE) file for more details.
