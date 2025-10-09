# Agri-Curve: Logistic Cost Prediction & Curve Generation Plan

## Project Overview

Build a time-series forecasting system to predict logistic costs for different agricultural transport routes in Brazil. The system will generate cost curves showing probable future costs after a cutoff date, enabling customers to make informed decisions about contract operations.

## Current State Analysis

### Existing Infrastructure
- **Data Generation**: Metaflow pipeline generating 500K synthetic logistics operations
- **Data Features**: 18 columns including dates, routes, commodities, distances, costs, and economic indicators
- **Routes**: 10 municipalities to 10 ports across Brazil (100 possible route combinations)
- **Commodities**: 8 types (Soy, Corn, Cotton, Sugar, Coffee, Soybean Meal, Soybean Oil, Wheat)
- **Time Range**: 2023-01-01 to 2024-12-31 (720 days of historical data)
- **Tech Stack**: Python 3.12, Metaflow, Pandas, Scikit-learn, Loguru
- **Deployment**: Kubernetes (Minikube) with ArgoCD for GitOps

### Data Structure
```
- operation_date: Date of transport operation
- route: Origin-Destination pair (e.g., "Sorriso_MT-Santos_SP")
- commodity: Agricultural product type
- distance_km: Route distance
- tonnage: Cargo weight
- total_freight_value: Total transport cost
- value_per_ton: Cost per ton
- commodity_reference_price: Market price reference
- month, year: Temporal features
- Coordinates: lat/lon for origin and destination
```

## Technology Stack

### Core Libraries
- **Metaflow**: Workflow orchestration and MLOps
- **Darts**: Time-series forecasting (Prophet, ARIMA, LSTM, etc.)
- **UV**: Fast Python package management
- **Loguru**: Structured logging
- **Plotly**: Interactive curve visualization
- **Pandas**: Data manipulation
- **Scikit-learn**: Feature engineering and preprocessing

### Additional Dependencies (to be added)
- `darts[all]>=0.27.0` - Time-series forecasting
- `plotly>=5.18.0` - Interactive visualization
- `prophet>=1.1.5` - Facebook Prophet for seasonality
- `statsmodels>=0.14.0` - Statistical models
- `pmdarima>=2.0.4` - Auto-ARIMA

## Development Plan

### Phase 1: Environment & Configuration Setup

#### 1.1 Update Dependencies
- [ ] Add Darts, Plotly, and time-series libraries to `pyproject.toml`
- [ ] Update `requirements.txt` for Docker compatibility
- [ ] Test UV package resolution
- [ ] Verify all dependencies work in Kubernetes environment

#### 1.2 Configuration Management
- [ ] Create `TrainingConfig` in `config/config.py`:
  - Model parameters (horizon, lookback_window, validation_split)
  - Route filtering options
  - Feature engineering settings
  - Cutoff date configuration
- [ ] Create `InferenceConfig`:
  - Prediction horizons (30, 60, 90 days)
  - Scenario simulation parameters
  - Output paths
- [ ] Create `VisualizationConfig`:
  - Chart styling options
  - Scenario definitions (optimistic, realistic, pessimistic)
  - Export formats

### Phase 2: Data Preprocessing & Feature Engineering

#### 2.1 Complete `src/nodes/preprocessing.py`
- [ ] Implement `split_data()`:
  - Time-based train/validation split
  - Respect temporal ordering
  - Handle route-specific splits
- [ ] Implement `generate_seasonality_features()`:
  - Cyclical encoding for month (sin/cos)
  - Quarter indicators
  - Holiday flags (Brazilian agricultural calendar)
  - Harvest season indicators per commodity
- [ ] Create `RouteAggregator` class:
  - Group data by route
  - Calculate route-level statistics (mean, std, trend)
  - Handle missing dates with forward fill
- [ ] Create `FeatureEngineer` class:
  - Lag features (7, 14, 30 days)
  - Rolling statistics (mean, std, min, max)
  - Price momentum indicators
  - Distance-cost efficiency ratios
- [ ] Add data quality checks:
  - Outlier detection
  - Missing value handling
  - Date continuity validation

#### 2.2 Create Preprocessing Metaflow
- [ ] Build `PreprocessFlow` in `src/pipelines/preprocessing.py`:
  - `start`: Load raw data
  - `filter_dates`: Apply DateFilter
  - `engineer_features`: Generate time-series features
  - `aggregate_routes`: Group by route
  - `validate_data`: Quality checks
  - `split_data`: Train/validation split
  - `save_artifacts`: Save processed datasets
  - `end`: Log statistics

