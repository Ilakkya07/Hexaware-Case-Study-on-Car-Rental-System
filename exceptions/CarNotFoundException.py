class CarNotFoundException(Exception):
    def __init__(self, vehicle_id):
        super().__init__(f"Car with ID {vehicle_id} not found in the database.")
        self.vehicle_id = vehicle_id

