from flask import Flask, render_template, request, jsonify, session
import plotly
import plotly.graph_objects as go
import numpy as np
import json
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    print("Warning: OPENAI_API_KEY not set in environment variables")

def get_openai_response(messages):
    """Wrapper function for OpenAI API calls with error handling"""
    try:
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set")
            
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content, None
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return None, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input')
def input_form():
    return render_template('input.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    # Extract user data
    user_profile = {
        'age': int(data['age']),
        'current_savings': float(data['current_savings']),
        'annual_income': float(data['annual_income']),
        'retirement_age': int(data['retirement_age']),
        'children': [
            {'age': int(child['age']), 'education_goal': child['education_goal']}
            for child in data['children']
        ]
    }
    
    # Generate visualizations
    plots = generate_plots(user_profile)
    
    # Generate financial health analysis
    analysis = analyze_financial_health(user_profile, plots)
    plots['analysis'] = analysis
    
    return jsonify(plots)

def analyze_financial_health(user_profile, plots):
    """Analyze financial health and provide recommendations."""
    annual_return_rate = 0.06
    savings_rate = 0.15
    annual_savings = user_profile['annual_income'] * savings_rate
    years_to_retirement = user_profile['retirement_age'] - user_profile['age']
    
    # Calculate total monthly obligations
    monthly_retirement = annual_savings / 12
    total_monthly = monthly_retirement
    
    # Education costs analysis
    education_risks = []
    if user_profile['children']:
        college_start_age = 18
        estimated_annual_college_cost = 35000
        college_inflation_rate = 0.05
        
        for child in user_profile['children']:
            years_to_college = college_start_age - child['age']
            future_cost = estimated_annual_college_cost * 4 * (1 + college_inflation_rate) ** years_to_college
            monthly_required = future_cost / (years_to_college * 12) if years_to_college > 0 else future_cost / 12
            total_monthly += monthly_required
            
            if monthly_required > user_profile['annual_income'] / 24:  # If monthly requirement exceeds half of monthly income
                education_risks.append(f"Child age {child['age']}: High monthly savings requirement (${monthly_required:,.2f})")
    
    # Calculate retirement savings projection
    final_savings = user_profile['current_savings']
    for _ in range(years_to_retirement):
        final_savings = final_savings * (1 + annual_return_rate) + annual_savings
    
    # Estimated monthly expenses in retirement (using 80% of current income as baseline)
    monthly_expenses_in_retirement = (user_profile['annual_income'] * 0.8) / 12
    years_of_retirement_covered = final_savings / (monthly_expenses_in_retirement * 12)
    
    # Generate analysis summary
    analysis = {
        'summary': '',
        'risks': [],
        'recommendations': []
    }
    
    # Risk assessment
    if years_of_retirement_covered < 20:
        analysis['risks'].append(f"Your retirement savings may only last {years_of_retirement_covered:.1f} years after retirement")
    
    if total_monthly > user_profile['annual_income'] / 12 * 0.5:
        analysis['risks'].append("Total monthly savings requirement exceeds 50% of your monthly income")
    
    analysis['risks'].extend(education_risks)
    
    # Recommendations
    if years_of_retirement_covered < 20:
        analysis['recommendations'].append(f"Consider increasing your retirement savings rate above the current {savings_rate*100}%")
    
    if user_profile['current_savings'] < user_profile['annual_income']:
        analysis['recommendations'].append("Build an emergency fund of at least 6 months of expenses")
    
    if education_risks:
        analysis['recommendations'].append("Consider starting a 529 college savings plan for each child")
        analysis['recommendations'].append("Research scholarship and financial aid opportunities")
    
    # Overall summary
    risk_level = "LOW" if len(analysis['risks']) == 0 else "MODERATE" if len(analysis['risks']) <= 2 else "HIGH"
    
    analysis['summary'] = f"""Financial Health Assessment: {risk_level} RISK

Retirement Outlook:
- You're saving ${annual_savings:,.2f} annually for retirement
- Projected savings at retirement: ${final_savings:,.2f}
- This could cover approximately {years_of_retirement_covered:.1f} years of retirement

Monthly Savings Requirements:
- Total monthly savings needed: ${total_monthly:,.2f}
- This represents {(total_monthly/(user_profile['annual_income']/12)*100):.1f}% of your monthly income

{"" if not user_profile['children'] else f"Education Planning:\n- You have {len(user_profile['children'])} children to plan for\n- Total education costs will be a significant portion of your savings goals"}"""
    
    return analysis

def generate_plots(user_profile):
    plots = {}
    
    # 1. Retirement Planning Visualization
    current_age = user_profile['age']
    retirement_age = user_profile['retirement_age']
    current_savings = user_profile['current_savings']
    annual_income = user_profile['annual_income']
    
    annual_return_rate = 0.06
    savings_rate = 0.15
    annual_savings = annual_income * savings_rate
    
    years = np.arange(current_age, retirement_age + 1)
    savings = []
    current = current_savings
    
    for _ in range(len(years)):
        savings.append(current)
        current = current * (1 + annual_return_rate) + annual_savings
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=years,
        y=savings,
        mode='lines+markers',
        name='Projected Savings',
        line=dict(color='#00ff00', width=3),
        marker=dict(size=8, symbol='circle')
    ))
    
    fig1.update_layout(
        title='Projected Retirement Savings Growth',
        title_x=0.5,
        xaxis_title='Age',
        yaxis_title='Savings ($)',
        showlegend=True,
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    plots['retirement'] = json.loads(fig1.to_json())
    
    # 2. Education Planning Visualization
    if user_profile['children']:
        children_data = user_profile['children']
        college_start_age = 18
        years_to_college = [(college_start_age - child['age']) for child in children_data]
        estimated_annual_college_cost = 35000
        college_inflation_rate = 0.05
        
        current_costs = [estimated_annual_college_cost * 4] * len(children_data)
        projected_costs = [
            estimated_annual_college_cost * 4 * (1 + college_inflation_rate) ** years 
            for years in years_to_college
        ]
        
        fig2 = go.Figure()
        
        for i, (current, projected) in enumerate(zip(current_costs, projected_costs)):
            fig2.add_trace(go.Bar(
                name=f'Child {i+1} Current',
                x=[f'Child {i+1}'],
                y=[current],
                marker_color='#3366cc'
            ))
            fig2.add_trace(go.Bar(
                name=f'Child {i+1} Projected',
                x=[f'Child {i+1}'],
                y=[projected],
                marker_color='#dc3912'
            ))
        
        fig2.update_layout(
            title='Projected 4-Year College Costs by Child',
            title_x=0.5,
            barmode='group',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        
        plots['education'] = json.loads(fig2.to_json())
        
        # 3. Monthly Savings Requirements
        retirement_monthly = annual_savings / 12
        college_monthly = []
        
        for years in years_to_college:
            future_cost = estimated_annual_college_cost * 4 * (1 + college_inflation_rate) ** years
            monthly_required = future_cost / (years * 12) if years > 0 else future_cost / 12
            college_monthly.append(monthly_required)
        
        goals = ['Retirement'] + [f'Child {i+1} Education' for i in range(len(children_data))]
        monthly_savings = [retirement_monthly] + college_monthly
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=goals,
            y=monthly_savings,
            marker=dict(
                color=monthly_savings,
                colorscale='Viridis',
            ),
            text=[f'${x:,.0f}' for x in monthly_savings],
            textposition='inside',
        ))
        
        fig3.update_layout(
            title='Required Monthly Savings by Financial Goal',
            title_x=0.5,
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        
        plots['monthly'] = json.loads(fig3.to_json())
    
    return plots

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No data received")
            
        user_message = data.get('message', '')
        if not user_message:
            raise ValueError("No message received")
            
        financial_data = data.get('financialData', {})
        
        # Initialize or get chat history
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        # Prepare context from financial data
        context = ""
        if financial_data:
            try:
                # Calculate key financial metrics
                current_age = financial_data.get('age')
                retirement_age = financial_data.get('retirement_age')
                current_savings = float(financial_data.get('current_savings', 0))
                annual_income = float(financial_data.get('annual_income', 0))
                years_to_retirement = retirement_age - current_age
                
                # Investment and savings calculations
                annual_return_rate = 0.06
                savings_rate = 0.15
                annual_savings = annual_income * savings_rate
                monthly_retirement_savings = annual_savings / 12
                
                # Project retirement savings
                final_savings = current_savings
                for _ in range(years_to_retirement):
                    final_savings = final_savings * (1 + annual_return_rate) + annual_savings
                
                # Education planning calculations
                children = financial_data.get('children', [])
                education_costs = []
                college_start_age = 18
                estimated_annual_college_cost = 35000
                college_inflation_rate = 0.05
                
                for child in children:
                    years_to_college = college_start_age - child['age']
                    future_cost = estimated_annual_college_cost * 4 * (1 + college_inflation_rate) ** years_to_college
                    monthly_required = future_cost / (years_to_college * 12) if years_to_college > 0 else future_cost / 12
                    education_costs.append({
                        'age': child['age'],
                        'years_to_college': years_to_college,
                        'total_cost': future_cost,
                        'monthly_savings_needed': monthly_required
                    })
                
                # Monthly expenses in retirement (80% of current income)
                monthly_expenses_in_retirement = (annual_income * 0.8) / 12
                years_of_retirement_covered = final_savings / (monthly_expenses_in_retirement * 12)
                
                context = f"""
                Financial Context:
                Personal Information:
                - Current Age: {current_age}
                - Annual Income: ${annual_income:,.2f}
                - Current Savings: ${current_savings:,.2f}
                - Target Retirement Age: {retirement_age}
                - Years until retirement: {years_to_retirement}
                
                Retirement Planning:
                - Projected retirement savings: ${final_savings:,.2f}
                - Years of retirement covered: {years_of_retirement_covered:.1f}
                - Monthly retirement savings needed: ${monthly_retirement_savings:,.2f}
                - Expected monthly expenses in retirement: ${monthly_expenses_in_retirement:,.2f}
                - Assumed annual return rate: {annual_return_rate*100}%
                - Current savings rate: {savings_rate*100}%
                
                Education Planning:
                - Number of Children: {len(children)}
                {chr(10).join([f'- Child {i+1}: Age {cost["age"]}, Years to college: {cost["years_to_college"]}, Total cost: ${cost["total_cost"]:,.2f}, Monthly savings needed: ${cost["monthly_savings_needed"]:,.2f}' for i, cost in enumerate(education_costs)])}
                
                Risk Assessment:
                - {"HIGH" if years_of_retirement_covered < 20 else "MODERATE" if years_of_retirement_covered < 25 else "LOW"} retirement risk
                - {"HIGH" if monthly_retirement_savings > annual_income/24 else "MODERATE" if monthly_retirement_savings > annual_income/36 else "LOW"} monthly savings burden
                """
            except (TypeError, ValueError) as e:
                print(f"Error formatting financial data: {str(e)}")
                context = "Financial data available but could not be formatted."
        
        # Prepare the conversation for GPT
        messages = [
            {"role": "system", "content": f"""You are an expert financial planning assistant. 
            Use this detailed context about the user's financial situation to provide specific, data-driven advice:
            {context}
            
            Important guidelines:
            1. Reference specific numbers from the context when giving advice
            2. Explain the reasoning behind your recommendations
            3. Consider both retirement and education planning in your answers
            4. Highlight any risks identified in the financial analysis
            5. Provide actionable steps with clear numbers and timeframes
            6. Format all monetary values as $1,234.56
            7. Consider the user's current age, income, and savings rate in your advice
            8. If relevant, discuss both short-term and long-term implications
            9. Provide specific savings targets when applicable
            10. Acknowledge both retirement and education goals in your planning"""},
            *[{"role": msg["role"], "content": msg["content"]} for msg in session['chat_history'][-5:]],
            {"role": "user", "content": user_message}
        ]
        
        # Get response from OpenAI
        assistant_message, error = get_openai_response(messages)
        
        if error:
            print(f"OpenAI API Error: {error}")
            raise Exception(error)
            
        if not assistant_message:
            raise Exception("No response received from OpenAI")
        
        # Update chat history
        session['chat_history'].extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_message}
        ])
        
        return jsonify({
            "response": assistant_message,
            "success": True
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"Chat Error: {error_msg}")
        return jsonify({
            "response": f"I apologize, but I encountered an error: {error_msg}. Please make sure you have set up your OpenAI API key and try again.",
            "success": False,
            "error": error_msg
        })

if __name__ == '__main__':
    app.run(debug=True)