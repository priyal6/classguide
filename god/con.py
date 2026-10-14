from dataclasses import dataclass

import httpx

@dataclass
class AppConfig:
    base_url: str = "https://jsonplaceholder.typicode.com"
    timeout: float =5.0

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

        response = self.client.get(
            url,
            timeout=self.config.timeout,
        )

        response.raise_for_status

        return response.json()

def main() -> None:
    config = AppConfig(
        timeout=3.0,
    )

    with httpx.Client() as client:
        user_api = UserAPIClient(
            config=config,
            client=client,
        )

        user = user_api.get_user(1)

        print(user["name"])
        print(user["email"])


if __name__ == "__main__":
    main()