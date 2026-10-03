# PJM Hourly Energy Consumption Forecasting

A time-series forecasting project using hourly PJM electricity demand data and an XGBoost regressor. The project includes a Jupyter notebook for data exploration/model development and a Streamlit interface for generating recursive hourly forecasts.

## Files

- `forecast.py` — Streamlit application
- `P679_Hourly_Energy_Consumption_Forecast.ipynb` — notebook for analysis and model development
- `PJMW_MW_Hourly.xlsx` — hourly electricity demand dataset
- `xgb_model.pkl` — trained XGBoost model (must be added)
- `feature_columns.pkl` — model feature list (must be added)
- `holiday_dates.pkl` — holiday calendar data (must be added)
- `requirements.txt` — Python dependencies
- `.gitignore` — files excluded from Git

## Setup

1. Clone or download this repository.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Place `xgb_model.pkl`, `feature_columns.pkl`, and `holiday_dates.pkl` in the project root, alongside `forecast.py` and the Excel dataset. These binary artifacts are required by the app and are not included in this starter bundle.
4. Start the app:

   ```bash
   streamlit run forecast.py
   ```

## Method

The notebook explores hourly electricity demand, creates time-based and lag/rolling features, compares forecasting models, and saves the selected XGBoost model and supporting metadata. The Streamlit app loads those saved artifacts and produces recursive hourly forecasts for a user-selected number of days.

## Notes

- Keep the model artifacts and dataset in the same directory as `forecast.py` unless you update its file paths.
- Only load `.pkl` files from trusted sources.
