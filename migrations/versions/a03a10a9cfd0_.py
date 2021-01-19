"""empty message

Revision ID: a03a10a9cfd0
Revises: 8d8b6f76e172
Create Date: 2020-06-22 16:47:21.539751

"""
#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a03a10a9cfd0'
down_revision = '8d8b6f76e172'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expression_mouse', sa.Column('e10_5', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('e11_5', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('e12_5', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('e13_5', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('human', sa.String(length=255), nullable=True))
    op.add_column('expression_mouse', sa.Column('p12_a', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('p12_b', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('p20_a', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('p20_b', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('p42_a', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('p42_b', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('p52_a', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('p52_b', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('p8_a', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('p8_b', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('web1_e10_5__12_5', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('web2_e11_5__13_5', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('web_p10_11_12_a', sa.Float(), nullable=True))
    op.add_column('expression_mouse', sa.Column('web_p10_11_12_b', sa.Float(), nullable=True))
    op.drop_index('ix_expression_mouse_gene', table_name='expression_mouse')
    op.drop_column('expression_mouse', 'lens3')
    op.drop_column('expression_mouse', 'homologous_gene')
    op.drop_column('expression_mouse', 'lens7')
    op.drop_column('expression_mouse', 'lens4')
    op.drop_column('expression_mouse', 'lens1')
    op.drop_column('expression_mouse', 'lens8')
    op.drop_column('expression_mouse', 'lens6')
    op.drop_column('expression_mouse', 'lens5')
    op.drop_column('expression_mouse', 'lens2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expression_mouse', sa.Column('lens2', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('expression_mouse', sa.Column('lens5', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('expression_mouse', sa.Column('lens6', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('expression_mouse', sa.Column('lens8', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('expression_mouse', sa.Column('lens1', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('expression_mouse', sa.Column('lens4', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('expression_mouse', sa.Column('lens7', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('expression_mouse', sa.Column('homologous_gene', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.add_column('expression_mouse', sa.Column('lens3', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.create_index('ix_expression_mouse_gene', 'expression_mouse', ['gene'], unique=False)
    op.drop_column('expression_mouse', 'web_p10_11_12_b')
    op.drop_column('expression_mouse', 'web_p10_11_12_a')
    op.drop_column('expression_mouse', 'web2_e11_5__13_5')
    op.drop_column('expression_mouse', 'web1_e10_5__12_5')
    op.drop_column('expression_mouse', 'p8_b')
    op.drop_column('expression_mouse', 'p8_a')
    op.drop_column('expression_mouse', 'p52_b')
    op.drop_column('expression_mouse', 'p52_a')
    op.drop_column('expression_mouse', 'p42_b')
    op.drop_column('expression_mouse', 'p42_a')
    op.drop_column('expression_mouse', 'p20_b')
    op.drop_column('expression_mouse', 'p20_a')
    op.drop_column('expression_mouse', 'p12_b')
    op.drop_column('expression_mouse', 'p12_a')
    op.drop_column('expression_mouse', 'human')
    op.drop_column('expression_mouse', 'e13_5')
    op.drop_column('expression_mouse', 'e12_5')
    op.drop_column('expression_mouse', 'e11_5')
    op.drop_column('expression_mouse', 'e10_5')
    # ### end Alembic commands ###
