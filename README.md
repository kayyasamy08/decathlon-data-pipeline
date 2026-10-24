# Decathlon Product Data Scraping

## Project Overview

This project uses Python and Scrapy to collect product information from the Decathlon category API. It retrieves product data from multiple categories, extracts structured fields from JSON responses, and exports the results to a CSV file for further analysis.

## Technologies Used

* Python
* Scrapy
* REST API
* JSON
* CSV

## Key Features

* Collect product data from five configured Decathlon categories.
* Retrieve product information through API requests.
* Handle pagination to collect products across multiple pages.
* Extract and normalize product attributes.
* Generate product page URLs using available product identifiers and slugs.
* Export the collected records to CSV format.

## Data Fields

The exported dataset includes:

* `objectID`
* `modelId`
* `brand`
* `productName`
* `slug`
* `web_page`
* `image`
* `rating`
* `reviews`
* `sellingPrice`
* `mrp`
* `discount`
* `isExpressEligible`
* `category_id`

## Project Workflow

1. Configure the product category IDs.
2. Send JSON requests to the Decathlon category API using Scrapy.
3. Retrieve product data and pagination information.
4. Extract product details from the API response.
5. Normalize the product fields into structured records.
6. Export the collected data to a CSV file.

## Project Structure

```text
decathlon-data-pipeline/
├── decathlon_products.py
├── requirements.txt
├── decathlon_sample.csv
└── README.md
```

*The sample CSV is optional and should be included only if uploaded.*

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/kayyasamy08/decathlon-data-pipeline.git
cd decathlon-data-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the scraper

```bash
python decathlon_products.py
```

The script is configured to export product records to `decathlon_1000_products.csv`.

The number of records collected depends on the API response and the products available in the configured categories.

## Learning Outcomes

* Working with APIs using Python.
* Using Scrapy to collect structured data.
* Handling JSON responses and pagination.
* Extracting and normalizing product attributes.
* Exporting structured data to CSV files.

## Author

Ayyasamy

GitHub: https://github.com/kayyasamy08
