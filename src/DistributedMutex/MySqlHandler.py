import mysql.connector
from FetchWeather import fetch_weather


class MySQLHandler:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    async def worker_task(self):
        """Đọc dữ liệu từ MySQL."""
        print(f" I am a follower. Fetching data from MySQL:")
        self.cursor.execute("SELECT city, temperature, humidity, description FROM weather ORDER BY timestamp DESC LIMIT 5")
        rows = self.cursor.fetchall()

        for row in rows:
            print(f"    City: {row[0]}, temperature: {row[1]}, Humidity: {row[2]}, Description: {row[3]}")

    async def leader_task(self):
        print("I am the leader. Inserting data into MySQL:")
        CITIES = ["Hanoi", "Tokyo", "New York", "London", "Paris"]
        for city in CITIES:
            self.save_weather_data(city)


    def save_weather_data(self, city: str):
        weatherData = fetch_weather(city)
        # Insert dữ liệu vào database
        self.cursor.execute(
            "INSERT INTO weather (city, temperature, humidity, description) VALUES (%s, %s, %s, %s)",
            (weatherData["city"], weatherData["temperature"], weatherData["humidity"], weatherData["description"])
        )
        self.connection.commit()
        print(f"Inserted: City: {weatherData['city']}, temperature: {weatherData['temperature']}, humidity: {weatherData['humidity']}, description: {weatherData['description']}")