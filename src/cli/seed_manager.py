import sys
import typer
from sqlalchemy.exc import SQLAlchemyError
from src.database.real_database import get_db
from src.database.seeders.user_seeder import run_user_seeder

app = typer.Typer(
    name="seeder_manager",
    help="CLI for database seeders management.",
    no_args_is_help=True,
)


@app.command(name="users")
def seed_users(
    count: int = typer.Option(50, "--count", "-c", help="Number of users to seed."),
) -> None:
    """
    Seed users table with mock data.
    """

    typer.echo("[SEEDER] Starting database for users seeder.")

    # Get database session generator object
    db_generator = get_db()
    # Yield database session
    db = next(db_generator)
    try:
        run_user_seeder(db=db, count=count)
    except SQLAlchemyError as e:
        typer.echo(f"[SEEDER] Error while trying to seed users: {e}", file=sys.stderr)
        raise typer.Exit(code=1)
    finally:
        try:
            # Terminate generator lifespan
            next(db_generator)
        except StopIteration:
            pass


@app.command(name="status")
def seed_status() -> None:
    """
    Show seeder status.
    """

    typer.echo("[SEEDER] Seeder manager ready.")


if __name__ == "__main__":
    app()
