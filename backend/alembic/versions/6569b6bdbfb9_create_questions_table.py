"""create questions table

Revision ID: 6569b6bdbfb9
Revises: dcbc104e4d77
Create Date: 2026-09-09 23:11:19.345023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6569b6bdbfb9'
down_revision: Union[str, Sequence[str], None] = 'dcbc104e4d77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ['lesson_id'],
            ['lessons.id']
        ),
        sa.ForeignKeyConstraint(
            ['teacher_id'],
            ['teachers.id']
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_quizzes_id'),
        'quizzes',
        ['id'],
        unique=False
    )

    op.create_table(
        'questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.String(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.Column('correct_answer', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['quiz_id'],
            ['quizzes.id']
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_questions_id'),
        'questions',
        ['id'],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f('ix_questions_id'),
        table_name='questions'
    )

    op.drop_table('questions')

    op.drop_index(
        op.f('ix_quizzes_id'),
        table_name='quizzes'
    )

    op.drop_table('quizzes')