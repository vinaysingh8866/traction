# flake8: noqa
"""v1-innkeeper-tenant-flows

Revision ID: 3d6a9333acc2
Revises: 135b4f1c8965
Create Date: 2022-07-29 12:35:16.755864

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3d6a9333acc2"
down_revision = "135b4f1c8965"
branch_labels = None
depends_on = None


create_timeline_func = """CREATE OR REPLACE FUNCTION i_t_flow_presentation_timeline_func() RETURNS trigger AS $body$
    BEGIN
        IF NEW.status IS DISTINCT FROM OLD.status OR NEW.state IS DISTINCT FROM OLD.state THEN
            INSERT INTO "timeline" ( "item_id", "status", "state", "error_status_detail" )
            VALUES(NEW."innkeeper_tenant_flow_id", NEW."status", NEW."state", NEW."error_status_detail");
            RETURN NEW;
        END IF;
        RETURN null;
    END;
    $body$ LANGUAGE plpgsql
"""

drop_timeline_func = """DROP FUNCTION i_t_flow_presentation_timeline_func"""

create_timeline_trigger = """CREATE TRIGGER i_t_flow_presentation_timeline_trigger
AFTER INSERT OR UPDATE OF status, state ON innkeeper_tenant_flow
FOR EACH ROW EXECUTE PROCEDURE i_t_flow_presentation_timeline_func();"""

drop_timeline_trigger = (
    """DROP TRIGGER i_t_flow_presentation_timeline_trigger ON innkeeper_tenant_flow"""
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "innkeeper_tenant_flow",
        sa.Column(
            "innkeeper_tenant_flow_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("flow_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("tenant_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("state", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "completed_value", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("error_status_detail", sa.VARCHAR(), nullable=True),
        sa.Column("comment", sa.VARCHAR(), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("innkeeper_tenant_flow_id"),
        sa.UniqueConstraint("tenant_id", "flow_type"),
    )
    op.create_index(
        op.f("ix_innkeeper_tenant_flow_tenant_id"),
        "innkeeper_tenant_flow",
        ["tenant_id"],
        unique=False,
    )
    # ### end Alembic commands ###
    # ### end Alembic commands ###
    op.execute(create_timeline_func)
    op.execute(create_timeline_trigger)


def downgrade():
    op.execute(drop_timeline_trigger)
    op.execute(drop_timeline_func)
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_innkeeper_tenant_flow_tenant_id"), table_name="innkeeper_tenant_flow"
    )
    op.drop_table("innkeeper_tenant_flow")
    # ### end Alembic commands ###