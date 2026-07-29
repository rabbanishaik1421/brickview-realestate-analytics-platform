# 🏠 BrickView Real Estate Analytics Dashboard

## 📌 Project Overview

BrickView is a Real Estate Analytics Dashboard developed using **Python**, **Streamlit**, **SQLite**, **Pandas**, and **Matplotlib**. The application provides comprehensive insights into property listings, sales, buyers, and agents through interactive dashboards, visualizations, SQL analytics, and complete CRUD operations.

The project enables users to explore real estate data, perform advanced filtering, visualize trends, and manage records efficiently.

---

# 🎯 Project Objectives

- Analyze real estate listings and sales data.
- Provide interactive dashboards with business insights.
- Perform advanced SQL-based analytics.
- Implement complete CRUD operations.
- Build interactive visualizations.
- Demonstrate modular programming and code reusability.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend Programming |
| Streamlit | Dashboard Development |
| SQLite | Database |
| Pandas | Data Analysis |
| Matplotlib | Data Visualization |
| SQL | Data Retrieval & Analysis |
| HTML/CSS | Custom UI Design |

---

# 📂 Project Structure

```
BrickView/
│
├── main.py
├── database.py
├── utils.py
├── dashboard.py
├── filters.py
├── visualizations.py
├── crud.py
├── sql_queries.py
├── common.py
├── style.css
├── brickviewdb.db
├── README.md
└── assets/
```

---

# 🗄️ Database Tables

The project contains the following tables:

- Listings
- Sales
- Buyers
- Agents
- Property Attributes

---

# ✨ Features

## 1. Dashboard

Displays Key Performance Indicators (KPIs):

- Total Listings
- Total Sales
- Total Buyers
- Total Agents
- Total Revenue

---

## 2. Filters & Explorer

Interactive filters include:

- City
- Property Type
- Price Range
- Agent
- Listed Date
- Sale Date

Displays filtered property listings dynamically.

---

## 3. Analytics & Visualizations

The dashboard includes:

- Property Listings Map
- Average Price by City (Bar Chart)
- Property Type Distribution (Pie Chart)
- Monthly Sales Trend (Line Chart)
- Interactive Data Tables

---

## 4. CRUD Operations

Implemented CRUD functionality for all database tables.

### Listings

- View Listings
- Add Listing
- Update Listing
- Delete Listing

### Sales

- View Sales
- Add Sale
- Update Sale
- Delete Sale

### Buyers

- View Buyers
- Add Buyer
- Update Buyer
- Delete Buyer

### Agents

- View Agents
- Add Agent
- Update Agent
- Delete Agent

### Property Attributes

- View Property Attributes
- Add Property Attributes
- Update Property Attributes
- Delete Property Attributes

---

## 5. SQL Analytics

Implemented **30 business SQL queries**, including:

- Highest Revenue Cities
- Average Property Price
- Sales by Property Type
- Loan Uptake Rate
- Monthly Sales Trend
- Fastest Selling Properties
- Average Days on Market
- Buyer Insights
- Agent Performance
- Sale-to-List Price Ratio

All query results are displayed in an interactive table.

---

# 📊 Visualizations

- Scatter Plot
- Bar Chart
- Pie Chart
- Line Chart
- Interactive Map
- Data Tables

---

# 💡 Business Insights

The dashboard helps answer questions such as:

- Which city has the highest property prices?
- Which property type sells the fastest?
- What are the monthly sales trends?
- Which agents generate the highest sales?
- Which cities have the highest loan uptake?
- How does metro distance affect property sales?

---

# 🔄 Code Reusability (Modular Programming)

The application follows a modular architecture:

- **database.py** – Database connection
- **utils.py** – Reusable helper functions
- **dashboard.py** – Dashboard page
- **filters.py** – Filter logic
- **visualizations.py** – Charts
- **crud.py** – CRUD operations
- **sql_queries.py** – SQL analytics
- **common.py** – Shared UI components

This improves:

- Code readability
- Maintainability
- Reusability
- Scalability

---

# 🚀 Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/BrickView.git
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run main.py
```

---

# 📷 Dashboard Modules

- Introduction
- Filters & Explorer
- Visualizations
- CRUD Operations
- SQL Query Explorer

---

# 📈 Future Enhancements

- User Authentication
- Export Reports (PDF/Excel)
- Interactive Map using Plotly
- Power BI Integration
- Machine Learning Price Prediction
- Real-Time API Integration

---

# 👨‍💻 Author

**Shaik Rabbani**

Assistant Professor | Senior Software Engineer

AI & Full Stack Development Enthusiast

---

# 📄 License

This project is developed for educational and analytical purposes.

---

# 🙏 Acknowledgements

- GUVI AI/ML Bootcamp
- Streamlit
- Pandas
- SQLite
- Matplotlib