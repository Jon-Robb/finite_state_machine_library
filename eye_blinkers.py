from side_blinkers import SideBlinkers


class EyeBlinkers(SideBlinkers):
    def __init__(self, robot) -> None:
        self.robot = robot