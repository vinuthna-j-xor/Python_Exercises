
class Vehicle:
    def start(self):
        print("Vehicle started")

    def stop(self):
        print("Vehicle stopped")



class Car(Vehicle):
    def play_music(self):
        print("Playing music")



class ElectricMixin:
    def start(self):
        print("Checking battery...")
        super().start()   



class AutopilotMixin:
    def start(self):
        print("Calibrating sensors...")
        super().start()   


class Tesla(AutopilotMixin, ElectricMixin, Car):
    pass



t = Tesla()
t.start()
t.play_music()
t.stop()
