from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np
from .models import Business
from .serializers import BusinessSerializer
import threading
from django.db import connection
import time
import pandas as pd
from io import BytesIO
import psycopg2
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
import json
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import random
from rest_framework.decorators import api_view
import mysql.connector
import os 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import status
import openai
from openai import OpenAI
OpenAI.api_key ="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"
OPENAI_API_KEY="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"

OpenAI.api_key = os.getenv('OPENAI_API_KEY') 
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY') 
openai.api_key = os.getenv('OPENAI_API_KEY')  

client = OpenAI(api_key="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")
# Authentication Views
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "username": user.username,
                        "email": user.email
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


def generate_sql(natural_language_query, table_description):
    """
    Generates an SQL query from natural language using OpenAI.

    Args:
        natural_language_query: The natural language query string.
        table_description: Description of the table schema.

    Returns:
        A valid SQL query string or None if an error occurs.
    """
    try:
        prompt = f"""
        You are an AI SQL query generator. 
        Given the following table schema:
        {table_description}
        
        Generate a SQL query to answer the following question:
        "{natural_language_query}"
        
        Important rules:
        - Return only the SQL query. Do not add any explanation, preface, or natural language response.
        - The query must be a valid SQL SELECT statement.
        - Use standard SQL syntax compatible with PostgreSQL.
        - remove sql before the query i need result with the first word select 
        """

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You generate PostgreSQL SQL queries based on user questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        sql_query = response.choices[0].message.content.strip()
        print(f"Generated SQL: {sql_query}")


        # Ensure response is a valid SQL SELECT statement
        if not sql_query.lower().startswith("select"):
            raise ValueError(f"Invalid SQL generated: {sql_query}")

        return sql_query

    except Exception as e:
        print(f"Error generating SQL: {e}")
        return None
def determine_graph_type(columns, results):
    """
    Determines the appropriate graph type based on the SQL results.
    - If there are two columns, use a **bar or pie chart** (if the second column is numeric).
    - If there are multiple numeric columns, use a **line or scatter plot**.
    """
    print(columns)
    print(results)
    print(len(columns))
    if len(columns) == 2 and all(isinstance(row[1], (int, float)) for row in results):
        return "bar"  # Suitable for category vs. value
    elif len(columns) > 2:
        return "line"  # Time-series or multi-variable trends
    return None  # No suitable graph

@api_view(["POST"])
def execute_query(request):
    try:
        # Get query from the request
        query = request.data.get("query", "")
        
        # Assuming table_description is required, pass it when calling generate_sql
        table_description = "business"  # Replace with appropriate description of the table
        
        # Generate the SQL query
        generated_query = generate_sql(query, table_description)
        
        # If no valid SQL is generated, return an error
        if not generated_query:
            return Response({"error": "Invalid SQL query generated."}, status=400)
        
        # Ensure SQL query starts with 'SELECT' (you may want to enforce this based on your use case)
        if not generated_query.lower().startswith("select"):
            return Response({"error": "Generated SQL query must be a SELECT statement."}, status=400)
        
        # Debug: Print the generated query for verification
        print("Generated SQL:", generated_query)

        # Execute the query on your PostgreSQL database (use appropriate db cursor)
        with connection.cursor() as cursor:
            cursor.execute(generated_query)
            columns = [col[0] for col in cursor.description]  # Extract column names
            results = cursor.fetchall()
        graph_type = determine_graph_type(columns, results)
        print(graph_type)
        
        # Return the results as a JSON response
        return JsonResponse({"columns": columns, "results": results, "graph_type": graph_type}, safe=False)
    
    except Exception as e:
        # Log the error to your logging system
        print(f"Error executing SQL: {e}")
        return Response({"error": f"An error occurred while executing the query: {str(e)}"}, status=500)

# Global variables for script control
script_running = False
script_thread = None

# Sample data
names = ["Company A", "Company B", "Company C", "Company D", "Company E"]
countries = ["USA", "Canada", "Germany", "India", "Australia"]

# Function to generate random business data
def generate_data():
    data = []
    for i in range(5):
        name = names[i]
        revenue = round(random.uniform(1000, 10000), 2)  # Random revenue
        profit = round(random.uniform(100, 5000), 2)  # Random profit
        employees = random.randint(10, 500)  # Integer number of employees
        country = random.choice(countries)
        data.append((name, revenue, profit, employees, country))
    return data

# Function to insert data into the 'business' table
def insert_data(conn, data):
    try:
        cur = conn.cursor()
        query = """
            INSERT INTO business (name, revenue, profit, employees, country) 
            VALUES (%s, %s, %s, %s, %s);
        """
        cur.executemany(query, data)  # Insert multiple rows
        conn.commit()  # Commit after inserting data
        print("Inserted data successfully!")
        cur.close()
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()  # Rollback if there's an error

# Function to run the script
def run_script():
    global script_running
    try:
        conn = mysql.connector.connect(
            database="postgres",
            user="sowji",
            password="Sairam#123",
            host="etlsql.mysql.database.azure.com",
            port="3306"
           
        )
        print("Connected to mysql successfully!")

        while script_running:
            data = generate_data()
            insert_data(conn, data)
            for row in data:
                print(row)
            time.sleep(20)

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()
            print("Database connection closed.")
