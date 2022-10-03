from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.test import TestCase
from ..serializers import GetUsersCats
from ..models import Categories, SpentModel, UserFromTg


class TelegramApiTest(APITestCase):
    def test_cats(self):
        key="hflwahdfuhfa"
        user = User.objects.create(username='TestUser'+key, password='password123')
        usertg = UserFromTg.objects.create(user=user, tguserid='123123')
        Categories.objects.create(title='Test'+key, user=user)
        Categories.objects.create(title='1Test'+key, user=user)
        resp = self.client.get('/api/v1/getuserscats/', data={'usertgid': '123123'})
        serializer = GetUsersCats(Categories.objects.filter(user=user), many=True)
        self.assertEquals(resp.data, serializer.data)


class TestSerializer(TestCase):
    def test_ser(self):
        key = 'ewfkjawlef'
        user = User.objects.create(username='TestUser'+key, password='password123')
        usertg = UserFromTg.objects.create(user=user, tguserid='123123')
        cat1 = Categories.objects.create(title='Test'+key, user=user)
        cat2 = Categories.objects.create(title='Test'+key, user=user)
        list = [cat1,cat2]
        serializer = GetUsersCats(list, many=True)
        expectation = [{'title':cat1.title, 'pk':cat1.pk },{'title':cat2.title, 'pk':cat2.pk}]
        self.assertEquals(serializer.data, expectation)


