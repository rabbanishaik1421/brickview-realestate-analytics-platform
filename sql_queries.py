import streamlit as st
from utils import run_query

def show_sqlqueries():
    st.subheader("SQL Queries")
    # st.subheader("Listings")

    queries = {
        "1. Total Listings by City":
        """
        SELECT City,
            COUNT(*) AS TotalListings
        FROM listings
        GROUP BY City
        ORDER BY TotalListings DESC
        """,

        "2. Average Property Price by City":
        """
        SELECT City,
            ROUND(AVG(Price),2) AS AveragePrice
        FROM listings
        GROUP BY City
        ORDER BY AveragePrice DESC
        """,

        "3. Top 10 Most Expensive Properties":
        """
        SELECT Listing_ID,
            City,
            Property_Type,
            Price
        FROM listings
        ORDER BY Price DESC
        LIMIT 10
        """,

        "4. Do properties closer to metro stations command higher prices?":
        """
            SELECT
                CASE
                    WHEN PA.metro_distance_km < 2 THEN '0-2 KM'
                    WHEN PA.metro_distance_km < 5 THEN '2-5 KM'
                    WHEN PA.metro_distance_km < 10 THEN '5-10 KM'
                    ELSE '10+ KM'
                END AS Metro_Distance,
                CAST(AVG(L.Price) AS INTEGER) AS Average_Price,
                COUNT(*) AS Total_Properties
            FROM listings L
            JOIN property_attributes PA
            ON L.Listing_ID = PA.listing_id
            GROUP BY Metro_Distance
            ORDER BY Average_Price;
        """,

        "5. Are rented properties priced differently from non-rented ones?":
        """
        SELECT
            CASE
                WHEN PA.is_rented = 1 THEN 'Rented'
                ELSE 'Non Rented'
            END AS RentalType,

            CAST(AVG(L.Price) AS INTEGER) AS Average_Price,
            COUNT(*) AS Total_Properties

        FROM listings L
        LEFT JOIN property_attributes PA
        ON L.Listing_ID = PA.listing_id

        GROUP BY RentalType""",

        "6. How do bedrooms and bathrooms affect pricing?":
        """
            SELECT
                PA.bedrooms,
                PA.bathrooms,
                CAST(AVG(L.Price) AS INTEGER) AS AveragePrice,
                COUNT(*) AS TotalProperties
            FROM listings L
            JOIN property_attributes PA
                ON L.Listing_ID = PA.listing_id
            GROUP BY
                PA.bedrooms,
                PA.bathrooms
            ORDER BY
                PA.bedrooms,
                PA.bathrooms;
        """,

        "7. Do properties with parking and power backup sell at higher prices?":
        """
            SELECT 
                CASE 
                    WHEN PA.parking_available = 1 THEN 'Yes'
                    ELSE 'No'
                END AS Parking,
        
                CASE 
                    WHEN PA.power_backup = 1 THEN 'Yes'
                    ELSE 'No'
                END AS Power_Backup,
                CAST(AVG(L.Price) AS INTEGER) AS AveragePrice,
                count(*) AS TotalProperties
            FROM listings L
            LEFT JOIN property_attributes PA
            ON L.Listing_ID=PA.listing_id
            GROUP BY Parking, Power_Backup
            ORDER BY AveragePrice DESC
        """,

        "8. How does year built influence listing price?":
        """
        SELECT PA.year_built AS BuiltYear, CAST(AVG(Price) AS INTEGER) AS AveragePrice, COUNT(*) AS TotalProperties
        FROM listings L
        JOIN property_attributes PA
        ON L.Listing_ID=PA.listing_id
        GROUP BY BuiltYear
        ORDER BY BuiltYear DESC
        """,

        "9. Which cities have the highest average property prices?":
        """SELECT avg(Price) as AveragePrice, City FROM listings GROUP BY City ORDER BY AveragePrice DESC LIMIT 1""",

        "10. How are properties distributed across price buckets?":
        """
        SELECT
            CASE
                WHEN Price < 500000 THEN 'Budget'
                WHEN Price BETWEEN 500000 AND 1000000 THEN 'Affordable'
                WHEN Price BETWEEN 1000001 AND 2000000 THEN 'Mid-Range'
                WHEN Price BETWEEN 2000001 AND 3000000 THEN 'Premium'
                WHEN Price BETWEEN 3000001 AND 4000000 THEN 'Luxury'
                ELSE 'Ultra Luxury'
            END AS PriceBucket,

            COUNT(*) AS TotalProperties,
            CAST(AVG(Price) AS INTEGER) AS AveragePrice

        FROM listings

        GROUP BY PriceBucket

        ORDER BY AveragePrice;
        """,

        "11. What is the average days on market by city?":
        """
        SELECT L.City, CAST(AVG(S.Days_on_Market) AS INTEGER) AS DaysOnMarket 
        FROM listings L JOIN sales S ON L.Listing_ID=S.listing_id
        GROUP BY L.City
        ORDER BY DaysOnMarket DESC
        """,

        "12. Which property types sell the fastest?":
        """
        SELECT
            L.Property_Type,
            CAST(AVG(S.Days_on_Market) AS INTEGER) AS AverageDaysToSell,
            COUNT(*) AS TotalSales
        FROM listings L
        INNER JOIN sales S
        ON L.Listing_ID = S.Listing_ID
        GROUP BY L.Property_Type
        ORDER BY AverageDaysToSell ASC
        """,

        "13. What percentage of properties are sold above listing price?":
        """
        SELECT
            COUNT(*) AS TotalSoldProperties,
        
            SUM(
                CASE
                    WHEN S.Sale_Price > L.Price THEN 1
                    ELSE 0
                END
            ) AS SoldAboveListing,
        
            ROUND(
                SUM(
                    CASE
                        WHEN S.Sale_Price > L.Price THEN 1
                        ELSE 0
                    END
                ) * 100.0 / COUNT(*),
                2
            ) AS PercentageSoldAboveListing
        
        FROM listings L
        INNER JOIN sales S
        ON L.Listing_ID = S.Listing_ID
        """,
        "14. What is the sale-to-list price ratio by city?":
        """
        SELECT
            L.City,
            ROUND(AVG((S.Sale_Price * 100.0) / L.Price), 2) AS SaleToListPriceRatio,
            COUNT(*) AS TotalSales
        FROM listings L
        INNER JOIN sales S
            ON L.Listing_ID = S.Listing_ID
        GROUP BY L.City
        ORDER BY SaleToListPriceRatio DESC
        """,

        "15. Which listings took more than 90 days to sell?":
        """
        SELECT 
            L.Listing_ID, 
            L.City,
            L.Property_Type,
            L.Price,
            S.Sale_Price,
            S.Days_on_Market
        FROM 
            listings L 
        LEFT JOIN sales S 
        ON L.Listing_ID=S.listing_id 
        WHERE 
            S.Days_on_Market>90 
        ORDER BY S.Days_on_Market DESC
        """,

        "16. How does metro distance affect time on market?":
        """
        SELECT
            PA.metro_distance_km,
            CAST(AVG(S.Days_on_Market) AS INTEGER) AS AverageDaysOnMarket,
            COUNT(*) AS TotalProperties
        FROM property_attributes PA
        INNER JOIN sales S
            ON PA.listing_id = S.Listing_ID
        GROUP BY PA.metro_distance_km
        ORDER BY PA.metro_distance_km ASC
        """,

        "17. What is the monthly sales trend?":
        """
        SELECT
            strftime('%Y-%m', Date_Sold) AS SaleMonth,
            COUNT(*) AS TotalSales
        FROM sales
        GROUP BY SaleMonth
        ORDER BY SaleMonth
        """,

        "18. Which properties are currently unsold?":
        """
        SELECT 
            L.* 
        FROM listings L
        INNER JOIN sales S
        ON L.Listing_ID=S.Listing_ID
        """,

        "19. Which agents have closed the most sales?":
        """
        SELECT 
            A.Agent_ID,
            A.Name,
            count(S.Listing_ID) as MostSales
        FROM sales S
        INNER JOIN listings L ON S.Listing_ID=L.Listing_ID
        INNER JOIN agents A ON L.Agent_ID=A.Agent_ID
        GROUP BY A.Agent_ID, A.Name 
        ORDER BY MostSales DESC
        """,

        "20. Who are the top agents by total sales revenue?":
        """
        SELECT 
            A.Agent_ID,
            A.Name,
            sum(S.Sale_Price) as TotalSalesRevenue
        FROM sales S
        INNER JOIN listings L ON S.Listing_ID=L.Listing_ID
        INNER JOIN agents A ON L.Agent_ID=A.Agent_ID
        GROUP BY A.Agent_ID, A.Name
        ORDER BY TotalSalesRevenue DESC
        """,

        "21. Which agents close deals fastest?":
        """
        SELECT 
            A.Agent_ID,
            A.Name,
            CAST(AVG(S.Days_on_Market) AS INTEGER) as FewerDays
        FROM sales S
        INNER JOIN listings L ON S.Listing_ID=L.Listing_ID
        INNER JOIN agents A ON L.Agent_ID=A.Agent_ID
        GROUP BY A.Agent_ID, A.Name
        ORDER BY FewerDays ASC
        """,

        "22. Does experience correlate with deals closed?":
        """
        SELECT
            experience_years,
            CAST(AVG(deals_closed) AS INTEGER) AS AverageDealsClosed,
            COUNT(*) AS TotalAgents
        FROM agents
        GROUP BY experience_years
        ORDER BY experience_years
        """,

        "23. Do agents with higher ratings close deals faster?":
        """
        SELECT 
            rating,
            CAST(AVG(deals_closed) AS INTEGER) AS AverageDealsClosed,
            COUNT(*) AS TotalAgents
        FROM 
            agents
        GROUP BY rating
        ORDER BY rating
        """,

        "24. What is the average commission earned by each agent?":
        """
        SELECT
            A.Agent_ID,
            A.Name,
            CAST(AVG((S.Sale_Price * A.commission_rate) / 100) AS INTEGER) AS AverageCommissionEarned
        FROM sales S
        INNER JOIN listings L
            ON S.Listing_ID = L.Listing_ID
        INNER JOIN agents A
            ON L.Agent_ID = A.Agent_ID
        GROUP BY
            A.Agent_ID,
            A.Name
        ORDER BY
            AverageCommissionEarned DESC;
        """,

        "25. Which agents currently have the most active listings?":
        """
        SELECT
            A.Agent_ID,
            A.Name,
            COUNT(L.Listing_ID) AS ActiveListings
        FROM listings L
        INNER JOIN agents A
            ON L.Agent_ID = A.Agent_ID
        LEFT JOIN sales S
            ON L.Listing_ID = S.Listing_ID
        WHERE S.Listing_ID IS NULL
        GROUP BY
            A.Agent_ID,
            A.Name
        ORDER BY
            ActiveListings DESC;
        """,

        "26. What percentage of buyers are investors vs end users?":
        """
        SELECT 
            buyer_type,
            COUNT(*) AS TotalBuyers,
            ROUND(
                (COUNT(*) * 100.0) / (SELECT COUNT(*) FROM buyers), 2
            ) AS Percentage     
        FROM 
            buyers
        GROUP BY 
            buyer_type
        """,

        "27. Which cities have the highest loan uptake rate?":
        """
        SELECT 
            L.City,
            COUNT(B.buyer_id) AS TotalBuyers,
            SUM(
                CASE 
                    WHEN B.loan_taken = 1 THEN 1 ELSE 0
                END
            ) AS LoanBuyers,
            ROUND(
                SUM(
                    CASE 
                        WHEN B.loan_taken = 1 THEN 1 ELSE 0
                    END
                ) * 100.0 / COUNT(B.buyer_id), 2
            ) AS HighestLoanUptake
        FROM listings L 
        LEFT JOIN buyers B ON L.Listing_ID=B.sale_id
        GROUP BY L.City
        ORDER BY HighestLoanUptake DESC
        """,

        "28. What is the average loan amount by buyer type?":
        """
        SELECT 
            CAST(AVG(loan_amount) AS INTEGER) AS AverageLoanAmount,
            buyer_type
        FROM 
            buyers
        WHERE loan_taken=1
        GROUP BY buyer_type
        ORDER BY AverageLoanAmount DESC
        """,

        "29. Which payment mode is most commonly used?":
        """
        SELECT 
            payment_mode,
            count(buyer_id) as TotalTransactions 
        FROM 
            buyers 
        GROUP BY payment_mode
        ORDER BY TotalTransactions DESC
        """,

        "30. Do loan-backed purchases take longer to close?":
        """
        SELECT
            CASE
                WHEN B.loan_taken = 1 THEN 'Loan'
                ELSE 'No Loan'
            END AS LoanStatus,
        
            CAST(AVG(S.Days_on_Market) AS INTEGER) AS AverageDaysToClose,
        
            COUNT(*) AS TotalPurchases
        
        FROM buyers B
        INNER JOIN sales S
        ON B.sale_id = S.Listing_ID
        
        GROUP BY LoanStatus
        ORDER BY AverageDaysToClose DESC
        """        

    }

    selected_query = st.selectbox(
        "Select SQL Query",
        list(queries.keys())
    )

    if selected_query:
        df = run_query(queries[selected_query])

        st.text(selected_query)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
