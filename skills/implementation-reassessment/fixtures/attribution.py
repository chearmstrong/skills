"""Fictional SDK fixture for a read-only implementation reassessment.

Requirement: usage must contain the authenticated user's reporting hierarchy.
Reporting changes may take up to one hour to appear during normal operation.
Caller-supplied metadata must not determine attribution. The design names no
required backing store. Tests below describe local behaviour, not live acceptance.
"""

from dataclasses import dataclass
import unittest


@dataclass(frozen=True)
class Snapshot:
    principal_id: str
    manager_id: str


@dataclass(frozen=True)
class AuthenticatedContext:
    # Supplied by the SDK from its user store, separate from request metadata.
    principal_id: str
    user_metadata: Snapshot


class GatewaySDK:
    USER_CACHE_SECONDS = 3600

    def authenticate(self, stored_snapshot: Snapshot) -> AuthenticatedContext:
        # The real cache is outside this fixture; the constant states its contract.
        return AuthenticatedContext(stored_snapshot.principal_id, stored_snapshot)


class Repository:
    def __init__(self, snapshot: Snapshot, available: bool = True):
        self.snapshot = snapshot
        self.available = available
        self.reads = 0

    def read_hierarchy(self, principal_id: str) -> Snapshot:
        self.reads += 1
        if not self.available:
            raise ConnectionError("reporting database unavailable")
        if self.snapshot.principal_id != principal_id:
            raise LookupError(principal_id)
        return self.snapshot


def attribute(context: AuthenticatedContext, repository: Repository) -> Snapshot:
    return repository.read_hierarchy(context.principal_id)


class AttributionTests(unittest.TestCase):
    def test_uses_the_latest_repository_hierarchy(self):
        old = Snapshot("user-1", "manager-1")
        current = Snapshot("user-1", "manager-2")
        context = GatewaySDK().authenticate(old)
        self.assertEqual(attribute(context, Repository(current)), current)

    def test_database_outage_prevents_attribution(self):
        snapshot = Snapshot("user-1", "manager-1")
        context = GatewaySDK().authenticate(snapshot)
        with self.assertRaises(ConnectionError):
            attribute(context, Repository(snapshot, available=False))


if __name__ == "__main__":
    unittest.main()