@api_view(['GET', 'POST'])
def business_list_create(request):
    if request.method == 'GET':
        businesses = Business.objects.all()
        serializer = BusinessSerializer(businesses, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
def business_update_delete(request, pk):
    try:
        business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'PUT':
        serializer = BusinessSerializer(business, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        business.delete()
        return Response({'message': 'Deleted successfully'}, status=204)

# View to start the script
class StartScript(APIView):
    def post(self, request):
        global script_running, script_thread
        if not script_running:
            script_running = True
            script_thread = threading.Thread(target=run_script)
            script_thread.start()
            return Response({"status": "Script started"}, status=status.HTTP_200_OK)
        return Response({"status": "Script is already running"}, status=status.HTTP_200_OK)
# View to stop the script
class StopScript(APIView):
    def post(self, request):
        global script_running, script_thread
        if script_running:
            script_running = False
            script_thread.join()
            return Response({"status": "Script stopped"}, status=status.HTTP_200_OK)
        return Response({"status": "Script is not running"}, status=status.HTTP_200_OK)

#class UploadBusinessExcel(APIView):
   # def post(self, request):
    #    if 'office' not in request.FILES:
     #       return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

      #  excel_file = request.FILES['office']
       # df = pd.read_excel(excel_file)

        #for _, row in df.iterrows():
         #   Business.objects.create(
          #      name=row.get('name', ''),
           #     revenue=row.get('revenue', 0),
            #    profit=row.get('profit', 0),
             #   employees=row.get('employees', 0),
              #  country=row.get('country', ''),
            #)

        #return Response({"message": "Business data uploaded"}, status=status.HTTP_201_CREATED)
class BusinessCreateView(APIView):
    def post(self, request):
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UploadBusinessExcel(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES['file']

        try:
            df = pd.read_excel(excel_file)  # Read Excel file
            
            for _, row in df.iterrows():
                Business.objects.create(
                    name=row['name'],
                    revenue=row['revenue'],
                    profit=row['profit'],
                    employees=row['employees'],
                    country=row['country']
                )

            return Response({"message": "Business data uploaded successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusinessStatistics(APIView):
    def get(self, request):
        business_data = Business.objects.values_list('revenue', 'profit', 'employees')

        if not business_data:
            return Response({"error": "No business data available"}, status=status.HTTP_404_NOT_FOUND)

        np_data = np.array(business_data)

        stats = {
            'mean': np.mean(np_data, axis=1).tolist(),
            'std_dev': np.std(np_data, axis=1).tolist(),
            'min': np.min(np_data, axis=1).tolist(),
        }

        return Response(stats, status=status.HTTP_200_OK)
class BusinessAnalytics(APIView):
    def get(self, request):
        businesses = Business.objects.values_list('revenue', 'profit', 'employees')

        if not businesses:
            return Response({"error": "No data available"}, status=status.HTTP_404_NOT_FOUND)

        np_data = np.array(businesses)

        stats = {
            'mean_revenue': np.mean(np_data[:, 0]).tolist(),
            'mean_profit': np.mean(np_data[:, 1]).tolist(),
            'mean_employees': np.mean(np_data[:, 2]).tolist(),
            'max_revenue': np.max(np_data[:, 0]).tolist(),
            'min_revenue': np.min(np_data[:, 0]).tolist(),
        }

        return Response(stats, status=status.HTTP_200_OK)

class Profit(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file)

        data = df[df['profit'] > 20000].to_dict(orient='records')

        return Response({"data": data}, status=status.HTTP_200_OK)

class USA(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file)

        usa_data = df[df['country'] == 'USA'].to_dict(orient='records')

        return Response({"data": usa_data}, status=status.HTTP_200_OK)

class Revenue(APIView):
    def post(self, request):
        #if 'office' not in request.FILES:
           # return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file)

        revenue_data = df[df['revenue'] > 50000].to_dict(orient='records')

        return Response({"data": revenue_data}, status=status.HTTP_200_OK)
# View for Top 5 Countries by Revenue
class TopCountriesByRevenue(APIView):
    def get(self, request):
        businesses = Business.objects.values_list('revenue', 'country')
        df = pd.DataFrame(businesses, columns=["revenue", "country"])

        if df.empty:
            return Response({"error": "No data available"}, status=status.HTTP_404_NOT_FOUND)

        top_countries = df.groupby('country')['revenue'].sum().sort_values(ascending=False).head(5).to_dict()
        return Response(top_countries, status=status.HTTP_200_OK)
# View for Profit by Country
class ProfitByCountry(APIView):
    def get(self, request):
        businesses = Business.objects.values_list('profit', 'country')
        df = pd.DataFrame(businesses, columns=["profit", "country"])

        if df.empty:
            return Response({"error": "No data available"}, status=status.HTTP_404_NOT_FOUND)

        profit_by_country = df.groupby('country')['profit'].mean().to_dict()
        return Response(profit_by_country, status=status.HTTP_200_OK)
# View for Top 5 Businesses by Revenue
class TopBusinessesByRevenue(APIView):
    def get(self, request):
        businesses = Business.objects.values_list('name', 'revenue')
        df = pd.DataFrame(businesses, columns=["name", "revenue"])

        if df.empty:
            return Response({"error": "No data available"}, status=status.HTTP_404_NOT_FOUND)

        top_businesses = df.sort_values('revenue', ascending=False).head(5).to_dict(orient='records')
        return Response(top_businesses, status=status.HTTP_200_OK)
