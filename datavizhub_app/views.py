from django.http import JsonResponse
from .models import DataFile
import pandas as pd
import matplotlib.pyplot as plt
from django.views.decorators.csrf import csrf_exempt
import os  # For dynamic folder creation

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            try:
                # Read CSV file
                data = pd.read_csv(file)

                # Data cleaning
                data_cleaned = data.dropna().drop_duplicates()

                # Create 'static' folder if missing
                output_dir = 'static'
                os.makedirs(output_dir, exist_ok=True)

                # Visualization
                plt.figure(figsize=(8, 5))
                data_cleaned.groupby('Month')['Sales'].sum().plot(kind='bar')  # Fixed Typo
                plt.title('Monthly Sales Performance')
                plt.savefig(os.path.join(output_dir, 'sales_chart.png'))

                return JsonResponse({'message': 'File uploaded and visualization created successfully'})
            except Exception as e:
                return JsonResponse({'error': f'Unexpected error: {str(e)}'})
        return JsonResponse({'error': 'No file uploaded'})
    return JsonResponse({'error': 'Invalid request method'})


from django.shortcuts import render

def display_chart(request):
    return render(request, 'visualization.html')
