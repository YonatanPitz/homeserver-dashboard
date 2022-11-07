class AirConditionerInterface:
    def __init__(self):
        pass

    def set_ac_state(self, name : str, state : dict):
        """Set the state of the air conditioner. state is expected to have the following keys:
        power: ON, OFF
        fan: Auto, Low, Med, High
        mode: HEAT, COOL, FAN
        temperature: int (17-30)
        """
        pass

    def get_ac_state(self, name : str) -> dict:
        """Get current state of air conditioner."""
        pass
    
    def get_all_ac_states(self) -> dict:
        """Get current state of all air conditioners."""
        pass