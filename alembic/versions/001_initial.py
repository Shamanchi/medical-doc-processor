"""Initial migration - create documents and entities tables

Revision ID: 001
Revises: 
Create Date: 2026-09-20

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('content_type', sa.String(100), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, default='pending'),
        sa.Column('metadata', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_documents_status', 'documents', ['status'])
    op.create_index('ix_documents_created_at', 'documents', ['created_at'])

    op.create_table(
        'entities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('normalized_code', sa.String(50), nullable=True),
        sa.Column('normalized_system', sa.String(50), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('start_char', sa.Integer(), nullable=True),
        sa.Column('end_char', sa.Integer(), nullable=True),
        sa.Column('attributes', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_entities_document_id', 'entities', ['document_id'])
    op.create_index('ix_entities_type', 'entities', ['entity_type'])
    op.create_index('ix_entities_normalized_code', 'entities', ['normalized_code'])


def downgrade() -> None:
    op.drop_index('ix_entities_normalized_code', table_name='entities')
    op.drop_index('ix_entities_type', table_name='entities')
    op.drop_index('ix_entities_document_id', table_name='entities')
    op.drop_table('entities')
    op.drop_index('ix_documents_created_at', table_name='documents')
    op.drop_index('ix_documents_status', table_name='documents')
    op.drop_table('documents')