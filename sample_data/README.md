# Sample Data for Multi-Agent AI System

This directory contains sample datasets and documents for testing the Multi-Agent AI System.

## Data Files

### 1. sales_data.csv
- **Description**: Sample sales data with product information, revenue, and customer details
- **Columns**: Date, Product, Category, Sales, Revenue, Customer_ID, Region, Quantity
- **Records**: 40 sales transactions from Q1-Q2 2023
- **Use Cases**: 
  - Revenue analysis queries
  - Product performance tracking
  - Regional sales comparisons
  - Time-based trend analysis

**Example Queries:**
- "What was the total revenue in Q1?"
- "Show me the top 5 products by sales"
- "Plot revenue trends over time"
- "Which region has the highest sales?"

### 2. customer_data.csv
- **Description**: Customer demographics and purchasing behavior data
- **Columns**: Customer_ID, Name, Age, Gender, Location, Join_Date, Total_Spent, Orders_Count, Segment
- **Records**: 30 customer profiles
- **Use Cases**:
  - Customer segmentation analysis
  - Demographics insights
  - Customer lifetime value analysis
  - Geographic distribution studies

**Example Queries:**
- "What's the average age of premium customers?"
- "Show customer distribution by segment"
- "Which customers have the highest total spent?"
- "Analyze customer demographics by region"

## Research Documents

### 1. sample_research_paper.txt
- **Title**: "Deep Learning Approaches for Computer Vision: A Comprehensive Survey"
- **Content**: Comprehensive research paper on computer vision and deep learning
- **Sections**: Abstract, Introduction, Methodology, Results, Challenges, Future Directions
- **Topics**: CNNs, Vision Transformers, Object Detection, Image Classification, Semantic Segmentation

**Example Queries:**
- "Summarize the research paper"
- "What are the main challenges in computer vision?"
- "Which deep learning architectures are discussed?"
- "What are the future research directions?"
- "What methodology was used in the study?"

## Usage Instructions

1. **For Data Analysis**: Upload the CSV files through the Streamlit interface and ask natural language questions about the data.

2. **For Research Queries**: Upload the research document (you may need to convert the .txt file to .pdf for the PDF processing agent) and ask questions about the content.

3. **Testing the Orchestrator**: Try mixed queries to test the intelligent routing between data and research agents.

## Sample Test Scenarios

### Scenario 1: Business Analytics
1. Upload `sales_data.csv`
2. Ask: "What was the total revenue in March 2023?"
3. Ask: "Plot sales trends by product category"
4. Ask: "Show me the top 5 customers by revenue"

### Scenario 2: Research Analysis
1. Upload the research document
2. Ask: "Summarize the paper on computer vision"
3. Ask: "What are the main deep learning architectures mentioned?"
4. Ask: "What challenges are identified in the paper?"

### Scenario 3: Mixed Queries (Orchestrator Testing)
1. Upload both data files and research document
2. Ask: "What was the total sales last quarter?" (should route to Data Agent)
3. Ask: "What methodology was used in the research?" (should route to Research Agent)
4. Ask ambiguous questions to test disambiguation

## Data Generation Notes

- Sales data includes seasonal patterns and realistic business scenarios
- Customer data represents diverse demographics and purchasing behaviors
- Research paper covers comprehensive topics in computer vision and AI
- All data is synthetic and created for demonstration purposes only
