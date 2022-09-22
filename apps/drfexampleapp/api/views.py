# Django rest
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Own app
from ..models import Animals
from .serializers import AnimalSerializer

# Create your views here.

class AnimalListCreateAPI(generics.ListCreateAPIView):
    """Generic class-based view that lists all animals.
        and allows user to create new animals.
        
    To get all animals just use GET.
    To Create a new animal use POST and send its info.

    """
    queryset = Animals.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (IsAuthenticated,)
    
class AnimalDetails(generics.RetrieveUpdateDestroyAPIView):
    """Generic class-based view that retrieves, updates or deletes a animal.
    
        To get a single animal, just send the id and use the get method.
        To update an animal, send the id and the new data and use the put method.
        To delete an animal, send the id and use the delete method.
    """
    queryset = Animals.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (IsAuthenticated,)
    
    # If you want to modify delete method
    def delete(self, request, *args, **kwargs):
        # Do something before delete
        return super(AnimalDetails, self).delete(request, *args, **kwargs)
    
    
    # If you want to modify update method
    # I'm not sure if it is def update or def put
    def put(self, request, *args, **kwargs):
        # Do something before update
        return super(AnimalDetails, self).update(request, *args, **kwargs)
    
    
    # If you want to modify retrieve method
    def get(self, request, *args, **kwargs):
        # Do something before retrieve
        return super(AnimalDetails, self).get(request, *args, **kwargs)
