
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

Contribution
