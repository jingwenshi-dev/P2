from userdata.models import *
from recipes.serializers import *
from accounts.serializers import *


class RatingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'recipe', 'score']
        extra_kwargs = {
            'score': {'required': True},
        }

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)
        score = validated_data['score']

        rating = Rating.objects.create(user=current_user, recipe=recipe, score=score)

        return rating

    def update(self, instance, validated_data):
        instance.score = validated_data["score"]
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'recipe', 'message']
        extra_kwargs = {
            'message': {'required': True}
        }

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)
        message = validated_data['message']

        comment = Comment.objects.create(user=current_user, recipe=recipe, message=message)

        return comment

    def update(self, instance, validated_data):
        instance.comment = validated_data['comment']
        instance.save()
        return instance


class LikedRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = pass