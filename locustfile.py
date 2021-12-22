from locust import HttpUser, task, between


class ServerTest(HttpUser):
    wait_tie = between(0.25, 2.5)

    @task
    def get_endpoint(self):
        self.client.get('/oslo')
