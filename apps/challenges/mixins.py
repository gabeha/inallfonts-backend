"""
This file was initially created to hold a mixin that would help with
serializing and deserializing tags for models that use django-taggit's
TaggableManager. However, the mixin was never used in the project because
django-taggit provides it out of the box, so it was commented out. The 
mixin is provided below for reference.
"""


# class TaggableSerializerMixin:
#     """
#     A mixin that expects:
#     1. A 'tags' field in the serializer's data (list of strings).
#     2. A model with a TaggableManager named 'tags'.

#     This mixin overrides create() and update() to handle
#     assigning tags properly.
#     """

#     def create(self, validated_data):
#         tags = validated_data.pop('tags', [])
#         instance = super().create(validated_data)
#         # If tags were supplied, add them to the TaggableManager
#         if tags:
#             # `instance.tags` is a TaggableManager provided by django-taggit
#             instance.tags.add(*tags)
#         return instance

#     def update(self, instance, validated_data):
#         tags = validated_data.pop('tags', None)
#         instance = super().update(instance, validated_data)
#         # If 'tags' is not None (meaning the payload included the key),
#         # set the tags to what's provided (possibly an empty list).
#         if tags is not None:
#             instance.tags.set(*tags)
#         return instance
