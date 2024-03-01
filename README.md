# Flask Adoption Agency

## Overview

Flask Adoption Agency is a web application built with Flask, a lightweight Python web framework. It allows users to manage pet adoption by providing features for adding, editing, and listing pets available for adoption.

## Getting Started

### Prerequisites

- Python 3.x: Download and install Python 3.x from the [official Python website](https://www.python.org/downloads/).
- PostgreSQL: Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/).

### Database Setup

#### PostgreSQL Setup

1. **Install PostgreSQL**: Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/).
2. **Start PostgreSQL Service**: After installation, start the PostgreSQL service on your system.
3. **Access PostgreSQL Shell**: Open a terminal and access the PostgreSQL shell by running the command `psql`.

#### Creating the Database

Once you have PostgreSQL set up, follow these steps to create the adopt database:

```sql
CREATE DATABASE adopt;
```

### Installation
1.Clone the repository:

```bash
git clone https://github.com/RicardoAlbornozgil/WTForms-Adoption-Agency.git
```

2. Navigate to the project directory:

```bash
cd flask-adoption-agency
```

3.Set up a virtual environment (optional): Follow the instructions to set up a virtual environment in the previous section.

4.Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage
Run the Flask application:

```bash
flask run
```

Open your web browser and navigate to http://localhost:5000 to access the application.

### Features
- Add new pets for adoption
- Edit existing pet information
- View a list of available pets
- Custom error handling with a 404 page

###Fork the repository
1.Create a new branch (git checkout -b feature/fooBar)
Make your changes
2.Commit your changes (git commit -am 'Add some fooBar')
3.Push to the branch (git push origin feature/fooBar)
4.Create a new Pull Request
### Acknowledgements
- Flask: Official Website
- SQLAlchemy: Official Website
- WTForms: Official Website