
<div align="center">

<h1>Walrus</h1>

</div>

Walrus is a FastAPI backend application that utilizes SQLAlchemy ORM to interact with a database. It provides endpoints to manage users, businesses, and reviews, allowing users to create, retrieve, update, and delete records.

![cartoon-walrus-isolated-on-white-background-free-vector](https://github.com/lofyhub/walrus/assets/60175531/0280a472-e605-4144-bb81-506af3b5025b)


## Database Models

The application uses the following database models:

### User

- `id`: Integer, primary key of the user.
- `name`: String(255), name of the user.
- `picture`: String(255), URL to the user's picture.
- `created_at`: DateTime, date and time of user creation.

### Business

- `id`: Integer, primary key of the business.
- `name`: String(255), name of the business.
- `handle`: String(255), handle of the business.
- `reviews`: Integer, number of reviews for the business.
- `review_score`: Float, review score of the business.
- `location`: String(255), location of the business.
- `opening`: Boolean, status of the business (open or closed).
- `business_description`: Text, description of the business.
- `creation_date`: String(255), date of business creation.
- `verified`: Boolean, verification status of the business.
- `telephone_number`: String(255), telephone number of the business.
- `category`: String(255), category of the business.
- `user_id`: Integer, foreign key referencing the User model.
- `user`: Relationship with the User model.

### Review

- `id`: Integer, primary key of the review.
- `name`: String(255), name of the reviewer.
- `rating`: Integer, rating of the review.
- `created_at`: DateTime, date and time of the review.
- `text`: Text, review text.
- `image`: String(255), URL to the review image.
- `business_id`: Integer, foreign key referencing the Business model.
- `business`: Relationship with the Business model.

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

## API ENDPOINTS

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


Contribution
