# disease_detection/views.py
from rest_framework.decorators import api_view  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from .serializers import DiseasePredictionSerializer
#from .services import fetch_weather_data, scrape_germini_data  # Import weather and scraping services
from .ml_utils import predict_leaf_disease  # Import image prediction function

@api_view(['POST'])
def predict_disease(request):
    serializer = DiseasePredictionSerializer(data=request.data)
    
    if serializer.is_valid():
        # 1. Extract Image and make disease prediction
        image = serializer.validated_data['image']
        result = predict_leaf_disease(image)  # Get prediction result (a dictionary)
        
        # Extract all relevant information from the result
        disease = result.get('disease')
        confidence = result.get('confidence')
        cause = result.get('cause')
        treatment = result.get('treatment')
        medicine = result.get('medicine', [])

        # 2. Get device location (latitude and longitude)
        lat = request.data.get('lat')
        lon = request.data.get('lon')
        
        # Optional: Uncomment if location is required
        # if not lat or not lon:
        #     return Response({'error': 'Location data (latitude and longitude) is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. Fetch weather data for the last 3 months using device location
        # weather_data = fetch_weather_data(lat, lon)
        
        # 4. Scrape Germini for more information on the predicted disease
        # additional_info = scrape_germini_data(disease)

        # 5. Check if confidence is less than 70%
        if confidence < 0.7:
            return Response({
                'message': 'Confidence is low. Redirecting to an expert.',
                'confidence': confidence,
                'prediction': disease,
                'cause': cause,
                'treatment': treatment,
                'medicine': medicine,
                # 'redirect_to_expert': True,
                # 'weather_data': weather_data,
                # 'additional_info': additional_info
            })
        
        # 6. Return the prediction result with full information
        return Response({
            'disease': disease,
            'cause': cause,
            'treatment': treatment,
            'medicine': medicine,
            'confidence': confidence,
            # 'weather_data': weather_data,
            # 'additional_info': additional_info
        })
    
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
