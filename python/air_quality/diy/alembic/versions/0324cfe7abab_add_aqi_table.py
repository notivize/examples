"""Add aqi table

Revision ID: 0324cfe7abab
Revises: 9e95673f2c46
Create Date: 2021-03-05 17:23:53.566864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0324cfe7abab'
down_revision = '9e95673f2c46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aqi_values',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_aqi_values_id'), 'aqi_values', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_aqi_values_id'), table_name='aqi_values')
    op.drop_table('aqi_values')
    # ### end Alembic commands ###
