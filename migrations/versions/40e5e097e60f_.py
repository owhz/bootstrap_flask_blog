"""empty message

Revision ID: 40e5e097e60f
Revises: 9800c8fa681d
Create Date: 2019-01-24 18:46:12.410388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40e5e097e60f'
down_revision = '9800c8fa681d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###
