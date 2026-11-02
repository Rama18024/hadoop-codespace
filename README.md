# Smart Canteen Big Data Analytics

## Project Overview
Smart Canteen Big Data Analytics is a mini-project that uses Big Data technologies and Machine Learning to analyze food consumption, identify food waste, and predict food demand in a canteen.

The project uses a synthetic dataset containing 100,000 canteen food records.

## Objectives
- Analyze food preparation and sales.
- Calculate leftover food and food waste.
- Compare waste across different food items and meal types.
- Predict food demand using Machine Learning.
- Display results through an interactive dashboard.

## Technologies Used
- Python
- Apache Hadoop
- Apache Hive
- MapReduce
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- Streamlit

## Project Structure
```text
hadoop-codespace/
├── docker-compose.yml
├── hadoop/
├── hive/
├── smart-canteen/
│   ├── data/
│   │   └── canteen_data.csv
│   ├── mapreduce/
│   ├── results/
│   ├── visualizations/
│   ├── app.py
│   ├── demand_prediction.py
│   └── generate_data.py
└── README.md
```

## Dataset
The dataset contains 100,000 records with the following fields:
- Date
- Food item
- Prepared quantity
- Sold quantity
- Leftover quantity
- Meal type

## Big Data Analysis Results
- Total prepared quantity: 11,953,762
- Total sold quantity: 10,455,042
- Total leftover quantity: 1,498,720
- Overall food waste: 12.54%

## Machine Learning
A Random Forest Regression model is used to predict the quantity of food likely to be sold.

Model performance:
- Mean Absolute Error (MAE): 13.46
- Root Mean Squared Error (RMSE): 17.31
- R-squared (R²): 0.8707

## Dashboard Features
The Streamlit dashboard includes:
1. Project Overview
2. Food Analysis
3. Waste Analysis
4. Meal Analysis
5. Demand Prediction

## Run the Dashboard
Activate the Python virtual environment:

```bash
source .venv/bin/activate
```

Install the required packages if needed:

```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn
```

Start the dashboard:

```bash
streamlit run smart-canteen/app.py --server.address 0.0.0.0 --server.port 8501
```

## Expected Outcome
The project helps identify food waste patterns, understand canteen demand, and support better food preparation decisions.

## Repository
GitHub: https://github.com/Rama18024/hadoop-codespace

## Author
Rama18024
