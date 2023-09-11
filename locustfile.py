from locust import HttpUser, between, task
import time

class QueryApp(HttpUser):
    wait_time = between(1,5)
    num = 0

    @task(3)
    def health_check(self):
        self.client.get('/health')
        self.client.get('/reviews')
        self.client.get('/businesses')
    
    @task
    def on_start(self):
        self.client.post('/users', json={
            "fullname": f"Locust Onyang{self.num}",
            "email": f"locust{self.num}@gmail.com",
            "tel_number": f"07107{self.num}9442",
            "picture":"https://images.pexels.com/photos/17404044/pexels-photo-17404044/free-photo-of-man-taking-picture-on-cellphone-in-green-forest.jpeg"
        })
        self.num+=1