### Phase 3: Model Training Pipeline

#### 3.1 Create Model Wrapper (`src/nodes/models.py`)
- [ ] `BaseForecaster` abstract class:
  - Standardized fit/predict interface
  - Model serialization
  - Metric calculation (MAE, RMSE, MAPE)
- [ ] `DartsForecaster` implementations:
  - `ProphetForecaster`: Handles seasonality well
  - `NHiTSForecaster`: Neural network for complex patterns
  - `LightGBMForecaster`: Gradient boosting for feature-rich data
  - `EnsembleForecaster`: Combine multiple models
- [ ] Each forecaster should:
  - Accept Darts `TimeSeries` objects
  - Support multivariate inputs (exogenous features)
  - Return prediction intervals (confidence bounds)

#### 3.2 Build Training Flow (`src/pipelines/train.py`)
- [ ] Design `TrainingFlow`:
  - `start`: Load preprocessed data
  - `create_timeseries`: Convert to Darts format
  - `train_models` (parallel):
    - Train Prophet model
    - Train NHiTS model
    - Train LightGBM model
  - `validate_models`: Calculate metrics on validation set
  - `select_best_model`: Choose best performer per route
  - `train_ensemble`: Create ensemble of top models
  - `save_models`: Serialize to artifacts
  - `log_metrics`: Record performance to MLflow or Metaflow
  - `end`: Generate training report

#### 3.3 Model Persistence
- [ ] Create `src/nodes/model_registry.py`:
  - Save models with metadata (route, date, metrics)
  - Version control for models
  - Load models by route and version
  - Model comparison utilities

### Phase 4: Inference & Curve Generation

#### 4.1 Inference Pipeline (`src/pipelines/inference.py`)
- [ ] Build `InferenceFlow`:
  - `start`: Define cutoff date and prediction horizon
  - `load_models`: Retrieve best models per route
  - `load_historical_data`: Get data up to cutoff
  - `predict_routes` (parallel):
    - Generate point forecasts
    - Generate prediction intervals (5%, 50%, 95% quantiles)
    - Create scenario simulations
  - `aggregate_predictions`: Combine route predictions
  - `generate_curves`: Prepare data for visualization
  - `save_predictions`: Export to CSV/Parquet
  - `end`: Summary statistics

#### 4.2 Scenario Simulation (`src/nodes/scenarios.py`)
- [ ] `ScenarioGenerator` class:
  - Optimistic: Lower bound of prediction interval
  - Realistic: Point forecast
  - Pessimistic: Upper bound of prediction interval
  - Custom: User-defined adjustments (fuel price +X%, demand surge, etc.)
- [ ] Apply scenario multipliers:
  - Fuel cost variations (±20%)
  - Seasonal demand shifts
  - Port congestion impacts

### Phase 5: Visualization & Reporting

#### 5.1 Create Plotly Curve Charts (`src/nodes/visualization.py`)
- [ ] `CurveVisualizer` class:
  - `plot_route_curve()`:
    - Historical data (actual costs)
    - Cutoff date vertical line
    - Future cost curves (scenarios)
    - Confidence intervals as filled areas
    - Interactive hover tooltips
  - `plot_multi_route_comparison()`:
    - Compare multiple routes side-by-side
    - Highlight best/worst scenarios
  - `plot_commodity_trends()`:
    - Aggregate by commodity type
    - Show seasonal patterns
  - `export_to_html()`:
    - Standalone interactive HTML reports
    - Embedded in dashboard apps

#### 5.2 Chart Configuration
- [ ] Design parameters:
  - Color schemes per scenario (green=optimistic, red=pessimistic)
  - Date range selectors
  - Zoom controls
  - Export buttons (PNG, SVG, PDF)
  - Responsive layout

#### 5.3 Model Explainability (`src/nodes/explainability.py`)

**Goal**: Explain predictions in plain language for business users, not data scientists.

