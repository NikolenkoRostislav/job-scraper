"""made seniority levels into enums instead of strings

Revision ID: 79f80e21142f
Revises: 8b4133a04f2b
Create Date: 2026-01-22 14:17:36.015369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '79f80e21142f'
down_revision: Union[str, Sequence[str], None] = '8b4133a04f2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'seniority_level') THEN
                CREATE TYPE seniority_level AS ENUM ('junior', 'mid', 'senior');
            END IF;
        END$$;
    """)


    op.execute("UPDATE job_listings SET seniority_levels = NULL;")
    
    op.execute("""
        ALTER TABLE job_listings 
        ALTER COLUMN seniority_levels 
        TYPE seniority_level[] 
        USING NULL::seniority_level[];
    """)


def downgrade() -> None:
    """Downgrade schema."""

    op.execute("UPDATE job_listings SET seniority_levels = NULL;")
    
    op.execute("""
        ALTER TABLE job_listings 
        ALTER COLUMN seniority_levels 
        TYPE varchar[] 
        USING ARRAY[]::varchar[];
    """)

    op.execute("DROP TYPE IF EXISTS seniority_level;")
