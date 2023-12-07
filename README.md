# Web API Data Sync for Inventory Adjustment Automation

## Purpose

The **Web API Data Synchronization** script is designed to streamline inventory adjustment processes through API connections to an Odoo database. Tailored for projects requiring real-time updates and adjustments to product data, this script ensures a smooth and efficient integration of new inventory data. It facilitates the creation of production orders and lot records, providing a reliable solution for keeping inventory information up-to-date.

## How It Works

### Configuration

1. Start by configuring the script with crucial parameters such as the Odoo URL, database name, user credentials, and server details.

### API Interaction

2. The script establishes a connection to the Odoo database using XML-RPC, authenticating the user with provided credentials.

### Data Processing

3. Upon successful authentication, the script processes incoming JSON data from a RESTful endpoint, extracting essential information for inventory adjustments.

### Inventory Adjustment

4. The script generates a new production order and lot record for each inventory adjustment, ensuring accurate tracking of product quantities and associated lots.

### Status Reporting

5. The script provides real-time status updates, indicating whether the data was successfully uploaded or if an error occurred during the process.

## Usage

1. **Inventory Adjustment Automation:**
   - Customize the script by updating the Odoo connection details, defining product and lot creation logic, and configuring the REST endpoint for data reception.

2. **Execution:**
   - Run the script using a Python interpreter. It automates the inventory adjustment process, creating production orders and lot records based on incoming data.

## Example Scenario

Consider a scenario where an external system needs to synchronize inventory adjustments with an Odoo database. The script seamlessly integrates incoming data, creating production orders and lot records for accurate inventory management. This tool is invaluable for businesses relying on real-time inventory tracking and adjustments.

**Author:** César Rodríguez
