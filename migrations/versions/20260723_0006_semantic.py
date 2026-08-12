"""create versioned semantic layer

Revision ID: 20260723_0006
Revises: 20260721_0005
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260723_0006"
down_revision: str | None = "20260721_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "semantic_layers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dataset_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="processing", nullable=False),
        sa.Column("business_domain", sa.String(length=80), nullable=True),
        sa.Column("glossary_json", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["dataset_version_id"], ["dataset_versions.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("dataset_version_id", name="uq_semantic_layers_dataset_version_id"),
    )
    op.create_index("ix_semantic_layers_dataset_id", "semantic_layers", ["dataset_id"])
    op.create_table(
        "semantic_fields",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("semantic_layer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_column", sa.String(length=255), nullable=False),
        sa.Column("canonical_name", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("data_type", sa.String(length=80), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("expression", sa.Text(), nullable=True),
        sa.Column("synonyms", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("is_user_defined", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["semantic_layer_id"], ["semantic_layers.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("semantic_layer_id", "source_column", name="uq_semantic_fields_layer_column"),
    )
    op.create_index("ix_semantic_fields_layer_id", "semantic_fields", ["semantic_layer_id"])
    op.create_table(
        "semantic_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("semantic_layer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_field_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_field_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("relationship_type", sa.String(length=30), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), server_default="{}", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["semantic_layer_id"], ["semantic_layers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_field_id"], ["semantic_fields.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_field_id"], ["semantic_fields.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_semantic_relationships_layer_id", "semantic_relationships", ["semantic_layer_id"])
    op.create_table(
        "glossary_terms",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("term", sa.String(length=255), nullable=False),
        sa.Column("definition", sa.Text(), nullable=False),
        sa.Column("synonyms", sa.JSON(), nullable=True),
        sa.Column("example_values", sa.JSON(), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("workspace_id", "term", name="uq_glossary_terms_workspace_term"),
    )
    op.create_index("ix_glossary_terms_workspace_id", "glossary_terms", ["workspace_id"])


def downgrade() -> None:
    op.drop_index("ix_glossary_terms_workspace_id", table_name="glossary_terms")
    op.drop_table("glossary_terms")
    op.drop_index("ix_semantic_relationships_layer_id", table_name="semantic_relationships")
    op.drop_table("semantic_relationships")
    op.drop_index("ix_semantic_fields_layer_id", table_name="semantic_fields")
    op.drop_table("semantic_fields")
    op.drop_index("ix_semantic_layers_dataset_id", table_name="semantic_layers")
    op.drop_table("semantic_layers")
