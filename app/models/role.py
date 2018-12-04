"""Role."""

from .base import Base, db


class Role(Base):
    """Role model."""

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)

    def __repr__(self):
        """Summary view of a role."""
        return self.title
