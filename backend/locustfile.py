import os
import random

from locust import HttpUser, task, between

API = "/api"


def _get_resources(client, path: str, name: str):
    with client.get(path, name=name, catch_response=True) as response:
        if response.status_code != 200:
            response.failure(f"HTTP {response.status_code}")
        else:
            response.success()


class AnonymousUser(HttpUser):
    wait_time = between(0.5, 2.0)

    @task(weight=5)
    def list_recipes(self):
        _get_resources(self.client, f"{API}/recipes/", f"{API}/recipes/ [list]")

    @task(weight=3)
    def list_ingredients(self):
        _get_resources(
            self.client, f"{API}/ingredients/", f"{API}/ingredients/ [list]"
        )

    @task(weight=2)
    def list_users(self):
        _get_resources(self.client, f"{API}/users/", f"{API}/users/ [list]")

    @task(weight=2)
    def list_recipes_paginated(self):
        page = random.randint(1, 3)
        with self.client.get(
            f"{API}/recipes/?page={page}",
            name=f"{API}/recipes/ [page]",
            catch_response=True,
        ) as response:
            if response.status_code in (200, 404):
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(weight=1)
    def get_recipe_detail(self):
        pk = random.randint(1, 200)
        with self.client.get(
            f"{API}/recipes/{pk}/",
            name=f"{API}/recipes/[id]/",
            catch_response=True,
        ) as response:
            if response.status_code == 404:
                response.success()
            elif response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
            else:
                response.success()


class AuthenticatedUser(HttpUser):
    wait_time = between(0.5, 2.5)

    def on_start(self):
        email = os.getenv("LOCUST_TEST_EMAIL", "test@example.com")
        password = os.getenv("LOCUST_TEST_PASSWORD", "testpass123")
        with self.client.post(
            f"{API}/auth/token/login/",
            data={"email": email, "password": password},
            name=f"{API}/auth/token/login/",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Login failed: {response.status_code}")
                return
            token = response.json().get("auth_token")
            if token:
                self.client.headers["Authorization"] = f"Token {token}"
            else:
                response.failure("No auth_token in response")

    @task(weight=4)
    def list_recipes(self):
        _get_resources(
            self.client, f"{API}/recipes/", f"{API}/recipes/ [auth list]"
        )

    @task(weight=2)
    def get_recipe_detail(self):
        pk = random.randint(1, 200)
        with self.client.get(
            f"{API}/recipes/{pk}/",
            name=f"{API}/recipes/[id]/ [auth]",
            catch_response=True,
        ) as response:
            if response.status_code in (200, 404):
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(weight=2)
    def list_ingredients(self):
        _get_resources(
            self.client, f"{API}/ingredients/", f"{API}/ingredients/ [auth]"
        )

    @task(weight=1)
    def list_users(self):
        _get_resources(self.client, f"{API}/users/", f"{API}/users/ [auth]")

    @task(weight=1)
    def subscriptions(self):
        _get_resources(
            self.client,
            f"{API}/users/subscriptions/",
            f"{API}/users/subscriptions/",
        )
