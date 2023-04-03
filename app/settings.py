from pydantic import BaseSettings


class Settings(BaseSettings):
    storage_account_name: str = "tvstorageaccount81382"
    storage_account_auth: str = (
        "3Frsoxc2mRK4d6EKHjtN8cOKSHZfCCPPTprC0rVez9MR/QNHrZH6WUHfVXjuhYsQT521chAf+76UOqu5uy7YnA=="
    )

    source_storage_container: str = "media"
    destination_storage_container: str = "backups"

    destination_prefix: str = source_storage_container + "/"


settings = Settings()
