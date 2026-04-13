# manual occupy/release functions for testing purposes
def manually_occupy_spot(self, spot_id):
    spot = self.get_spot(spot_id)
    if spot is not None:
        spot.occupy()

def manually_release_spot(self, spot_id):
    spot = self.get_spot(spot_id)
    if spot is not None:
        spot.release()