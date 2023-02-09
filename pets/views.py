from rest_framework.views import APIView, Response, Request, status
from .models import Pet
from groups.models import Group
from traits.models import Trait
from .serializer import PetSerializer
from rest_framework.pagination import PageNumberPagination


class PetsView(APIView, PageNumberPagination):

    def get(self, request: Request):

        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):

        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trait_data = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")

        group_obj = Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).first()

        if not group_obj:
            group_obj = Group.objects.create(**group_data)

        pet_obj = Pet.objects.create(**serializer.validated_data,
                                     group=group_obj)

        for trait in trait_data:
            trait_obj = Trait.objects.filter(
                name__iexact=trait["name"]
            ).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait)

            pet_obj.traits.add(trait_obj)

        serializer = PetSerializer(pet_obj)

        return Response(serializer.data, status.HTTP_201_CREATED)
