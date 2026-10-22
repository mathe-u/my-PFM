from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import CustomUser

class UserAuthAndProfileTests(APITestCase):
    def setUp(self):
        # URLs nomeadas definidas no seu user_urls.py
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.me_url = reverse('me')
        
        # Dados de usuário padrão para testes
        self.user_data = {
            'name': 'João Silva',
            'email': 'joao@example.com',
            'password': 'PasswordSegura123!'
        }
        
        # Usuário pré-cadastrado para testes de login e perfil
        self.user = CustomUser.objects.create_user(
            username='joao@example.com',
            name='João Silva',
            email='joao@example.com',
            password='PasswordSegura123!'
        )

    def test_register_new_user_success(self):
        """Testa o cadastro bem-sucedido de um novo usuário via RegisterView"""
        data = {
            'name': 'Maria Souza',
            'email': 'maria@example.com',
            'password': 'PasswordSegura123!'
        }
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='maria@example.com').exists())

    def test_login_user_success(self):
        """Testa o login bem-sucedido retornando tokens JWT e dados do usuário"""
        data = {
            'email': 'joao@example.com',
            'password': 'PasswordSegura123!'
        }
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], self.user.email)

    def test_login_user_invalid_credentials(self):
        """Testa falha de login com senha incorreta"""
        data = {
            'email': 'joao@example.com',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_me_authenticated(self):
        """Testa a recuperação de dados do próprio usuário logado (UserMeView)"""
        # Força a autenticação do usuário no cliente de teste
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_user_me_unauthenticated(self):
        """Testa se rota protegida bloqueia usuários não autenticados"""
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)