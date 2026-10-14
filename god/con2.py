from dataclasses import dataclass

@dataclass
class AppConfig:
    api_url: str = ""
    timeout:float = 5.0
    debug:bool = False


class Logger:
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


class UserService:
    def __init__(
            self,
            config: AppConfig,
            logger: Logger,
    ):
        self.config = config
        self.logger = logger

    def get_user(self, user_id: int) -> str:
        self.logger.log(f"Fetching user {user_id}")

        url = f"{self.config.api_url}/user/{user_id}"

        self.logger.log(f"Request URL: {url}")

        return f"User {user_id}"

def main() -> None:
    config = AppConfig(
        api_url="https://my-api.com",
        timeout=10.0,
    )

    logger = Logger()

    user_service = UserService(
        config=config,
        logger=logger,
    )

    user = user_service.get_user(42)

    print(user)

if __name__ == "__main__":
    main()