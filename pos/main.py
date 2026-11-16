from json import JSONDecodeError
from pos.domain.models import DomainError
from pos.infrastructure.container import Container
from pos.result.cli import ConsoleUI


def main():
    try:
        container = Container(data_dir="data")
    except (JSONDecodeError, DomainError, OSError) as error:
        print(f"Не удалось загрузить данные: {error}")
        return
    app = container.create_app()
    console = ConsoleUI(app)
    console.run()

if __name__ == "__main__":
    main()
