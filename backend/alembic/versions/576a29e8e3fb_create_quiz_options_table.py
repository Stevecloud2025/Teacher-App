"""create quiz options table

Revision ID: 576a29e8e3fb
Revises: 6569b6bdbfb9
Create Date: 2026-09-10 00:06:08.456963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '576a29e8e3fb'
down_revision: Union[str, Sequence[str], None] = '6569b6bdbfb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'quiz_options',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('option_text', sa.String(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['question_id'],
            ['questions.id'],
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_quiz_options_id'),
        'quiz_options',
        ['id'],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f('ix_quiz_options_id'),
        table_name='quiz_options'
    )

    op.drop_table('quiz_options')