- [ ] `BusinessExplainer` class:

  **1. Trend Explanation**:
  - Extract Prophet trend component
  - Translate to narrative:
    - "Costs are trending UP by 8% over the next 90 days"
    - "Costs are expected to STABILIZE around 450 BRL/ton"
    - "Costs are trending DOWN due to off-peak season"

  **2. Seasonality Explanation**:
  - Extract Prophet seasonal patterns
  - Generate user-friendly insights:
    - "February-April is historically HIGH SEASON (soy harvest) - costs increase 20%"
    - "June-August shows lower demand - expect 10-15% cost reduction"
    - "December has moderate activity - costs near annual average"

  **3. Key Drivers Identification**:
  - Analyze which factors changed most vs historical average
  - Present as bullet points:
    - "⬆️ Higher tonnage demand (15% above normal)"
    - "⬆️ Port congestion at Santos (major routes affected)"
    - "⬇️ Fuel prices stabilizing (5% decrease expected)"

  **4. Historical Context**:
  - Compare prediction to past periods
  - Simple comparisons:
    - "This December will be 12% MORE expensive than last December"
    - "Similar to costs seen in Q2 2023"
    - "Within normal range for this route"

  **5. Confidence Level Communication**:
  - Translate prediction intervals to confidence language:
    - Wide interval (±30%): "LOW confidence - market is volatile"
    - Medium interval (±15%): "MODERATE confidence - some uncertainty"
    - Narrow interval (±5%): "HIGH confidence - stable market conditions"

  **6. Risk Indicators**:
  - Flag unusual patterns:
    - "⚠️ WARNING: Prices trending above historical highs"
    - "✓ STABLE: Costs within expected range"
    - "✓ OPPORTUNITY: Below-average costs expected"

  **7. Scenario Narratives**:
  - Explain what causes each scenario:
    - **Optimistic**: "If fuel prices stay low + off-peak demand continues"
    - **Realistic**: "If market conditions remain similar to recent weeks"
    - **Pessimistic**: "If harvest season peaks + port delays occur"

  **8. Model Agreement Indicator**:
  - Show consensus across models in simple terms:
    - "All 3 models AGREE: costs will increase" (strong signal)
    - "Models DISAGREE: high uncertainty" (proceed with caution)
    - "2 of 3 models predict stability" (moderate confidence)

- [ ] `InsightGenerator` class:

  **Automatic Insight Discovery**:
  - [ ] Identify cost-saving opportunities:
    - "Best shipping window: November 5-12 (lowest costs)"
    - "Avoid shipping after November 20 (15% price spike)"

  - [ ] Route comparisons:
    - "Alternative route via Paranaguá is 8% cheaper in December"
    - "This route is the 2nd most cost-effective for soy"

  - [ ] Timing recommendations:
    - "Consider booking contracts NOW - prices increasing in 30 days"
    - "Wait 2 weeks - prices expected to drop 5%"

  - [ ] Risk alerts:
    - "High volatility ahead - consider fixed-rate contracts"
    - "Stable period - spot market may offer better rates"

- [ ] `VisualizationNarratives` class:

  **Add explanatory text to charts**:
  - [ ] Annotate key points on curves:
    - "Peak cost period" (arrow pointing to highest point)
    - "Best time to ship" (green highlight)
    - "Historical average" (dashed reference line)

  - [ ] Color-coded insights:
    - Green zones: "Below average costs"
    - Yellow zones: "Average costs"
    - Red zones: "Above average costs - consider alternatives"

  - [ ] Simple legend:
    - Replace "95th percentile" with "Worst case scenario"
    - Replace "50th percentile" with "Most likely outcome"
    - Replace "5th percentile" with "Best case scenario"

