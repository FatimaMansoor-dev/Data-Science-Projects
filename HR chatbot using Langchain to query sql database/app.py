from flask import Flask, render_template, request, jsonify
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
from sqlalchemy import create_engine
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities.sql_database import SQLDatabase
import google.generativeai as genai
import seaborn as sns
import io
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Google Generative AI
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# Database configuration
database_uri = os.getenv('DATABASE_URI')
engine = create_engine(database_uri)

# Set up the Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
generate_query = create_sql_query_chain(llm, SQLDatabase.from_uri(database_uri))
execute_query = QuerySQLDataBaseTool(db=SQLDatabase.from_uri(database_uri))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form.get("msg")
    if msg:
        if 'bar' in msg.lower() or 'pie' in msg.lower() or 'line' in msg.lower():
            response = generate_plot(msg)
        else:
            response = generate_response(msg)
        return response
    return jsonify(response="No input provided.")

def generate_response(question):
    """Generate a response based on a question."""
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
        Firstly, clean and make the query 100% syntactically correct and ready to execute, then answer the user question without mentioning any errors in the query.

        Question: {question}
        SQL Query: {clean_query}
        SQL Result: {result}
        Answer: """
    )
    
    rephrase_answer = answer_prompt | llm | StrOutputParser()

    # Generate and clean the query
    query = generate_query.invoke({"question": question})
    if 'SQLQuery:' in query:
        query = query.split('SQLQuery: ')[1]
    clean_query = query.strip().replace("```", "").replace("sql", "").strip()
    print(clean_query)

    # Execute the query and generate the response
    chain = (
        RunnableLambda(lambda inputs: {"clean_query": clean_query, "question": question})
        .assign(result=lambda inputs: execute_query(inputs["clean_query"]))
        | rephrase_answer
    )
    answer = chain.invoke({"question": question})
    return answer

def generate_plot(question):
    """Generate a plot based on a question."""
    try:
        sql_query = generate_query.invoke({"question": question}).split(": ")[-1]
        sql_query = re.sub(r'^```sql\s*|\s*```$', '', sql_query).strip()
        df = pd.read_sql(sql_query, engine)
        
        column1 = df.columns[0]
        column2 = df.columns[1]
        
        img = io.BytesIO()

        if 'bar' in question.lower():
            plt.figure(figsize=(6, 6))
            
            # Plot the bar chart
            bar_plot = sns.barplot(x=column1, y=column2, data=df, palette='Set2')
            
            # Set the title
            plt.title(f'Bar Chart of {column1} vs {column2}', fontsize=14, fontweight='bold')
            
            # Remove the X-axis labels
            plt.gca().set_xticklabels([])
            
            # Add values on top of the bars
            for p in bar_plot.patches:
                bar_plot.annotate(format(p.get_height(), '.1f'), 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                ha='center', va='center', 
                                xytext=(0, 10), textcoords='offset points')

            # Create a list of unique values from column1 for the legend
            unique_values = df[column1].unique()
            
            # Add a legend/key with the unique values
            plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=str(value),
                                        markersize=10, markerfacecolor=sns.color_palette('Set2')[i])
                                for i, value in enumerate(unique_values)],
                    loc='upper right', title=column1)

            # Adjust layout and save
            plt.tight_layout()
            plt.savefig(img, format='png')
            plt.close()

        
        elif 'pie' in question.lower():
            plt.figure(figsize=(5, 5))
            
            # Ensure that there are at least 2 unique values
            if len(df[column2].unique()) < 2:
                raise ValueError("Pie chart requires at least two unique values in the data.")
            
            # Ensure that the lengths of labels and data match
            if len(df[column2]) != len(df[column1]):
                raise ValueError("Length of data and labels must be the same.")
            
            # Create a color palette that matches the number of segments
            colors = sns.color_palette('colorblind', n_colors=len(df[column2]))
            explode = [0.05] * len(df[column2])
            
            # Plot pie chart without labels
            wedges, _, _ = plt.pie(
                df[column2], 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=colors, 
                explode=explode, 
                wedgeprops={'edgecolor': 'black', 'linewidth': 1},
                labels=None  # Do not display labels on pie slices
            )
            
            # Add a title
            plt.title(f'Pie Chart of {column1}', fontsize=14, fontweight='bold')
            
            # Add legend
            plt.legend(
                wedges, 
                df[column1],  # Use the column1 values as legend labels
                title="Categories",
                loc="upper left",  # Position the legend in the upper-left corner
                bbox_to_anchor=(1, 1),  # Anchor the legend box to the upper-right corner of the plot
                frameon=False,  # Remove the frame around the legend if desired
                fontsize='small'  # Adjust font size to fit more labels
            )
            
            # Equal aspect ratio ensures the pie chart is circular
            plt.axis('equal')
            
            # Save and close the plot
            plt.savefig(img, format='png', bbox_inches='tight')  # Ensure the bounding box is tight to include legend
            plt.close()


        elif 'line' in question.lower():
            plt.figure(figsize=(2, 3))
            plt.plot(df[column1], df[column2], marker='o', linestyle='-', color='b')
            plt.title(f'Line Chart of {column1} vs {column2}')
            plt.xticks(rotation=45)
            plt.ylabel(column2)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(img, format='png')
            plt.close()

        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return f'<img src="data:image/png;base64,{plot_url}" />'

    except Exception as e:
        return f"Error generating plot: {e}"

if __name__ == '__main__':
    app.run()
