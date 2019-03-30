"""empty message

Revision ID: fe178d640aea
Revises: e60d5def54bd
Create Date: 2019-03-03 22:42:58.947398

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fe178d640aea'
down_revision = 'e60d5def54bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('is_read', sa.Boolean(), nullable=True))
    op.add_column('messages', sa.Column('receiver_id', sa.Integer(), nullable=True))
    op.drop_constraint('messages_ibfk_1', 'messages', type_='foreignkey')
    op.create_foreign_key(None, 'messages', 'users', ['receiver_id'], ['id'])
    op.drop_column('messages', 'recipient_id')
    op.add_column('users', sa.Column('is_confirmed', sa.Boolean(), nullable=True))
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('users', 'is_confirmed')
    op.add_column('messages', sa.Column('recipient_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.create_foreign_key('messages_ibfk_1', 'messages', 'users', ['recipient_id'], ['id'])
    op.drop_column('messages', 'receiver_id')
    op.drop_column('messages', 'is_read')
    # ### end Alembic commands ###