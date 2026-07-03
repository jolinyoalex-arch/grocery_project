from django.test import TestCase
from django.urls import reverse

from .models import Category, Order, OrderItem, Product, User, Vendor


class AuthPagesTests(TestCase):
    def test_login_page_opens(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_register_page_opens(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')


class OrderFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='customer', password='secret123')
        self.category = Category.objects.create(name='Rice')
        self.vendor = Vendor.objects.create(
            user=self.user,
            shop_name='Duka la John',
            address='Dar es Salaam',
        )
        self.product = Product.objects.create(
            vendor=self.vendor,
            category=self.category,
            name='Mchele wa Kyela',
            price='3000.00',
            stock=10,
        )

    def test_compare_prices_page_opens(self):
        response = self.client.get(reverse('compare_prices'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Compare Prices')
        self.assertContains(response, 'Mchele wa Kyela')

    def test_orders_requires_login_redirects_to_login_page(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('orders')}")

    def test_cart_page_opens(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Cart')

    def test_customer_can_add_to_cart_and_checkout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        cart_page = self.client.get(reverse('cart'))
        self.assertContains(cart_page, 'Mchele wa Kyela')

        update_response = self.client.post(reverse('update_cart', args=[self.product.id]), {'quantity': 2})
        self.assertEqual(update_response.status_code, 302)

        remove_response = self.client.get(reverse('remove_from_cart', args=[self.product.id]))
        self.assertEqual(remove_response.status_code, 302)

        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        checkout_response = self.client.post(
            reverse('checkout'),
            {'delivery_address': 'Mbezi Beach'},
        )
        self.assertEqual(checkout_response.status_code, 302)
        self.assertRedirects(checkout_response, reverse('orders'))
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        order = Order.objects.get()
        self.assertEqual(order.items.get().quantity, 1)
        self.assertEqual(order.delivery_address, 'Mbezi Beach')

        orders_page = self.client.get(reverse('orders'))
        self.assertContains(orders_page, 'Mchele wa Kyela')
        self.assertContains(orders_page, 'Pending')
