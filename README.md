# Mini-Inventory-Management-System

## 📌 Project Overview
This project is a **Mini Inventory Management System** built for a fictional small-scale retail business.  
It allows the business to **track products, suppliers, and sales transactions** efficiently in a simple, user-friendly web application.

This is developed as part of the **"Mini ERP Lite Module"** assessment and follows the requirements outlined in the assignment PDF.

---

## 🎯 Objectives
- Maintain a **product catalog** with quantity, pricing, and supplier details.
- Record **purchase and sale transactions** with automatic stock adjustments.
- Monitor **low stock items** for timely reordering.
- View **basic reports** on inventory value and stock status.

---

## ✨ Features
### 1. **Dashboard**
- Total number of products
- Current inventory value
- Low stock alerts (products at/below reorder level)

### 2. **Product Management**
- Add, edit, and delete products
- Assign SKU, price, quantity, and reorder level
- Link products to suppliers

### 3. **Supplier Management**
- Add and manage supplier details
- Associate suppliers with products

### 4. **Transactions**
- Record **purchase** transactions (increase stock)
- Record **sale** transactions (decrease stock)
- Prevent sales if stock is insufficient

### 5. **Reports (API Endpoints)**
- `/api/reports/low_stock` → Products at/below reorder level
- `/api/reports/inventory_value` → Total inventory value

---

## 🛠 Technology Stack
- **Backend:** Flask (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML + Jinja2 Templates + Tailwind CSS (CDN)
- **Language:** Python 3.8+
- **Additional:** JSON APIs for reports

---

## 📂 Project Structure
