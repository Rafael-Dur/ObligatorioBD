# Project: EcomDB Data Generator

This project is designed to populate an `ecom` database with consistent and meaningful data. It's built to support university projects requiring a realistic dataset for testing and development. Instead of manually entering data or generating random, incoherent entries, this tool helps create interconnected data across various tables, ensuring referential integrity and logical relationships.

---

## Configuration

To connect to your database, you'll need to set up a `.env` file in the root directory of this project. 
This file will store your database credentials securely.

Here's an example of what your `.env` file should look like:

Navigate to the root of your project (where your `README.md` is located) and run the following command:
```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

We create a requirements.txt file.
This file will list all the libraries your project uses, along with their specific versions.
This is vital so other developers (or you yourself in the future) can replicate your exact environment.

To run it:
```bash
pip install -r requirements.txt
```