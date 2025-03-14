from django.http import JsonResponse, FileResponse
from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
from django.views.decorators.csrf import csrf_exempt
import os




@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')

        if file:
            try:
            
                if not os.path.exists('static'):
                    os.makedirs('static')

                
                if file.name.endswith('.csv'):
                    data = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    data = pd.read_excel(file, engine='openpyxl')
                else:
                    return JsonResponse({'error': 'Unsupported file format. Please upload CSV or Excel.'})

               
                if 'Sales' in data.columns:
                    data['Sales'] = data['Sales'].fillna(data['Sales'].mean())

                if 'Region' in data.columns:
                    data.loc[:, 'Region'] = data['Region'].fillna(data['Region'].mode()[0])

                if 'Product Category' in data.columns:
                    data.loc[:, 'Product Category'] = data['Product Category'].fillna(data['Product Category'].mode()[0])

                if 'Discount Applied' in data.columns:
                    data.loc[:, 'Discount Applied'] = data['Discount Applied'].fillna(0)

                if 'Customer Name' in data.columns:
                    data = data.dropna(subset=['Customer Name'])

                if 'Customer Email' in data.columns:
                    data = data.dropna(subset=['Customer Email'])


                
                filtered_data_file = 'static/filtered_sales_data.csv'
                data.to_csv(filtered_data_file, index=False)

                # Visualization Logic
                plt.figure(figsize=(12, 6))
                plt.grid(True)
                data.groupby('Month')['Sales'].sum().plot(kind='line', marker='o', linestyle='-', color='b')
                plt.title('Yearly Sales Performance')
                plt.xlabel('Month')
                plt.ylabel('Total Sales')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig('static/sales_chart.png')

                return JsonResponse({
                    'message': 'File uploaded, filtered, and visualization created successfully',
                    'chart_url': '/static/sales_chart.png',
                    'filtered_data': filtered_data_file
                })

            except Exception as e:
                return JsonResponse({'error': f'Unexpected error: {str(e)}'})

        return JsonResponse({'error': 'No file uploaded'})

    return JsonResponse({'error': 'Invalid request method'})


def dashboard(request):
    data_file = 'static/filtered_sales_data.csv'
    if not os.path.exists(data_file):
        return render(request, 'dashboard.html', {'error': 'No data available'})

    data = pd.read_csv(data_file)

    # Key Metrics
    total_sales = data['Sales'].sum()
    average_sales = round(data['Sales'].mean(), 2)
    top_region = data.groupby('Region')['Sales'].sum().idxmax()
    total_customers = len(data['Customer Name'].unique())

    # Sales Trend Visualization
    plt.figure(figsize=(10, 5))
    data.groupby('Month')['Sales'].sum().plot(kind='line', marker='o', color='blue')
    plt.title('Monthly Sales Trend')
    plt.savefig('static/sales_chart.png')

    # Product Category Chart
    plt.figure(figsize=(6, 6))
    data['Product Category'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title('Product Category Distribution')
    plt.ylabel('')
    plt.savefig('static/category_chart.png')

    context = {
        'total_sales': total_sales,
        'average_sales': average_sales,
        'top_region': top_region,
        'total_customers': total_customers,
        'chart_url': '/static/sales_chart.png',
        'category_chart_url': '/static/category_chart.png',
    }

    return render(request, 'dashboard.html', context)


def apply_filters(request):
    try:
        data = pd.read_csv('static/filtered_sales_data.csv')

        # Filters
        year = request.GET.get('year')
        selected_months = request.GET.get('months').split(',')
        sales_range = request.GET.get('sales_range')
        category = request.GET.get('category')
        region = request.GET.get('region')

        # Filter by Year
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
            data = data[data['Date'].dt.year == int(year)]

        # Filter by Selected Months
        if selected_months:
            data = data[data['Date'].dt.strftime('%B').isin(selected_months)]

        # Filter by Sales Range
        if sales_range == 'lt_2000':
            data = data[data['Sales'] < 2000]
        elif sales_range == '2000_4000':
            data = data[(data['Sales'] >= 2000) & (data['Sales'] <= 4000)]
        elif sales_range == 'gt_4000':
            data = data[data['Sales'] > 4000]

        # Filter by Category
        if category:
            data = data[data['Product Category'].str.contains(category, case=False, na=False)]

        # Filter by Region
        if region:
            data = data[data['Region'].str.contains(region, case=False, na=False)]

        # Correct Month Order
        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        data['Month'] = pd.Categorical(data['Date'].dt.strftime('%B'),
                                       categories=month_order, ordered=True)

        # Visualization Logic
        plt.figure(figsize=(10, 5))
        filtered_data = data.groupby('Month')['Sales'].sum()

        if filtered_data.empty:
            plt.text(0.5, 0.5, 'No Data Found', fontsize=15, ha='center')
        else:
            filtered_data.plot(kind='bar', color='green')

        plt.title(f'Sales Trend for {year} - {", ".join(selected_months)}')
        plt.xlabel('Month')
        plt.ylabel('Total Sales')
        plt.tight_layout()
        plt.savefig('static/filtered_sales_chart.png')

        # Key Metrics
        total_records = len(data)
        total_unique_months = data['Month'].nunique()
        highest_sales = data['Sales'].max() if not data.empty else 0
        lowest_sales = data['Sales'].min() if not data.empty else 0
        median_sales = data['Sales'].median() if not data.empty else 0

        return JsonResponse({
            'chart_url': '/static/filtered_sales_chart.png',
            'total_records': total_records,
            'total_unique_months': total_unique_months,
            'highest_sales': highest_sales,
            'lowest_sales': lowest_sales,
            'median_sales': median_sales
        })
    except Exception as e:
        return JsonResponse({'error': f'Error applying filters: {str(e)}'})






# def apply_filters(request):
#     try:
#         data = pd.read_csv('static/filtered_sales_data.csv')

#         region_filter = request.Get.get('region')
#         min_sales = request.Get.get('min_sales')


        

        
#         plt.figure(figsize=(10, 5))
#         data.groupby('Month')['Sales'].sum().plot(kind='line', marker='o', color='green')
#         plt.title('Filtered Sales Trend')
#         plt.savefig('static/filtered_sales_chart.png')

#         return JsonResponse({'chart_url': '/static/filtered_sales_chart.png'})
#     except Exception as e:
#         return JsonResponse({'error': f'Error applying filters: {str(e)}'})