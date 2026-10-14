from dataclasses import dataclass
import time

import httpx

@dataclass
class AppConfig:
    base_url: str = "https://jsonplaceholder.typicode.com"
    timeout: float = 3.0
    retries: int = 3
    retry_delay: float = 1.0

class UserAPIClient:
    def __init__(
            self,
            config: AppConfig,
            client: httpx.Client,
    ):
        self.config = config
        self.client = client

    def get_user(self, user_id: int) -> dict:
        url = f"{self.config.base_url}/users/{user_id}"

        for attempt in range(self.config.retries + 1):
            try:
                response = self.client.get(
                    url,
                    timeout=self.config.timeout,
                )

                response.raise_for_status()

                return response.json()

            except (
                httpx.TimeoutException,
                httpx.NetworkError,
            ) as e:
                print(f"Attempt {attempt} failed: {e}")

                if attempt == self.config.retries:
                    raise

            except httpx.HTTPStatusError as e:
                status = e.response.status_code

                if status >=500 and attempt < self.config.retries:
                    print(f"Server error {status}. Retrying in ")
                    time.sleep(self.config.retry_delay)
                    continue

                raise

def main() -> None:
    config = AppConfig(
        timeout=3.0,
        retries=3,
        retry_delay=1.0,
    )

    with httpx.Client() as client:
        api = UserAPIClient(
            config=config,
            client=client,
        )

        user = api.get_user(1)

        print(user["name"])
        print(user["email"])

if __name__ == "__main__":
    main()