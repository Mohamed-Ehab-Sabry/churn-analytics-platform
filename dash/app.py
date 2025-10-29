import os
import duckdb
import pandas as pd
from datetime import datetime

import dash
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

# -----------------------------
# Configuration
# -----------------------------
DUCKDB_PATH = r"C:\Users\COMPUMARTS\Desktop\dashboard\churn_warehouse.duckdb"

# -----------------------------
# Load data
# -----------------------------
def load_data():
    con = duckdb.connect(DUCKDB_PATH, read_only=True)
    try:
        query = """
            SELECT
                customerID,
                gender,
                MonthlyCharges,
                TotalCharges,
                Contract,
                Churn
            FROM customer_churn_data
        """
        df = con.execute(query).fetch_df()
    finally:
        con.close()

    # Rename columns to match dashboard convention
    df = df.rename(columns={
        'customerID': 'customer_id',
        'MonthlyCharges': 'monthly_charges',
        'TotalCharges': 'total_charges',
        'Contract': 'contract_type',
        'Churn': 'churn'
    })

    # Convert churn to 0/1
    df['churn'] = df['churn'].map({'Yes': 1, 'No': 0})
    df['churn_label'] = df['churn'].map({0: 'Active', 1: 'Churned'})

    # Optional: fill missing numeric columns
    df['monthly_charges'] = pd.to_numeric(df['monthly_charges'], errors='coerce').fillna(0)
    df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce').fillna(0)

    return df

DATA = load_data()

# -----------------------------
# Filter options
# -----------------------------
contract_options = sorted(DATA['contract_type'].dropna().unique())

min_charge = int(DATA['monthly_charges'].min())
max_charge = int(DATA['monthly_charges'].max())

# -----------------------------
# Dash app setup
# -----------------------------
app: Dash = dash.Dash(__name__)
server = app.server

card_style = {
    'padding': '12px 16px',
    'border': '1px solid #e5e7eb',
    'borderRadius': '10px',
    'background': 'white',
    'boxShadow': '0 1px 2px rgba(0,0,0,0.05)'
}

app.layout = html.Div(
    style={'fontFamily': 'Segoe UI, Arial', 'background': '#f8fafc', 'minHeight': '100vh', 'padding': '16px'},
    children=[
        html.Div([
            html.H2('Customer Churn Dashboard', style={'margin': 0}),
            html.Div('Understand why customers leave and how to retain them', style={'color': '#64748b'})
        ], style={'marginBottom': '16px'}),

        # Filters
        html.Div([
            html.Div([
                html.Label('Contract Type'),
                dcc.Dropdown(
                    id='filter-contract',
                    options=[{'label': c, 'value': c} for c in contract_options],
                    value=contract_options,
                    multi=True,
                    placeholder='Select contract types'
                )
            ], style={'flex': 1, 'minWidth': '220px'}),
            html.Div([
                html.Label('Monthly Charges'),
                dcc.RangeSlider(
                    id='filter-monthly-charges',
                    min=min_charge,
                    max=max_charge,
                    value=[min_charge, max_charge],
                    tooltip={'placement': 'bottom', 'always_visible': False}
                )
            ], style={'flex': 2, 'minWidth': '260px', 'padding': '0 12px'}),
            html.Div([
                html.Label('Status'),
                dcc.Checklist(
                    id='filter-churn',
                    options=[{'label': 'Active', 'value': 0}, {'label': 'Churned', 'value': 1}],
                    value=[0, 1],
                    inline=True
                )
            ], style={'flex': 1, 'minWidth': '220px'})
        ], style={'display': 'flex', 'gap': '12px', 'marginBottom': '16px'}),

        # KPIs
        html.Div([
            html.Div([
                html.Div('Total Customers', style={'color': '#64748b'}),
                html.H3(id='kpi-total', style={'margin': 0})
            ], style=card_style),
            html.Div([
                html.Div('Churned Customers', style={'color': '#64748b'}),
                html.H3(id='kpi-churned', style={'margin': 0})
            ], style=card_style),
            html.Div([
                html.Div('Churn Rate', style={'color': '#64748b'}),
                html.H3(id='kpi-churn-rate', style={'margin': 0})
            ], style=card_style),
            html.Div([
                html.Div('Avg Monthly Charges', style={'color': '#64748b'}),
                html.H3(id='kpi-avg-rev-lost', style={'margin': 0})
            ], style=card_style),
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '12px', 'marginBottom': '16px'}),

        # Charts
        html.Div([
            html.Div([dcc.Graph(id='fig-churn-pie', config={'displayModeBar': False})], style=card_style),
            html.Div([dcc.Graph(id='fig-churn-contract', config={'displayModeBar': False})], style=card_style),
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '12px', 'marginBottom': '16px'}),

        # Table
        html.Div([
            html.H4('Customer details'),
            dash_table.DataTable(
                id='detail-table',
                columns=[{"name": c, "id": c} for c in [
                    'customer_id', 'churn_label', 'monthly_charges', 'total_charges', 'contract_type', 'gender'
                ]],
                page_size=10,
                style_table={'overflowX': 'auto'},
                sort_action='native',
                filter_action='native'
            )
        ], style=card_style)
    ]
)

