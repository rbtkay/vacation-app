"""create vacations for employees

Revision ID: d6eb6a4f967c
Revises: 27bf2aa3b8c7
Create Date: 2024-12-21 19:42:37.633819

"""
from alembic import op
import sqlalchemy as sa
from app.model.base import CustomUUID


# revision identifiers, used by Alembic.
revision = 'd6eb6a4f967c'
down_revision = '27bf2aa3b8c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vacation',
    sa.Column('start_date', sa.DATE(), nullable=False),
    sa.Column('end_date', sa.DATE(), nullable=False),
    sa.Column('employee_id', CustomUUID(), nullable=False),
    sa.Column('id', CustomUUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vacation_id'), 'vacation', ['id'], unique=False)
    op.add_column('employee', sa.Column('created_at', sa.DateTime(timezone=True), nullable=False))
    op.add_column('employee', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employee', 'updated_at')
    op.drop_column('employee', 'created_at')
    op.drop_index(op.f('ix_vacation_id'), table_name='vacation')
    op.drop_table('vacation')
    # ### end Alembic commands ###
