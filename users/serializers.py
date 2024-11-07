from rest_framework import serializers

from users.models import CommonUser, Customer


class CommonUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CommonUser
        fields = ("id", "email", "first_name", "last_name", "password")
        read_only_fields = ("id",)

        lookup_field = "id"
        extra_kwargs = {
            "url": {
                "lookup_field": "id"
            }
        }


class CustomerSerializer(serializers.ModelSerializer):
    user = CommonUserSerializer()
    telephone_number = serializers.CharField()

    class Meta:
        model = Customer
        fields = ('user', 'telephone_number')

        lookup_field = "id"
        extra_kwargs = {
            "url": {
                "lookup_field": "id"
            }
        }
        read_only_fields = ("id",)

    def create(self, validated_data) -> (Customer, CommonUser):
        """
        Overrode 'create' method specifically for the 'customer' field with nested serializer.
        """

        CommonUser_data = validated_data.pop('user')
        NewCommonUser = CommonUser(**CommonUser_data)
        NewCommonUser.set_password(CommonUser_data['password'])
        NewCommonUser.save()
        NewCustomer = Customer.objects.create(user=NewCommonUser, **validated_data)
        return NewCustomer
