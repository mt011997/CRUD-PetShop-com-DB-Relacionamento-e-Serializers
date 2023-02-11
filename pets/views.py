from rest_framework.views import APIView, Response, Request, status
from .models import Pet
from groups.models import Group
from traits.models import Trait
from .serializer import PetSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class PetsView(APIView, PageNumberPagination):
    def get(self, request: Request):
        traits = request.query_params.get("trait")

        if traits:
            pets = Pet.objects.filter(traits__name=traits)
        else:
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

        pet_obj = Pet.objects.create(**serializer.validated_data, group=group_obj)

        for trait in trait_data:
            trait_obj = Trait.objects.filter(name__iexact=trait["name"]).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait)

            pet_obj.traits.add(trait_obj)

        serializer = PetSerializer(pet_obj)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetsDetailView(APIView):
    def get(self, request: Request, pet_id=int):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return Response(serializer.data)

    def patch(self, request, pet_id):
        pet: Pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.pop("group", None)
        traits = serializer.validated_data.pop("traits", None)

        if group:
            try:
                group_obj = Group.objects.get(
                    scientific_name__iexact=group["scientific_name"]
                )
                pet.group = group_obj
            except Group.DoesNotExist:
                new_group = Group.objects.create(**group)
                pet.group = new_group

        if traits:
            traits_list = []
            for trait_obj in traits:
                trait = Trait.objects.filter(name__iexact=trait_obj["name"]).first()
                if trait:
                    traits_list.append(trait)
                else:
                    new_trait = Trait.objects.create(**trait_obj)
                    traits_list.append(new_trait)

            pet.traits.set(traits_list)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()

        serializer = PetSerializer(pet)
        return Response(serializer.data, 200)

    def delete(self, request: Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
