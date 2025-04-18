class LeaseNotFoundException(Exception):
    def __init__(self, lease_id):
        super().__init__(f"Lease with ID {lease_id} not found in the database.")
        self.lease_id = lease_id
