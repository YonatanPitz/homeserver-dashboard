class SwitchInterface:
    def __init__(self):
        pass

    def set_switch_state(self, id : str, state : bool):
        pass

    def get_switch_state(self, id : str) -> dict:
        pass

    def get_all_switch_states(self) -> dict:
        pass