# -----------------------------
# Callbacks
# -----------------------------
def apply_filters(df: pd.DataFrame, contracts, monthly_range, churn_vals):
    f = df.copy()
    if contracts and len(contracts):
        f = f[f['contract_type'].isin(contracts)]
    if monthly_range and len(monthly_range) == 2:
        f = f[(f['monthly_charges'] >= monthly_range[0]) & (f['monthly_charges'] <= monthly_range[1])]
    if churn_vals is not None and len(churn_vals):
        f = f[f['churn'].isin(churn_vals)]
    return f

@app.callback(
    [
        Output('kpi-total', 'children'),
        Output('kpi-churned', 'children'),
        Output('kpi-churn-rate', 'children'),
        Output('kpi-avg-rev-lost', 'children'),
        Output('fig-churn-pie', 'figure'),
        Output('fig-churn-contract', 'figure'),
        Output('detail-table', 'data')
    ],
    [
        Input('filter-contract', 'value'),
        Input('filter-monthly-charges', 'value'),
        Input('filter-churn', 'value')
    ]
)
def update_dashboard(contracts, monthly_range, churn_vals):
    df = apply_filters(DATA, contracts, monthly_range, churn_vals)

    # KPIs
    total_customers = len(df)
    churned_customers = int(df['churn'].sum())
    churn_rate = (churned_customers / total_customers * 100) if total_customers else 0
    avg_monthly = df.loc[df['churn'] == 1, 'monthly_charges'].mean() if churned_customers else 0

    # Pie chart
    pie_df = df['churn_label'].value_counts().reset_index()
    pie_df.columns = ['churn_label', 'count']
    fig_pie = px.pie(pie_df, names='churn_label', values='count', color='churn_label',
                     color_discrete_map={'Active':'#22c55e','Churned':'#ef4444'},
                     title='Churn vs Active')
    fig_pie.update_traces(textposition='inside', textinfo='percent+label', hole=0.35)

    # Contract churn rate
    contract_df = df.groupby('contract_type').agg(total=('customer_id','count'), churned=('churn','sum')).reset_index()
    contract_df['churn_rate'] = (contract_df['churned']/contract_df['total']*100).round(2)
    fig_contract = px.bar(contract_df, x='contract_type', y='churn_rate', title='Churn rate by contract',
                          color='churn_rate', color_continuous_scale='Reds')

    # Table data
    table_cols = ['customer_id','churn_label','monthly_charges','total_charges','contract_type','gender']
    detail_data = df[table_cols].to_dict('records') if len(df) else []

    return (
        f"{total_customers:,}",
        f"{churned_customers:,}",
        f"{churn_rate:.1f}%",
        f"${avg_monthly:,.2f}",
        fig_pie,
        fig_contract,
        detail_data
    )

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8050, debug=True)