#### 5.4 Reporting Pipeline
- [ ] Create `ReportingFlow`:
  - Generate HTML report with:
    - **Executive Summary** (plain language):
      - "What will happen": 1-sentence prediction
      - "Why": Top 3 drivers in bullet points
      - "Confidence level": High/Medium/Low with explanation
      - "Recommended action": Clear next step

    - **Prediction Curves**:
      - Route-level curve charts with scenarios
      - Annotated with key dates and insights
      - Confidence intervals labeled as "Range of possible costs"

    - **Model Explanation Section** (NEW - Non-technical):
      - **"How We Made This Prediction"**:
        - Simple description: "We analyzed 2 years of data for this route..."
        - "Our models looked at: seasonality, historical trends, and market conditions"

      - **"What's Driving These Costs"**:
        - Top 5 factors as simple bullet points with icons
        - Example: "📅 Seasonal demand (harvest period)"
        - Example: "⛽ Fuel price trends"
        - Example: "🚢 Port efficiency"

      - **"Trend Analysis"**:
        - Line chart showing historical trend
        - "Costs have been increasing at 2% per month"
        - "This is typical for pre-harvest season"

      - **"Model Confidence"**:
        - Traffic light indicator (green/yellow/red)
        - "Why we're confident": Explanation in 1-2 sentences
        - "All our forecasting methods agree on this trend"

      - **"Historical Comparison"**:
        - Side-by-side bar chart: Last year vs This year prediction
        - "Compared to last December: 12% higher"
        - "Compared to 6-month average: 5% higher"

    - **Scenario Analysis**:
      - Scenario comparison table with simple labels
      - **For each scenario**: Plain-language explanation of assumptions
      - Risk assessment: "If costs reach pessimistic scenario, consider..."

    - **Action Recommendations**:
      - Clear, numbered steps: "1. Book shipments before Nov 15..."
      - Cost-saving opportunities highlighted
      - Alternative routes suggested if applicable

    - **Glossary Section** (for any technical terms used):
      - Simple definitions
      - Visual examples

  - Export to `data/reports/` directory
  - Timestamp reports for version control
  - Mobile-friendly responsive design

### Phase 6: Integration & Testing

#### 6.1 End-to-End Pipeline
- [ ] Create `src/pipelines/full_pipeline.py`:
  - Chain: DataGen → Preprocess → Train → Inference → Report
  - Add conditional logic (skip training if models exist)
  - Implement caching for expensive steps
  - Add error handling and rollback

#### 6.2 Testing Strategy
- [ ] Unit tests:
  - Feature engineering functions
  - Model wrapper interfaces
  - Scenario calculations
- [ ] Integration tests:
  - Metaflow flows with small datasets
  - Model training and loading
  - Visualization generation
- [ ] Data validation tests:
  - Schema validation
  - Date continuity
  - Cost reasonableness checks

#### 6.3 Logging & Monitoring
- [ ] Enhance Loguru usage:
  - Structured logs with context (route, date, model)
  - Performance metrics (runtime, memory)
  - Data quality alerts
  - Model performance degradation warnings

### Phase 7: Deployment & Automation

#### 7.1 Docker Updates
- [ ] Update `Dockerfile`:
  - Include Darts and visualization dependencies
  - Optimize layer caching
  - Add health check endpoints
- [ ] Test container builds locally
- [ ] Push new image versions to registry

#### 7.2 Kubernetes Configuration
- [ ] Update `deployment.yaml`:
  - Increase resource limits (Darts models can be memory-intensive)
  - Add volume mounts for model artifacts
  - Configure environment variables (cutoff dates, horizons)
- [ ] Update CronJob:
  - Daily data generation
  - Weekly model retraining
  - Daily inference and curve generation
- [ ] Configure ArgoCD sync policies

#### 7.3 Monitoring & Alerts
- [ ] Set up metrics collection:
  - Model accuracy over time
  - Prediction errors vs actuals
  - Processing times
- [ ] Create dashboards (Grafana/Kubernetes Dashboard):
  - Pipeline health
  - Data volume trends
  - Model performance

## Implementation Order

### Sprint 1: Foundation (Week 1)
1. Update dependencies and configuration
2. Complete preprocessing nodes
3. Build PreprocessFlow
4. Test with sample data

### Sprint 2: Modeling (Week 2)
5. Implement model wrappers (Darts integration)
6. Build TrainingFlow
7. Train baseline models on sample routes
8. Validate prediction quality

### Sprint 3: Inference & Visualization (Week 3)
9. Build InferenceFlow
10. Implement scenario generation
11. Create Plotly curve visualizations
12. Generate sample reports

### Sprint 4: Integration & Deployment (Week 4)
13. Build full pipeline
14. Add testing and validation
15. Update Docker/Kubernetes configs
16. Deploy and monitor

## Key Technical Decisions

### Model Selection Rationale
- **Prophet**: Excellent for capturing seasonality and holidays
- **NHiTS**: State-of-the-art neural network for time-series
- **LightGBM**: Fast, handles rich feature sets well
- **Ensemble**: Combines strengths, reduces overfitting

### Route-Level Modeling
- Each route gets dedicated models (100 routes × N models)
- Allows route-specific patterns (distance, port efficiency, regional factors)
- Alternative: Global model with route embeddings (can explore in v2)

