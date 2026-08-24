import sqlalchemy as sa

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("display_name", sa.String(120), nullable=False),
        sa.Column(
            "role",
            sa.Enum("author", "admin", name="author_role"),
            nullable=False,
            server_default="author",
        ),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_authors_email", "authors", ["email"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_authors_email", table_name="authors")
    op.drop_table("authors")
    sa.Enum(name="author_role").drop(op.get_bind())
