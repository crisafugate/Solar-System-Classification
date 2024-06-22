from experta import *
import json

# planets have a mass greater than the moon
# dwarf planets have a mass less than the moon
# inner system comets have an aphelion beyond 3.5au
# an asteroid has a aphelion less than 3.5au
# outer system comets have a perihelion < 5au and an aphelion beyond neptune
# a simple kuiper belt object has a perihelion > 5au and an aphelion beyond neptune
# a kuiper belt object moon orbits a kiuper belt object
# distance is either measures in AU or KM (for moons)
# diameter is measured in KM
# mass is measures in 10^24KM

class SolarSystemClassification(KnowledgeEngine):
    moon_mass = 0.073
    asteroid_limit = 3.5
    jupiter_dist = 4.95
    neptune_dist = 30.4
    
    @DefFacts()
    def load_data(self):
        with open('ssc_data.json') as fh:
            file_data = fh.read()
        json_data = json.loads(file_data)

        for obj in json_data:
            yield Fact(name=obj["name"],
                       orbits=obj["orbits"],
                       min_dist=obj["min_dist"],
                       max_dist=obj["max_dist"],
                       diameter=obj["diameter"],
                       mass=obj["mass"],
                       shape=obj["shape"])

    @Rule(AND(Fact(name=MATCH.name, orbits='sun', mass=P(lambda mass: mass > SolarSystemClassification.moon_mass),
                   shape='round'),
              NOT(Fact(name=MATCH.name, type='planet'))),
          salience=1)    
    def classify_planet(self, name):
        self.declare(Fact(name=name, type='planet'))
        print(f"{name} is a planet")

    @Rule(AND(Fact(name=MATCH.name, orbits='sun', mass=P(lambda mass: mass < SolarSystemClassification.moon_mass),
                   shape='round'),
              NOT(Fact(name=MATCH.name, type='dwarf_planet'))))
    def classify_dwarf_planet(self, name):
        self.declare(Fact(name=name, type='dwarf_planet'))
        print(f"{name} is a dwarf planet")
        

    @Rule(Fact(name=MATCH.name, orbits=P(lambda orbits: orbits!='sun')),
          NOT(Fact(name=MATCH.name, type="moon")))
    def classify_moon(self, name):
        self.declare(Fact(name=name, type='moon'))
        print(f"{name} is a moon")


    @Rule(AND(Fact(name=MATCH.name, orbits="sun", mass=P(lambda mass: mass < SolarSystemClassification.moon_mass),
                   max_dist=P(lambda dist: dist <= SolarSystemClassification.asteroid_limit), shape='irregular'),
              NOT(Fact(name=MATCH.name, type="asteroid"))))
    def classify_asteroid(self, name):
        self.declare(Fact(name=name, type="asteroid"))
        print(f"{name} is an asteroid")
        
    @Rule(AND(Fact(name=MATCH.name, orbits="sun",
                   max_dist=P(lambda dist: dist > SolarSystemClassification.asteroid_limit) & P(lambda dist: dist < SolarSystemClassification.jupiter_dist),
                   mass=P(lambda mass: mass < SolarSystemClassification.moon_mass)),
              NOT(Fact(name=MATCH.name, type="comet"))))
    def classify_inner_system_comet(self, name):
        self.declare(Fact(name=name, type="comet"))
        self.declare(Fact(name=name, type="inner_system"))
        print(f"{name} is an inner system comet")


    @Rule(AND(Fact(name=MATCH.name, orbits="sun",
                   min_dist=P(lambda dist: dist < 5),
                   max_dist=P(lambda dist: dist > SolarSystemClassification.neptune_dist)),
              NOT(Fact(name=MATCH.name, type="comet"))))                   
    def classify_outer_system_comet(self, name):
        self.declare(Fact(name=name, type="comet"))
        self.declare(Fact(name=name, type="outer_system"))
        print(f"{name} is an outer system comet")

    @Rule(AND(Fact(name=MATCH.name, orbits="sun",
                   min_dist=P(lambda dist: dist > 5) &
                   max_dist=P(lambda dist: dist > SolarSystemClassification.neptune_dist)),
              NOT(Fact(name=MATCH.name, type="KBO"))))
    def classify_kuiper_belt_object(self, name):
        self.declare(Fact(name=name, type="KBO"))
        print(f"{name} is a kuiper belt object")


    @Rule(AND(Fact(name=MATCH.name1, type="moon"),
              Fact(name=MATCH.name1, orbits=MATCH.name2),
              Fact(name=MATCH.name2, type='KBO'),
              NOT(Fact(name=MATCH.name1, type='KBO'))))
    def classify_kbo_moon(self, name1, name2):
        self.declare(Fact(name=name1, type="KBO"))
        print(f"{name1} is a KBO moon")


    engine = SolarSystemClassification()
    engine.reset()
    engine.run()
    
    
                     
        