### Forecast Horizon
- Primary: 90 days (typical contract planning window)
- Secondary: 30, 60, 180 days
- Update frequency: Daily new predictions

### Scenario Simulation Approach
- Statistical: Use prediction interval bounds
- Economic: Apply multiplier scenarios
- Hybrid: Combine both methods

## Data Flow Architecture

```
Raw Data (500K ops)
    ↓
[DateFilter + FeatureEngineering]
    ↓
Route-Level Time Series (100 routes)
    ↓
[Train/Val Split]
    ↓
Model Training (parallel per route)
    ↓
Model Registry (best models)
    ↓
Inference (cutoff date → horizon)
    ↓
Scenario Generation (3-5 scenarios)
    ↓
Plotly Curves + HTML Reports
    ↓
Output: data/reports/{route}_{date}_curves.html
```

## File Structure (After Implementation)

```
agri-curve/
├── config/
│   ├── config.py (updated with TrainingConfig, InferenceConfig, VisualizationConfig, ExplainabilityConfig)
├── src/
│   ├── nodes/
│   │   ├── datagen.py (existing)
│   │   ├── preprocessing.py (complete feature engineering)
│   │   ├── models.py (NEW - model wrappers)
│   │   ├── scenarios.py (NEW - scenario generation)
│   │   ├── visualization.py (NEW - Plotly charts)
│   │   ├── explainability.py (NEW - business-friendly explanations)
│   │   └── model_registry.py (NEW - model management)
│   ├── pipelines/
│   │   ├── datagen.py (existing)
│   │   ├── preprocessing.py (NEW - preprocessing flow)
│   │   ├── train.py (NEW - training flow)
│   │   ├── inference.py (NEW - inference flow)
│   │   └── full_pipeline.py (NEW - end-to-end)
├── data/
│   ├── raw/ (existing)
│   ├── processed/ (existing)
│   ├── models/ (NEW - serialized models)
│   ├── explanations/ (NEW - insights and narratives)
│   └── reports/ (NEW - HTML curve reports)
├── tests/
│   ├── test_preprocessing.py
│   ├── test_models.py
│   ├── test_explainability.py
│   └── test_pipelines.py
├── notebooks/
│   └── curve_analysis.ipynb (for interactive exploration)
├── pyproject.toml (updated)
├── requirements.txt (updated)
└── claude_plan.md (this file)
```

## Success Metrics

### Model Performance
- MAE < 50 BRL per ton (value_per_ton prediction)
- MAPE < 15% (industry standard for logistics)
- Prediction intervals cover 90% of actual values

### System Performance
- Full pipeline runs in < 30 minutes
- Inference for all routes in < 5 minutes
- Reports generate in < 2 minutes

### Business Value
- Provide 90-day cost forecasts for all 100 routes
- Deliver 3+ scenario simulations per route
- Enable contract decision-making with confidence intervals

## Risk Mitigation

### Technical Risks
1. **Model overfitting on synthetic data**
   - Mitigation: Cross-validation, regularization, ensemble methods
2. **Long training times for 100 routes**
   - Mitigation: Parallel execution with Metaflow, GPU acceleration for neural models
3. **Kubernetes resource constraints**
   - Mitigation: Optimize model sizes, implement batch processing

### Data Risks
1. **Insufficient historical data (2 years)**
   - Mitigation: Use models designed for limited data (Prophet, ensemble)
2. **Seasonality may not fully capture real patterns**
   - Mitigation: Validate with domain experts, add economic indicators

## Next Steps

1. **Immediate**: Review and approve this plan
2. **Start Implementation**: Phase 1 (Environment Setup)
3. **Continuous**: Update plan based on findings during development
4. **Future Enhancements**:
   - Real-time data ingestion
   - Web dashboard for interactive exploration
   - Multi-horizon forecasting comparison
   - Cost optimization recommendations
   - Integration with ERP systems

## Questions to Resolve

1. What is the primary decision cutoff date? (Default: today)
2. Which routes are highest priority? (Default: all 100)
3. Are there specific scenarios to simulate beyond optimistic/pessimistic?
4. Should reports be per-route or aggregated?
5. What is the acceptable prediction error tolerance?

---

**Plan Created**: 2025-10-09
**Status**: Ready for Implementation
**Tech Stack**: Metaflow, Darts, UV, Loguru, Plotly, Pandas, Scikit-learn
