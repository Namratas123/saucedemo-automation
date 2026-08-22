# SauceDemo Automation Tests

## Overview

This project contains Selenium WebDriver automation tests for the SauceDemo
e-commerce application.

The tests cover:

- Valid user login
- Add product and complete checkout
- Locked-out user login validation

## Tech Stack

- Python
- Selenium WebDriver
- PyTest

## Test Credentials

Username: standard_user
Password: secret_sauce

Locked user: locked_out_user
Password: secret_sauce

## Setup

Clone the repository and install the required packages:

pip install -r requirements.txt

## Run Tests

Run all tests:

pytest

Run a specific test:

pytest tests/test_login.py

## Test Coverage

### Valid Login
Verifies that standard_user can successfully login.

### Checkout
Verifies adding a product to the cart and completing checkout.

### Locked User
Verifies that locked_out_user cannot login and that the expected
error message is displayed.