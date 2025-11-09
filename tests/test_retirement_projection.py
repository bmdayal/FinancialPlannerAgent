import json
import math

from financial_planner.app import generate_plots


def compute_expected_final_savings(current_savings, annual_income, savings_rate, annual_return_rate, years):
    annual_savings = annual_income * savings_rate
    final = current_savings
    for _ in range(years):
        final = final * (1 + annual_return_rate) + annual_savings
    return final


def test_retirement_projection_normal_case():
    profile = {
        'age': 30,
        'retirement_age': 65,
        'current_savings': 10000.0,
        'annual_income': 80000.0,
        'children': []
    }

    plots = generate_plots(profile)
    retirement_fig = plots.get('retirement')
    assert retirement_fig is not None, "Retirement figure missing from plots"

    # extract y values from the Plotly JSON structure
    y_values = retirement_fig.get('data', [])[0].get('y', [])
    assert len(y_values) > 0

    years = profile['retirement_age'] - profile['age']
    expected = compute_expected_final_savings(
        current_savings=profile['current_savings'],
        annual_income=profile['annual_income'],
        savings_rate=0.15,
        annual_return_rate=0.06,
        years=years
    )

    # The plot stores the projected savings at each year; compare the final value
    plotted_final = float(y_values[-1])
    assert math.isclose(plotted_final, expected, rel_tol=1e-9, abs_tol=1e-2), (
        f"Plotted final ({plotted_final}) != expected ({expected})"
    )


def test_retirement_projection_zero_current_savings():
    profile = {
        'age': 25,
        'retirement_age': 65,
        'current_savings': 0.0,
        'annual_income': 60000.0,
        'children': []
    }

    plots = generate_plots(profile)
    retirement_fig = plots.get('retirement')
    assert retirement_fig is not None

    y_values = retirement_fig.get('data', [])[0].get('y', [])
    assert len(y_values) > 0

    years = profile['retirement_age'] - profile['age']
    expected = compute_expected_final_savings(
        current_savings=profile['current_savings'],
        annual_income=profile['annual_income'],
        savings_rate=0.15,
        annual_return_rate=0.06,
        years=years
    )

    plotted_final = float(y_values[-1])
    assert math.isclose(plotted_final, expected, rel_tol=1e-9, abs_tol=1e-2)
