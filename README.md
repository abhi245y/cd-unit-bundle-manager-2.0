# CD Unit Bundle Manager 2.0

A comprehensive bundle management application for the CD Unit, designed to streamline bundle tracking and management.

## Overview

CD Unit Bundle Manager 2.0 is a significant upgrade to the previous version, introducing new features and improvements to enhance bundle management. Formerly reliant on MongoDB, the application has been restructured to utilize a MySQL database, providing better data management and scalability.

## Key Features

* **Advanced Searching**: Utilize Gen AI-powered searching to quickly locate bundles based on various criteria, including college name, messenger, date of entry, received date, and more.
* **Multi-Filter Searching**: Apply multiple filters to narrow down search results, making it easier to find specific bundles.
* **Bundle Tracking**: Track bundle movement and status, ensuring timely updates and minimizing errors.
* **College and Messenger Management**: Manage college and messenger data, enabling efficient bundle assignment and tracking.

## UI Components

The application consists of two primary UI components:

* **Bundle Browser**: A comprehensive UI for searching, updating, and deleting bundles. It utilizes various filters and Gen AI-powered searching to quickly locate bundles.
* **Add Bundles**: A separate UI for adding new bundle records to the database. It streamlines the process of entering bundle details, ensuring accurate and efficient data entry.

## System Requirements

* Python 3.x
* PyQt6
* MySQL database
* Groq AI library

## Installation

### Easy Installation (Recommended)

I have provide a pre-packaged executable file for easy installation(packages using pyinstaller). Please visit the [Release Page] and download the latest version. Once downloaded, you can run the application by executing the executable file.

### Installation from Source

If you prefer to build the application from source, please follow these steps:

1. Install Python 3.x on your system.
2. Install requirements using requirements.txt
3. Create a MySQL database.
4. Create a `config.yaml` file in the root directory with the following configuration:
```yml
db_username: <your_db_username>
db_pass: <your_db_password>
db_link: <your_db_link>
db_name: <your_db_name>
GROQ_API_KEY: <your_GROQ_API_KEY>
```
Replace the placeholders with your actual database credentials and GROQ API key.
6. Run the application using the `BrowseBundlesUtil.py` or `addBundlesUI.py` script.

## Usage

1. Launch the application by running the `BrowseBundlesUtil.py` script or executing the executable file.
2. Enter the database connection settings in the GUI.
3. Perform search operations by entering the desired criteria in the search fields.
4. Update bundle information by selecting the corresponding row and editing the fields.
5. Delete bundles by selecting the corresponding row and clicking the "Delete" button.
6. Add new bundle records by running the `addBundlesUI.py` script and filling out the input fields.

## What's New in 2.0

* **Gen AI-powered searching**: Quickly locate bundles using advanced search capabilities.
* **Multi-filter searching**: Apply multiple filters to narrow down search results.
* **MySQL database**: Improved data management and scalability.
* **Enhanced UI**: Streamlined and intuitive UI components for efficient bundle management.

## License

This application is released under the MIT License. See the LICENSE file for details.
