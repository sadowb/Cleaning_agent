import random

class Room:
    def __init__(self, dirtiness=0):
        self.dirtiness = dirtiness

    def is_dirty(self):
        return self.dirtiness > 0

    def clean(self):
        self.dirtiness = 0

    def make_dirty(self, level=None):
        if level is None:
            level = random.randint(1, 5)
        self.dirtiness = level

    def __repr__(self):
        if self.is_dirty():
            return f"Dirtiness({self.dirtiness})"
        return "Clean"


class Environment:
    def __init__(self, N):
        self.rooms = []
        for _ in range(N):  # initial state of the room is 50% chance clean and 50% dirty
            if random.random() < 0.5:
                self.rooms.append(Room(0))
            else:
                self.rooms.append(Room(random.randint(1,5)))


    def update_dirtiness(self):
        for room in self.rooms:
            if not room.is_dirty():
                if random.random() < 0.1:
                    room.make_dirty()

    def all_clean(self):
        return all(not room.is_dirty() for room in self.rooms)

    def get_room(self, index):
        return self.rooms[index]

    def __repr__(self):
        return str(self.rooms)


class Agent:
    def __init__(self, N):
        self.position = 0
        self.energy = 2.5 * N
        self.actions = []
        self.cleaned_rooms = 0

    def perceive(self, env):
        room = env.get_room(self.position)
        return {
            "position": self.position,
            "dirtiness": room.dirtiness,
            "energy": self.energy
        }

    def decide(self, percept, N):
        if percept["dirtiness"] > 0 and self.energy >= percept["dirtiness"]:
            return "Suck"
        elif self.position < N - 1 and self.energy >= 2:
            return "MoveRight"
        elif self.position > 0 and self.energy >= 2:
            return "MoveLeft"
        else:
            return "Stop"  # fixed capitalization

    def act(self, action, env):
        if action == "Suck":
            cost = env.get_room(self.position).dirtiness
            if self.energy >= cost:
                env.get_room(self.position).clean()
                self.energy -= cost
                self.cleaned_rooms += 1
        elif action == "MoveRight":
            if self.position < len(env.rooms) - 1 and self.energy >= 2:
                self.position += 1
                self.energy -= 2
        elif action == "MoveLeft":
            if self.position > 0 and self.energy >= 2:
                self.position -= 1
                self.energy -= 2

        self.actions.append(action)


class Simulation:
    def __init__(self, N, T):
        self.env = Environment(N)
        self.agent = Agent(N)
        self.T = T

    def run(self):
        print("Initial state:", self.env)
        print ("Initial enrgy",self.agent.energy)
        for t in range(self.T):
            # 1. Environment update
            self.env.update_dirtiness()

            # 2. Agent perceives
            percept = self.agent.perceive(self.env)

            # 3. Agent decides
            action = self.agent.decide(percept, len(self.env.rooms))

            if action == "Stop":
                print(f"\nStopping at timestep {t}. No more actions possible.")
                break

            # 4. Agent acts
            self.agent.act(action, self.env)

            # Show timestep state
            print(f"Step {t+1}: Action = {action}, Energy = {self.agent.energy}, Rooms = {self.env}")

            # End if no energy or all rooms clean
            if self.agent.energy <= 0 or self.env.all_clean():
                break

        # Final report
        print("\nFinal Report:")
        print("Final room states:", self.env)
        print("Rooms cleaned:", self.agent.cleaned_rooms)
        print("Total energy consumed:", int(2.5 * len(self.env.rooms)) - self.agent.energy)
        print("Remaining energy:", self.agent.energy)
        print("Actions taken:", self.agent.actions)


# Run it
if __name__ == "__main__":
    N = 3   # number of rooms
    T =  100 # number of timesteps
    sim = Simulation(N, T)
    sim.run()
